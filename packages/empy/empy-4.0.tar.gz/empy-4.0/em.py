#!/usr/bin/env python3

"""
A system for processing Python via markup embeded in text.
"""

__project__ = "EmPy"
__program__ = "empy"
__module__ = "em"
__version__ = "4.0"
__url__ = "http://www.alcyone.com/software/empy/"
__author__ = "Erik Max Francis <max@alcyone.com>"
__contact__ = "software@alcyone.com"
__copyright__ = "Copyright (C) 2002-2023 Erik Max Francis"
__license__ = "BSD"

#
# imports
#

import codecs
import copy
import getopt
import os
import re
import sys
import unicodedata

#
# compatibility
#

# Initializes the following global names based on Python 2.x vs. 3.x:
#
# - major          Detected major Python version
# - minor          Detected minor Python version
# - minimum        Minimum supported Python version (major, minor)
# - compat         List of Python backward-compatibility features applied
# - narrow         Was this Python built with narrow Unicode (UTF-16 natively)?
# - nativeStr      The native str type (str in Python 3.x; str in Python 2.x)
# - str (_unicode) The str type (str in Python 3.x; unicode in Python 2.x)
# - bytes (_str)   The bytes type (bytes in Python 3.x; str in Python 2.x)
# - strType        The str type (Python 3.x) or the bytes and str types (2.x)
# - chr            The chr function (unichr in Python 2.x)
# - input          The input function (raw_input in Python 2.x)
# - evalFunc       The eval function
# - execFunc       The exec function
# - BaseException  The base exception class for all exceptions
# - StringIO       The StringIO class
# - isIdentifier   Is this string a valid Python identifier?
# - uliteral       Return a version-specific wide Unicode literal ('\U...')
# - toString       Convert an arbitrary object to a Unicode-compatible string

# The major version of Python (2 or 3).
major = sys.version_info[0]
# The minor version of Python.
minor = sys.version_info[1]
# Minimum supported version of Python.
minimum = (2, 3)
# Version check.
if (major, minor) < minimum:
    raise RuntimeError("EmPy requires at least Python %s.%s" % minimum)
# A list of Python backward-compatibility features which were applied.
compat = []
# The native str type/function.
nativeStr = str
# The eval function.
evalFunc = eval
if major == 2:
    # We're using Python 2.x!  Make sure there are Python 3.x-like names for
    # the basic types and functions; hereafter, use str for unicode and bytes
    # for str, respectively.
    bytes = _str = str
    str = _unicode = unicode
    strType = (bytes, str)
    chr = unichr
    input = raw_input
    # In Python 2.x, StringIO is contained in the cStringIO module.
    try:
        from cStringIO import StringIO
    except ImportError:
        # If cStringIO is not present for some reason, try to use the slower
        # StringIO module.
        from StringIO import StringIO
    if minor < 5:
        # Starting with Python 2.5, a new BaseException class serves as the
        # base class of all exceptions; prior to that, it was just Exception.
        # So create a name for it if necessary.
        compat.append('BaseException')
        BaseException = Exception
    # In Python 2.x, exec is a statement; in Python 3.x, it's a function.  Make
    # a new function that will simulate the Python 3.x form but work in Python
    # 2.x.
    def execFunc(code, globals=None, locals=None):
        if globals is None:
            exec("""exec code""")
        else:
            if locals is None:
                exec("""exec code in globals""")
            else:
                exec("""exec code in globals, locals""")
    def toString(value):
        """Convert value to a (Unicode) string.  Also serves as a
        sentinel to represent a str or bytes type."""
        if isinstance(value, _unicode):
            # Good to go.
            return value
        elif isinstance(value, _str):
            # It's already a str (bytes), convert it to a unicode (str).
            return _unicode(value)
        else:
            # In Python 2.x, __str__ returns a str, not a unicode.  Convert the
            # object to a str (bytes), then convert it to a unicode (str).
            return _unicode(_str(value))
    def isIdentifier(string, first=True):
        """Is this string a valid identifier?  If first is true, make
        sure the first character is a valid starting identifier character."""
        for char in string:
            if first:
                if not (char.isalpha() or char == '_'):
                    return False
                first = False
            else:
                if not (char.isalpha() or char.isdigit() or char == '_'):
                    return False
        return True
    def uliteral(i):
        """Return a wide Unicode string literal."""
        return r"u'\U%08x'" % i
elif major >= 3:
    # We're using Python 3.x!  Add Python 2.x-like names for the basic types
    # and functions.  The name duplication is so that there will always be a
    # definition of both str and types in the globals (as opposed to the
    # builtins).
    bytes = _str = bytes
    str = _unicode = str
    strType = str
    chr = chr
    input = input
    # In Python 3.x, the module containing StringIO is io.
    from io import StringIO
    # In Python 3.x, exec is a function, but attempting to reference it as such
    # in Python 2.x generates an error.  Since this needs to also compile in
    # Python 2.x, defer the evaluation past the parsing phase.
    try:
        execFunc = evalFunc('exec')
    except NameError:
        execFunc = evalFunc('__builtins__.exec')
    def toString(value):
        """Convert value to a (Unicode) string.  Also serves as a
        sentinel to represent a str or bytes type."""
        return str(value)
    def isIdentifier(string, first=True):
        """Is this string a valid identifier?  If first is true, make
        sure the first character is a valid starting identifier character."""
        if first:
            return string.isidentifier()
        else:
            return ('_' + string).isidentifier()
    def uliteral(i):
        """Return a wide Unicode string literal."""
        return r"'\U%08x'" % i

# Was this Python interpreter built with narrow Unicode?  That is, does it use
# a UTF-16 encoding (with surrgoate pairs) vs. UTF-32 internally?
if hasattr(sys, 'maxunicode'):
    narrow = sys.maxunicode < 0x10000
else:
    narrow = len(evalFunc(uliteral(0x10000))) > 1
if narrow:
    # Narrow Python builds will raise a ValueError when calling chr (unichr) on
    # a code point value outside of the Basic Multilingual Plane (U+0000
    # .. U+FFFF).  See if it needs to be replaced.
    _chr = chr
    if major == 2:
        if minor >= 6:
            # Versions 2.6 and up can use this struct/decode trick.
            compat.append('chr/decode')
            def chr(i, _chr=_chr):
                if i < 0x10000:
                    return _chr(i)
                else:
                    import struct
                    try:
                        return struct.pack('i', i).decode('utf-32')
                    except UnicodeDecodeError:
                        raise ValueError("chr() arg not in range")
        else:
            # Earlier versions (2.5 and below) need to evaluate a literal.
            compat.append('chr/uliteral')
            def chr(i, _chr=_chr):
                if i < 0x10000:
                    return _chr(i)
                else:
                    try:
                        return evalFunc(uliteral(i))
                    except (SyntaxError, UnicodeDecodeError):
                        raise ValueError("chr() arg not in range")
    compat.append('narrow')

#
# constants
#

# Character information.
UNDERSCORE_CHAR = '_'
DOT_CHAR = '.'
BACKSLASH_CHAR = '\\'
CARET_CHAR = '^'
STROKE_CHAR = '|'
OCTOTHORPE_CHAR = '#'
ASTERISK_CHAR = '*'
QUESTION_CHAR = '?'
EXCLAMATION_CHAR = '!'
PERCENT_CHAR = '%'
OPEN_PARENTHESIS_CHAR = '('
OPEN_BRACE_CHAR = '{'
OPEN_BRACKET_CHAR = '['
OPEN_ANGLE_CHAR = '<'
BACKQUOTE_CHAR = '`'
DOLLAR_CHAR = '$'
COLON_CHAR = ':'
WHITESPACE_CHARS = ' \t\v\f\r\n'
CARRIAGE_RETURN_CHAR = '\r'
NEWLINE_CHAR = '\n'
OPENING_CHARS = '([{<'
PHRASE_OPENING_CHARS = '(['
CLOSING_CHARS = ')]}>'
QUOTE_CHARS = '\'\"'
ENDING_CHAR_MAP = {'(': ')', '[': ']', '{': '}', '<': '>'}

# Environment variable names.
OPTIONS_ENV = 'EMPY_OPTIONS'
CONFIG_ENV = 'EMPY_CONFIG'
PREFIX_ENV = 'EMPY_PREFIX'
PSEUDO_ENV = 'EMPY_PSEUDO'
FLATTEN_ENV = 'EMPY_FLATTEN'
RAW_ERRORS_ENV = 'EMPY_RAW_ERRORS'
INTERACTIVE_ENV = 'EMPY_INTERACTIVE'
DELETE_ON_ERROR_ENV = 'EMPY_DELETE_ON_ERROR'
NO_PROXY_ENV = 'EMPY_NO_PROXY'
BUFFERING_ENV = 'EMPY_BUFFERING'
BINARY_ENV = 'EMPY_BINARY'
ENCODING_ENV = 'EMPY_ENCODING'
INPUT_ENCODING_ENV = 'EMPY_INPUT_ENCODING'
OUTPUT_ENCODING_ENV = 'EMPY_OUTPUT_ENCODING'
ERRORS_ENV = 'EMPY_ERRORS'
INPUT_ERRORS_ENV = 'EMPY_INPUT_ERRORS'
OUTPUT_ERRORS_ENV = 'EMPY_OUTPUT_ERRORS'

# A regular expression string suffix which will match singificators; prepend
# the interpreter prefix to make a full regular expression string.  A
# successful match will yield six groups, arranged in two clusters of three.
# Each cluster contains the following three named groups in index order:
#
# - string: A `!` to represent a stringized significator, or blank
# - key: The significator key
# - value: The significator value; can be blank
#
# The value should be stripped before being tested.  If it is blank and if the
# significator is not stringized, then the resulting significator value will be
# None.
#
# The first cluster (with group names ending in 2: string2, key2, value2)
# matches multiline significators; the second (with group names ending in 1:
# string1, key1, value1) matches singleline ones.  Only one of these clusters
# will be set.
#
# The regular expression should be compiled with the following flags:
# re.MULTILINE|re.DOTALL|re.VERBOSE.  To get a compiled regular expression
# object for a given config, call `config.significatorRe()`.
SIGNIFICATOR_RE_STRING_SUFFIX = r"""
                    # Flags: re.MULTILINE|re.DOTALL|re.VERBOSE
%                   # Opening `%`
(?:                 # Start non-grouping choice: Multiline
 %                  #  A second `%`
 (?P<string2>!?)    #  An optional `!` [string2]
 [ \t\v\f\r]*       #  Zero or more non-newline whitespace
 (?P<key2>\S+)      #  One or more non-whitespace [key2]
 \s*                #  Zero or more whitespace
 (?P<value2>[^%]*)  #  Zero or more non-`%` characters [value2]
 \s*                #  Zero or more whitespace
 %%                 #  Closing `%%`
|                   # Next non-grouping choice: Singleline
 (?P<string1>!?)    #  An optional `!` [string1]
 [ \t\v\f\r]*       #  Zero or more non-newline whitespace
 (?P<key1>\S+)      #  One or more non-whitespace [key1]
 [ \t\v\f\r]*       #  Zero or more non-newline whitespace
 (?P<value1>[^\n]*) #  Zero or more non-newline characters [value1]
 [ \t\v\f\r]*       #  Zero or more non-newline whitespace
)                   # End choice
$                   # End string
"""

#
# Error ...
#

class Error(Exception):

    def __init__(self, *args, **kwargs):
        # super does not work here for old versions of Python 2.x.
        Exception.__init__(self, *args)
        self.__dict__.update(kwargs)

class ConsistencyError(Error): pass
class DiversionError(Error): pass
class FilterError(Error): pass
class StackUnderflowError(Error): pass

class InvocationError(Error): pass
class ConfigurationError(Error): pass
class ConfigurationFileNotFoundError(ConfigurationError): pass

class ParseError(Error): pass
class TransientParseError(ParseError): pass

class BadKeyError(Error, KeyError): pass
class UnknownEmojiError(BadKeyError): pass

#
# Flow ...
#

class Flow(Exception): pass
class ContinueFlow(Flow): pass
class BreakFlow(Flow): pass

#
# Root
#

class Root(object):

    """The root class of all EmPy class hierarchies.  It defines a default
    __repr__ method which will work appropriately whether or not the subclass
    defines a __str__ method.  Very old versions of Python 2.x won't
    print the proper __str__ form, but so be it."""

    def __repr__(self):
        if (hasattr(self, '__str__') and hasattr(type(self), '__str__') and
            getattr(type(self), '__str__') is not getattr(Root, '__str__')):
            return '%s(%s)' % (self.__class__.__name__, toString(self))
        else:
            return '<%s @ 0x%x>' % (self.__class__.__name__, id(self))

#
# Module
#

class Module(Root):

    """The abstraction of an emoji module that may or may not be available
    for usage."""

    def __init__(self, name, attribute, format):
        self.name = name
        self.attribute = attribute
        self.format = format
        self.ok = False
        self.initialize()

    def __str__(self):
        return self.name

    def initialize(self):
        """Attempt to initialize this emoji module.  Set ok to true if
        successful."""
        try:
            self.module = __import__(self.name)
            self.function = getattr(self.module, self.attribute, None)
        except ImportError:
            self.module = self.function = None
        if self.function is not None:
            self.ok = True

    def substitute(self, text):
        """Substitute text using this module.  Return None if
        unsuccessful."""
        assert self.ok
        wrapped = self.format % text
        try:
            result = self.function(wrapped)
        except KeyError:
            return None
        if wrapped == result:
            return None
        else:
            return result


#
# Configuration
#

class Configuration(Root):

    """The configuration encapsulates all the defaults and parameterized
    behavior of an interpreter.  When created, an interpreter is assigned
    a configuration; multiple configurations can be shared between different
    interpreters.  To override the defaults of an interpreter, create a
    Configuration instance and then modify its attributes."""

    # Constants.

    version = __version__
    bangpath = '#!'
    unknownScriptName = '<->'
    significatorReStringSuffix = SIGNIFICATOR_RE_STRING_SUFFIX
    fullBuffering = -1
    noBuffering = 0
    lineBuffering = 1
    unwantedGlobalsKeys = [None, '__builtins__'] # None = pseudomodule name
    unflattenableGlobalsKeys = ['globals']
    priorityVariables = ['checkVariables']
    emojiModuleInfos = [
        # module name, attribute name, wrapping format
        ('emoji', 'emojize', ':%s:'),
        ('emojis', 'encode', ':%s:'),
        ('emoji_data_python', 'replace_colons', ':%s:'),
        ('unicodedata', 'lookup', '%s'),
    ]

    # Defaults.

    defaultName = 'default'
    defaultPrefix = '@'
    defaultPseudomoduleName = 'empy'
    defaultBuffering = 16384
    defaultContextFormat = '%(name)s:%(line)d:%(column)d'
    defaultNormalizationForm = 'NFKC'
    defaultErrors = 'strict'
    defaultConfigVariableName = '_'
    defaultStdout = sys.stdout
    defaultSuccessCode = 0
    defaultFailureCode = 1
    defaultUnknownCode = 2
    defaultSignificatorDelimiters = ('__', '__')
    defaultEmptySignificator = None
    defaultAutoValidateIcons = True
    defaultEmojiModuleNames = [
        'emoji',
        'emojis',
        'emoji_data_python',
        'unicodedata',
    ]
    defaultNoEmojiModuleNames = [
        'unicodedata',
    ]

    # Statics.

    baseException = BaseException
    topLevelErrors = (ConfigurationError,)
    fallThroughErrors = (SyntaxError,)
    proxyWrapper = None
    useContextFormatMethod = None
    emojiModules = None
    iconsSignature = None
    verboseFile = sys.stderr
    factory = None
    ignorableErrorAttributes = ['args', 'message', 'add_note', 'with_traceback']

    tokens = None # list of token factories; intialized below

    _initialized = False # change only in instances

    # Dictionaries.

    controls = {
        'NUL':    (0x0000, "null"),
        'SOH':    (0x0001, "start of heading"),
        'STX':    (0x0002, "start of text"),
        'ETX':    (0x0003, "end of text"),
        'EOT':    (0x0004, "end of transmission, end of data"),
        'ENQ':    (0x0005, "enquiry"),
        'ACK':    (0x0006, "acknowledge"),
        'BEL':    (0x0007, "bell, alert"),
        'BS':     (0x0008, "backspace"),
        'HT':     (0x0009, "horizontal tabulation, tab"),
        'LF':     (0x000a, "linefeed, newline"),
        'NL':     (0x000a, "linefeed, newline"),
        'LT':     (0x000b, "line tabulation, vertical tab"),
        'VT':     (0x000b, "line tabulation, vertical tab"),
        'FF':     (0x000c, "form feed"),
        'CR':     (0x000d, "carriage return"),
        'SO':     (0x000e, "shift out"),
        'SI':     (0x000f, "shift in"),
        'DLE':    (0x0010, "data link escape"),
        'DC1':    (0x0011, "device control one, xon"),
        'XON':    (0x0011, "device control one, xon"),
        'DC2':    (0x0012, "device control two"),
        'XOFF':   (0x0013, "device control three, xoff"),
        'DC3':    (0x0013, "device control three, xoff"),
        'DC4':    (0x0014, "device control four"),
        'NAK':    (0x0015, "negative acknowledge"),
        'SYN':    (0x0016, "synchronous idle"),
        'ETB':    (0x0017, "end of transmission block"),
        'CAN':    (0x0018, "cancel"),
        'EM':     (0x0019, "end of medium"),
        'SUB':    (0x001a, "substitute"),
        'ESC':    (0x001b, "escape"),
        'FS':     (0x001c, "file separator, information separator four"),
        'IS4':    (0x001c, "file separator, information separator four"),
        'GS':     (0x001d, "group separator, information separator three"),
        'IS3':    (0x001d, "group separator, information separator three"),
        'RS':     (0x001e, "record separator, information separator two"),
        'IS2':    (0x001e, "record separator, information separator two"),
        'US':     (0x001f, "unit separator, information separator one"),
        'IS1':    (0x001f, "unit separator, information separator one"),
        'SP':     (0x0020, "space"),
        'DEL':    (0x007f, "delete"),
        'PAD':    (0x0080, "padding character"),
        'HOP':    (0x0081, "high octet preset"),
        'BPH':    (0x0082, "break permitted here"),
        'NBH':    (0x0083, "no break here"),
        'IND':    (0x0084, "index"),
        'NEL':    (0x0085, "next line"),
        'SSA':    (0x0086, "start of selected area"),
        'ESA':    (0x0087, "end of selected area"),
        'HTS':    (0x0088, "character tabulation set"),
        'HTJ':    (0x0089, "character tabulation with justification"),
        'VTS':    (0x008a, "line tabulation set"),
        'PLD':    (0x008b, "partial line forward"),
        'PLU':    (0x008c, "partial line backward"),
        'RI':     (0x008d, "reverse line feed"),
        'SS2':    (0x008e, "single shift two"),
        'SS3':    (0x008f, "single shift three"),
        'DCS':    (0x0090, "device control string"),
        'PV1':    (0x0091, "private use one"),
        'PV2':    (0x0092, "private use two"),
        'STS':    (0x0093, "set transmission state"),
        'CHC':    (0x0094, "cancel character"),
        'MW':     (0x0095, "message waiting"),
        'SPA':    (0x0096, "start guarded area"),
        'EPA':    (0x0097, "end guarded area"),
        'SOS':    (0x0098, "start of string"),
        'SCI':    (0x009a, "single character introducer"),
        'CSI':    (0x009b, "control sequence introducer"),
        'ST':     (0x009c, "string terminator"),
        'OSC':    (0x009d, "operating system command"),
        'PM':     (0x009e, "privacy message"),
        'APC':    (0x009f, "application program command"),
        'NBSP':   (0x00a0, "no-break space"),
        'SHY':    (0x00ad, "soft hyphen, discretionary hyphen"),
        'CGJ':    (0x034f, "combining grapheme joiner"),
        'NQSP':   (0x2000, "en quad"),
        'MQSP':   (0x2001, "em quad, mutton quad"),
        'ENSP':   (0x2002, "en space, nut"),
        'EMSP':   (0x2003, "em space, mutton"),
        '3MSP':   (0x2004, "three-per-em space, thick space"),
        '4MSP':   (0x2005, "four-per-em space, mid space"),
        '6MSP':   (0x2006, "six-per-em space"),
        'FSP':    (0x2007, "figure space"),
        'PSP':    (0x2008, "punctuation space"),
        'THSP':   (0x2009, "thin space"),
        'HSP':    (0x200a, "hair space"),
        'ZWSP':   (0x200b, "zero width space"),
        'ZWNJ':   (0x200c, "zero width non-joiner"),
        'ZWJ':    (0x200d, "zero width joiner"),
        'LRM':    (0x200e, "left-to-right mark"),
        'RLM':    (0x200f, "right-to-left mark"),
        'NBH':    (0x2011, "non-breaking hyphen"),
        'LSEP':   (0x2028, "line separator"),
        'PSEP':   (0x2029, "paragraph separator"),
        'LRE':    (0x202a, "left-to-right encoding"),
        'RLE':    (0x202b, "right-to-left encoding"),
        'PDF':    (0x202c, "pop directional formatting"),
        'LRO':    (0x202d, "left-to-right override"),
        'RLO':    (0x202e, "right-to-left override"),
        'NNBSP':  (0x202f, "narrow no-break space"),
        'MMSP':   (0x205f, "medium mathematical space"),
        'WJ':     (0x2060, "word joiner"),
        'FA':     (0x2061, "function application (`f()`)"),
        'IT':     (0x2062, "invisible times (`x`)"),
        'IS':     (0x2063, "invisible separator (`,`)"),
        'ISS':    (0x206a, "inhibit symmetric swapping"),
        'ASS':    (0x206b, "activate symmetric swapping"),
        'IAFS':   (0x206c, "inhibit arabic form shaping"),
        'AAFS':   (0x206d, "activate arabic form shaping"),
        'NADS':   (0x206e, "national digit shapes"),
        'NODS':   (0x206f, "nominal digit shapes"),
        'IDSP':   (0x3000, "ideographic space"),
        'IVI':    (0x303e, "ideographic variation indicator"),
        'VS1':    (0xfe00, "variation selector 1"),
        'VS2':    (0xfe01, "variation selector 2"),
        'VS3':    (0xfe02, "variation selector 3"),
        'VS4':    (0xfe03, "variation selector 4"),
        'VS5':    (0xfe04, "variation selector 5"),
        'VS6':    (0xfe05, "variation selector 6"),
        'VS7':    (0xfe06, "variation selector 7"),
        'VS8':    (0xfe07, "variation selector 8"),
        'VS9':    (0xfe08, "variation selector 9"),
        'VS10':   (0xfe09, "variation selector 10"),
        'VS11':   (0xfe0a, "variation selector 11"),
        'VS12':   (0xfe0b, "variation selector 12"),
        'VS13':   (0xfe0c, "variation selector 13"),
        'VS14':   (0xfe0d, "variation selector 14"),
        'VS15':   (0xfe0e, "variation selector 15, text display"),
        'TEXT':   (0xfe0e, "variation selector 15, text display"),
        'VS16':   (0xfe0f, "variation selector 16, emoji display"),
        'EMOJI':  (0xfe0f, "variation selector 16, emoji display"),
        'BOM':    (0xfeff, "zero width no-break space, byte order mark"),
        'ZWNBSP': (0xfeff, "zero width no-break space, byte order mark"),
        'IAA':    (0xfff9, "interlinear annotation anchor"),
        'IAS':    (0xfffa, "interlinear annotation separator"),
        'IAT':    (0xfffb, "interlinear annotation terminator"),
        'ORC':    (0xfffc, "object replacement character"),
        'RC':     (0xfffd, "replacement character"),
    }

    diacritics = {
        '`': (0x0300, "grave"),
        "'": (0x0301, "acute"),
        '^': (0x0302, "circumflex accent"),
        '~': (0x0303, "tilde"),
        '-': (0x0304, "macron"),
        '_': (0x0305, "overline"),
        '(': (0x0306, "breve"),
        '.': (0x0307, "dot"),
        ':': (0x0308, "diaeresis"),
        '?': (0x0309, "hook above"),
        'o': (0x030a, "ring above"),
        '"': (0x030b, "double acute accent"),
        'v': (0x030c, "caron"),
        's': (0x030d, "vertical line above"),
        'S': (0x030e, "double vertical line above"),
        '[': (0x030f, "double grave accent"),
        '@': (0x0310, "candrabinu"),
        ')': (0x0311, "inverted breve"),
        '1': (0x0312, "turned comma above"),
        '2': (0x0313, "comma above"),
        '3': (0x0314, "reversed comma above"),
        '4': (0x0315, "comma above right"),
        ']': (0x0316, "grave accent below"),
        '[': (0x0317, "acute accent below"),
        '<': (0x0318, "left tack below"),
        '>': (0x0319, "right tack below"),
        'A': (0x031a, "left angle above"),
        'h': (0x031b, "horn"),
        'r': (0x031c, "left half ring below"),
        'u': (0x031d, "up tack below"),
        'd': (0x031e, "down tack below"),
        '+': (0x031f, "plus sign below"),
        'm': (0x0320, "minus sign below"),
        'P': (0x0321, "palatalized hook below"),
        'R': (0x0322, "retroflex hook below"),
        'D': (0x0323, "dot below"),
        'E': (0x0324, "diaeresis below"),
        'O': (0x0325, "ring below"),
        'c': (0x0326, "comma below"),
        ',': (0x0327, "cedilla"),
        'K': (0x0328, "ogonek"),
        'V': (0x0329, "vertical line below"),
        '$': (0x032a, "bridge below"),
        'W': (0x032b, "inverted double arch below"),
        'H': (0x032c, "caron below"),
        'C': (0x032d, "circumflex accent below"),
        'B': (0x032e, "breve below"),
        'N': (0x032f, "inverted breve below"),
        'T': (0x0330, "tilde below"),
        'M': (0x0331, "macron below"),
        'l': (0x0332, "low line"),
        'L': (0x0333, "double low line"),
        '&': (0x0334, "tilde overlay"),
        '!': (0x0335, "short stroke overlay"),
        '|': (0x0336, "long stroke overlay"),
        '%': (0x0337, "short solidays overlay"),
        '/': (0x0338, "long solidus overlay"),
        'g': (0x0339, "right half ring below"),
        '*': (0x033a, "inverted bridge below"),
        '#': (0x033b, "square below"),
        'G': (0x033c, "seagull below"),
        'x': (0x033d, "x above"),
        ';': (0x033e, "vertical tilde"),
        '=': (0x033f, "double overline"),
    }

    icons = {
        '!':    ([0x2757, 0xfe0f], "exclamation mark"),
        '$':    (0x1f4b2, "heavy dollar sign"),
        '%%':   (0x1f3b4, "flower playing cards"),
        '%':    None,
        '%c':   ([0x2663, 0xfe0f], "club suit"),
        '%d':   ([0x2666, 0xfe0f], "diamond suit"),
        '%e':   (0x1f9e7, "red gift envelope"),
        '%h':   ([0x2665, 0xfe0f], "heart suit"),
        '%j':   (0x1f0cf, "joker"),
        '%r':   (0x1f004, "Mahjong red dragon"),
        '%s':   ([0x2660, 0xfe0f], "spade suit"),
        '&!':   ([0x1f396, 0xfe0f], "military medal"),
        '&$':   (0x1f3c6, "trophy"),
        '&':    None,
        '&0':   (0x1f3c5, "sports medal"),
        '&1':   (0x1f947, "first place medal"),
        '&2':   (0x1f948, "second place medal"),
        '&3':   (0x1f949, "third place medal"),
        '*':    None,
        '**':   ([0x2716, 0xfe0f], "heavy multiplication sign"),
        '*+':   ([0x2795, 0xfe0f], "heavy plus sign"),
        '*-':   ([0x2796, 0xfe0f], "heavy minus sign"),
        '*/':   ([0x2797, 0xfe0f], "heavy division sign"),
        '+':    (0x1f53a, "red triangle pointed up"),
        ',':    None,
        ',+':   (0x1f44d, "thumbs up"),
        ',-':   (0x1f44e, "thumbs down"),
        ',a':   ([0x261d, 0xfe0f], "point above"),
        ',d':   (0x1f447, "point down"),
        ',f':   (0x1f44a, "oncoming fist"),
        ',l':   (0x1f448, "point left"),
        ',o':   (0x1faf5, "point out"),
        ',r':   (0x1f449, "point right"),
        ',s':   (0x1f91d, "handshake"),
        ',u':   (0x1f446, "point up"),
        '-':    (0x1f53b, "red triangle pointed down"),
        '.':    None,
        '.d':   ([0x2b07, 0xfe0f], "down arrow"),
        '.l':   ([0x2b05, 0xfe0f], "left arrow"),
        '.r':   ([0x27a1, 0xfe0f], "right arrow"),
        '.u':   ([0x2b06, 0xfe0f], "up arrow"),
        '/':    ([0x2714, 0xfe0f], "check mark"),
        ':$':   (0x1f911, "money-mouth face"),
        ':':    None,
        ':(':   (0x1f61e, "disappointed face"),
        ':)':   (0x1f600, "grinning face"),
        ':*':   (0x1f618, "face blowing a kiss"),
        ':/':   (0x1f60f, "smirking face"),
        ':0':   (0x1f636, "face without mouth"),
        ':1':   (0x1f914, "thinking face"),
        ':2':   (0x1f92b, "shushing face"),
        ':3':   (0x1f617, "kissing face"),
        ':4':   (0x1f605, "grinning face with sweat"),
        ':5':   (0x1f972, "smiling face with tear"),
        ':6':   (0x1f602, "face with tears of joy"),
        ':7':   (0x1f917, "smiling face with open hands"),
        ':8':   (0x1f910, "zipper-mouth face"),
        ':9':   (0x1f923, "rolling on the floor laughing"),
        ':D':   (0x1f601, "beaming face with smiling eyes"),
        ':O':   (0x1f62f, "hushed face"),
        ':P':   (0x1f61b, "face with tongue"),
        ':S':   (0x1fae1, "saluting face"),
        ':T':   (0x1f62b, "tired face"),
        ':Y':   (0x1f971, "yawning face"),
        ':Z':   (0x1f634, "sleeping face"),
        ':[':   (0x1f641, "frowning face"),
        ':\\':  (0x1f615, "confused face"),
        ':]':   ([0x263a, 0xfe0f], "smiling face"),
        ':|':   (0x1f610, "neutral face"),
        ';':    None,
        ';)':   (0x1f609, "winking face"),
        '<':    None,
        '<3':   ([0x2764, 0xfe0f], "red heart"),
        '?':    ([0x2753, 0xfe0f], "question mark"),
        'B':    None,
        'B)':   (0x1f60e, "smiling face with sunglasses"),
        'E':    (0x2130, "script capital E"),
        'F':    (0x2131, "script capital F"),
        'M':    (0x2133, "script capital M"),
        '\"':   None,
        '\"(':  (0x201c, "left double quotation mark"),
        '\")':  (0x201d, "right double quotation mark"),
        '\"\"': (0x0022, "quotation mark"),
        '\'':   None,
        '\'(':  (0x2018, "left single quotation mark"),
        '\')':  (0x2019, "right single quotation mark"),
        '\'/':  (0x00b4, "acute accent"),
        '\'\'': (0x0027, "apostrophe"),
        '\'\\': (0x0060, "grave accent"),
        '\\':   ([0x274c, 0xfe0f], "cross mark"),
        '^':    ([0x26a0, 0xfe0f], "warning sign"),
        '{!!':  None,
        '{!!}': ([0x203c, 0xfe0f], "double exclamation mark"),
        '{!':   None,
        '{!?':  None,
        '{!?}': ([0x2049, 0xfe0f], "exclamation question mark"),
        '{':    None,
        '{(':   None,
        '{()':  None,
        '{()}': (0x1f534, "red circle"),
        '{[':   None,
        '{[]':  None,
        '{[]}': (0x1f7e5, "red square"),
        '{{':   None,
        '{{}':  None,
        '{{}}': ([0x2b55, 0xfe0f], "hollow red circle"),
        '|':    (0x1f346, "aubergine"),
        '~':    ([0x3030, 0xfe0f], "wavy dash"),
    }

    emojis = {}

    def __init__(self, **kwargs):
        # Meta variables.
        self._names = []
        self._specs = {}
        self._initials = {}
        self._descriptions = {}
        self._nones = {}
        self._functions = {}
        # Initialize.
        self.initialize()
        # Mark initialized.
        self._initialized = True
        # Update with any keyword arguments, if specified.
        self.update(**kwargs)

    def __setattr__(self, name, value):
        self.set(name, value)

    def __contains__(self, name):
        return name in self.__dict__

    def __bool__(self): return self._initialized # 3.x
    def __nonzero__(self): return self._initialized # 2.x

    def __iter__(self):
        return iter(self._names)

    def __str__(self):
        results = []
        for name in self._names:
            results.append("%s=%s" % (name, repr(self.get(name))))
        return ', '.join(results)

    # Initialization.

    def initialize(self):
        """Setup the declarations and definitions for the defined
        attributes."""
        self.define('name', strType, self.defaultName, "The name of this configuration (optional)")
        self.define('notes', None, None, "Notes for this configuration (optional)")
        self.define('prefix', strType, self.defaultPrefix, "The prefix", none=True, env=PREFIX_ENV)
        self.define('pseudomoduleName', strType, self.defaultPseudomoduleName, "The pseudomodule name", env=PSEUDO_ENV)
        self.define('verbose', bool, False, "Verbose processing (for debugging)?")
        self.define('rawErrors', bool, None, "Print Python stacktraces on error?", env=RAW_ERRORS_ENV)
        self.define('exitOnError', bool, True, "Exit after an error?")
        self.define('contextFormat', strType, self.defaultContextFormat, "Context format")
        self.define('goInteractive', bool, None, "Go interactive after done processing?", env=INTERACTIVE_ENV)
        self.define('deleteOnError', bool, None, "Delete output file on error?", env=DELETE_ON_ERROR_ENV)
        self.define('doFlatten', bool, None, "Flatten pseudomodule members at start?", env=FLATTEN_ENV)
        self.define('useProxy', bool, None, "Install a stdout proxy?", env=NO_PROXY_ENV, invert=True)
        self.define('relativePath', bool, False, "Add EmPy script path to sys.path?")
        self.define('buffering', int, self.defaultBuffering, "Specify buffering strategy for files:\n0 (none), 1 (line), -1 (full), or N", env=BUFFERING_ENV, func=self.setBuffering)
        self.define('noCallbackIsError', bool, True, "Is custom markup with no callback an error?")
        self.define('replaceNewlines', bool, True, "Replace newlines with spaces in expressions?")
        self.define('ignoreBangpaths', bool, True, "Treat bangpaths as comments?")
        self.define('noneSymbol', (strType, None), None, "String to write when expanding None")
        self.define('missingConfigIsError', bool, True, "Is a missing configuration file an error?")
        self.define('pauseAtEnd', bool, False, "Prompt at the end of processing?")
        self.define('startingLine', int, 1, "Line number to start with")
        self.define('startingColumn', int, 1, "Column number to start with")
        self.define('significatorDelimiters', tuple, self.defaultSignificatorDelimiters, "Significator variable delimiters")
        self.define('emptySignificator', object, self.defaultEmptySignificator, "Value to use for empty significators", none=True)
        self.define('autoValidateIcons', bool, self.defaultAutoValidateIcons, "Automatically validate icons before each use?")
        self.define('emojiModuleNames', list, self.defaultEmojiModuleNames, "List of emoji modules to try to use\n", none=True)
        self.define('emojiNotFoundIsError', bool, True, "Is an unknown emoji an error?")
        self.define('useBinary', bool, False, "Open files as binary (Python 2.x Unicode)?", env=BINARY_ENV)
        defaultEncoding = self.environment(ENCODING_ENV, self.getDefaultEncoding())
        self.define('inputEncoding', strType, defaultEncoding, "Set input Unicode encoding", none=True, env=INPUT_ENCODING_ENV, helpFunction=lambda x: x == 'utf_8' and 'utf-8' or x)
        self.define('outputEncoding', strType, defaultEncoding, "Set output Unicode encoding", none=True, env=OUTPUT_ENCODING_ENV, helpFunction=lambda x: x == 'utf_8' and 'utf-8' or x)
        defaultErrors = self.environment(ERRORS_ENV, self.defaultErrors)
        self.define('inputErrors', strType, defaultErrors, "Set input Unicode error handler", none=True, env=INPUT_ERRORS_ENV)
        self.define('outputErrors', strType, defaultErrors, "Set output Unicode error handler", none=True, env=OUTPUT_ERRORS_ENV)
        self.define('normalizationForm', strType, self.defaultNormalizationForm, "Specify Unicode normalization form", none=True)
        self.define('autoPlayDiversions', bool, True, "Auto-play diversions on exit?")
        self.define('expandUserConstructions', bool, True, "Expand ~ and ~user constructions")
        self.define('configVariableName', strType, self.defaultConfigVariableName, "Configuration variable name while loading")
        self.define('successCode', int, self.defaultSuccessCode, "Exit code to return on script success")
        self.define('failureCode', int, self.defaultFailureCode, "Exit code to return on script failure")
        self.define('unknownCode', int, self.defaultUnknownCode, "Exit code to return on bad configuration")
        self.define('checkVariables', bool, True, "Check configuration variables on assignment?")
        self.define('pathSeparator', strType, sys.platform.startswith('win') and ';' or ':', "Path separator for configuration file paths")

        # Redefine static configuration variables so they're in the help.
        self.define('controls', dict, self.controls, "Controls dictionary")
        self.define('diacritics', dict, self.diacritics, "Diacritics dictionary")
        self.define('icons', dict, self.icons, "Icons dictionary")
        self.define('emojis', dict, self.emojis, "Emojis dictionary")
        # If the encoding or error handling has changed, enable binary
        # implicitly, just as if it had been specified on the command line.
        if (self.inputEncoding != defaultEncoding or
            self.outputEncoding != defaultEncoding or
            self.inputErrors != defaultErrors or
            self.outputErrors != defaultErrors):
            self.enableBinary(major, minor)

    def isInitialized(self):
        """Is this configuration initialized and ready for use?"""
        return self._initialized

    def check(self, inputFilename, outputFilename):
        """Do a sanity check on the configuration settings."""
        if self.prefix == '' or self.prefix == 'none' or self.prefix == 'None':
            self.prefix = None
        if self.buffering is None:
            self.buffering = self.defaultBuffering
        if isinstance(self.prefix, strType) and len(self.prefix) != 1:
            raise ConfigurationError("prefix must be single-character string")
        if not self.pseudomoduleName:
            raise ConfigurationError("pseudomodule name must be non-empty string")
        if self.deleteOnError and outputFilename is None:
            raise ConfigurationError("-d only makes sense with -o, -a, -O or -A arguments")
        if self.hasNoBuffering() and not self.hasBinary():
            raise ConfigurationError("no buffering requires file open in binary mode; try adding -u option")

    # Access.

    def declare(self, name, specs, initial, description,
                none=False, helpFunction=None):
        """Declare the configuration attribute."""
        self._names.append(name)
        self._specs[name] = specs
        self._initials[name] = initial
        self._descriptions[name] = description
        self._nones[name] = none
        self._functions[name] = helpFunction

    def define(self, name, specs, value, description, none=False,
               env=None, func=None, blank=None, invert=False, helpFunction=None):
        """Define a configuration attribute with the given name, type
        specification, initial value, and description.  If none is true, None
        is a legal value.  Also, allow an optional corresponding environment
        variable, and, if present, an optional blank variable to set the
        value to if the environment variable is defined but is blank.  If
        both env and func are present, call the function to set the
        environment variable.  Finally, if invert is true, invert the
        (bool) environment variable.  Additionally, if the type specification
        is or contains toString, convert the value to a proper string."""
        if isinstance(specs, tuple):
            isString = str in specs or bytes in specs
        else:
            isString = str is specs or bytes is specs
        if value is not None and specs is not None:
            assert isinstance(value, specs)
        if env is not None:
            if func is not None:
                if self.hasEnvironment(env):
                    value = func(self.environment(env, value))
            elif isString:
                value = self.environment(env, value, blank)
            elif specs is bool:
                value = self.hasEnvironment(env)
                if invert:
                    value = not value
            elif not isinstance(specs, tuple):
                value = specs(self.environment(env, value, blank))
            else:
                assert False, "environment attribute type must be bool or str: %s" % name
        if isString and value is not None:
            value = toString(value)
        self.declare(name, specs, value, description, none, helpFunction)
        self.set(name, value)

    def has(self, name):
        """Is this name a valid configuration attribute?"""
        return name in self.__dict__ or name in self.__class__.__dict__

    def get(self, name, default=None):
        """Get this (valid, existing) configuration attribute."""
        return getattr(self, name, default)

    def set(self, name, value):
        """Set the (valid) configuration attribute, checking its type
        if necessary."""
        if self._initialized and self.checkVariables:
            if not name.startswith('_'):
                # If this attribute is not already present, it's invalid.
                if not self.has(name):
                    raise ConfigurationError("unknown configuration attribute: %s" % name)
                # If there's a registered type for this attribute, check it.
                specs = self._specs.get(name)
                if specs is not None:
                    if value is None:
                        if not self._nones[name]:
                            raise ConfigurationError("configuration value cannot be None: %s: %s; %s" % (name, value, specs))
                    elif not isinstance(value, specs):
                        raise ConfigurationError("configuration value has invalid type: %s: %s; %s" % (name, value, specs))
        self.__dict__[name] = value

    def update(self, **kwargs):
        """Update the configuration by keyword arguments."""
        for name, value in kwargs.items():
            if not self.has(name):
                raise ConfigurationError("unknown configuration attribute: %s" % name)
            self.set(name, value)

    # Configuration file loading.

    def run(self, statements):
        """Run some configuration variable assignment statements."""
        locals = {self.configVariableName: self}
        execFunc(statements, globals(), locals)
        keys = list(locals.keys())
        # Put the priority variables first.
        for priority in self.priorityVariables:
            if priority in locals:
                keys.remove(priority)
                keys.insert(0, priority)
        for key in keys:
            if not key.startswith('_') and key != self.configVariableName:
                setattr(self, key, locals[key])
        return True

    def load(self, filename, required=None):
        """Update the configuration by loading from a resource
        file.  If required is true, raise an exception; if false,
        ignore; if None, use the default in this configuration.
        Return whether or not the load succeeded."""
        if required is None:
            required = self.missingConfigIsError
        try:
            file = self.open(filename, 'r')
        except IOError:
            if required:
                raise ConfigurationFileNotFoundError("cannot open configuration file: %s" % filename, filename)
            return False
        locals = {self.configVariableName: self}
        try:
            contents = file.read()
            return self.run(contents)
        finally:
            file.close()

    def path(self, path, required=None):
        """Attempt to load several resource paths, either as a
        list of paths or a delimited string of paths.  If required
        is true, raise an exception; if false, ignore; if None,
        use the default in this configuration."""
        if isinstance(path, list):
            filenames = path
        else:
            filenames = path.split(self.pathSeparator)
        for filename in filenames:
            self.load(filename, required)

    # Environment.

    def hasEnvironment(self, name):
        """Is the current environment variable defined in the environment?
        The value does not matter."""
        return name in os.environ

    def environment(self, name, default=None, blank=None):
        """Get the value of the given environment variable, or default
        if it is not set.  If a variable is set to an empty value and
        blank is non-None, return blank instead."""
        if name in os.environ:
            value = os.environ[name]
            if not value and blank is not None:
                return blank
            else:
                return value
        else:
            return default

    # Convenience.

    def escaped(self, ord, prefix='\\'):
        """Write a valid Python string escape sequence for the given
        character ordinal."""
        if ord <= 0xff:
            return '%sx%02x' % (prefix, ord)
        elif ord <= 0xffff:
            return '%su%04x' % (prefix, ord)
        else:
            return '%sU%08x' % (prefix, ord)

    def hasDefaultPrefix(self):
        """Is this configuration's prefix the default or
        non-existent?"""
        return self.prefix is None or self.prefix == self.defaultPrefix

    # Buffering.

    def hasFullBuffering(self): return self.buffering <= self.fullBuffering
    def hasNoBuffering(self): return self.buffering == self.noBuffering
    def hasLineBuffering(self): return self.buffering == self.lineBuffering
    def hasFixedBuffering(self):
        return self.buffering is not None and self.buffering > self.lineBuffering

    def setBuffering(self, name):
        """Set the buffering by name or value."""
        if isinstance(name, int):
            self.buffering = name
        elif name == 'none':
            self.buffering = self.noBuffering
        elif name == 'line':
            self.buffering = self.lineBuffering
        elif name == 'full':
            self.buffering = self.fullBuffering
        elif name is None or name == 'default' or name == '':
            self.buffering = self.defaultBuffering
        else:
            try:
                self.buffering = int(name)
            except ValueError:
                raise ConfigurationError("invalid buffering name: %s" % name)
        if self.buffering < self.fullBuffering:
            self.buffering = self.fullBuffering
        return self.buffering

    # Token factories.

    def createFactory(self, tokens=None):
        """Create a token factory and return it."""
        if tokens is None:
            tokens = self.tokens
        return Factory(tokens)

    def adjustFactory(self):
        """Adjust the factory to take into account a non-default
        prefix."""
        self.factory.adjust(self)

    def getFactory(self, tokens=None, force=False):
        """Get a factory (creating one if one has not yet been
        created).  If force is true, always create a new one."""
        if self.factory is None or force:
            self.factory = self.createFactory(tokens)
            self.adjustFactory()
        return self.factory

    def resetFactory(self):
        """Clear the current factory."""
        self.factory = None

    # Binary/Unicode.

    def hasBinary(self):
        """Is binary/Unicode file open support enabled?"""
        return self.useBinary

    def enableBinary(self, major=None, minor=None):
        """Enable binary/Unicode file open support.  This is needed in
        Python 2.x for Unicode support.  If major/minor is present, only
        enable it implicitly if this is in fact Python 2.x."""
        if major is None or major == 2:
            self.useBinary = True

    def disableBinary(self):
        """Disable binary/Unicode support for this configuration."""
        self.useBinary = False

    # File I/O.

    def isDefaultEncodingErrors(self, encoding=None, errors=None, asInput=True):
        """Are both of the encoding/errors combinations the default?
        If either passed value is None the value in this configuration
        is what is checked.  Check for input if asInput is true;
        otherwise check output."""
        if encoding is None:
            if asInput:
                encoding = self.inputEncoding
            else:
                encoding = self.outputEncoding
        if encoding is not None and encoding != self.getDefaultEncoding():
            return False
        if errors is None:
            if asInput:
                errors = self.inputErrors
            else:
                errors = self.outputErrors
        if errors is not None and errors != self.defaultErrors:
            return False
        return True

    def getDefaultEncoding(self, default='unknown'):
        """What is the default encoding?"""
        try:
            return sys.getdefaultencoding()
        except AttributeError:
            return default

    def open(self, filename,
             mode=None, buffering=-1, encoding=None, errors=None,
             expand=None):
        """Open a new file, handling whether or not binary
        (Unicode) should be employed.  Raise if the selection
        cannot be complied with.  Arguments:

        - filename: The filename to open;
        - mode: The file open mode, None for read;
        - buffering: The buffering setting (int);
        - encoding: The encoding to use, None for default;
        - errors: The error handler to use, None for default;
        - expand: Expand user constructions? (~ and ~user)"""
        if expand is None:
            expand = self.expandUserConstructions
        if expand:
            filename = os.path.expanduser(filename)
        if mode is None:
            # Default to read.
            mode = 'r'
            if self.useBinary and 'b' not in mode:
                # Make it binary if it needs to be.
                mode += 'b'
        # Figure out the encoding and error handler.
        if 'w' in mode or 'a' in mode:
            if encoding is None:
                encoding = self.outputEncoding
            if errors is None:
                errors = self.outputErrors
        else:
            if encoding is None:
                encoding = self.inputEncoding
            if errors is None:
                errors = self.inputErrors
        if self.useBinary:
            # Use binary mode, so call codecs.open.
            return codecs.open(filename, mode, encoding, errors, buffering)
        else:
            # If it's not binary mode, them use the standard open call.
            if major >= 3:
                # If it's Python 3.x, just pass the arguments through.
                return open(filename, mode, buffering, encoding, errors)
            else:
                # For Python 2.x, open doesn't take encoding and error handler
                # arguments.  Check to make sure non-default encodings and
                # error handlers haven't been chosen, because we can't comply.
                if not self.isDefaultEncodingErrors(encoding, errors):
                    raise ConfigurationError("cannot comply with non-default Unicode encoding/errors selected in Python 2.x; use -u option: %s/%s" % (encoding, errors))
                return open(filename, mode, buffering)

    # Significators.

    def significatorReString(self):
        """Return a string that can be compiled into a regular
        expression representing a significator.  If multi is true,
        it will match multiline significators."""
        return self.prefix + self.significatorReStringSuffix

    def significatorRe(self, flags=re.MULTILINE|re.DOTALL,
                       baseFlags=re.VERBOSE):
        """Return a regular expression object with the given
        flags that is suitable for parsing significators."""
        return re.compile(self.significatorReString(), flags|baseFlags)

    def significatorFor(self, key):
        """Return the significator name for this key."""
        prefix, suffix = self.significatorDelimiters
        return prefix + toString(key) + suffix

    # Contexts.

    def setContextFormat(self, rawFormat):
        """Set the context format, auto-detecting which
        mechanism to use."""
        useFormatMethod = None
        format = rawFormat
        if format.startswith('format:'):
            useFormatMethod = True
            format = format.split(':', 1)[1]
        elif format.startswith('operator:'):
            useFormatMethod = False
            format = format.split(':', 1)[1]
        elif format.startswith('variable:'):
            useFormatMethod = False
            format = format.split(':', 1)[1]
            format = format.replace('$NAME', '%(name)s')
            format = format.replace('$LINE', '%(line)d')
            format = format.replace('$COLUMN', '%(column)d')
            format = format.replace('$CHARS', '%(chars)d')
        else:
            useFormatMethod = '%' not in format
        self.contextFormat = format
        self.useContextFormatMethod = useFormatMethod

    def renderContext(self, context):
        """Render the context as a string according to this
        configuration."""
        if self.useContextFormatMethod is None:
            self.setContextFormat(self.contextFormat)
        return context.render(self.contextFormat, self.useContextFormatMethod)

    # Icons.

    def calculateIconsSignature(self, icons=None):
        """Calculate a signature of the icons dict.  If the value
        changes, it's likely (but not certain) that the underlying
        dict has changed.  The signature will always differ from
        None."""
        if icons is None:
            icons = self.icons
        length = len(icons)
        try:
            # Include the size of the dictionary, if possible.  If it's not
            # available, that's okay.
            sizeof = sys.getsizeof(icons)
        except (AttributeError, TypeError):
            sizeof = -1
        return length, sizeof

    def signIcons(self, icons=None):
        """Sign the icons dict."""
        self.iconsSignature = self.calculateIconsSignature(icons)
        return self.iconsSignature

    def transmogrifyIcons(self, icons=None):
        """Process the icons and make sure any keys' prefixes are
        backfilled with Nones.  Call this method after modifying
        icons."""
        if icons is None:
            icons = self.icons
        additions = {}
        for parent in icons.keys():
            key = parent
            while len(key) > 1:
                key = key[:-1]
                if key in icons:
                    value = icons[key]
                    if value is None:
                        continue
                    else:
                        raise ConfigurationError("icon '%s' makes icon '%s' inaccessible" % (key, parent))
                else:
                    additions[key] = None
        icons.update(additions)
        return icons

    def validateIcons(self, icons=None):
        """If the icons have not been transmogrified yet, do so
        and store their signature for future reference."""
        if icons is None:
            icons = self.icons
        if icons is None:
            raise ConfigurationError("icons not configured")
        if not self.autoValidateIcons:
            return icons
        if self.iconsSignature is None:
            self.transmogrifyIcons(icons)
            self.signIcons(icons)
        return icons

    # Emojis.

    def initializeEmojiModules(self, moduleNames=None):
        """Initialize the emoji modules.  If moduleNames is not
        specified, check the defaults.  Idempotent."""
        if self.emojiModules is None:
            okNames = []
            # Use the config default if not specified.
            if moduleNames is None:
                moduleNames = self.emojiModuleNames
            # If it's still blank, specify no modules.
            if moduleNames is None:
                moduleNames = []
            # Create a map of module names for fast lookup.  (This would be a
            # set, but sets aren't available in early versions of Python 2.x.)
            nameMap = {}
            for moduleName in moduleNames:
                nameMap[moduleName] = None
            # Now iterate over each potential module.
            self.emojiModules = {}
            for info in self.emojiModuleInfos:
                moduleName = info[0]
                if moduleName in nameMap:
                    module = Module(*info)
                    if module.ok:
                        okNames.append(moduleName)
                        self.emojiModules[moduleName] = module
            # Finally, replace the requested module names with the ones
            # actually present.
            self.emojiModuleNames = okNames
            if not self.emojiModules and not self.emojis:
                raise ConfigurationError("no emoji lookup methods available; install modules and set emoji modules or set emojis dictionary in configuration")

    def substituteEmoji(self, text):
        """Substitute emojis from the provided string.  Return
        the resulting substitution or None."""
        if self.replaceNewlines:
            text = text.replace('\n', ' ')
        self.initializeEmojiModules()
        for moduleName in self.emojiModuleNames:
            module = self.emojiModules[moduleName]
            result = module.substitute(text)
            if result is not None:
                return result

    # Exit codes and errors.

    def isSuccessCode(self, code):
        """Does this exit code indicate success?"""
        return code == self.successCode

    def isExitError(self, error):
        """Is this error a SystemExit?"""
        return isinstance(error, SystemExit)

    def errorToExitCode(self, error):
        """Determine the exit code (can be a string) from the
        error.  If the error is None, then it is success."""
        isExit = self.isExitError(error)
        if isExit:
            if len(error.args) == 0:
                return self.successCode
            else:
                # This can be a string which is okay.
                return error.args[0]
        else:
            return self.failureCode

    def isNotAnError(self, error):
        """Is this error None (no error) or does it indicate a
        successful exit?"""
        if error is None:
            return True
        else:
            return self.isSuccessCode(self.errorToExitCode(error))

    def formatError(self, error, prefix=None, suffix=None):
        """Format an error into a string for printing."""
        parts = []
        if prefix is not None:
            parts.append(prefix)
        parts.append(error.__class__.__name__)
        args = []
        # Check for arguments.
        if len(error.args) > 0:
            parts.append(": ")
            args = [toString(x) for x in error.args]
        # Check for keyword arguments.
        pairs = []
        for attrib in dir(error):
            if (attrib not in self.ignorableErrorAttributes and
                not attrib.startswith('_')):
                pairs.append((attrib, getattr(error, attrib)))
        if pairs:
            pairs.sort()
            for key, value in pairs:
                args.append("%s=%s" % (key, value))
        # Fold the arguments together.
        parts.append(', '.join(args))
        if suffix is not None:
            parts.append(suffix)
        return ''.join(parts)

#
# Version
#

class Version(Root):

    """An enumerated type representing version detail levels."""

    NONE, VERSION, INFO, BASIC, PYTHON, SYSTEM, PLATFORM, RELEASE, ALL = range(9)
    DATA = BASIC

#
# Stack
#

class Stack(Root):

    """A simple stack that is implemented as a sequence."""

    def __init__(self, seq=None):
        if seq is None:
            seq = []
        self.data = seq

    def __bool__(self): return len(self.data) != 0 # 3.x
    def __nonzero__(self): return len(self.data) != 0 # 2.x

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.data[-(index + 1)]

    def __str__(self):
        return '[%s]' % ', '.join([repr(x) for x in self.data])

    def top(self):
        """Access the top element on the stack."""
        if self.data:
            return self.data[-1]
        else:
            raise StackUnderflowError("stack is empty for top")

    def pop(self):
        """Pop the top element off the stack and return it."""
        if self.data:
            return self.data.pop()
        else:
            raise StackUnderflowError("stack is empty for pop")

    def push(self, object):
        """Push an element onto the top of the stack."""
        self.data.append(object)

    def replace(self, object):
        """Replace the top element of the stack with another one."""
        if self.data:
            self.data[-1] = object
        else:
            raise StackUnderflowError("stack is empty for replace")

    def filter(self, function):
        """Filter the elements of the stack through the function."""
        self.data = list(filter(function, self.data))

    def purge(self, function=None):
        """Purge the stack, calling an optional function on each element
        first from top to bottom."""
        if function is None:
            self.data = []
        else:
            while self.data:
                element = self.data.pop()
                function(element)

    def clone(self):
        """Create a duplicate of this stack."""
        return self.__class__(self.data[:])

#
# File ...
#

class File(Root):

    """An abstract filelike object."""

    def write(self, data): raise NotImplementedError
    def writelines(self, lines): raise NotImplementedError
    def flush(self): raise NotImplementedError
    def close(self): raise NotImplementedError


class NullFile(File):

    """A simple class that supports all the file-like object methods
    but simply does nothing at all."""

    def write(self, data): pass
    def writelines(self, lines): pass
    def flush(self): pass
    def close(self): pass


class DelegatingFile(File):

    """A simple class which wraps around a delegate file-like object
    and lets everything through."""

    def __init__(self, delegate):
        self.delegate = delegate

    def __repr__(self):
        return "<%s : %s @ 0x%x>" % (
            self.__class__.__name__,
            repr(self.delegate),
            id(self))

    def write(self, data):
        self.delegate.write(data)

    def writelines(self, lines):
        self.delegate.writelines(data)

    def flush(self):
        self.delegate.flush()

    def close(self):
        self.delegate.close()
        self.unlink()

    def unlink(self):
        """Unlink from the delegate."""
        self.delegate = None


class UncloseableFile(DelegatingFile):

    """A delegating file class that lets through everything except
    close calls, which it turns into a flush."""

    def close(self):
        self.flush()


class ProxyFile(File):

    """The proxy file object that is intended to take the place of
    sys.stdout.  The proxy can manage a stack of interpreters (and
    their file object streams) it is writing to, and an underlying
    bottom file object."""

    def __init__(self, bottom, wrapper=None):
        """Create a new proxy file object with bottom as the
        underlying stream.  If wrapper is not None (and is an instance
        of (a subclass of) a DelegatingFile), we should wrap and
        unwrap the bottom file with it for protection."""
        assert bottom is not None
        self._EmPy_original = sys.stdout
        self._EmPy_count = 0
        self.stack = Stack()
        self.bottom = bottom
        self.wrapper = wrapper
        self.wrap()

    def __getattr__(self, attribute):
        return getattr(self.bottom, attribute)

    def __repr__(self):
        return "<%s [count %d] : %s @ 0x%x>" % (
            self.__class__.__name__,
            self._EmPy_count,
            repr(self.bottom),
            id(self))

    # Bottom file protection.

    def shouldWrap(self):
        """Should the bottom file be wrapped and unwrapped?"""
        return self.wrapper is not None

    def wrap(self):
        """Wrap the bottom file in a delegate."""
        if self.shouldWrap():
            assert issubclass(self.wrapper, DelegatingFile)
            self.bottom = self.wrapper(self.bottom)

    def unwrap(self):
        """Unwrap the bottom file from the delegate, and unlink the
        delegate."""
        if self.shouldWrap():
            wrapped = self.bottom
            self.bottom = wrapped.delegate
            wrapped.unlink()

    # File methods.

    def write(self, data):
        top = self.top()
        assert top is not None
        top.write(data)

    def writelines(self, lines):
        top = self.top()
        assert top is not None
        top.writelines(lines)

    def flush(self):
        top = self.top()
        assert top is not None
        top.flush()

    def close(self):
        """Close the current file.  If the current file is the bottom,
        then flush it (don't close it) and dispose of it."""
        top = self.top()
        assert top is not None
        if top is self.bottom:
            # If it's the bottom stream, flush it, don't close it, and mark
            # this proxy done.
            top.flush()
            self.bottom = None
        else:
            top.close()

    # Stack management.

    def top(self):
        """Get the current stream (not interpreter) to write to."""
        if self.stack:
            return self.stack.top().top()
        else:
            return self.bottom

    def push(self, interpreter):
        self.stack.push(interpreter)

    def pop(self, interpreter):
        top = self.stack.pop()
        assert interpreter is top

    def clear(self, interpreter):
        self.stack.filter(lambda x, i=interpreter: x is not i)

    # Special.

    def _EmPy_evocare(self, increment):
        """Do the EmPy magic:  Increment or decrement the reference
        count.  Either way, return the current reference count.
        Beware of Exodus!"""
        if increment > 0:
            self._EmPy_count += increment
        elif increment < 0:
            self._EmPy_count += increment # note: adding a negative number
            if self._EmPy_count <= 0:
                assert self._EmPy_original is not None
                self.unwrap()
                sys.stdout = self._EmPy_original
        return self._EmPy_count

#
# Diversion
#

class Diversion(File):

    """The representation of an active diversion.  Diversions act as
    (writable) file objects, and then can be recalled either as pure
    strings or (readable) file objects."""

    def __init__(self, name):
        self.name = name
        self.file = StringIO()

    def __str__(self):
        return self.name

    # These methods define the writable file-like interface for the diversion.

    def write(self, data):
        self.file.write(data)

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

    # These methods are specific to diversions.

    def preferFile(self):
        """Would this particular diversion prefer to be treated as a
        file (true) or a string (false)?  This allows future
        optimization of diversions into actual files if they get
        overly large."""
        return False

    def asString(self):
        """Return the diversion as a string."""
        return self.file.getvalue()

    def asFile(self):
        """Return the diversion as a file."""
        return StringIO(self.file.getvalue())

    def spool(self, output, chunkSize=Configuration.defaultBuffering):
        """Spool the diversion to the given output file."""
        if self.preferFile():
            # Either write it a chunk at a time ...
            input = self.asFile()
            while True:
                chunk = input.read(chunkSize)
                if not chunk:
                    break
                output.write(chunk)
        else:
            # ... or write it all at once.
            output.write(self.asString())

#
# Stream
#

class Stream(File):

    """A wrapper around an (output) file object which supports
    diversions and filtering."""

    # File methods.

    def __init__(self, file, diversions):
        assert file is not None
        self.file = file
        self.current = None
        self.diversions = diversions
        self.filter = file
        self.done = False

    def __repr__(self):
        return '<%s : %s @ 0x%x>' % (
            self.__class__.__name__,
            repr(self.file),
            id(self))

    def write(self, data):
        if self.current is None:
            self.filter.write(toString(data))
        else:
            self.diversions[self.current].write(toString(data))

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        self.filter.flush()

    def close(self):
        if not self.done:
            self.filter.close()
            self.done = True

    # Filters.

    def count(self):
        """Count the number of filters."""
        thisFilter = self.filter
        result = 0
        while thisFilter is not None and thisFilter is not self.file:
            thisFilter = thisFilter.follow()
            result += 1
        return result

    def last(self):
        """Find the last filter in the current filter chain, or None if
        there are no filters installed."""
        if self.filter is None:
            return None
        thisFilter, lastFilter = self.filter, None
        while thisFilter is not None and thisFilter is not self.file:
            lastFilter = thisFilter
            thisFilter = thisFilter.follow()
        return lastFilter

    def install(self, filters=None):
        """Install a list of filters as a chain, replacing the current
        chain."""
        self.filter.flush()
        if filters is None:
            filters = []
        if len(filters) == 0:
            # An empty sequence means no filter.
            self.filter = self.file
        else:
            # If there's more than one filter provided, chain them together.
            lastFilter = None
            for filter in filters:
                if lastFilter is not None:
                    lastFilter.attach(filter)
                lastFilter = filter
            lastFilter.attach(self.file)
            self.filter = filters[0]

    def prepend(self, filter):
        """Attach a solitary filter (no sequences allowed here)
        at the beginning of the current filter chain."""
        self.filter.flush()
        firstFilter = self.filter
        if firstFilter is None:
            # Just install it from scratch if there is no active filter.
            self.install([filter])
        else:
            # Attach this filter to the current one, and set this as the main
            # filter.
            filter.attach(firstFilter)
            self.filter = filter

    def append(self, filter):
        """Attach a solitary filter (no sequences allowed here) at the
        end of the current filter chain."""
        self.filter.flush()
        lastFilter = self.last()
        if lastFilter is None:
            # Just install it from scratch if there is no active filter.
            self.install([filter])
        else:
            # Attach the last filter to this one, and this one to the file.
            lastFilter.attach(filter)
            filter.attach(self.file)

    # Diversions.

    def names(self):
        """Return a sorted sequence of diversion names."""
        keys = list(self.diversions.keys())
        keys.sort()
        return keys

    def has(self, name):
        """Does this stream have a diversion with the given name?"""
        return name in self.diversions

    def revert(self):
        """Reset any current diversions."""
        self.current = None

    def create(self, name):
        """Create a diversion if one does not already exist, but do not
        divert to it yet.  Return the diversion."""
        if name is None:
            raise DiversionError("diversion name must be non-None")
        diversion = None
        if not self.has(name):
            diversion = Diversion(name)
            self.diversions[name] = diversion
        return diversion

    def retrieve(self, name, *defaults):
        """Retrieve the given diversion.  If an additional argument is
        provided, return that instead of raising on a nonexistent
        diversion."""
        if name is None:
            raise DiversionError("diversion name must be non-None")
        if self.has(name):
            return self.diversions[name]
        else:
            if defaults:
                return defaults[0]
            else:
                raise DiversionError("nonexistent diversion: %s" % name)

    def divert(self, name):
        """Start diverting."""
        if name is None:
            raise DiversionError("diversion name must be non-None")
        self.create(name)
        self.current = name

    def undivert(self, name, dropAfterwards=False):
        """Undivert a particular diversion."""
        if name is None:
            raise DiversionError("diversion name must be non-None")
        if self.has(name):
            diversion = self.diversions[name]
            diversion.spool(self.filter)
            if dropAfterwards:
                self.drop(name)
        else:
            raise DiversionError("nonexistent diversion: %s" % name)

    def drop(self, name):
        """Drop the specified diversion."""
        if name is None:
            raise DiversionError("diversion name must be non-None")
        if self.has(name):
            del self.diversions[name]
            if self.current == name:
                self.current = None

    def undivertAll(self, dropAfterwards=True):
        """Undivert all pending diversions."""
        if self.diversions:
            self.revert() # revert before undiverting!
            for name in self.names():
                self.undivert(name, dropAfterwards)

    def dropAll(self):
        """Eliminate all existing diversions."""
        if self.diversions:
            self.diversions.clear()
        self.current = None

#
# Context ...
#

class Context(Root):

    """A simple interpreter context, storing only the current data.
    It is not intended to be modified."""

    format = Configuration.defaultContextFormat

    def __init__(self, name, line, column, chars=0):
        self.name = name
        self.line = line
        self.column = column
        self.chars = chars

    def __str__(self):
        return self.render(self.format)

    def render(self, format, useFormatMethod=None):
        """Render the context with the given format.  If
        useFormatMethod is true, use the format method; if false, use
        the % operator.  If useFormatMethod is None, try to trivially
        auto-detect given the format."""
        record = {
            'name': self.name,
            'line': self.line,
            'column': self.column,
            'chars': self.chars,
        }
        if useFormatMethod is None:
            # If it contains a percent sign, it looks like it's not using the
            # format method.
            useFormatMethod = '%' not in format
        if useFormatMethod:
            return format.format(**record)
        else:
            return format % record

    def identify(self):
        return self.name, self.line, self.column, self.chars


class FullContext(Context):

    """An full interpreter context, which stores the current data as
    well as data to accumulate."""

    def __init__(self, name, line, column, chars=0,
                 startingLine=None, startingColumn=None):
        # Don't use super for very early Python 2.x compatibility.
        super(FullContext, self).__init__(name, line, column, chars)
        if startingLine is None:
            startingLine = line
        self.startingLine = startingLine
        if startingColumn is None:
            startingColumn = column
        self.startingColumn = startingColumn
        self.pendingLines = 0
        self.pendingColumns = 0
        self.pendingChars = 0

    def reset(self):
        """Reset the context to the start."""
        self.line = startingLine
        self.column = startingColumn
        self.chars = 0

    def track(self, string, start, end):
        """Track the information for the substring in [start, end) in
        the context and mark it pending."""
        assert end >= start
        if end > start:
            length = end - start
            self.pendingLines += string.count(NEWLINE_CHAR, start, end)
            loc = string.rfind(NEWLINE_CHAR, start, end)
            if loc == -1:
                self.pendingColumns += length
            else:
                self.pendingColumns = self.startingColumn + end - loc - 1
            self.pendingChars += length

    def accumulate(self):
        """Accumulate the pending information and incorporate it into
        the total."""
        self.line += self.pendingLines
        if self.pendingLines > 0:
            self.column = self.pendingColumns # replaced, not added
        else:
            self.column += self.pendingColumns
        self.chars += self.pendingChars
        self.pendingLines = 0
        self.pendingColumns = 0
        self.pendingChars = 0

    def save(self, strict=False):
        """Take a snapshot of the current context."""
        if strict and self.pendingChars == 0:
            raise ConsistencyError("context %s has pending chars" % toString(self))
        return Context(self.name, self.line, self.column, self.chars)

    def restore(self, old, strict=False):
        """Restore an old context."""
        if strict and self.pendingChars == 0:
            raise ConsistencyError("context %s has pending chars" % toString(self))
        self.name = old.name
        self.line = old.line
        self.column = old.column
        self.chars = old.chars

#
# Token ...
#

class Token(Root):

    """An element resulting from parsing."""

    def __init__(self, current):
        self.current = current

    def __str__(self):
       return self.string()

    def string(self):
        raise NotImplementedError

    def run(self, interpreter, locals):
        raise NotImplementedError


class TextToken(Token):

    """A chunk of text not containing markups."""

    def __init__(self, current, data):
        super(TextToken, self).__init__(current)
        self.data = data

    def string(self):
        return self.data

    def run(self, interpreter, locals):
        interpreter.write(self.data)


class ExpansionToken(Token):

    """A token that involves an expansion."""

    last = None # subclasses should always define a first class attribute

    def __init__(self, current, config, first):
        super(ExpansionToken, self).__init__(current)
        self.config = config
        # Only record a local copy of first/last if it's ambiguous.
        if self.first is None or len(self.first) != 1:
            self.first = first
            self.last = ENDING_CHAR_MAP.get(first)

    def scan(self, scanner):
        pass

    def run(self, interpreter, locals):
        pass


class CommentToken(ExpansionToken):

    """The abstract base class for the comment tokens."""

    pass


class LineCommentToken(CommentToken):

    """A line comment markup: ``@# ... NL``"""

    first = OCTOTHORPE_CHAR

    def scan(self, scanner):
        loc = scanner.find(NEWLINE_CHAR)
        if loc >= 0:
            self.comment = scanner.chop(loc, 1)
        else:
            raise TransientParseError("comment expects newline")

    def string(self):
        return '%s%s%s\n' % (self.config.prefix, self.first, self.comment)

    def run(self, interpreter, locals):
        interpreter.invoke('preLineComment', comment=self.comment)


class InlineCommentToken(CommentToken):

    first = ASTERISK_CHAR

    """An inline comment markup: ``@* ... *``"""

    def scan(self, scanner):
        # Find the run of starting characters to match.
        self.count = 1
        start = scanner.last(self.first)
        self.count += start
        scanner.advance(start)
        # Then match them with the same number of closing characters.
        loc = scanner.find(self.first * self.count, self.count)
        if loc >= 0:
            self.comment = scanner.chop(loc, self.count)
        else:
            raise TransientParseError("inline comment expects asterisk")

    def string(self):
        return '%s%s%s%s' % (
            self.config.prefix,
            self.first * self.count,
            self.comment,
            self.first * self.count)

    def run(self, interpreter, locals):
        interpreter.invoke('preInlineComment', comment=self.comment)


class LiteralToken(ExpansionToken):

    """The abstract base class of the literal tokens.  If used as a
    concrete token class, it will expand to the first character."""

    def string(self):
        return '%s%s' % (self.config.prefix, self.first)

    def run(self, interpreter, locals):
        interpreter.write(self.first)


class WhitespaceToken(LiteralToken):

    """A whitespace markup: ``@ WS``"""

    first = '<whitespace>'

    def string(self):
        return '%s%s' % (self.config.prefix, self.first)

    def run(self, interpreter, locals):
        interpreter.invoke('preWhitespace', whitespace=self.first)


class PrefixToken(LiteralToken):

    """A prefix markup: ``@@``"""

    first = None # prefix

    def string(self):
        return self.config.prefix * 2

    def run(self, interpreter, locals):
        if interpreter.invoke('prePrefix'):
            return
        interpreter.write(self.config.prefix)


class StringToken(LiteralToken):

    """A string token markup: ``@'...'``, ``@'''...'''``, ``@"..."``,
    ``@\"\"\"...\"\"\"``"""

    first = QUOTE_CHARS

    def scan(self, scanner):
        scanner.retreat()
        assert scanner[0] == self.first, (scanner[0], self.first)
        i = scanner.quote()
        self.literal = scanner.chop(i)

    def string(self):
        return '%s%s' % (self.config.prefix, self.literal)

    def run(self, interpreter, locals):
        if interpreter.invoke('preString', string=self.literal):
            return
        interpreter.literal(self.literal, locals)
        interpreter.invoke('postString')


class BackquoteToken(LiteralToken):

    """A backquote markup: ``@`...```"""

    first = BACKQUOTE_CHAR

    def scan(self, scanner):
        # Find the run of starting characters to match.
        self.count = 1
        start = scanner.last(self.first)
        self.count += start
        scanner.advance(start)
        # Then match them with the same number of closing characters.
        loc = scanner.find(self.first * self.count)
        if loc >= 0:
            self.literal = scanner.chop(loc, self.count)
        else:
            raise TransientParseError("backquote markup expects %d backquotes" % self.count)

    def string(self):
        return '%s%s%s%s' % (
            self.config.prefix,
            self.first * self.count,
            self.literal,
            self.first * self.count)

    def run(self, interpreter, locals):
        if interpreter.invoke('preBackquote', literal=self.literal):
            return
        interpreter.write(self.literal)
        interpreter.invoke('postBackquote', result=self.literal)


class ExecutionToken(ExpansionToken):

    """The abstract base class for execution tokens (expressions,
    statements, controls, etc.)"""

    pass


class ExpressionToken(ExecutionToken):

    """An expression markup: ``@(...)``"""

    first = OPEN_PARENTHESIS_CHAR
    last = ENDING_CHAR_MAP[first]

    def scan(self, scanner):
        start = 0
        end = scanner.complex(self.first, self.last)
        try:
            except_ = scanner.next('$', start, end, True)
        except ParseError:
            except_ = end
        # Build up a list of relevant indices (separating start/if/then/else
        # clauses)
        indices = [start - 1] # start, if, then, [if, then]..., [else]
        while True:
            try:
                first = scanner.next('?', start, except_, True)
                indices.append(first)
                try:
                    last = scanner.next('!', first, except_, True)
                    indices.append(last)
                except ParseError:
                    last = except_
                    break
            except ParseError:
                first = last = except_
                break
            start = last + 1
        indices.append(except_)
        code = scanner.chop(end, 1)
        # Now build up the ifThenCodes pair chain.
        self.ifThenCodes = []
        prev = None
        pair = None
        for index in indices:
            if prev is not None:
                # pair can either be None or a 2-list, possibly with None as
                # the second element.
                if pair is None:
                    pair = [code[prev + 1:index], None]
                else:
                    pair[1] = code[prev + 1:index]
                    self.ifThenCodes.append(pair)
                    pair = None
            prev = index
        # If there's a half-constructed pair not yet added to the chain, add it
        # now.
        if pair is not None:
            self.ifThenCodes.append(pair)
        self.exceptCode = code[except_ + 1:end]

    def string(self):
        fragments = []
        sep = None
        for ifCode, thenCode in self.ifThenCodes:
            if sep:
                fragments.append(sep)
            fragments.append(ifCode)
            if thenCode is not None:
                fragments.append('?')
                fragments.append(thenCode)
            sep = '!'
        if self.exceptCode:
            fragments.append('$' + self.exceptCode)
        return '%s%s%s%s' % (
            self.config.prefix, self.first,
            ''.join(fragments), self.last)

    def run(self, interpreter, locals):
        # ifThenCodes is a list of 2-lists.  A list of one sublist whose second
        # subelement is None is a simple expression to evaluate; no
        # if-then-else logic.  A list of more than one sublist is a chained
        # if-then-if-then-...-else clause with each sublist containing an if
        # and a then subelement.  If the second subelement is None, then the
        # first element is not an if but an else.
        if interpreter.invoke('preExpression', pairs=self.ifThenCodes,
                              except_=self.exceptCode, locals=locals):
            return
        result = None
        try:
            for ifCode, thenCode in self.ifThenCodes:
                # An if or an else clause; evaluate it.
                result = interpreter.evaluate(ifCode, locals)
                if thenCode is None:
                    # If there's no then clause, then this is an isolated if or
                    # a final else, so we're done.
                    break
                else:
                    if result:
                        # With a then clause with a true if clause, evaluate
                        # it.
                        result = interpreter.evaluate(thenCode, locals)
                        # If it's true, we're done.
                        if result:
                            break
                    else:
                        # Otherwise, go again.  If there no remaining pairs,
                        # return None (no expansion).
                        result = None
        except self.config.fallThroughErrors:
            # Don't catch these errors; let them fall through.
            raise
        except:
            if self.exceptCode:
                result = interpreter.evaluate(self.exceptCode, locals)
            else:
                raise
        interpreter.serialize(result)
        interpreter.invoke('postExpression', result=result)


class SimpleExpressionToken(ExecutionToken):

    """A simple expression markup: ``@x``, ``@x.y``, ``@x(y)``, ``@x[y]``,
    ``@f{...}``"""

    first = '<identifier>'

    def scan(self, scanner):
        i = scanner.simple()
        self.code = self.first + scanner.chop(i)
        # Now scan ahead for functional expressions.
        self.subtokens = []
        scanner.acquire()
        try:
            while True:
                if not scanner:
                    raise TransientParseError("need more context for end of simple expression")
                if scanner[0] != '{':
                    break
                scanner.chop(1)
                self.subtokens.append([])
                level = 0
                while True:
                    peek = scanner.read()
                    if peek == '{':
                        level += 1
                        scanner.chop(1)
                        current = self.config.renderContext(scanner.context)
                        scanner.currents.replace(current)
                        self.subtokens[-1].append(TextToken(current, '{'))
                    elif peek == '}':
                        level -= 1
                        scanner.chop(1)
                        if level < 0:
                            break
                        current = self.config.renderContext(scanner.context)
                        scanner.currents.replace(current)
                        self.subtokens[-1].append(TextToken(current, '}'))
                    token = scanner.one('{}')
                    self.subtokens[-1].append(token)
        finally:
            scanner.release()

    def string(self):
        results = ['%s%s' % (self.config.prefix, self.code)]
        for tokens in self.subtokens:
            results.append('{%s}' % ''.join(map(str, tokens)))
        return ''.join(results)

    def run(self, interpreter, locals):
        if interpreter.invoke('preSimple', code=self.code,
                              subtokens=self.subtokens, locals=locals):
            return
        result = None
        if self.subtokens:
            result = interpreter.functional(self.code, self.subtokens, locals)
        else:
            result = interpreter.evaluate(self.code, locals)
        interpreter.serialize(result)
        interpreter.invoke('postSimple', result=result)


class InPlaceToken(ExecutionToken):

    """An in-place markup: ``@$...$...$``"""

    first = DOLLAR_CHAR

    def scan(self, scanner):
        i = scanner.next(self.first)
        j = scanner.next(self.first, i + 1)
        self.code = scanner.chop(i, j - i + 1)

    def string(self):
        return '%s%s%s%s%s' % (
            self.config.prefix, self.first, self.code, self.first, self.first)

    def run(self, interpreter, locals):
        if interpreter.invoke('preInPlace', code=self.code, locals=locals):
            return
        result = None
        interpreter.write("%s%s%s%s" % (
            self.config.prefix, self.first,
            self.code, self.first))
        try:
            result = interpreter.evaluate(self.code, locals)
            interpreter.serialize(result)
        finally:
            interpreter.write(self.first)
        interpreter.invoke('postInPlace', result=result)


class StatementToken(ExecutionToken):

    """A statement markup: ``@{...}``"""

    first = OPEN_BRACE_CHAR
    last = ENDING_CHAR_MAP[first]

    def scan(self, scanner):
        i = scanner.complex(self.first, self.last)
        self.code = scanner.chop(i, 1)

    def string(self):
        return '%s%s%s%s' % (
            self.config.prefix, self.first, self.code, self.last)

    def run(self, interpreter, locals):
        if interpreter.invoke('preStatement', code=self.code, locals=locals):
            return
        interpreter.execute(self.code, locals)
        interpreter.invoke('postStatement')


class ControlToken(ExecutionToken):

    """A control markup: ``@[...]``"""

    first = OPEN_BRACKET_CHAR
    last = ENDING_CHAR_MAP[first]

    class Chain(Root):

        """A chain of tokens with a starting token and the rest
        that follow."""

        def __init__(self, head, tail):
            self.head = head
            self.tail = tail

        def __str__(self):
            return '(%s, %s)' % (self.head, self.tail)

        def getType(self):
            return self.head.type

        def hasType(self, name):
            return self.head.type == name

    PRIMARY = ['if', 'for', 'while', 'dowhile', 'try', 'with', 'defined', 'def']
    SECONDARY = ['elif', 'else', 'except', 'finally']
    TERTIARY = ['continue', 'break']
    GREEDY = [
        'if', 'elif', 'for', 'while', 'dowhile', 'with', 'defined', 'def', 'end'
    ]
    END = ['end']

    ALLOWED = {
        'if': ['elif', 'else'],
        'for': ['else'],
        'while': ['else'],
        'dowhile': ['else'],
        'try': ['except', 'else', 'finally'],
        'with': [],
        'defined': ['else'],
        'def': None,
        'continue': None,
        'break': None,
    }

    IN_RE = re.compile(r"\bin\b")
    AS_RE = re.compile(r"\bas\b")

    runPrefix = 'run_'

    def scan(self, scanner):
        scanner.acquire()
        try:
            i = scanner.complex(self.first, self.last)
            self.contents = scanner.chop(i, 1)
            fields = self.contents.strip().split(None, 1)
            if len(fields) > 1:
                self.type, self.rest = fields
            else:
                self.type = fields[0]
                self.rest = None
            self.subtokens = []
            if self.type in self.GREEDY and self.rest is None:
                raise ParseError("control '%s' needs arguments" % self.type)
            if self.type in self.PRIMARY:
                self.subscan(scanner, self.type)
                self.kind = 'primary'
            elif self.type in self.SECONDARY:
                self.kind = 'secondary'
            elif self.type in self.TERTIARY:
                self.kind = 'tertiary'
            elif self.type in self.END:
                self.kind = 'end'
            else:
                raise ParseError("unknown control markup: '%s'" % self.type)
        finally:
            scanner.release()

    def subscan(self, scanner, primary):
        """Do a subscan for contained tokens."""
        while True:
            token = scanner.one()
            if token is None:
                raise TransientParseError("control '%s' needs more tokens" % primary)
            if isinstance(token, ControlToken) and token.type in self.END:
                if token.rest != primary:
                    raise ParseError("control must end with 'end %s'" % primary)
                break
            self.subtokens.append(token)

    def build(self, allowed):
        """Process the list of subtokens and divide it up into a list
        of chains, returning that list.  Allowed specifies a list of
        the only secondary markup types which are allowed."""
        result = []
        current = []
        result.append(self.Chain(self, current))
        for subtoken in self.subtokens:
            if (isinstance(subtoken, ControlToken) and 
                subtoken.kind == 'secondary'):
                if subtoken.type not in allowed:
                    raise ParseError("control unexpected secondary: '%s'" % subtoken.type)
                current = []
                result.append(self.Chain(subtoken, current))
            else:
                current.append(subtoken)
        return result

    def subrun(self, tokens, interpreter, locals):
        """Execute a list of tokens."""
        interpreter.runSeveral(tokens, locals)

    def substring(self):
        return ''.join([toString(x) for x in self.subtokens])

    def string(self):
        if self.kind == 'primary':
            return ('%s[%s]%s%s[end %s]' %
                    (self.config.prefix, self.contents, self.substring(),
                     self.config.prefix, self.type))
        else:
            return '%s[%s]' % (self.config.prefix, self.contents)

    def run(self, interpreter, locals):
        if interpreter.invoke('preControl', type=self.type,
                              rest=self.rest, locals=locals):
            return
        try:
            allowed = self.ALLOWED[self.type]
        except KeyError:
            raise ParseError("control '%s' cannot be at this level" % self.type)
        if allowed is not None:
            chains = self.build(allowed)
        else:
            chains = None
        try:
            method = getattr(self, self.runPrefix + self.type)
        except AttributeError:
            raise ConsistencyError("unknown handler for control type '%s'" % self.type)
        method(chains, interpreter, locals)
        interpreter.invoke('postControl')

    # Type handlers.

    def run_if(self, chains, interpreter, locals):
        # @[if E]...@[end if]
        # @[if E]...@[else]...@[end if]
        # @[if E]...@[elif E2]...@[end if]
        # @[if E]...@[elif E2]...@[else]...@[end if]
        # @[if E]...@[elif E2]... ... @[else]...@[end if]
        if chains[-1].hasType('else'):
            elseChain = chains.pop()
        else:
            elseChain = None
        first = True
        for chain in chains:
            if first:
                if not chain.hasType('if'):
                    raise ParseError("control 'if' expected: '%s'" % chain.head.type)
                first = False
            else:
                if not chain.hasType('elif'):
                    raise ParseError("control 'elif' expected: '%s'" % chain.head.type)
            if interpreter.evaluate(chain.head.rest, locals):
                self.subrun(chain.tail, interpreter, locals)
                break
        else:
            if elseChain:
                self.subrun(elseChain.tail, interpreter, locals)

    def run_for(self, chains, interpreter, locals):
        # @[for N in E]...@[end for]
        # @[for N in E]...@[else]...@[end for]
        sides = self.IN_RE.split(self.rest, 1)
        if len(sides) != 2:
            raise ParseError("control 'for' expected 'for x in ...'")
        iterator, iterableCode = sides
        forChain = chains[0]
        assert forChain.hasType('for')
        elseChain = None
        if chains[-1].hasType('else'):
            elseChain = chains.pop()
        if len(chains) != 1:
            raise ParseError("control 'for' expects at most one 'else'")
        iterable = interpreter.evaluate(iterableCode, locals)
        for element in iterable:
            try:
                interpreter.assign(iterator, element, locals)
                self.subrun(forChain.tail, interpreter, locals)
            except ContinueFlow:
                continue
            except BreakFlow:
                break
        else:
            if elseChain:
                self.subrun(elseChain.tail, interpreter, locals)

    def run_while(self, chains, interpreter, locals):
        # @[while E]...@[end while]
        # @[while E]...@[else]...@[end while]
        testCode = self.rest
        whileChain = chains[0]
        assert whileChain.hasType('while')
        elseChain = None
        if chains[-1].hasType('else'):
            elseChain = chains.pop()
        if len(chains) != 1:
            raise ParseError("control 'while' expects at most one 'else'")
        exitedNormally = False
        while True:
            try:
                if not interpreter.evaluate(testCode, locals):
                    exitedNormally = True
                    break
                self.subrun(whileChain.tail, interpreter, locals)
            except ContinueFlow:
                continue
            except BreakFlow:
                break
        if exitedNormally and elseChain:
            self.subrun(elseChain.tail, interpreter, locals)

    def run_dowhile(self, chains, interpreter, locals):
        # @[dowhile E]...@[end dowhile]
        # @[dowhile E]...@[else]...@[end dowhile]
        testCode = self.rest
        doWhileChain = chains[0]
        assert doWhileChain.hasType('dowhile')
        elseChain = None
        if chains[-1].hasType('else'):
            elseChain = chains.pop()
        if len(chains) != 1:
            raise ParseError("control 'dowhile' expects at most one 'else'")
        exitedNormally = False
        done = False
        while True:
            try:
                self.subrun(doWhileChain.tail, interpreter, locals)
                if not interpreter.evaluate(testCode, locals):
                    exitedNormally = True
                    break
            except ContinueFlow:
                continue
            except BreakFlow:
                break
        if exitedNormally and elseChain:
            self.subrun(elseChain.tail, interpreter, locals)

    def run_try(self, chains, interpreter, locals):
        # @[try]...@[except]...@[end try]
        # @[try]...@[except C]...@[end try]
        # @[try]...@[except C as N]...@[end try]
        # @[try]...@[except C, N]...@[end try]
        # @[try]...@[except (C1, C2, ...) as N]...@[end try]
        # @[try]...@[except C1]...@[except C2]...@[end try]
        # @[try]...@[except C1]...@[except C2]... ... @[end try]
        # @[try]...@[finally]...@[end try]
        # @[try]...@[except ...]...@[finally]...@[end try]
        # @[try]...@[except ...]...@[else]...@[end try]
        # @[try]...@[except ...]...@[else]...@[finally]...@[end try]
        if len(chains) == 1:
            raise ParseError("control 'try' expects at least one 'except' or 'finally'")
        tryChain = None
        exceptChains = []
        elseChain = None
        finallyChain = None
        # Process the chains and verify them.
        for chain in chains:
            if chain.hasType('try'):
                if exceptChains or elseChain or finallyChain:
                    raise ParseError("control 'try' must be first")
                tryChain = chain
            elif chain.hasType('except'):
                if elseChain:
                    raise ParseError("control 'try' cannot have 'except' following 'else'")
                elif finallyChain:
                    raise ParseError("control 'try' cannot have 'except' following 'finally'")
                exceptChains.append(chain)
            elif chain.hasType('else'):
                if not exceptChains:
                    raise ParseError("control 'try' cannot have 'else' with no preceding 'except'")
                elif elseChain:
                    raise ParseError("control 'try' cannot have more than one 'else'")
                elif finallyChain:
                    raise ParseError("control 'try' cannot have 'else' following 'finally'")
                elseChain = chain
            elif chain.hasType('finally'):
                if finallyChain:
                    raise ParseError("control 'try' cannot have more than one 'finally'")
                finallyChain = chain
            else:
                assert False, chain
        try:
            try:
                self.subrun(tryChain.tail, interpreter, locals)
                if elseChain:
                    self.subrun(elseChain.tail, interpreter, locals)
            except Flow:
                raise
            except self.config.baseException:
                type, error, traceback = sys.exc_info()
                for chain in exceptChains:
                    exception, variable = interpreter.clause(chain.head.rest)
                    if isinstance(error, exception):
                        if variable is not None:
                            interpreter.assign(variable, error, locals)
                        self.subrun(chain.tail, interpreter, locals)
                        break
                else:
                    raise
        finally:
            if finallyChain:
                self.subrun(finallyChain.tail, interpreter, locals)

    def run_with(self, chains, interpreter, locals):
        # @[with E as N]...@[end with]
        # @[with N]...@[end with]
        # @[with E]...@[end with]
        fields = self.AS_RE.split(self.rest, 1)
        if len(fields) == 1:
            # One field means either the expression only or the
            # variable only.
            field = fields[0].strip()
            if interpreter.defined(field, locals):
                expression = None
                variable = field
            else:
                expression = field
                variable = None
        else: # len(fields) == 2
            expression, variable = fields
            variable = variable.strip()
        if expression is not None:
            manager = interpreter.evaluate(expression, locals)
            resource = manager
            if variable is not None:
                interpreter.assign(variable, resource, locals)
        else:
            manager = interpreter.lookup(variable, locals)
        if len(chains) != 1:
            raise ParseError("control 'with' must be simple")
        withChain = chains[0]
        assert withChain.hasType('with')
        # As per Python's compound statement reference documentation.
        enter = manager.__enter__
        exit = manager.__exit__
        resource = enter()
        oops = False
        try:
            try:
                self.subrun(withChain.tail, interpreter, locals)
            except:
                oops = True
                if not exit(*sys.exc_info()):
                    raise
        finally:
            if not oops:
                exit(None, None, None)

    def run_defined(self, chains, interpreter, locals):
        # @[defined N]...@[end defined]
        # @[defined N]...@[else]...@[end defined]
        testName = self.rest.strip()
        if not testName:
            raise ParseError("control 'defined' expects an argument")
        definedChain = chains[0]
        assert definedChain.hasType('defined')
        if len(chains) > 3:
            raise ParseError("control 'defined' expects at most one 'else'")
        if len(chains) == 2:
            elseChain = chains[1]
        else:
            elseChain = None
        if interpreter.defined(testName, locals):
            self.subrun(definedChain.tail, interpreter, locals)
        elif elseChain:
            self.subrun(elseChain.tail, interpreter, locals)

    def run_def(self, chains, interpreter, locals):
        # @[def F(...)]...@[end def]
        assert chains is None
        signature = self.rest
        definition = self.substring()
        code = ('def %s:\n'
                ' r"""%s"""\n'
                ' return %s.expand(r"""%s""", locals())\n' %
                (signature, definition,
                 interpreter.config.pseudomoduleName, definition))
        interpreter.execute(code, locals)

    def run_continue(self, chains, interpreter, locals):
        # @[continue]
        assert chains is None
        raise ContinueFlow("control 'continue' encountered without loop control")

    def run_break(self, chains, interpreter, locals):
        # @[break]
        assert chains is None
        raise BreakFlow("control 'break' encountered without loop control")


class CodedToken(ExpansionToken):

    """The abstract base class for a token that supports codings."""

    def recode(self, result):
        """Convert a lookup table entry into a string.  A
        result can be a string itself, an integer corresponding to a
        code point, or a 2-tuple, the first value of which is one of the
        above (the second is a description)."""
        assert result is not None
        # If it's a tuple, then use the first element; the remaining elements
        # are descriptions..
        if isinstance(result, tuple):
            result = result[0]
        # If it's an int, then it's a character code.
        if isinstance(result, int):
            result = chr(result)
        # If it's a list, then it's a sequence of some the above.  Turn them
        # all into strings and then concatenate them.
        if isinstance(result, list):
            fragments = []
            for elem in result:
                fragments.append(self.recode(elem))
            result = ''.join(fragments)
        return result


class EscapeToken(CodedToken):

    """An escape markup: ``@\\...``"""

    first = BACKSLASH_CHAR

    def scan(self, scanner):
        try:
            code = scanner.chop(1)
            result = None
            if code in '()[]{}<>\\\'\"?': # literals
                result = code
            elif code == '0': # NUL, null
                result = 0x00
            elif code == 'a': # BEL, bell
                result = 0x07
            elif code == 'b': # BS, backspace
                result = 0x08
            elif code == 'B': # freeform binary code
                binaryCode = scanner.enclosure()
                result = int(binaryCode, 2)
            elif code == 'd': # three-digit decimal code
                decimalCode = scanner.chop(3)
                result = int(decimalCode, 10)
            elif code == 'D': # freeform decimal code
                decimalCode = scanner.enclosure()
                result = int(decimalCode, 10)
            elif code == 'e': # ESC, escape
                result = 0x1b
            elif code == 'f': # FF, form feed
                result = 0x0c
            elif code == 'h': # DEL, delete
                result = 0x7f
            elif code == 'k': # ACK, acknowledge
                result = 0x06
            elif code == 'K': # NAK, negative acknowledge
                result = 0x15
            elif code == 'n': # LF, linefeed; newline
                result = 0x0a
            elif code == 'N': # Unicode character name
                if unicodedata is None:
                    raise ConfigurationError("unicodedata module not available; cannot use @\\N{...} markup")
                name = scanner.enclosure()
                try:
                    if self.config.replaceNewlines:
                        name = name.replace('\n', ' ')
                    result = unicodedata.lookup(name)
                except AttributeError:
                    raise ConfigurationError("unicodedata.lookup function not available; cannot use @\\N{...} markup")
                except KeyError:
                    raise ParseError("unknown Unicode character name: %s" % name)
            elif code == 'o': # three-digit octal code
                octalCode = scanner.chop(3)
                result = int(octalCode, 8)
            elif code == 'O': # freeform octal code
                octalCode = scanner.enclosure()
                result = int(octalCode, 8)
            elif code == 'q': # four-digit quaternary code
                quaternaryCode = scanner.chop(4)
                result = int(quaternaryCode, 4)
            elif code == 'Q': # freeform quaternary code
                quaternaryCode = scanner.enclosure()
                result = int(quaternaryCode, 4)
            elif code == 'r': # CR, carriage return
                result = 0x0d
            elif code == 's' or code in WHITESPACE_CHARS: # SP, space
                result = ' '
            elif code == 'S': # NBSP, no-break space
                result = 0xa0
            elif code == 't': # HT, horizontal tab
                result = 0x09
            elif code == 'u': # 16-bit (four-digit) hexadecimal Unicode
                hexCode = scanner.chop(4)
                result = int(hexCode, 16)
            elif code == 'U': # 32-bit (eight-digit) hexadecimal Unicode
                hexCode = scanner.chop(8)
                result = int(hexCode, 16)
            elif code == 'v': # VT, vertical tab
                result = 0x0b
            elif code == 'V': # variation selector
                name = scanner.enclosure()
                try:
                    selector = int(name)
                except ValueError:
                    raise ParseError("variation selector must be int: %s" % name)
                if selector < 1 or selector > 256:
                    raise ParseError("variation selector must be between 1 and 256 inclusive: %d" % selector)
                if selector <= 16:
                    result = 0xfe00 + selector - 1
                else:
                    result = 0xe0100 + (selector - 17)
            elif code == 'w': # variation selector 15; text display
                result = 0xfe0e
            elif code == 'W': # variation selector 16; emoji display
                result = 0xfe0f
            elif code == 'x': # 8-bit (two-digit) hexadecimal code
                hexCode = scanner.chop(2)
                result = int(hexCode, 16)
            elif code == 'X': # freeform hexadecimal code
                hexCode = scanner.enclosure()
                result = int(hexCode, 16)
            elif code == 'y': # SUB, substitution
                result = 0x1a
            elif code == 'Y': # RC, replacement character
                result = 0xfffd
            elif code == 'z': # EOT, end of transmission
                result = 0x04
            elif code == 'Z': # ZWNBSP/BOM, zero-width no-break space/byte order mark
                result = 0xfeff
            elif code == ',': # thin space
                result = 0x2009
            elif code == '^': # control character
                controlCode = scanner.chop(1).upper()
                if controlCode == '{':
                    if self.config.controls is None:
                        raise ConfigurationError("controls not configured")
                    name = scanner.grab('}')
                    try:
                        result = self.config.controls[name.upper()]
                    except KeyError:
                        raise ParseError("unknown control character name: %s" % name)
                elif controlCode >= '@' and controlCode <= '`':
                    result = ord(controlCode) - ord('@')
                elif controlCode == '?':
                    result = 0x7f
                else:
                    raise ParseError("invalid escape control code")
            else:
                raise ParseError("unrecognized escape code: %s" % code)
            self.code = self.recode(result)
        except ValueError:
            raise ParseError("invalid numeric escape code")

    def string(self):
        """Return a general hexadecimal escape sequence rather than
        the exact one that was input."""
        return self.config.escaped(ord(self.code),
                                   self.config.prefix + self.first)

    def run(self, interpreter, locals):
        if interpreter.invoke('preEscape', code=self.code):
            return
        interpreter.write(self.code)
        interpreter.invoke('postEscape')


class DiacriticToken(CodedToken):

    """A diacritic markup: ``@^...``"""

    first = CARET_CHAR

    def scan(self, scanner):
        if self.config.diacritics is None:
            raise ConfigurationError("diacritics not configured")
        character = scanner.chop(1)
        diacritics = scanner.chop(1)
        if diacritics == '{':
            diacritics = scanner.grab('}')
        combiners = []
        try:
            for diacritic in diacritics:
                combiner = self.config.diacritics[diacritic]
                combiner = self.recode(combiner)
                combiners.append(combiner)
        except KeyError:
            raise ParseError("unknown diacritical mark: %s" % diacritic)
        result = character + ''.join(combiners)
        try:
            if self.config.normalizationForm:
                result = unicodedata.normalize(
                    self.config.normalizationForm, result)
        except AttributeError:
            raise ConfigurationError("unicodedata.normalize function not available; cannot use normalization form (must be blank or None)")
        except ValueError:
            pass
        self.character = character
        self.diacritics = diacritics
        self.code = result

    def string(self):
        if len(self.diacritics) > 1:
            return '%s%s%s{%s}' % (
                self.config.prefix, self.first, self.character, self.diacritics)
        else:
            return '%s%s%s%s' % (
                self.config.prefix, self.first, self.character, self.diacritics)

    def run(self, interpreter, locals):
        if interpreter.invoke('preDiacritic', code=self.code):
            return
        interpreter.write(self.code)
        interpreter.invoke('postDiacritic')


class IconToken(CodedToken):

    """An icon markup: ``@|...``"""

    first = STROKE_CHAR

    def scan(self, scanner):
        self.config.validateIcons()
        key = ''
        while True:
            key += scanner.chop(1)
            try:
                result = self.config.icons[key]
            except KeyError:
                raise ParseError("unknown icon sequence: %s" % key)
            if result is None:
                continue
            else:
                break
        self.key = key
        self.code = self.recode(result)

    def string(self):
        return '%s%s%s' % (self.config.prefix, self.first, self.key)

    def run(self, interpreter, locals):
        if interpreter.invoke('preIcon', code=self.code):
            return
        interpreter.write(self.code)
        interpreter.invoke('postIcon')


class EmojiToken(CodedToken):

    """An emoji markup: ``@:...:``"""

    first = COLON_CHAR

    def scan(self, scanner):
        i = scanner.next(self.first)
        self.name = scanner.chop(i, 1)
        if not self.name:
            raise ParseError("emoji cannot be blank")

    def string(self):
        return '%s%s%s%s' % (
            self.config.prefix, self.first, self.name, self.first)

    def run(self, interpreter, locals):
        if interpreter.invoke('preEmoji', name=self.name):
            return
        if (self.config.emojis is not None and
            self.name in self.config.emojis):
            code = self.config.emojis[self.name]
        else:
            code = self.config.substituteEmoji(self.name)
            if code is None:
                if self.config.emojiNotFoundIsError:
                    raise UnknownEmojiError("emoji not found: %s" % self.name)
                else:
                    code = '%s%s%s' % (self.first, self.name, self.first)
        code = self.recode(code)
        interpreter.write(code)
        interpreter.invoke('postEmoji')


class SignificatorToken(ExpansionToken):

    """A significator markup: ``@%... ... NL``, ``@%!... ... NL``,
    ``@%%... ... %% NL``, ``@%%!... ... %% NL``"""

    first = PERCENT_CHAR

    def ending(self, multiline):
        if multiline:
            return (self.first * 2) + NEWLINE_CHAR
        else:
            return NEWLINE_CHAR

    def scan(self, scanner):
        self.multiline = self.stringized = False
        peek = scanner.read()
        if peek == self.first:
            self.multiline = True
            scanner.advance(1)
            peek = scanner.read()
        if peek == '!':
            self.stringized = True
            scanner.advance(1)
        loc = scanner.find(self.ending(self.multiline))
        if loc >= 0:
            contents = scanner.chop(loc, len(self.ending(self.multiline)))
            if not contents:
                raise ParseError("significator must have nonblank key")
            contents = contents.strip()
            # Work around a subtle CPython-Jython difference by stripping the
            # string before splitting it: 'a '.split(None, 1) has two elements
            # in Jython 2.1).
            fields = contents.strip().split(None, 1)
            self.key = fields[0]
            if len(fields) > 1:
                self.value = fields[1].strip()
            else:
                self.value = ''
            if not self.value and not self.stringized:
                self.value = self.config.emptySignificator
        else:
            if self.multiline:
                raise TransientParseError("significator expects %s and then newline" % (self.first * 2))
            else:
                raise TransientParseError("significator expects newline")

    def string(self):
        if self.value is None:
            return '%s%s%s%s\n' % (
                self.config.prefix, self.first,
                ['', '!'][self.stringized],
                self.key)
        else:
            if self.multiline:
                return '%s%s%s%s %s%s\n' % (
                    self.config.prefix, self.first * 2,
                    ['', '!'][self.stringized],
                    self.key, self.value,
                    self.first * 2)
            else:
                return '%s%s%s%s %s\n' % (
                    self.config.prefix, self.first,
                    ['', '!'][self.stringized],
                    self.key, self.value)

    def run(self, interpreter, locals):
        if interpreter.invoke('preSignificator', key=self.key,
                              value=self.value, stringized=self.stringized):
            return
        value = self.value
        if value is not None and not self.stringized:
            value = interpreter.evaluate(value, locals, replace=False)
        interpreter.significate(self.key, value, locals)
        interpreter.invoke('postSignificator')


class ContextToken(ExpansionToken):

    """A base class for the context tokens."""

    pass


class ContextNameToken(ContextToken):

    """A context name change markup: ``@?...``"""

    first = QUESTION_CHAR

    def scan(self, scanner):
        loc = scanner.find(NEWLINE_CHAR)
        if loc >= 0:
            self.name = scanner.chop(loc, 1).strip()
        else:
            raise TransientParseError("context name expects newline")

    def string(self):
        return '%s%s%s\n' % (self.config.prefix, self.first, self.name)

    def run(self, interpreter, locals):
        if interpreter.invoke('preContextName', name=self.name):
            return
        context = interpreter.getContext()
        context.name = self.name
        interpreter.invoke('postContextName', context=context)


class ContextLineToken(ContextToken):

    """A context line change markup: ``@!...``"""

    first = EXCLAMATION_CHAR

    def scan(self, scanner):
        loc = scanner.find(NEWLINE_CHAR)
        if loc >= 0:
            try:
                self.line = int(scanner.chop(loc, 1))
            except ValueError:
                raise ParseError("context line requires integer")
        else:
            raise TransientParseError("context line expects newline")

    def string(self):
        return '%s%s%d\n' % (self.config.prefix, self.first, self.line)

    def run(self, interpreter, locals):
        if interpreter.invoke('preContextLine', line=self.line):
            return
        context = interpreter.getContext()
        context.line = self.line
        interpreter.invoke('postContextLine', context=context)


class CustomToken(ExpansionToken):

    """A custom markup: ``@<...>``"""

    first = OPEN_ANGLE_CHAR
    last = ENDING_CHAR_MAP[first]

    def scan(self, scanner):
        # Find the run of starting characters to match.
        self.count = 1
        start = scanner.last(self.first)
        self.count += start
        scanner.advance(start)
        # Then match them with the same number of closing characters.
        loc = scanner.find(self.last * self.count)
        if loc >= 0:
            self.contents = scanner.chop(loc, self.count)
        else:
            raise TransientParseError("custom markup expects %d close angle brackets" % self.count)

    def string(self):
        return '%s%s%s%s' % (
            self.config.prefix,
            self.first * self.count,
            self.contents,
            self.last * self.count)

    def run(self, interpreter, locals):
        if interpreter.invoke('preCustom', contents=self.contents):
            return
        result = interpreter.invokeCallback(self.contents)
        interpreter.serialize(result)
        interpreter.invoke('postCustom', result=result)


Configuration.tokens = [
    LineCommentToken,
    InlineCommentToken,
    WhitespaceToken,
    PrefixToken,
    StringToken,
    BackquoteToken,
    ExpressionToken,
    SimpleExpressionToken,
    InPlaceToken,
    StatementToken,
    ControlToken,
    EscapeToken,
    DiacriticToken,
    IconToken,
    EmojiToken,
    SignificatorToken,
    ContextNameToken,
    ContextLineToken,
    CustomToken,
]

#
# Factory
#

class Factory(Root):

    """Turn a first character into a token class.  Token classes
    have a first attribute which is either None to indicate
    whatever the current prefix is; a string in angle brackets to
    indicate a special test; or a character or characters.  Token
    classes are then retrieved by lookup table, or special test.
    Initialize this meta-factory with a list of factory classes
    and it will automatically setup the lookup tables based on
    their first attributes."""

    def __init__(self, factories):
        self.byChar = {}
        self.identifier = None
        self.whitespace = None
        for factory in factories:
            first = factory.first
            if first is None:
                # A prefix.
                assert None not in self.byChar
                self.byChar[None] = factory
            elif first.startswith('<') and first.endswith('>'):
                # A special case.
                if first == '<identifier>':
                    assert self.identifier is None
                    self.identifier = factory
                elif first == '<whitespace>':
                    assert self.whitespace is None
                    self.whitespace = factory
                else:
                    raise ConsistencyError("unknown special token case: %s" % first)
            else:
                # A character or characters.
                for char in first:
                    assert char not in self.byChar
                    self.byChar[char] = factory
        assert self.identifier is not None
        assert self.whitespace is not None

    def __contains__(self, first):
        return first in self.byChar

    def __getitem__(self, first):
        return self.byChar[first]

    def __call__(self, first):
        if first in self.byChar:
            return self.byChar[first]
        else:
            if first.isspace():
                return self.whitespace
            elif isIdentifier(first):
                return self.identifier
        return None

    def adjust(self, config):
        """Adjust this factory to swap the markup for a non-default
        prefix, if necessary."""
        if not config.hasDefaultPrefix() and config.prefix in self:
            oldFactory = self[config.prefix]
            self.byChar[config.defaultPrefix] = oldFactory
            oldFactory._first = oldFactory.first
            oldFactory.first = None # config.defaultPrefix

#
# Scanner
#

class Scanner(Root):

    """A scanner holds a buffer for lookahead parsing and has the
    ability to scan for special symbols and indicators in that
    buffer."""

    def __init__(self, config, context, currents, data=''):
        self.config = config
        self.context = context
        self.currents = currents
        self.head = 0
        self.pointer = 0
        self.buffer = data
        self.lock = 0
        self.factory = config.getFactory()

    def __bool__(self):
        return self.head + self.pointer < len(self.buffer) # 3.x
    def __nonzero__(self):
        return self.head + self.pointer < len(self.buffer) # 2.x

    def __len__(self): return len(self.buffer) - self.pointer - self.head

    if major >= 3:
        def __getitem__(self, index):
            if isinstance(index, slice):
                assert index.step is None or index.step == 1
                return self.__getslice__(index.start, index.stop)
            else:
                return self.buffer[self.head + self.pointer + index]
    else:
        def __getitem__(self, index):
            return self.buffer[self.head + self.pointer + index]

    def __getslice__(self, start, stop):
        if start is None:
            start = 0
        if stop is None:
            stop = len(self)
        if stop > len(self):
            stop = len(self)
        return self.buffer[self.head + self.pointer + start:
                           self.head + self.pointer + stop]

    # Meta.

    def advance(self, count=1):
        """Advance the pointer count characters."""
        self.pointer += count

    def retreat(self, count=1):
        self.pointer -= count
        if self.pointer < 0:
            raise ParseError("can't retreat back over synced out chars")

    def set(self, data):
        """Start the scanner digesting a new batch of data; start the pointer
        over from scratch."""
        self.head = 0
        self.pointer = 0
        self.buffer = data

    def feed(self, data):
        """Feed some more data to the scanner."""
        self.rectify()
        if self.buffer:
            self.buffer += data
        else:
            self.buffer = data

    def acquire(self):
        """Lock the scanner so it doesn't destroy data on sync."""
        self.lock += 1

    def release(self):
        """Unlock the scanner."""
        self.lock -= 1

    def track(self):
        """Accumulate the moved pointer into the context."""
        if self.pointer > 0:
            self.context.track(self.buffer,
                               self.head, self.head + self.pointer)

    def accumulate(self):
        """Update the accumulated context into the actual context."""
        self.context.accumulate()

    def rectify(self):
        """Reset the read head and trim down the buffer."""
        if self.head + self.pointer > 0:
            self.buffer = self.buffer[self.head + self.pointer:]
        self.head = 0
        self.pointer = 0

    def sync(self):
        """Sync up the buffer with the read head."""
        if self.lock == 0 and self.pointer > 0:
            self.track()
            self.head += self.pointer
            self.pointer = 0

    def unsync(self):
        """Undo changes; reset the read head."""
        if self.lock == 0:
            self.pointer = 0

    def rest(self):
        """Get the remainder of the buffer."""
        return self[:]

    # Active.

    def chop(self, count=None, slop=0):
        """Chop the first count + slop characters off the front, and
        return the first count, advancing the pointer past them.  If
        count is not specified, then return everything."""
        if count is None:
            assert slop == 0
            count = len(self)
        if count > len(self):
            raise TransientParseError("not enough data to read")
        result = self[:count]
        self.advance(count + slop)
        return result

    def enclosure(self, begin='{', end='}'):
        """Consume and return the next enclosure (text wrapped
        in the given delimiters)."""
        if self.chop(len(begin)) == begin:
            name = self.grab(end)
            return name
        else:
            raise ParseError("enclosure must start with %s" % begin)

    def read(self, start=0, count=1):
        """Read count chars starting from start; raise a transient
        error if there aren't enough characters remaining."""
        if len(self) < start + count:
            raise TransientParseError("need more data to read")
        else:
            return self[start:start + count]

    def find(self, sub, start=0, end=None):
        """Find the next occurrence of the substring, or return -1."""
        if end is None:
            end = len(self)
        return self.rest().find(sub, start, end)

    def trivial(self, sub, start=0, end=None):
        """Find the first occurrence of the substring where the
        previous character is _not_ the escape character `\\`)."""
        head = start
        while True:
            i = self.find(sub, head, end)
            if i == -1:
                raise TransientParseError("substring not found: %s" % sub)
            if i > 0 and self[i - 1] == BACKSLASH_CHAR:
                head = i + len(sub)
                continue
            return i

    def last(self, chars, start=0, end=None):
        """Find the first character that is _not_ one of the specified
        characters."""
        if end is None:
            end = len(self)
        i = start
        while i < end:
            if self[i] not in chars:
                return i
            i += 1
        else:
            raise TransientParseError("expecting other than %s" % chars)

    def grab(self, sub, start=0, end=None):
        """Find the next occurrence of the substring and chop the
        intervening characters, disposing the substring found."""
        i = self.find(sub, start, end)
        if i >= 0:
            return self.chop(i, len(sub))
        else:
            raise TransientParseError("delimiter not found: %s" % sub)

    def next(self, target, start=0, end=None, mandatory=False):
        """Scan for the next occurrence of one of the characters in
        the target string; optionally, make the scan mandatory."""
        if mandatory:
            assert end is not None
        quote = None
        if end is None:
            end = len(self)
        i = start
        while i < end:
            newQuote = self.check(i, quote)
            if newQuote:
                if newQuote == quote:
                    quote = None
                else:
                    quote = newQuote
                i += len(newQuote)
            else:
                c = self[i]
                if quote:
                    if c == '\\':
                        i += 1
                else:
                    if c in target:
                        return i
                i += 1
        else:
            if mandatory:
                raise ParseError("expecting %s, not found" % target)
            else:
                raise TransientParseError("expecting ending character")

    def check(self, start=0, archetype=None):
        """Scan for the next single or triple quote, optionally with
        the specified archetype.  Return the found quote or None."""
        quote = None
        i = start
        if len(self) - i <= 1:
            raise TransientParseError("need to scan for rest of quote")
        if self[i] in QUOTE_CHARS:
            quote = self[i]
            if self[i + 1] == quote:
                if len(self) - i <= 2:
                    raise TransientParseError("need more context to complete quote")
                if self[i + 2] == quote:
                    quote *= 3
        if quote is not None:
            if archetype is None:
                return quote
            else:
                if archetype == quote:
                    return archetype
                elif len(archetype) < len(quote) and archetype[0] == quote[0]:
                    return archetype
                else:
                    return None
        else:
            return None

    def quote(self, start=0, end=None, mandatory=False):
        """Scan for the end of the next quote."""
        assert self[start] in QUOTE_CHARS
        quote = self.check(start)
        if end is None:
            end = len(self)
        i = start + len(quote)
        while i < end:
            newQuote = self.check(i, quote)
            if newQuote:
                i += len(newQuote)
                if newQuote == quote:
                    return i
            else:
                c = self[i]
                if c == '\\':
                    i += 1
                i += 1
        else:
            if mandatory:
                raise ParseError("expecting end of string literal")
            else:
                raise TransientParseError("expecting end of string literal")

    def nested(self, enter, exit, start=0, end=None):
        """Scan from start for an ending sequence, respecting entries and exits
        only."""
        depth = 0
        if end is None:
            end = len(self)
        i = start
        while i < end:
            c = self[i]
            if c == enter:
                depth += 1
            elif c == exit:
                depth -= 1
                if depth < 0:
                    return i
            i += 1
        else:
            raise TransientParseError("expecting end of complex expression")

    def complex(self, enter, exit, comment=OCTOTHORPE_CHAR,
                start=0, end=None, skip=None):
        """Scan from start for an ending sequence, respecting quotes,
        entries and exits."""
        quote = None
        depth = 0
        if end is None:
            end = len(self)
        lastNonQuote = None
        commented = False
        i = start
        while i < end:
            if commented:
                c = self[i]
                if c == '\n':
                    commented = False
                elif c == exit:
                    return i
                i += 1
            else:
                newQuote = self.check(i, quote)
                if newQuote:
                    if newQuote == quote:
                        quote = None
                    else:
                        quote = newQuote
                    i += len(newQuote)
                else:
                    c = self[i]
                    if quote:
                        if c == '\\':
                            i += 1
                    else:
                        if skip is None or lastNonQuote != skip:
                            if c == enter:
                                depth += 1
                            elif c == exit:
                                depth -= 1
                                if depth < 0:
                                    return i
                        if c == comment and depth == 0:
                            commented = True
                    lastNonQuote = c
                    i += 1
        else:
            raise TransientParseError("expecting end of complex expression")

    def word(self, start=0, additional='._'):
        """Scan from start for a simple word."""
        length = len(self)
        i = start
        while i < length:
            if not (self[i].isalnum() or self[i] in additional):
                return i
            i += 1
        else:
            raise TransientParseError("expecting end of word")

    def phrase(self, start=0):
        """Scan from start for a phrase (e.g., 'word', 'f(a, b, c)',
        'a[i]', or combinations like 'x[i](a)'."""
        # Find the word.
        i = self.word(start)
        while i < len(self) and self[i] in PHRASE_OPENING_CHARS:
            enter = self[i]
            exit = ENDING_CHAR_MAP[enter]
            i = self.complex(enter, exit, None, i + 1) + 1
        return i

    def simple(self, start=0):
        """Scan from start for a simple expression, which consists of
        one more phrases separated by dots.  Return a tuple giving the
        end of the expression and a list of tuple pairs consisting of
        the simple expression extensions found, if any."""
        i = self.phrase(start)
        length = len(self)
        while i < length and self[i] == DOT_CHAR:
            i = self.phrase(i)
        # Make sure we don't end with a trailing dot.
        while i > 0 and self[i - 1] == DOT_CHAR:
            i -= 1
        return i

    def one(self, firebreaks=None):
        """Parse, scan, and return one token, or None if the scanner
        is empty.  If the firebreaks argument is supplied, chop up
        text tokens before a character in that string."""
        if not self:
            return None
        if not self.config.prefix:
            loc = -1
        else:
            loc = self.find(self.config.prefix)
        if loc < 0:
            # If there's no prefix in the buffer, then set the location to the
            # end so the whole thing gets processed.
            loc = len(self)
        if loc == 0:
            # If there's a prefix at the beginning of the buffer, process
            # an expansion.
            prefix = self.chop(1)
            assert prefix == self.config.prefix
            try:
                first = self.chop(1)
                if first == self.config.prefix:
                    first = None
                factory = self.factory(first)
                if factory is None:
                    raise ParseError("unknown markup sequence: %s%s" % (self.config.prefix, first))
                current = self.config.renderContext(self.context)
                self.currents.replace(current)
                token = factory(current, self.config, first)
                token.scan(self)
            except TransientParseError:
                # If a transient parse error occurs, reset the buffer pointer
                # so we can (conceivably) try again later.
                self.unsync()
                raise
        else:
            # Process everything up to loc as a text token, unless there are
            # intervening firebreaks before loc.
            if firebreaks:
                for firebreak in firebreaks:
                    i = self.find(firebreak, 0, loc)
                    if i >= 0 and i < loc:
                        loc = i
            data = self.chop(loc)
            current = self.config.renderContext(self.context)
            self.currents.replace(current)
            token = TextToken(current, data)
        self.sync()
        return token

#
# Command ...
#

class Command(Root):

    """A generic high-level processing command."""

    def __init__(self, noun):
        self.noun = noun

    def __str__(self):
        return self.noun

    def cleanup(self):
        pass

    def process(self, interpreter, n):
        """Run the command."""
        raise NotImplementedError


class DocumentCommand(Command):

    """Read and execute an EmPy document."""

    def process(self, interpreter, n):
        name = self.noun
        method = interpreter.file
        self.target = interpreter.config.open(self.noun, 'r')
        result = interpreter.protect(name, method, self.target)

    def cleanup(self):
        self.target.close()


class ImportCommand(Command):

    """Import a Python module."""

    def process(self, interpreter, n):
        name = '<import:%d>' % n
        context = interpreter.newContext(name)
        interpreter.pushContext(context)
        try:
            module = __import__(self.noun)
            interpreter.atomic(self.noun, module)
            method = interpreter.string
            target = '%s{import %s}' % (interpreter.config.prefix, self.noun)
            return name, method, (target,), {}
        finally:
            interpreter.popContext()


class DefineCommand(Command):

    """Define a Python variable."""

    def process(self, interpreter, n):
        name = '<define:%d>' % n
        context = interpreter.newContext(name)
        interpreter.pushContext(context)
        try:
            if '=' in self.noun:
                interpreter.execute(self.noun)
            else:
                interpreter.atomic(self.noun.strip(), None)
        finally:
            interpreter.popContext()


class StringCommand(Command):

    """Define a Python string variable."""

    def process(self, interpreter, n):
        method = None
        if '=' in self.noun:
            key, value = self.noun.split('=', 1)
            key = key.strip()
            value = value.strip()
        else:
            key = self.noun.strip()
            value = ''
        interpreter.atomic(key, value)

class ExecCommand(Command):

    """Execute a Python statement."""

    def process(self, interpreter, n):
        name = '<exec:%d>' % n
        context = interpreter.newContext(name)
        interpreter.pushContext(context)
        try:
            interpreter.execute(self.noun)
        finally:
            interpreter.popContext()


class FileCommand(Command):

    """Load an execute a Python file."""

    def process(self, interpreter, n):
        name = '<file:%d>' % n
        context = interpreter.newContext(name)
        interpreter.pushContext(context)
        try:
            file = interpreter.config.open(self.noun, 'r')
            try:
                data = file.read()
            finally:
                file.close()
            interpreter.execute(data)
        finally:
            interpreter.popContext()


#
# Interpreter
#

class Interpreter(Root):

    """An interpreter can process chunks of EmPy code."""

    # Compatibility.

    version = __version__
    compat = compat

    # Constants.

    ASSIGN_TOKEN_RE = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*|\(|\)|,")
    AS_RE = re.compile(r"\bas\b")

    # Statics.

    _proxy = None # the installed proxy or None

    # Construction, initialization, destruction.

    def __init__(self, **kwargs):
        """Accept keyword arguments only, so users will never have to
        worry about the ordering of arguments."""
        self.initialize(
            kwargs.get('config', None),
            kwargs.get('globals', None),
            kwargs.get('output', None),
            kwargs.get('executable', '?'),
            kwargs.get('argv', None),
            kwargs.get('filespec', None),
            kwargs.get('hooks', None),
            kwargs.get('callback', None),
            kwargs.get('handler', None),
            kwargs.get('evalFunc', eval),
            kwargs.get('execFunc', execFunc),
            kwargs.get('input', sys.stdin),
            kwargs.get('immediately', True))

    def __del__(self):
        self.shutdown()

    def __repr__(self):
        return '<%s pseudomodule/interpreter object @ 0x%x>' % (
            self.config.pseudomoduleName, id(self))

    def __bool__(self): return self.ok # 3.x
    def __nonzero__(self): return self.ok # 2.x

    def __enter__(self):
        self.check()
        return self

    def __exit__(self, *exc):
        self.shutdown()

    def initialize(self, config=None, globals=None, output=None,
                   executable=None, argv=None, filespec=None,
                   hooks=None, callback=None, handler=None,
                   evalFunc=evalFunc, execFunc=execFunc, input=sys.stdin,
                   immediately=True):
        """Initialize the interpreter with the given arguments (all of
        which have defaults).  The number and order of arguments here
        is subject to change."""
        self.ok = None # is the interpreter initialized?
        self.error = None # last error that occurred or None
        # Set up the configuration.
        if config is None:
            config = Configuration()
        self.config = config
        self.filespec = filespec
        self.globals = globals
        # Handle the executable and arguments.
        self.executable = executable
        if argv is None:
            argv = [None]
        if argv[0] is None:
            argv[0] = config.unknownScriptName
        self.argv = argv
        # The interpreter stacks.
        self.contexts = Stack()
        self.streams = Stack()
        self.currents = Stack()
        # Initialize hooks.
        if hooks is None:
            hooks = []
        self.hooks = []
        self.hooksEnabled = None
        for hook in self.hooks:
            self.addHook(hook)
        # Initialize callback.
        self.callback = callback
        # Initialize handler.
        self.handler = handler
        # Install a proxy stdout if one hasn't been already.
        self.output = self.installProxy(output)
        # Setup the execution environment.
        self.evalFunc = evalFunc
        self.execFunc = execFunc
        self.input = input
        # Now declare that we've started up.
        self.ok = True
        self.invoke('atStartup')
        # And, finally, reset the state and ready up.
        self.reset(True, immediately)

    def reset(self, clearStacks=False, immediately=True):
        """Completely reset the interpreter state.  If clearStacks is
        true, wipe the call stacks.  If immediately is true, declare
        the interpreter ready."""
        self.ok = False
        self.error = None
        # None is a special sentinel meaning "false until added."
        self.hooksEnabled = len(self.hooks) > 0 and True or None
        # Set up a diversions dictionary.
        self.diversions = {}
        # Significators.
        self.significators = {}
        # Finalizers.
        self.finals = []
        # Now set up the globals.
        self.fixGlobals()
        self.globalsHistory = Stack()
        # Now, clear the state of all the stacks.
        if clearStacks:
            self.clear()
        self.current = None
        # Done.  Now declare that we've started up.
        self.ok = True
        if immediately:
            self.ready()

    def ready(self):
        """Declare the interpreter ready for normal operations."""
        self.invoke('atReady')

    def finalize(self):
        """Execute any remaining final routines."""
        self.push()
        self.invoke('atFinalize')
        try:
            # Pop them off one at a time so they get executed in reverse order
            # and we remove them as they're executed in case something bad
            # happens.
            while self.finals:
                final = self.finals.pop()
                if self.invoke('beforeFinalizer', finalizer=final):
                    continue
                final()
                self.invoke('afterFinalizer')
        finally:
            self.pop()

    def succeeded(self):
        """Did the interpreter succeed?  That is, is the logged
        error not an error?"""
        return self.config.isNotAnError(self.error)

    def pause(self):
        """Pause (at the end of processing)."""
        try:
            self.input.readline()
        except EOFError:
            pass

    def shutdown(self):
        """Declare this interpreting session over; close all the
        stream file objects, and if this is the last interpreter,
        uninstall the proxy.  This method is idempotent."""
        if self.ok:
            succeeded = self.succeeded()
            try:
                self.finalize()
                self.invoke('atShutdown')
                while self.streams:
                    stream = self.streams.pop()
                    if self.streams:
                        stream.close()
                    else:
                        # Don't close the bottom stream; auto-play diversions
                        # and just flush it.
                        if self.config.autoPlayDiversions and succeeded:
                            stream.undivertAll()
                        stream.flush()
                self.clear()
            finally:
                self.uninstallProxy()
            # Finally, pause if desired.
            if self.config.pauseAtEnd:
                self.pause()
            self.ok = False

    def check(self):
        """Check the verify this interpreter is still alive."""
        if not self.ok:
            raise ConsistencyError("interpreter has already been shutdown")

    # Writeable file-like methods.

    def write(self, data):
        stream = self.top()
        assert stream is not None
        stream.write(data)

    def writelines(self, lines):
        stream = self.top()
        assert stream is not None
        stream.writelines(lines)

    def flush(self):
        stream = self.top()
        assert stream is not None
        stream.flush()

    def close(self):
        self.shutdown()

    def serialize(self, thing):
        """Output the string version of an object, or a special token if
        it is None."""
        if thing is None:
            if self.config.noneSymbol is not None:
                self.write(self.config.noneSymbol)
        else:
            self.write(toString(thing))

    # Stack-related activity.

    def top(self):
        """Get the top stream."""
        return self.streams.top()

    def push(self):
        if self.config.useProxy:
            try:
                sys.stdout.push(self)
            except AttributeError:
                raise ConsistencyError("stdout proxy lost; cannot push stream")

    def pop(self):
        if self.config.useProxy:
            try:
                sys.stdout.pop(self)
            except AttributeError:
                raise ConsistencyError("stdout proxy lost; cannot pop stream")

    def clear(self):
        self.streams.purge()
        self.streams.push(Stream(self.output, self.diversions))
        context = self.newContext('<root>')
        self.contexts.purge()
        self.contexts.push(context)
        self.currents.purge()
        self.currents.push(self.config.renderContext(context))
        if self.config.useProxy:
            sys.stdout.clear(self)

    # Entry-level processing.

    def include(self, fileOrFilename, locals=None, name=None):
        """Do an include pass on a file or filename."""
        if isinstance(fileOrFilename, strType):
            # Either it's a string representing a filename ...
            filename = fileOrFilename
            if not name:
                name = filename
            file = self.config.open(filename, 'r')
        else:
            # ... or a file object.
            file = fileOrFilename
            if not name:
                name = '<%s>' % toString(file.__class__.__name__)
        if self.invoke('beforeInclude', file=file, locals=locals, name=name):
            return
        if name:
            context = self.newContext(name)
            self.pushContext(context)
        self.file(file, locals)
        if name:
            self.popContext()
        self.invoke('afterInclude')

    def expand(self, data, locals=None, name='<expand>'):
        """Do an explicit expansion on a subordinate stream in a
        new automatic context."""
        outFile = StringIO()
        stream = Stream(outFile, self.diversions)
        if self.invoke('beforeExpand', string=data, locals=locals, name=name):
            return
        self.streams.push(stream)
        try:
            if name:
                context = self.newContext(name)
                self.pushContext(context)
            try:
                self.string(data, locals)
            finally:
                if name:
                    self.popContext()
            stream.flush()
            expansion = outFile.getvalue()
            self.invoke('afterExpand', result=expansion)
            return expansion
        finally:
            self.streams.pop()

    # High-level processing.

    def go(self, inputFilename, inputMode, preprocessing, postprocessing):
        """Execute an interpreter stack at a high level.  Return any
        error which occurs or None."""
        error = None
        # Execute any preprocessing commands.
        self.process(preprocessing)
        # Ready!
        self.ready()
        # Now process the primary file.
        method = self.file
        if inputFilename is None:
            # Check to see if the encoding/errors are default.
            if not self.config.isDefaultEncodingErrors(asInput=True):
                raise InvocationError("non-default Unicode input encoding/errors but using interactive; give explicit input filename: %s/%s" % (self.config.inputEncoding, self.config.inputErrors))
            self.config.goInteractive = True
        else:
            name = inputFilename
            if name == '-':
                file = sys.stdin
                name = '<stdin>'
            else:
                file = self.config.open(inputFilename, inputMode, self.config.buffering)
                if self.config.relativePath:
                    dirname = os.path.split(inputFilename)[0]
                    sys.path.insert(0, dirname)
            try:
                error = self.protect(name, method, file)
                if error:
                    exitCode = self.config.errorToExitCode(error)
            finally:
                if file is not sys.stdin:
                    file.close()
        # If we're supposed to go interactive afterwards, do it.
        if self.config.goInteractive:
            self.interact()
        # Finally, execute any postprocessing commands.
        self.process(postprocessing)
        return error

    def protect(self, name, callable, *args, **kwargs):
        """Wrap around an application of a callable in a new
        context (named name).  Return any error that occurred
        (if still running) or None."""
        if name:
            context = self.newContext(name)
            self.pushContext(context)
        try:
            if kwargs is None:
                kwargs = {}
            callable(*args, **kwargs)
        finally:
            if name and self.contexts:
                self.popContext()

    def interact(self):
        """Perform interaction.  Return whether or not it succeded."""
        self.invoke('atInteract')
        done = False
        result = None
        while not done:
            error = self.protect('<interact>', self.fileLines, self.input)
            if self.config.exitOnError:
                done = True
            else:
                if not error:
                    done = True
        return result

    def file(self, file, locals=None):
        """Parse a file according to the current buffering strategy."""
        config = self.config
        if config.hasNoBuffering() or config.hasLineBuffering():
            self.fileLines(file, locals)
        elif config.hasFullBuffering():
            self.fileFull(file, locals)
        else: # if self.hasFixedBuffering()
            self.fileChunks(file, config.buffering, locals)

    def fileLines(self, file, locals=None):
        """Parse the entire contents of a file-like object, line by line."""
        if self.invoke('beforeFileLines', file=file, locals=locals):
            return
        scanner = Scanner(self.config, self.getContext(), self.currents)
        done = False
        first = True
        while not done:
            line = file.readline()
            if first:
                if self.config.ignoreBangpaths and self.config.prefix:
                    if line.startswith(self.config.bangpath):
                        line = self.config.prefix + line
                first = False
            if line:
                scanner.feed(line)
            else:
                done = True
            self.safe(scanner, done, locals)
        self.invoke('afterFileLines')

    def fileChunks(self, file, bufferSize=0, locals=None):
        """Parse the entire contents of a file-like object, in
        buffered chunks."""
        assert bufferSize > 0, bufferSize
        if self.invoke('beforeFileChunks', file=file,
                       bufferSize=bufferSize, locals=locals):
            return
        scanner = Scanner(self.config, self.getContext(), self.currents)
        done = False
        first = True
        while not done:
            chunk = file.read(bufferSize)
            if first:
                if self.config.ignoreBangpaths and self.config.prefix:
                    if chunk.startswith(self.config.bangpath):
                        chunk = self.config.prefix + chunk
                first = False
            if chunk:
                scanner.feed(chunk)
            else:
                done = True
            while not self.safe(scanner, done, locals):
                pass
        self.invoke('afterFileChunks')

    def fileFull(self, file, locals=None):
        """Parse the entire contents of a file-like object, in one big
        chunk."""
        if self.invoke('beforeFileFull', file=file, locals=locals):
            return
        scanner = Scanner(self.config, self.getContext(), self.currents)
        data = file.read()
        if self.config.ignoreBangpaths and self.config.prefix:
            if data.startswith(self.config.bangpath):
                data = self.config.prefix + data
        scanner.feed(data)
        self.safe(scanner, True, locals)
        self.invoke('afterFileFull')

    def string(self, data, locals=None):
        """Parse a string.  Cleans up after itself."""
        if self.invoke('beforeString', string=data, locals=locals):
            return
        scanner = Scanner(self.config, self.getContext(), self.currents, data)
        self.safe(scanner, True, locals)
        self.invoke('afterString')

    def safe(self, scanner, final=False, locals=None):
        """Do a protected parse.  Catch transient parse errors; if
        final is true, then make a final pass with a terminator,
        otherwise ignore the transient parse error (more data is
        pending).  Return true if the scanner is exhausted or if
        more data is needed."""
        try:
            return self.parse(scanner, locals)
        except TransientParseError:
            if final:
                buffer = scanner.rest()
                # If the buffer ends with a prefix, it's a real parse
                # error.
                if buffer and buffer.endswith(self.config.prefix):
                    raise
                # Try tacking on a dummy terminator to take into account
                # greedy tokens.
                scanner.feed(self.config.prefix + NEWLINE_CHAR)
                try:
                    # A TransientParseError thrown from here is a real parse
                    # error.
                    self.parse(scanner, locals)
                except TransientParseError:
                    self.handle(sys.exc_info())
            return True
        except KeyboardInterrupt:
            # Handle keyboard interrupts specially: We should always exit
            # from these.
            self.handle(sys.exc_info(), fatal=True)
        except self.config.baseException:
            # A standard exception, excluding a keyboard interrupt.  Note
            # that this includes a system exit exception.
            self.handle(sys.exc_info())
        except:
            # If we get here, then either it's an exception not derived
            # from BaseException.
            type, error, traceback = sys.exc_info()
            if error is None:
                # In ancient versions of Python 2.x, None for an error
                # object means it's a string exception whose value is type.
                error = type
            self.handle((type, error, traceback))

    def parse(self, scanner, locals=None):
        """Parse and run as much from this scanner as possible.  Return
        true if the scanner ran out of tokens."""
        self.invoke('atParse', scanner=scanner, locals=locals)
        while True:
            token = scanner.one()
            if token is None:
                break
            self.invoke('atToken', token=token)
            self.run(token, locals)
            scanner.accumulate()
        return True

    def process(self, commands):
        """Process a sequence of high-level commands."""
        n = 0
        for command in commands:
            if self.invoke('beforeProcess', command=command, n=n):
                return
            try:
                command.process(self, n)
            finally:
                command.cleanup()
            self.invoke('afterProcess')
            n += 1

    # Medium-level processing.

    def tokens(self, tokens, locals=None):
        """Do an explicit expansion on a sequence of tokens.
        Cleans up after itself."""
        outFile = StringIO()
        stream = Stream(outFile, self.diversions)
        if self.invoke('beforeTokens', tokens=tokens, locals=locals):
            return
        self.streams.push(stream)
        try:
            self.runSeveral(tokens, locals)
            stream.flush()
            expansion = outFile.getvalue()
            self.invoke('afterTokens', result=expansion)
            return expansion
        finally:
            self.streams.pop()

    def quote(self, data):
        """Quote the given string so that if it were expanded it would
        evaluate to the original."""
        if self.invoke('beforeQuote', string=data):
            return
        scanner = Scanner(self.config, self.getContext(), self.currents, data)
        result = []
        i = 0
        try:
            j = scanner.next(self.config.prefix, i)
            result.append(data[i:j])
            result.append(self.config.prefix * 2)
            i = j + 1
        except TransientParseError:
            pass
        result.append(data[i:])
        result = ''.join(result)
        self.invoke('afterQuote', result=result)
        return result

    def escape(self, data, more=''):
        """Escape a string so that nonprintable or non-ASCII characters
        are replaced with compatible EmPy expansions.  Also treat
        characters in more as escapes."""
        if self.invoke('beforeEscape', string=data, more=more):
            return
        result = []
        for char in data:
            if char in more:
                result.append(self.config.prefix + '\\' + char)
            elif char < ' ' or char > '~':
                result.append(self.config.escaped(ord(char),
                                                  self.config.prefix + '\\'))
            else:
                result.append(char)
        result = ''.join(result)
        self.invoke('afterEscape', result=result)
        return result

    def tokenize(self, name):
        """Take an lvalue string and return a name or a (possibly recursive)
        list of names."""
        result = []
        stack = [result]
        for garbage in self.ASSIGN_TOKEN_RE.split(name):
            garbage = garbage.strip()
            if garbage:
                raise ParseError("unexpected assignment token: '%s'" % garbage)
        tokens = self.ASSIGN_TOKEN_RE.findall(name)
        # While processing, put a None token at the start of any list in which
        # commas actually appear.
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                top = stack.pop()
                if len(top) == 1:
                    top = top[0] # no None token means that it's not a 1-tuple
                elif top[0] is None:
                    del top[0] # remove the None token for real tuples
                stack[-1].append(top)
            elif token == ',':
                if len(stack[-1]) == 1:
                    stack[-1].insert(0, None)
            else:
                stack[-1].append(token)
        # If it's a 1-tuple at the top level, turn it into a real subsequence.
        if result and result[0] is None:
            result = [result[1:]]
        if len(result) == 1:
            return result[0]
        else:
            return result

    def atomic(self, name, value, locals=None):
        """Do an atomic assignment."""
        if self.invoke('beforeAtomic', name=name, value=value, locals=locals):
            return
        if locals is None:
            self.globals[name] = value
        else:
            locals[name] = value
        self.invoke('afterAtomic')

    def multi(self, names, values, locals=None):
        """Do a (potentially recursive) assignment."""
        if self.invoke('beforeMulti', names=names, values=values, locals=locals):
            return
        values = tuple(values) # to force an exception if not a sequence
        if len(names) != len(values):
            raise ValueError("unpack tuple of wrong size")
        for name, value in zip(names, values):
            if isinstance(name, strType):
                self.atomic(name, value, locals)
            else:
                self.multi(name, value, locals)
        self.invoke('afterMulti')

    def assign(self, name, value, locals=None):
        """Do a potentially complex (including tuple unpacking) assignment."""
        left = self.tokenize(name)
        # The return value of tokenize can either be a string or a list of
        # (lists of) strings.
        if isinstance(left, strType):
            self.atomic(left, value, locals)
        else:
            self.multi(left, value, locals)

    def significate(self, key, value=None, locals=None):
        """Declare a significator."""
        if self.invoke('beforeSignificate', key=key, value=value, locals=locals):
            return
        name = self.config.significatorFor(key)
        self.atomic(name, value, locals)
        self.significators[key] = value
        self.invoke('afterSignificate')

    def import_(self, name, locals=None):
        """Do an import."""
        if self.invoke('beforeImport', name=name, locals=locals):
            return
        self.execute('import %s' % name, locals)
        self.invoke('afterImport')

    def clause(self, catch, locals=None):
        """Given the string representation of an except clause, turn
        it into a 2-tuple consisting of the class name or tuple of
        names, and either a variable name or None.  If the
        representation is None, then it's all exceptions and no name."""
        if self.invoke('beforeClause', catch=catch, locals=locals):
            return
        done = False
        if catch is None:
            exceptionCode, variable = None, None
            done = True
        if not done:
            match = self.AS_RE.search(catch)
            if match:
                exceptionCode, variable = self.AS_RE.split(catch.strip(), 1)
                exceptionCode = exceptionCode.strip()
                variable = variable.strip()
            else:
                comma = catch.rfind(',')
                if comma >= 0:
                    exceptionCode, variable = catch[:comma], catch[comma + 1:]
                    exceptionCode = exceptionCode.strip()
                    variable = variable.strip()
                else:
                    exceptionCode, variable = catch.strip(), None
        if not exceptionCode:
            exception = self.config.baseException
        else:
            exception = self.evaluate(exceptionCode, locals)
        self.invoke('afterClause', exception=exception, variable=variable)
        return exception, variable

    def dictionary(self, code, locals=None):
        """Given a string representing a key-value argument list, turn
        it into a dictionary."""
        code = code.strip()
        self.push()
        try:
            if self.invoke('beforeDictionary', code=code, locals=locals):
                return
            if code.strip():
                result = self.evaluate('{%s}' % code, locals)
            else:
                result = {}
            self.invoke('afterDictionary', result=result)
            return result
        finally:
            self.pop()

    def literal(self, text, locals=None):
        """Process a string literal."""
        if self.invoke('beforeLiteral', text=text, locals=locals):
            return
        result = self.evaluate(text, locals, replace=False)
        self.serialize(result)
        self.invoke('afterLiteral', result=result)

    def functional(self, code, tokensLists, locals=None):
        """Handle a functional expression like @f{x}.  tokensLists
        is a list of list of tokens.  If write is true, write a
        string version of the result (if not None); otherwise,
        return it."""
        self.push()
        try:
            if self.invoke('beforeFunctional', code=code, lists=tokensLists,
                           locals=locals):
                return
            function = self.evaluate(code, locals)
            arguments = []
            for tokensSublist in tokensLists:
                arguments.append(self.tokens(tokensSublist, locals))
            result = function(*tuple(arguments))
            self.invoke('afterFunctional', result=result)
            return result
        finally:
            self.pop()

    # Low-level evaluation.

    def run(self, token, locals=None):
        """Run a token, tracking the current context."""
        token.run(self, locals)

    def runSeveral(self, tokens, locals=None):
        """Run a sequence of tokens."""
        for token in tokens:
            self.run(token, locals)

    def defined(self, name, locals=None):
        """Return a Boolean indicating whether or not the name is
        defined either in the locals or the globals."""
        if self.invoke('beforeDefined', name=name, locals=locals):
            return
        result = False
        if locals is not None and name in locals:
            result = True
        elif name in self.globals:
            result = True
        self.invoke('afterDefined', result=result)
        return result

    def lookup(self, variable, locals=None):
        """Lookup the value of a variable."""
        if locals is not None and variable in locals:
            return locals[variable]
        else:
            return self.globals[variable]

    def evaluate(self, expression, locals=None, replace=True):
        """Evaluate an expression.  If replace is true, replace
        newlines in the expression with spaces if that config
        variable is set; otherwise, don't do it regardless."""
        self.push()
        try:
            if self.invoke('beforeEvaluate', 
                           expression=expression, locals=locals, replace=replace):
                return
            if replace and self.config.replaceNewlines:
                expression = expression.replace('\n', ' ')
            if locals is not None:
                result = self.evalFunc(expression, self.globals, locals)
            else:
                result = self.evalFunc(expression, self.globals)
            self.invoke('afterEvaluate', result=result)
            return result
        finally:
            self.pop()

    def execute(self, statements, locals=None):
        """Execute a statement(s)."""
        # If there are any carriage returns (as opposed to linefeeds/newlines)
        # in the statements code, then remove them.  Even on Windows platforms,
        # this will work in the Python interpreter.
        if CARRIAGE_RETURN_CHAR in statements:
            statements = statements.replace(CARRIAGE_RETURN_CHAR, '')
        # If there are no newlines in the statements code, then strip any
        # leading or trailing whitespace.
        if statements.find(NEWLINE_CHAR) < 0:
            statements = statements.strip()
        self.push()
        try:
            if self.invoke('beforeExecute',
                           statements=statements, locals=locals):
                return
            self.execFunc(statements, self.globals, locals)
            self.invoke('afterExecute')
        finally:
            self.pop()

    def single(self, source, locals=None):
        """Execute an expression or statement, just as if it were
        entered into the Python interactive interpreter."""
        self.push()
        try:
            if self.invoke('beforeSingle', 
                           source=source, locals=locals):
                return
            code = compile(source, '<single>', 'single')
            result = self.execFunc(code, self.globals, locals)
            self.invoke('afterSingle', result=result)
            return result
        finally:
            self.pop()

    # Proxy.

    def evocare(self, increment):
        """Try to call the EmPy special method on the proxy with the
        given increment argument and return the resulting count value.
        If the magic method is not present (no proxy installed) return None."""
        method = getattr(sys.stdout, '_EmPy_evocare', None);
        if method is not None:
            try:
                return method(increment)
            except:
                raise ConsistencyError("proxy increment method should not raise")
        else:
            return None

    def installProxy(self, output=None):
        """Install a proxy if necessary around the given output,
        wrapped to be uncloseable, which can be None.  Return the
        wrapped object (but not the proxy)."""
        if not self.config.useProxy:
            return UncloseableFile(self.config.defaultStdout)
        # Unfortunately, there's no surefire way to make sure that installing a
        # sys.stdout proxy is idempotent, what with different interpreters
        # running from different modules.  The best we can do here is to try to
        # access the special method on the proxy ...
        count = self.evocare(+1)
        if count is not None:
            # ... and if it's present, this is definitely a proxy.  Call it and
            # record it.
            if Interpreter._proxy is None:
                Interpreter._proxy = sys.stdout
            else:
                if sys.stdout is not Interpreter._proxy:
                    raise ConsistencyError("stdout proxy duplicated")
            self.invoke('atInstallProxy', proxy=sys.stdout, new=False)
            output = sys.stdout.bottom
        else:
            # ... but if the current sys.stdout object doesn't have one, then
            # check to see if we think _this_ particular Interpreter class has
            # installed it before ...
            if Interpreter._proxy is not None:
                # ... and if so, we have a problem.
                raise ConsistencyError("stdout proxy lost; has sys.stdout been rebound?: %s" % repr(sys.stdout))
            else:
                # If not, setup the output file, install the proxy, and
                # increment the reference count.
                if output is None:
                    output = self.config.defaultStdout
                proxy = ProxyFile(output, self.config.proxyWrapper)
                sys.stdout = Interpreter._proxy = proxy
                self.evocare(+1)
            self.invoke('atInstallProxy', proxy=sys.stdout, new=True)
        assert output is not None
        return output

    def uninstallProxy(self):
        """Uninstall a proxy if necessary."""
        if not self.config.useProxy:
            return
        # Try decrementing the reference count; if it hits zero, it will
        # automatically remove itself and restore sys.stdout.
        try:
            proxy = sys.stdout
            done = not self.evocare(-1)
            self.invoke('atUninstallProxy', proxy=proxy, done=done)
        except AttributeError:
            if Interpreter._proxy is not None:
                raise ConsistencyError("stdout proxy lost; did you not call shutdown?: %s" % repr(sys.stdout))
        Interpreter._proxy = None

    def checkProxy(self, abandonIsError=True):
        """Check whether a proxy is installed.  Returns the
        current reference count (positive means one is
        installed), None (for no proxy installed), or 0 if the
        proxy has been abandoned.  Thus, true means a proxy is
        installed, false means one isn't.  If abandonIsError
        is true, raise instead of returning 0 on abandonment."""
        if not self.config.useProxy:
            return False
        count = self.evocare(0)
        if count is not None:
            if count == 0 and abandonIsError:
                raise ConsistencyError("stdout proxy abandoned; proxy present but with zero reference count: %s" % repr(sys.stdout))
            return count
        else:
            return None

    #
    # Pseudomodule routines.
    #

    # Identification.

    def identify(self):
        """Identify the topmost context with a tuple of the name and
        counters."""
        return self.getContext().identify()

    # Contexts.

    def getContext(self):
        """Get the top context."""
        return self.contexts.top()

    def newContext(self, name='<unnamed>', line=None, column=None):
        """Create and return a new context."""
        if line is None:
            line = self.config.startingLine
        if column is None:
            column = self.config.startingColumn
        return FullContext(name, line, column)

    def pushContext(self, context):
        """Push a new context on the stack."""
        self.invoke('pushContext', context=context)
        self.contexts.push(context)
        self.currents.push(self.config.renderContext(context))

    def popContext(self):
        """Pop the top context."""
        context = self.contexts.pop()
        self.currents.pop()
        self.invoke('popContext', context=context)

    def setContext(self, context):
        """Replace the top context."""
        self.contexts.replace(context)
        self.invoke('setContext', context=context)

    def setContextName(self, name):
        """Set the name of the topmost context."""
        context = self.getContext()
        context.name = name
        self.invoke('setContext', context=context)

    def setContextLine(self, line):
        """Set the line number of the topmost context."""
        context = self.getContext()
        context.line = line
        self.invoke('setContext', context=context)

    def setContextColumn(self, column):
        """Set the column number of the topmost context."""
        context = self.getContext()
        context.column = column
        self.invoke('setContext', context=context)

    def setContextData(self, name=None, line=None, column=None):
        """Set any of the name, line, or column of the topmost context."""
        context = self.getContext()
        if name is not None:
            context.name = name
        if line is not None:
            context.line = line
        if column is not None:
            context.column = column
        self.invoke('setContext', context=context)

    def restoreContext(self, oldContext, strict=False):
        """Restore from an old context."""
        context = self.getContext()
        context.restore(oldContext, strict)
        self.invoke('restoreContext', context=context)

    # Finalizers.

    def clearFinalizers(self):
        """Clear all finalizers."""
        self.finals.clear()

    def appendFinalizer(self, finalizer):
        """Register a function to be called at exit."""
        self.finals.append(finalizer)

    def prependFinalizer(self, finalizer):
        """Register a function to be called at exit."""
        self.finals.insert(0, finalizer)

    atExit = appendFinalizer

    # Globals.

    def fixGlobals(self):
        """Reset the globals, stamping in the pseudomodule."""
        if self.globals is None:
            self.globals = {}
        # Make sure that there is no collision between two interpreters'
        # globals.
        if self.config.pseudomoduleName in self.globals:
            if self.globals[self.config.pseudomoduleName] is not self:
                raise ConsistencyError("interpreter pseudomodule collision in globals")
        # And finally, flatten the namespaces if that option has been set.
        if self.config.doFlatten:
            self.flattenGlobals()
        self.globals[self.config.pseudomoduleName] = self

    def unfixGlobals(self):
        """Remove the pseudomodule (if present) from the globals."""
        for unwantedKey in self.config.unwantedGlobalsKeys:
            # None is a special sentinel that must be replaced with the name of
            # the pseudomodule.
            if unwantedKey is None:
                unwantedKey = self.config.pseudomoduleName
            if unwantedKey in self.globals:
                del self.globals[unwantedKey]

    def getGlobals(self):
        """Retrieve the globals."""
        return self.globals

    def setGlobals(self, globals):
        """Set the globals to the specified dictionary."""
        self.globals = globals
        self.fixGlobals()

    def updateGlobals(self, otherGlobals):
        """Merge another mapping object into this interpreter's globals."""
        self.globals.update(otherGlobals)
        self.fixGlobals()

    def clearGlobals(self):
        """Clear out the globals with a brand new dictionary."""
        self.globals = {}
        self.fixGlobals()

    def saveGlobals(self, deep=True):
        """Save a copy of the globals off onto the history stack."""
        if deep:
            copyMethod = copy.deepcopy
        else:
            copyMethod = copy.copy
        self.unfixGlobals()
        self.globalsHistory.push(copyMethod(self.globals))
        self.fixGlobals()

    def restoreGlobals(self, destructive=True):
        """Restore the most recently saved copy of the globals."""
        if destructive:
            fetchMethod = self.globalsHistory.pop
        else:
            fetchMethod = self.globalsHistory.top
        self.unfixGlobals()
        self.globals = fetchMethod()
        self.fixGlobals()

    def flattenGlobals(self, skipKeys=None):
        """Flatten the contents of the pseudo-module into the globals
        namespace."""
        flattened = {}
        if skipKeys is None:
            skipKeys = self.config.unflattenableGlobalsKeys
        # The pseudomodule is really a class instance, so we need to fumble
        # using getattr instead of simply fumbling through the instance's
        # __dict__.
        for key in self.__dict__.keys():
            if key not in skipKeys:
                flattened[key] = getattr(self, key)
        for key in self.__class__.__dict__.keys():
            if key not in skipKeys:
                flattened[key] = getattr(self, key)
        # Stomp everything into the globals namespace.
        self.globals.update(flattened)

    # Prefix.

    def getPrefix(self):
        """Get the current prefix."""
        return self.config.prefix

    def setPrefix(self, prefix):
        """Set the prefix."""
        assert (prefix is None or
                (isinstance(prefix, strType) and len(prefix) == 1)), prefix
        self.config.prefix = prefix

    # Diversions.

    def stopDiverting(self):
        """Stop any diverting."""
        self.top().revert()

    def createDiversion(self, name):
        """Create a diversion (but do not divert to it) if it does not
        already exist."""
        self.top().create(name)

    def retrieveDiversion(self, name, *defaults):
        """Retrieve the diversion object associated with the name."""
        return self.top().retrieve(name, *defaults)

    def startDiversion(self, name):
        """Start diverting to the given diversion name."""
        self.top().divert(name)

    def playDiversion(self, name, drop=True):
        """Play the given diversion and then drop it."""
        self.top().undivert(name, drop)

    def replayDiversion(self, name, drop=False):
        """Replay the diversion without dropping it."""
        self.top().undivert(name, drop)

    def dropDiversion(self, name):
        """Eliminate the given diversion."""
        self.top().drop(name)

    def playAllDiversions(self):
        """Play all existing diversions and then drop them."""
        self.top().undivertAll(True)

    def replayAllDiversions(self):
        """Replay all existing diversions without dropping them."""
        self.top().undivertAll(False)

    def dropAllDiversions(self):
        """Drop all existing diversions."""
        self.top().dropAll()

    def getCurrentDiversionName(self):
        """Get the name of the current diversion."""
        return self.top().current

    def getAllDiversionNames(self):
        """Get the names of all existing diversions."""
        return self.top().names()

    def isExistingDiversionName(self, name):
        """Does a diversion with this name currently exist?"""
        return self.top().has(name)

    # Filters.

    def resetFilter(self):
        """Reset the filter stream so that it does no filtering."""
        self.top().install(None)

    def getFilter(self):
        """Get the top-level filter."""
        filter = self.top().filter
        if filter is self.top().file:
            return None
        else:
            return filter

    getFirstFilter = getFilter

    def getLastFilter(self):
        """Get the last filter in the current chain."""
        return self.top().last()

    def getFilterCount(self):
        """Get the number of chained filters; 0 means no active
        filters."""
        return self.top().count()

    def setFilter(self, *filters):
        """Set the filter."""
        self.top().install(filters)

    def prependFilter(self, filter):
        """Attach a single filter to the end of the current filter chain."""
        self.top().prepend(filter)

    def appendFilter(self, filter):
        """Attach a single filter to the end of the current filter chain."""
        self.top().append(filter)

    def setFilterChain(self, filters):
        """Set the filter."""
        self.top().install(filters)

    # Hooks.

    def invokeHook(self, _name, **kwargs):
        """Invoke the hook(s) associated with the hook name, should they
        exist.  Stop and return on the first hook which returns a true
        result."""
        if self.config.verbose:
            self.config.verboseFile.write("%s: %s\n" % (_name, repr(kwargs)))
        if self.hooksEnabled:
            for hook in self.hooks:
                try:
                    method = getattr(hook, _name)
                    result = method(**kwargs)
                    if result:
                        return result
                finally:
                    pass

    invoke = invokeHook

    def areHooksEnabled(self):
        """Return whether or not hooks are presently enabled."""
        if self.hooksEnabled is None:
            # None is a special value indicate that hooks are enabled but none
            # have been added yet.  It is equivalent to true for testing but
            # can be optimized away upon invocation.
            return True
        else:
            return self.hooksEnabled

    def enableHooks(self):
        """Enable hooks."""
        self.hooksEnabled = True

    def disableHooks(self):
        """Disable hooks."""
        self.hooksEnabled = False

    def getHooks(self):
        """Get the current hooks."""
        return self.hooks

    def addHook(self, hook, prepend=False):
        """Add a new hook; optionally insert it rather than appending it."""
        hook.register(self)
        if self.hooksEnabled is None:
            self.hooksEnabled = True
        if prepend:
            self.hooks.insert(0, hook)
        else:
            self.hooks.append(hook)

    def appendHook(self, hook):
        """Append the given hook."""
        self.addHook(hook, False)

    def prependHook(self, hook):
        """Prepend the given hook."""
        self.addHook(hook, True)

    def removeHook(self, hook):
        """Remove a preexisting hook."""
        hook.deregister(self)
        self.hooks.remove(hook)

    def clearHooks(self):
        """Clear all hooks."""
        for hook in self.hooks:
            hook.deregister(self)
        self.hooks = []
        self.hooksEnabled = None

    # Callbacks.

    def hasCallback(self):
        """Is there a custom callback registered?"""
        return self.callback is not None

    def getCallback(self):
        """Get the custom markup callback registered with this
        interpreter, or None."""
        return self.callback

    def registerCallback(self, callback):
        """Register a custom markup callback with this interpreter."""
        self.callback = callback

    def deregisterCallback(self):
        """Remove any previously registered custom markup callback
        with this interpreter."""
        self.callback = None

    def invokeCallback(self, contents):
        """Call the custom markup callback."""
        if self.invoke('beforeCallback', contents=contents):
            return
        result = None
        if self.callback is None:
            if self.config.noCallbackIsError:
                raise ConfigurationError("custom markup invoked with no defined callback")
        else:
            result = self.callback(contents)
        self.invoke('afterCallback', result=result)
        return result

    # Error handling.

    def exit(self, exitCode):
        """Exit on an error."""
        # If we are supposed to delete the file on error, do it.
        if self.filespec is not None and self.config.deleteOnError:
            # But don't do it on a successful exit.
            if exitCode != self.config.successCode:
                os.remove(self.filespec[0])
        sys.exit(exitCode)

    def handle(self, info, fatal=False):
        """Handle an actual error that occurred."""
        self.invoke('atHandle', info=info, fatal=fatal, contexts=self.currents)
        type, error, traceback = info
        self.error = error
        exitCode = self.config.errorToExitCode(error)
        if self.config.isExitError(error):
            # No Python exception, but we're going to exit.
            fatal = True
        else:
            useDefault = True
            if self.handler is not None:
                useDefault = self.handler(type, error, traceback)
            if useDefault:
                useDefault = self.defaultHandler(type, error, traceback)
            if self.config.rawErrors:
                raise
        if fatal or self.config.exitOnError:
            self.shutdown()
            self.exit(exitCode)

    def defaultHandler(self, type, error, traceback):
        """Report an error."""
        first = True
        self.flush()
        sys.stderr.write('\n')
        for current in self.currents:
            if current is None:
                current = self.config.renderContext(self.getContext())
            if first:
                if error is not None:
                    description = "error: %s" % self.config.formatError(error)
                else:
                    description = "error"
            else:
                description = "from this context"
            first = False
            sys.stderr.write('%s: %s\n' % (current, description))
        sys.stderr.flush()

    def getHandler(self):
        """Get the current handler, or None for the default."""
        return self.handler

    def setHandler(self, handler, exitOnError=False):
        """Set the current handler.  Additionally, specify whether
        errors should exit (defaults to false with a custom
        handler)."""
        self.handler = handler
        if exitOnError is not None:
            self.config.exitOnError = exitOnError

    def invokeHandler(self, *args):
        """Manually invoke the error handler with the given
        exception info 3-tuple or three arguments."""
        if len(args) == 1:
            self.handler(*args[0])
        else:
            self.handler(*args)

    # Emojis.

    def initializeEmojiModules(self, moduleNames=None):
        """Determine which emoji module to use.  If moduleNames is not
        specified, use the defaults."""
        return self.config.initializeEmojiModules(moduleNames)

    def getEmojiModule(self, moduleName):
        """Return an abstracted emoji module by name or return
        None."""
        return self.config.emojiModules.get(moduleName)

    def getEmojiModuleNames(self):
        """Return the emoji module names in usage in their proper
        order."""
        return self.config.emojiModuleNames

    def substituteEmoji(self, text):
        """Substitute an emoji text or return None."""
        return self.config.substituteEmoji(text)

#
# functions
#

def details(level, prelim="Welcome to ", postlim=".\n",
            file=sys.stdout):
    """Write some details, using the details subsystem if available."""
    write = file.write
    details = None
    if level > Version.VERSION:
        try:
            import emlib
            details = emlib.Details()
        except ImportError:
            raise ConfigurationError("missing emlib module; details subsystem not available")
    if details:
        try:
            details.show(level, prelim, postlim, file)
        except TypeError:
            raise
    else:
        write("%s%s version %s%s" % (prelim, __project__, __version__, postlim))
    sys.stdout.flush()

def expand(data, config=None, globals=None, argv=None, name='<expand>',
           **locals):
    """Do a self-contained expansion of the given source data,
    creating and shutting down an interpreter dedicated to the task.
    Any additional keyword arguments are treated as a locals
    dictionary.  The sys.stdout object is saved off and then replaced
    before this function returns."""
    if len(locals) == 0:
        # If there were no keyword arguments specified, don't use a locals
        # dictionary at all.
        locals = None
    output = NullFile()
    interpreter = None
    result = None
    try:
        interpreter = Interpreter(
            config=config,
            globals=globals,
            output=output,
            argv=argv)
        result = interpreter.expand(data, locals, name)
    finally:
        if interpreter:
            interpreter.shutdown()
            if globals is not None:
                interpreter.unfixGlobals() # remove pseudomodule to prevent clashes
    return result

def invoke(args, executable='?', config=None, globals=None, output=None,
           callback=None, handler=None, errors=()):
    """Run a standalone instance of an EmPy interpreter with the
    given globals, config, and output (any of which can be None).
    Return the resulting exit code.  Errors is a variable that
    represents a tuple of exception types to catch and print
    rather than let through; if it is None, use the defaults from
    the configuration."""
    # Initialize the options.
    if config is None:
        config = Configuration()
    if errors is None:
        errors = config.topLevelErrors
    try:
        inputFilename = None
        inputMode = 'r'
        outputFilename = None
        outputMode = None
        nullFile = False
        preprocessing = []
        postprocessing = []
        configStatements = []
        configPaths = []
        hooks = []
        level = Version.NONE
        topics = None
        # Note any configuration files from the environment.
        configPath = config.environment(CONFIG_ENV)
        if configPath is not None:
            configPaths.append(configPath)
        # Get any extra arguments from the environment.
        extraArguments = config.environment(OPTIONS_ENV)
        if extraArguments is not None:
            extraArguments = extraArguments.split()
            args = extraArguments + args
        # Parse the arguments.
        try:
            SHORTS = 'VWZh?H:vp:qm:fkeridnc:Co:a:O:A:b:NLBP:Q:I:D:S:E:F:G:wluxyz'
            LONGS = ['version', 'info', 'details', 'help', 'topics=', 'extended-help=', 'verbose', 'prefix=', 'no-prefix', 'no-output', 'pseudomodule=', 'module=', 'flatten', 'keep-going', 'ignore-errors', 'raw-errors', 'interactive', 'delete-on-error', 'no-proxy', 'no-override-stdout', 'config=', 'configuration=', 'config-file=', 'configuration-file=', 'config-variable=', 'configuration-variable=', 'ignore-missing-config', 'output=' 'append=', 'output-binary=', 'append-binary=', 'output-mode=', 'input-mode=', 'buffering=', 'default-buffering', 'no-buffering', 'line-buffering', 'full-buffering', 'preprocess=', 'postprocess=', 'import=', 'define=', 'string=', 'execute=', 'file=', 'postfile=', 'pause-at-end', 'relative-path', 'no-callback-error', 'no-replace-newlines', 'no-ignore-bangpaths', 'no-expand-user', 'no-auto-validate-icons', 'none-symbol', 'starting-line=', 'starting-column=', 'emoji-modules=', 'no-emoji-modules', 'disable-emoji-modules', 'ignore-emoji-not-found', 'binary', 'input-binary', 'unicode', 'encoding=', 'unicode-encoding=', 'input-encoding=', 'unicode-input-encoding=', 'output-encoding=', 'unicode-output-encoding=', 'errors=', 'unicode-errors=', 'input-errors=', 'unicode-input-errors=', 'output-errors=', 'unicode-output-errors=', 'normalization-form=', 'unicode-normalization-form=', 'auto-play-diversions', 'no-auto-play-diversions', 'check-variables', 'no-check-variables', 'path-separator', 'context-format=', 'success-code=', 'failure-code=', 'unknown-code=', 'null-hook']
            pairs, argv = getopt.getopt(args, SHORTS, LONGS)
        except getopt.GetoptError:
            type, error, traceback = sys.exc_info()
            if error.args[1] == 'H':
                # A missing argument with -H should be interpreted as -H all.
                pairs = []
                topics = 'all'
            else:
                raise InvocationError(*error.args)
        for option, argument in pairs:
            if option in ['-V', '--version']:
                level += 1
            elif option in ['-W', '--info']:
                level = Version.INFO
            elif option in ['-Z', '--details']:
                level = Version.ALL
            elif option in ['-h', '-?', '--help']:
                if not topics:
                    topics = 'default'
                elif topics == 'default':
                    topics = 'more'
                else:
                    topics = 'all'
            elif option in ['-H', '--topics', '--extended-help']:
                topics = argument
                if ',' in topics:
                    topics = topics.split(',')
                else:
                    topics = [topics]
            elif option in ['-v', '--verbose']:
                config.verbose = True
            elif option in ['-p', '--prefix']:
                config.prefix = argument
            elif option in ['--no-prefix']:
                config.prefix = None
            elif option in ['-q', '--no-output']:
                nullFile = True
            elif option in ['-m', '--pseudomodule', '--module']:
                config.pseudomoduleName = argument
            elif option in ['-f', '--flatten']:
                config.doFlatten = True
            elif option in ['-k', '--keep-going']:
                config.exitOnError = False
            elif option in ['-e', '--ignore-errors']:
                def noop(*args, **kwargs):
                    pass
                handler = noop
                config.exitOnError = False
            elif option in ['-r', '--raw-errors']:
                config.rawErrors = True
            elif option in ['-i', '--interactive']:
                config.goInteractive = True
            elif option in ['-d', '--delete-on-error']:
                config.deleteOnError = True
            elif option in ['-n', '--no-proxy', '--no-override-stdout']:
                config.useProxy = False
            elif option in ['--config', '--configuration']:
                configStatements.append(argument)
            elif option in ['-c', '--config-file', '--configuration-file']:
                configPaths.append(argument)
            elif option in ['--config-variable', '--configuration-variable']:
                config.configVariableName = argument
            elif option in ['-C', '--ignore-missing-config']:
                config.missingConfigIsError = False
            elif option in ['-o', '--output']:
                outputFilename = argument
                outputMode = 'w'
            elif option in ['-a', '--append']:
                outputFilename = argument
                outputMode = 'a'
            elif option in ['-O', '--output-binary']:
                outputFilename = argument
                outputMode = 'wb'
            elif option in ['-A', '--append-binary']:
                outputFilename = argument
                outputMode = 'ab'
            elif option in ['--output-mode']:
                outputMode = argument
            elif option in ['--input-mode']:
                inputMode = argument
            elif option in ['-b', '--buffering']:
                config.setBuffering(argument)
            elif option in ['--default-buffering']:
                config.setBuffering(config.defaultBuffering)
            elif option in ['-N', '--no-buffering']:
                config.setBuffering(config.noBuffering)
            elif option in ['-L', '--line-buffering']:
                config.setBuffering(config.lineBuffering)
            elif option in ['-B', '--full-buffering']:
                config.setBuffering(config.fullBuffering)
            elif option in ['-P', '--preprocess']:
                preprocessing.append(DocumentCommand(argument))
            elif option in ['-Q', '--postprocess']:
                postprocessing.append(DocumentCommand(argument))
            elif option in ['-I', '--import']:
                for module in argument.split(','):
                    module = module.strip()
                    preprocessing.append(ImportCommand(module))
            elif option in ['-D', '--define']:
                preprocessing.append(DefineCommand(argument))
            elif option in ['-S', '--string']:
                preprocessing.append(StringCommand(argument))
            elif option in ['-E', '--execute']:
                preprocessing.append(ExecCommand(argument))
            elif option in ['-F', '--file']:
                preprocessing.append(FileCommand(argument))
            elif option in ['-G', '--postfile']:
                postprocessing.append(FileCommand(argument))
            elif option in ['-w', '--pause-at-end']:
                config.pauseAtEnd = True
            elif option in ['-l', '--relative-path']:
                config.relativePath = True
            elif option in ['--no-callback-error']:
                config.noCallbackIsError = False
            elif option in ['--no-replace-newlines']:
                config.replaceNewlines = False
            elif option in ['--no-ignore-bangpaths']:
                config.ignoreBangpaths = False
            elif option in ['--no-expand-user']:
                config.expandUserConstructions = False
            elif option in ['--no-auto-validate-icons']:
                config.autoValidateIcons = False
            elif option in ['--none-symbol']:
                config.noneSymbol = argument
            elif option in ['--starting-line']:
                config.startingLine = int(argument)
            elif option in ['--starting-column']:
                config.startingColumn = int(argument)
            elif option in ['--emoji-modules']:
                moduleNames = [x.strip() for x in argument.split(',')]
                if moduleNames == ['None'] or moduleNames == ['']:
                    moduleNames = None
                config.emojiModuleNames = moduleNames
            elif option in ['--no-emoji-modules']:
                config.emojiModuleNames = config.defaultNoEmojiModuleNames
            elif option in ['--disable-emoji-modules']:
                config.emojiModuleNames = None
            elif option in ['--ignore-emoji-not-found']:
                config.emojiNotFoundIsError = False
            elif option in ['-u', '--binary', '--input-binary', '--unicode']:
                config.enableBinary()
            elif option in ['-x', '--encoding', '--unicode-encoding']:
                config.enableBinary(major, minor)
                config.inputEncoding = config.outputEncoding = argument
            elif option in ['--input-encoding', '--unicode-input-encoding']:
                config.enableBinary(major, minor)
                config.inputEncoding = argument
            elif option in ['--output-encoding', '--unicode-output-encoding']:
                config.enableBinary(major, minor)
                config.outputEncoding = argument
            elif option in ['-y', '--errors', '--unicode-errors']:
                config.enableBinary(major, minor)
                config.inputErrors = config.outputErrors = argument
            elif option in ['--input-errors', '--unicode-input-errors']:
                config.enableBinary(major, minor)
                config.inputErrors = argument
            elif option in ['--output-errors', '--unicode-output-errors']:
                config.enableBinary(major, minor)
                config.outputErrors = argument
            elif option in ['-z', '--normalization-form', '--unicode-normalization-form']:
                if argument == 'none' or argument == 'None':
                    argument = ''
                config.normalizationForm = argument
            elif option in ['--auto-play-diversions']:
                config.autoPlayDiversions = True
            elif option in ['--no-auto-play-diversions']:
                config.autoPlayDiversions = False
            elif option in ['--check-variables']:
                config.checkVariables = True
            elif option in ['--no-check-variables']:
                config.checkVariables = False
            elif option in ['--path-separator']:
                config.pathSeparator = argument
            elif option in ['--context-format']:
                config.setContextFormat(argument)
                Context.format = config.contextFormat
            elif option in ['--success-code']:
                config.successCode = int(argument)
            elif option in ['--failure-code']:
                config.failureCode = int(argument)
            elif option in ['--unknown-code']:
                config.unknownCode = int(argument)
            elif option in ['--null-hook']:
                try:
                    import emlib
                    hooks.append(emlib.Hook())
                except ImportError:
                    raise InvocationError("missing emlib module; --null-hook not available")
            else:
                assert False, "unhandled option: %s" % option
        # Show the details and exit if desired.
        if level > 0:
            details(level)
            return config.successCode
        # Load any configuration files.
        for configStatement in configStatements:
            config.run(configStatement)
        for configPath in configPaths:
            config.path(configPath)
        # Show the help if desired.
        if topics is not None:
            try:
                import emhelp
                usage = emhelp.Usage(config)
                usage.hello()
                usage.show(topics)
            except ImportError:
                raise InvocationError("missing emhelp subsystem module; no help available")
            return config.successCode
        # Set up the main script filename and the arguments.
        if not argv:
            argv.append(None)
        else:
            inputFilename = argv[0]
        # Do sanity checks on the configuration.
        config.check(inputFilename, outputFilename)
        # Now initialize the output file.
        if nullFile:
            output = NullFile()
            filespec = None
        elif outputFilename is not None:
            if output is not None:
                raise InvocationError("can't specify more than one output")
            filespec = outputFilename, outputMode, config.buffering
            output = config.open(*filespec)
        else:
            # Check to see if the encoding/errors are default.
            if not config.isDefaultEncodingErrors(asInput=False):
                raise InvocationError("non-default Unicode output encoding/errors selected but using stdout; use -o/-a option: %s/%s" % (config.outputEncoding, config.outputErrors))
            filespec = None
        # Get ready!
        interpreter = None
        exitCode = config.successCode
        try:
            # Create the interpreter.
            interpreter = Interpreter(
                config=config,
                globals=globals,
                output=output,
                argv=argv,
                filespec=filespec,
                hooks=hooks,
                callback=callback,
                handler=handler,
                executable=executable,
                immediately=False)
            # Run it.
            error = interpreter.go(
                inputFilename, inputMode, preprocessing, postprocessing)
        finally:
            # Finally, handle any cleanup.
            if interpreter.ok:
                interpreter.shutdown()
    except SystemExit:
        type, error, traceback = sys.exc_info()
        if len(error.args) > 0:
            exitCode = error.args[0] # okay even if a string
    except errors:
        type, error, traceback = sys.exc_info()
        sys.stderr.write(config.formatError(error, "ERROR: ", "\n"))
        exitCode = config.unknownCode
    except:
        raise
    # Old versions of Python 3.x don't flush sys.__stdout__ when redirecting
    # stdout for some reason.
    if sys.__stdout__ is not None:
        sys.__stdout__.flush()
    return exitCode

#
# main
#

def main():
    exitCode = invoke(sys.argv[1:], executable=sys.argv[0], errors=None)
    sys.exit(exitCode)

if __name__ == '__main__': main()
