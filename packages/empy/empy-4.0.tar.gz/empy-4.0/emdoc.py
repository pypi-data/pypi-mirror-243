#!/usr/bin/env python3

"""
EmPy documentation generating system.  This module requires a modern
Python 3.x interpreter.
"""

#
# imports
#

import hashlib
import os
import subprocess
import sys
import time

import em
import emhelp
import emlib

#
# constants
#

PREFIX = ":::{important}\n"
SUFFIX = "\n:::\n"
EMOJIS = {
    '...': ('\N{HORIZONTAL ELLIPSIS}', "horizontal ellipsis"),
    '!!!': (PREFIX + "!!! \u2757\ufe0f" + SUFFIX, "exclamation mark"),
    '???': (PREFIX + "??? \u2753\ufe0f" + SUFFIX, "question mark"),
    '^^^': (PREFIX + "^^^ \u26a0\ufe0f" + SUFFIX, "warning sign"),
    '///': (PREFIX + "/// \u2714\ufe0f" + SUFFIX, "check mark"),
    '\\\\\\': (PREFIX + "\\\\\\ \u274c\ufe0f" + SUFFIX, "cross mark"),
    '+++': (PREFIX + "+++ \U0001f53a" + SUFFIX, "red triangle pointed up"),
    '---': (PREFIX + "--- \U0001f53b" + SUFFIX, "red triangle pointed down"),
    '-->': ('\N{LONG RIGHTWARDS ARROW}', "long rightwards arrow"),
}

#
# Identity
#

class Identity:

    """Dynamically access magic attributes on both the interpreter and
    underlying module."""

    def __init__(self, pseudo, module):
        self.pseudo = pseudo
        self.module = module

    def __str__(self):
        try:
            return self.__getattr__('project')
        except AttributeError:
            return self.__getattr__('program')

    def __getattr__(self, attr):
        attribute = '__{}__'.format(attr)
        if attribute in self.pseudo.globals:
            return self.pseudo.globals[attribute]
        elif attribute in self.module.__dict__:
            return self.module.__dict__[attribute]
        else:
            raise AttributeError("unknown attribute: {}".format(__attribute__))

    def tarball(self, version='latest'):
        if version is None:
            version = self.version
        return '{}{}-{}.tar.gz'.format(self.url, self.program, version)

    def path(self, suffix=None):
        if suffix is not None:
            return self.url + suffix
        else:
            return self.url

#
# Information
#

class Information:

    """A helper information class to generate documentation."""

    timeFormat = '%Y-%m-%d %H:%M:%S'
    extensions = ['.md.em', '.md.pre', '.md', '']
    hashFactory = hashlib.sha1
    hashName = 'SHA1'
    encoding = 'utf-8'

    class Flag:

        """Encapsulate a flag:  a command line option, a configuration
        variable, and/or an environment variable."""

        def __init__(self, config, options, var=None, env=None):
            self.config = config
            self.options = options
            self.var = var
            self.env = env

        def __str__(self):
            return str((self.options, self.var))

        def render(self, file, key, verbose=False):
            isOption = key.startswith('-')
            options = '/'.join("`{}`".format(x) for x in self.options)
            environ = '`{}`'.format(self.env) if self.env else None
            variable = '`{}`'.format(self.var) if self.var else None
            fragments = []
            if verbose:
                if isOption:
                    assert options
                    # It's an option, so list those first.
                    primary = options
                    if environ:
                       fragments.extend(["_environment variable:_ " + environ])
                    if variable:
                        fragments.extend(["_configuration variable:_ " + variable])
                elif key.startswith('EMPY_'):
                    assert environ
                    # If it starts with EMPY_, it's an environment variable.
                    primary = environ
                    if options:
                        fragments.extend(["_command line option:_ " + options])
                    if variable:
                        fragments.extend(["_configuration variable:_ " + variable])
                else:
                    assert variable
                    # Otherwise, it's a configuration variable.
                    primary = variable
                    types = self.config._specs[key]
                    if types is not None:
                        if types == (bytes, str):
                            types = str
                        if not isinstance(types, tuple):
                            types = (types,)
                        types = ' | '.join(
                            'None' if x is None else x.__name__
                            for x in types)
                        primary = primary[:-1] + ": {}`".format(types)
                    if options:
                        fragments.extend(["_command line option:_ " + options])
                    if environ:
                       fragments.extend(["_environment variable:_ " + environ])
                if fragments:
                    file.write('{} ({})'.format(primary, ', '.join(fragments)))
                else:
                    file.write(primary)
            else:
                if isOption:
                    file.write(options)
                else:
                    file.write('`{}`'.format(key))

    noLanguage = 'text'

    def __init__(self, pseudo, moduleName, file=sys.stdout):
        self.pseudo = pseudo
        self.moduleName = moduleName
        self.file = file
        self.module = __import__(moduleName)
        self.ident = Identity(pseudo, self.module)
        self.details = emlib.Details()
        self.config = em.Configuration()
        self.usage = emhelp.Usage(config=self.config)
        self.options = self.process()

    def process(self):
        options = {}
        section = self.usage.payload['options']
        for entry in section.entries:
            fullOptions = [x for x in entry.raw if not x.isspace()]
            theseOptions = [x.split('=', 1)[0] for x in fullOptions]
            flag = self.Flag(self.config, fullOptions, entry.var, entry.env)
            for key in theseOptions:
                assert key not in options, key
                options[key] = flag
            if entry.var:
                options[entry.var] = flag
            if entry.env:
                options[entry.env.split(' ', 1)[0]] = flag
        for key, value in self.config.__dict__.items():
            if key in options:
                options[key].val = value
            else:
                flag = self.Flag(self.config, [], key)
                options[key] = flag
        return options

    def topic(self, topic, separator=False):
        self.file.write("```{}\n".format(self.noLanguage))
        self.usage.show([topic], separator)
        self.file.write("```\n")

    def option(self, key, verbose=False, default=False):
        if verbose is None:
            self.file.write('`{}`'.format(key))
            return
        self.options[key].render(self.file, key, verbose)
        if default and key in self.config:
            if key == 'pathSeparator':
                value = "`;` (Windows), `:` (others)"
            else:
                value = getattr(self.config, key)
                if isinstance(value, tuple):
                    value = repr(value)
                if isinstance(value, dict):
                    value = "{...}"
                value = "`{}`".format(value)
            self.file.write(" [{}]".format(value))

    def variable(self, variable):
        self.file.write("`{}`".format(variable))

    def source(self, filename='README'):
        for extension in self.extensions:
            if os.path.exists(filename + extension):
                return filename + extension
        else:
            raise FileNotFoundError("source file not found: {}".format(filename))

    def filter(self, text, lines=None):
        if isinstance(text, bytes) and self.encoding:
            text = text.decode(self.encoding)
        text = (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))
        chunks = []
        for line in text.splitlines():
            if line.startswith('...'):
                chunks.append("<i>{}</i>".format(line))
            else:
                chunks.append(line)
            if lines is not None and len(chunks) >= lines:
                chunks.append('...')
                break
        return '\n'.join(chunks)
    
    def shell(self, command, output, prefix='% ', lines=None, exitCode=0):
        display = command
        if isinstance(display, list):
            display = ' '.join(display)
        self.file.write("<pre class=\"shell\">")
        if display:
            self.file.write("<b><i>{}{}</i></b>\n".format(
                prefix, self.filter(display)))
        self.file.write(self.filter(output, lines))
        if exitCode != 0:
            self.file.write("<i>Exit code {}</i>".format(exitCode))
        self.file.write("</pre>\n")

    def execute(self, command, prefix='% ', lines=None, check=True):
        oldPath = os.environ['PATH']
        try:
            # Make sure that if it's em.py, it's the local one.
            path = '.:' + oldPath
            os.environ['PATH'] = path
            result = subprocess.run(command, capture_output=True)
            output = result.stdout
            self.shell(command, output, prefix, lines, exitCode=result.returncode)
        finally:
            os.environ['PATH'] = oldPath

    def summarize(self):
        filename = self.source()
        hasher = self.hashFactory()
        with open(filename, 'rb') as f:
            data = f.read()
        length = len(data)
        hasher.update(data)
        hash = hasher.hexdigest()
        record = os.stat(filename)
        when = time.localtime(record.st_mtime)
        timeStamp = time.strftime(self.timeFormat, when)
        out = em.StringIO('w')
        self.details.show(file=out)
        self.file.write("""\
_This documentation for {} version {} was generated from {} ({} `{}`, {} bytes) at {} with {}._
""".format(
    self.ident, self.ident.version, filename,
    self.hashName, hash, length,
    timeStamp, out.getvalue()))
        self.done()

    def done(self):
        if self.config:
            self.pseudo.dropAllDiversions()
            self.config = None

#
# Callback
#

class Callback(emlib.Callback):

    """The EmPy documentation custom callback."""

    languages = {
        'empy': '' # to eliminate Pygments warning
    }

    asTable = False

    def __init__(self, interp):
        super(Callback, self).__init__(interp)
        self.current = 0

    def __call__(self, source):
        caption = None
        if source.startswith('['):
            language = 'empy'
            caption, source = source[1:].split(']', 1)
            example = True
        else:
            if not source.startswith('\n'):
                language, source = source.split('\n', 1)
                language = language.strip()
            else:
                language = ''
            example = False
        if caption:
            suffix = ': ' + caption
        else:
            suffix = ''
        source = source.strip() + '\n'
        if example:
            number = self.next()
            self.interp.startDiversion(caption)
            self.interp.write(":::{{admonition}} Example {}{}\n".format(
                number, suffix))
            output = em.expand(source,
                name='<example {}>'.format(number))
            if self.asTable:
                self.interp.write("&nbsp;  \n")
                self.interp.write("<table>\n")
                self.interp.write("<tr><th>Source</th><th>Output</th></tr>\n")
                self.interp.write("<tr><td valign=top>\n\n")
                self.interp.write("``````\n{}``````\n\n".format(source))
                self.interp.write("</td><td valign=top>\n\n")
                self.interp.write("``````\n{}``````\n\n".format(output))
                self.interp.write("</td></tr>\n")
                self.interp.write("</table>\n")
            else:
                self.interp.write("&nbsp;  \n")
                self.interp.write("&nbsp;  \n")
                self.interp.write("_Source_:\n")
                self.interp.write("``````{}\n".format(self.languages.get(language, language)))
                self.interp.write(source)
                self.interp.write("``````\n")
                self.interp.write("\n")
                self.interp.write("_Output_:\n")
                self.interp.write("``````\n")
                self.interp.write(output)
                self.interp.write("``````\n")
            self.interp.write(":::\n")
            self.interp.stopDiverting()
            self.interp.replayDiversion(caption)
        else:
            self.interp.write("``````{}\n".format(self.languages.get(language, language)))
            self.interp.write(source)
            self.interp.write("``````\n")

    def next(self, amount=1):
        self.current += amount
        return self.current

#
# Hook
#

class Hook(emlib.Hook):

    """The EmPy documentation hook."""

    delimiter = '`'

    def __init__(self, interp):
        self.interp = interp

    def preBackquote(self, literal):
        if self.delimiter in literal:
            for count in range(1, 10):
                if '`' * count not in literal:
                    count -= 1
                    break
        else:
            count = 0
        affix = self.delimiter * (count + 1)
        self.interp.write("{}{}{}".format(affix, literal, affix))
        return True

#
# init
#

def init(pseudo, moduleName, paths=['../..', '.']):
    """Initialize the information object."""
    for path in paths:
        sys.path.insert(0, os.path.abspath(path))
    pseudo.config.emojis = EMOJIS
    pseudo.addHook(Hook(pseudo))
    pseudo.registerCallback(Callback(pseudo))
    return Information(pseudo, moduleName)
