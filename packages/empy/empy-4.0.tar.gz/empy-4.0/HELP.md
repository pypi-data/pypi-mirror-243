# Help topic summaries

The following subsections contain the output of EmPy's builtin help
system (`emhelp`).

## Command line usage summary

```text
USAGE:
./em.py [<options>] [<filename, or `-` for stdin> [<argument>...]]
  - Options begin with `-` or `--`
  - Specify a filename (and arguments) to process that file as input
  - Specify `-` (and arguments) to process stdin with standard buffering
  - Specify no filename to enter interactive mode with line buffering
```

## Command line options summary

```text
OPTIONS:
Valid command line options (defaults in brackets):
  -V --version                  Print version
  -W --info                     Print version and system information
  -Z --details                  Print extensive system and platform details
  -h --help                     Print help; more -h options for more help
  -H --topics=TOPICS            Print usage for comma-separated topics
  -v --verbose                  Show verbose debugging while processing
  -p --prefix=CHAR              Choose desired prefix [@]
     --no-prefix                Do not do any markup processing at all
  -q --no-output                Suppress all output
  -m --pseudomodule=NAME        Change internal pseudomodule name [empy]
  -f --flatten                  Flatten pseudomodule members at start [False]
  -k --keep-going               Don't exit on errors; continue
  -e --ignore-errors            Ignore errors completely
  -r --raw-errors               Show full tracebacks of Python errors [False]
  -i --interactive              Enter interactive mode after processing [False]
  -d --delete-on-error          Delete output file on error
                                (-o or -a needed) [False]
  -n --no-proxy                 Do not override sys.stdout with proxy [True]
     --config=STATEMENTS        Do configuration variable assignments
  -c --config-file=FILENAME     Load configuration resource path(s)
     --config-variable=NAME     Configuration variable name while loading [_]
  -C --ignore-missing-config    Don't raise for missing configuration files
  -o --output=FILENAME          Specify file for output as write
  -a --append=FILENAME          Specify file for output as append
  -O --output-binary=FILENAME   Specify file for binary output as write
  -A --append-binary=FILENAME   Specify file for binary output as append
     --output-mode=MODE         Explicitly specify the mode for output
     --input-mode=MODE          Explicitly specify the mode for input
  -b --buffering                Specify buffering strategy for files:
                                none (= 0), line (= 1), full (= -1), default,
                                or another value for fixed [16384]
     --default-buffering        Specify default buffering for files
  -N --no-buffering             Specify no buffering for reads on files
  -L --line-buffering           Specify line buffering for files
  -B --full-buffering           Specify full buffering for files
  -P --preprocess=FILENAME      Interpret EmPy file before main file
  -Q --postprocess=FILENAME     Interpret EmPy file after main file
  -I --import=MODULES           Import Python modules before processing
  -D --define=DEFN              Execute Python assignment statement
  -S --string=STR               Execute string literal assignment
  -E --execute=STATEMENT        Execute Python statement before main file
  -F --file=FILENAME            Execute Python file before main file
  -G --postfile=FILENAME        Execute Python file after main file
  -w --pause-at-end             Prompt at the ending of processing
  -l --relative-path            Add path of EmPy script to sys.path [False]
     --no-callback-error        Custom markup with no callback is ignored
     --no-replace-newlines      Don't replace expression newlines with spaces
     --no-ignore-bangpaths      Don't treat bangpaths as comments
     --no-expand-user           Don't expand user constructions in filenames
     --no-auto-validate-icons   Don't auto-validate icons
     --none-symbol              String to write when expanding None [None]
     --starting-line            Line number to start with [1]
     --starting-column          Column number to start with [1]
     --emoji-modules            Comma-separated list of emoji modules to try
                                [emoji,emojis,emoji_data_python,unicodedata]
     --no-emoji-modules         Only use unicodedata for emoji markup
     --disable-emoji-modules    Disable emoji modules; use emojis dictionary
     --ignore-emoji-not-found   Emoji not found is not an error
  -u --binary --unicode         Read input file as binary?
                                (enables Unicode support in Python 2.x) [False]
  -x --encoding=E               Set both input and output Unicode encodings
     --input-encoding=E         Set input Unicode encoding [utf-8]
     --output-encoding=E        Set output Unicode encoding [utf-8]
  -y --errors=E                 Set both input and output Unicode error handler
     --input-errors=E           Set input Unicode error handler [strict]
     --output-errors=E          Set output Unicode error handler [strict]
  -z --normalization-form=F     Specify Unicode normalization form [NFKC]
     --no-auto-play-diversions  Don't autoplay diversions on exit [True]
     --no-check-variables       Don't validate configuration variables [True]
     --path-separator           Path separator for configuration paths [:]
     --context-format           Context format [%(name)s:%(line)d:%(column)d]
     --success-code=N           Exit code to return on script success [0]
     --failure-code=N           Exit code to return on script failure [1]
     --unknown-code=N           Exit code to return on bad configuration [2]
```

## Markup summary

```text
MARKUP:
The following markups are supported:
  @# ... NL                  Line comment; remove everything including newline
  @* ... *                   Inline comment; remove everything inside
  @ WHITESPACE               Ignore whitespace; line continuation
  @@                         Literal @; @ is escaped (duplicated prefix)
  @' STRING '                Replace with string literal contents
  @" STRING "                Replace with string literal contents
  @''' STRING ... '''        Replace with multiline string literal contents
  @""" STRING ... """        Replace with multiline string literal contents
  @` LITERAL `               Write everything inside literally (no expansion)
  @( EXPRESSION )            Evaluate expression and substitute with str
  @( TEST ? THEN )           If test, evaluate then, otherwise do nothing
  @( TEST ? THEN ! ELSE )    If test, evaluate then, otherwise evaluate else;
                             can be chained with repeated test/then/[else]
  @( TRY $ EXCEPT )          Evaluate try expression, or except if it raises
  @ SIMPLE_EXPRESSION        Evaluate simple expression and substitute;
                             (e.g., @x, @x.y, @f(a, b), @l[i], @f{...}, etc.)
  @$ EXPRESSION $ [DUMMY] $  Evaluates to @$ EXPRESSION $ EXPANSION $
  @{ STATEMENTS }            Statements are executed for side effects
  @[ CONTROL ]               Control markups: if E; elif E; for N in E;
                             while E; try; except E as N; finally;
                             continue; break; else; defined N; def F(...);
                             end X
  @\ ESCAPE_CODE             A C-style escape sequence
  @^ CHAR DIACRITIC          A two-character diacritic sequence
                             (e.g., e' for an e with acute accent)
  @| ICON                    A custom icon sequence
                             (e.g., '( for a single open curly quote)
  @: EMOJI :                 Lookup emoji by name
  @% KEY NL                  Significator form of __KEY__ = None
  @% KEY WS VALUE NL         Significator form of __KEY__ = VALUE
  @%! KEY NL                 Significator form of __KEY__ = ""
  @%! KEY WS STRING NL       Stringized significator form: __KEY__ = "STRING"
  @%% KEY WS VALUE %% NL     Multiline significator form
  @%%! KEY WS STRING %% NL   Multiline stringized significator form
  @? NAME NL                 Set the current context name
  @! INTEGER NL              Set the current context line number
  @< CONTENTS >              Custom markup; meaning provided via callback
```

## Escape sequences summary

```text
ESCAPES:
Valid escape sequences are:
  @\0          U+0000; NUL, null
  @\a          U+0007; BEL, bell
  @\b          U+0008; BS, backspace
  @\B{BIN}     freeform binary code BIN (e.g., {1000001} for A)
  @\dDDD       three-digit decimal code DDD (e.g., 065 for A)
  @\D{DEC}     freeform decimal code DEC (e.g., {65} for A)
  @\e          U+001B; ESC, escape
  @\f          U+000C; FF, form feed
  @\h          U+007F; DEL, delete
  @\k          U+0006; ACK, acknowledge
  @\K          U+0015; NAK, negative acknowledge
  @\n          U+000A; LF, linefeed; newline
  @\N{NAME}    Unicode character named NAME (e.g., LATIN CAPITAL LETTER A)
  @\oOOO       three-digit octal code OOO (e.g., 101 for A)
  @\O{OCT}     freeform octal code OCT (e.g., {101} for A)
  @\qQQQQ      four-digit quaternary code QQQQ (e.g., 1001 for A)
  @\Q{QUA}     freeform quaternary code QUA (e.g., {1001} for A)
  @\r          U+000D; CR, carriage return
  @\s          U+0020; SP, space
  @\S          U+00A0; NBSP, no-break space
  @\t          U+0009; HT, horizontal tab
  @\uHHHH      16-bit hexadecimal Unicode HHHH (e.g., 0041 for A)
  @\UHHHHHHHH  32-bit hexadecimal Unicode HHHHHHHH (e.g., 00000041 for A)
  @\v          U+000B; VT, vertical tab
  @\V{VS}      VS, variation selector (1 .. 256) (e.g., 16 for emoji display)
  @\w          U+FE0E; VS15, variation selector 15; text display
  @\W          U+FE0F; VS16, variation selector 16; emoji display
  @\xHH        8-bit hexadecimal code HH (e.g., 41 for A)
  @\X{HEX}     freeform hexadecimal code HEX (e.g., {41} for A)
  @\y          U+001A; SUB, substitution
  @\Y          U+FFFD; RC, replacement character: �
  @\z          U+0004; EOT, end of transmission
  @\Z          U+FEFF; ZWNBSP/BOM, zero-width no-break space/byte order mark
  @\,          U+2009; THSP, thin space
  @\^C         Control character C (e.g., [ for ESC)
  @\^{NAME}    Control character named NAME (e.g., ESC)
  @\(          U+0028; Literal (: (
  @\)          U+0029; Literal ): )
  @\[          U+005B; Literal [: [
  @\]          U+005D; Literal ]: ]
  @\{          U+007B; Literal {: {
  @\}          U+007D; Literal }: }
  @\<          U+003C; Literal <: <
  @\>          U+003E; Literal >: >
  @\\          U+005C; Literal \: \
  @\'          U+0027; Literal ': '
  @\"          U+0022; Literal ": "
  @\?          U+003F; Literal ?: ?
```

## Environment variables summary

```text
ENVIRON:
The following environment variables are recognized (with corresponding
command line arguments):
  EMPY_OPTIONS          Specify additional options to be included
  EMPY_CONFIG           Specify configuration file(s) to load: -c PATHS
  EMPY_PREFIX           Specify the default prefix: -p PREFIX
  EMPY_PSEUDO           Specify name of pseudomodule: -m NAME
  EMPY_FLATTEN          Flatten empy pseudomodule if defined: -f
  EMPY_RAW_ERRORS       Show raw errors if defined: -r
  EMPY_INTERACTIVE      Enter interactive mode if defined: -i
  EMPY_DELETE_ON_ERROR  Delete output file on error: -d
  EMPY_NO_PROXY         Do not install sys.stdout proxy if defined: -n
  EMPY_BUFFERING        Buffer size (-1, 0, 1, or n): -b VALUE
  EMPY_BINARY           Open input file as binary (for Python 2.x Unicode): -u
  EMPY_ENCODING         Unicode both input and output encodings
  EMPY_INPUT_ENCODING   Unicode input encoding
  EMPY_OUTPUT_ENCODING  Unicode output encoding
  EMPY_ERRORS           Unicode both input and output error handlers
  EMPY_INPUT_ERRORS     Unicode input error handler
  EMPY_OUTPUT_ERRORS    Unicode output error handler
```

## Pseudomodule attributes and methods summary

```text
PSEUDO:
The empy pseudomodule contains the following attributes and methods:
  version                         String representing EmPy version
  compat                          List of applied Python compatibility features
  executable                      The EmPy executable
  argv                            EmPy script name and command line arguments
  config                          The configuration for this interpreter
  __init__(**kwargs)              The interpreter constructor
  __enter__/__exit__(...)         Context manager support
  reset()                         Reset the interpreter state
  ready()                         Declare the interpreter ready
  shutdown()                      Shutdown the interpreter
  write(data)                     Write data to stream
  writelines(lines)               Write a sequence of lines to stream
  flush()                         Flush the stream
  serialize(object)               Write a string version of the object
  identify()                      Identify top context as name, line
  getContext()                    Return the current context
  newContext(...)                 Return a new context with name and counts
  pushContext(context)            Push a context
  popContext()                    Pop the current context
  setContext(context)             Replace the current context
  setContextName(name)            Set the name of the current context
  setContextLine(line)            Set the line number of the current context
  setContextColumn(column)        Set the column number of the current context
  setContextData(...)             Set any of the name, line, column number
  restoreContext(context)         Replace the top context with an existing one
  removeFinalizers()              Remove all finalizers
  appendFinalizer(finalizer)      Append function to be called at shutdown
  prependFinalizer(finalizer)     Prepend function to be called at shutdown
  getGlobals()                    Retrieve this interpreter's globals
  setGlobals(dict)                Set this interpreter's globals
  updateGlobals(dict)             Merge dictionary into interpreter's globals
  clearGlobals()                  Start globals over anew
  saveGlobals([deep])             Save a copy of the globals
  restoreGlobals([pop])           Restore the most recently saved globals
  include(file, [loc])            Include filename or file-like object
  expand(string, [loc])           Explicitly expand string and return
  defined(name, [loc])            Find if the name is defined
  lookup(name, [loc])             Lookup the variable name
  evaluate(expression, [loc])     Evaluate the expression (and write?)
  execute(statements, [loc])      Execute the statements
  single(source, [loc])           Execute the expression or statement
  atomic(name, value, [loc])      Perform an atomic assignment
  assign(name, value, [loc])      Perform an arbitrary assignment
  significate(key, [value])       Significate the given key, value pair
  quote(string)                   Quote prefixes in provided string and return
  escape(data)                    Escape EmPy markup in data and return
  flatten([keys])                 Flatten module contents to globals namespace
  getPrefix()                     Get current prefix
  setPrefix(char)                 Set new prefix
  stopDiverting()                 Stop diverting; data sent directly to output
  createDiversion(name)           Create a diversion but do not divert to it
  retrieveDiversion(name, [def])  Retrieve the actual named diversion object
  startDiversion(name)            Start diverting to given diversion
  playDiversion(name)             Recall diversion and then eliminate it
  replayDiversion(name)           Recall diversion but retain it
  dropDiversion(name)             Drop diversion
  playAllDiversions()             Stop diverting and play all diversions
  replayAllDiversions()           Stop diverting and replay all diversions
  dropAllDiversions()             Stop diverting and drop all diversions
  getCurrentDiversionName()       Get the name of the current diversion
  getAllDiversionNames()          Get a sorted sequence of diversion names
  isExistingDiversionName(name)   Is this the name of a diversion?
  getFilter()                     Get the first filter in the current chain
  getLastFilter()                 Get the last filter in the current chain
  getFilterCount()                Get the number of filters in current chain
  resetFilter()                   Reset filter; no filtering
  setFilter(filter...)            Install new filter(s), replacing any chain
  prependFilter(filter)           Prepend filter to beginning of current chain
  appendFilter(filter)            Append a filter to end of current chain
  setFilterChain(filters)         Install a new filter chain
  areHooksEnabled()               Return whether or not hooks are enabled
  enableHooks()                   Enable hooks (default)
  disableHooks()                  Disable hook invocation
  getHooks()                      Get all the hooks
  appendHook(hook)                Append the given hook
  prependHook(hook)               Prepend the given hook
  removeHook(hook)                Remove an already-registered hook
  clearHooks()                    Clear all hooks
  invokeHook(_name, ...)          Manually invoke hook
  hasCallback()                   Is there a custom callback?
  getCallback()                   Get custom callback
  registerCallback(callback)      Register custom callback
  deregisterCallback()            Deregister custom callback
  invokeCallback(contents)        Invoke the custom callback directly
  defaultHandler(t, e, tb)        The default error handler
  getHandler()                    Get the current error handler (or None)
  setHandler(handler, [eoe])      Set the error handler
  invokeHandler(t, e, tb)         Manually invoke the error handler
  initializeEmojiModules(names)   Initialize the emoji modules
  getEmojiModule(name)            Get an abstracted emoji module
  getEmojiModuleNames()           Return the list of emoji module names
  substituteEmoji(text)           Do an emoji substitution
```

## Configuration variables summary

```text
CONFIG:
The following configuration variable attributes are supported (defaults in
brackets, with dictionaries being summarized with their length):
  name                     The name of this configuration (optional) [default]
  notes                    Notes for this configuration (optional) [None]
  prefix                   The prefix [@]
  pseudomoduleName         The pseudomodule name [empy]
  verbose                  Verbose processing (for debugging)? [False]
  rawErrors                Print Python stacktraces on error? [False]
  exitOnError              Exit after an error? [True]
  contextFormat            Context format [%(name)s:%(line)d:%(column)d]
  goInteractive            Go interactive after done processing? [False]
  deleteOnError            Delete output file on error? [False]
  doFlatten                Flatten pseudomodule members at start? [False]
  useProxy                 Install a stdout proxy? [True]
  relativePath             Add EmPy script path to sys.path? [False]
  buffering                Specify buffering strategy for files:
                           0 (none), 1 (line), -1 (full), or N [16384]
  noCallbackIsError        Is custom markup with no callback an error? [True]
  replaceNewlines          Replace newlines with spaces in expressions? [True]
  ignoreBangpaths          Treat bangpaths as comments? [True]
  noneSymbol               String to write when expanding None [None]
  missingConfigIsError     Is a missing configuration file an error? [True]
  pauseAtEnd               Prompt at the end of processing? [False]
  startingLine             Line number to start with [1]
  startingColumn           Column number to start with [1]
  significatorDelimiters   Significator variable delimiters [('__', '__')]
  emptySignificator        Value to use for empty significators [None]
  autoValidateIcons        Automatically validate icons before each use? [True]
  emojiModuleNames         List of emoji modules to try to use
                           [['emoji', 'emojis', 'emoji_data_python', 'unicodedata']]
  emojiNotFoundIsError     Is an unknown emoji an error? [True]
  useBinary                Open files as binary (Python 2.x Unicode)? [False]
  inputEncoding            Set input Unicode encoding [utf-8]
  outputEncoding           Set output Unicode encoding [utf-8]
  inputErrors              Set input Unicode error handler [strict]
  outputErrors             Set output Unicode error handler [strict]
  normalizationForm        Specify Unicode normalization form [NFKC]
  autoPlayDiversions       Auto-play diversions on exit? [True]
  expandUserConstructions  Expand ~ and ~user constructions [True]
  configVariableName       Configuration variable name while loading [_]
  successCode              Exit code to return on script success [0]
  failureCode              Exit code to return on script failure [1]
  unknownCode              Exit code to return on bad configuration [2]
  checkVariables           Check configuration variables on assignment? [True]
  pathSeparator            Path separator for configuration file paths [:]
  controls                 Controls dictionary [{138}]
  diacritics               Diacritics dictionary [{63}]
  icons                    Icons dictionary [{108}]
  emojis                   Emojis dictionary [{0}]
```

## Configuration methods summary

```text
METHODS:
The configuration instance contains the following methods:
  initialize()                    Initialize the instance
  shutdown()                      Shutdown the instance
  isInitialize()                  Is this configuration initialized?
  pauseIfRequired()               Pause if required
  check(in, out)                  Check file settings
  has(name)                       Is this variable defined?
  get(name[, default])            Get this variable value
  set(name, value)                Set this variable
  update(**kwargs)                Update with dictionary
  run(statements)                 Run configuration commands
  load(filename, [required])      Load configuration file
  path(filename, [required])      Load configuration file(s) path
  hasEnvironment(name)            Is this environment variable defined?
  environment(name, ...)          Get the enviroment variable value
  hasDefaultPrefix()              Is the prefix the default?
  hasFullBuffering()              Is the buffering set to full?
  hasNoBuffering()                Is the buffering set to none?
  hasLineBuffering()              Is the buffering set to line?
  hasFixedBuffering()             Is the buffering set to fixed?
  createFactory([tokens])         Create token factory
  adjustFactory()                 Adjust token factory for non-default prefix
  getFactory([tokens], [force])   Get a token factory
  restFactory()                   Clear the current token factory
  hasBinary()                     Is binary (Unicode) support enabled?
  enableBinary(...)               Enable binary (Unicode) support
  disableBinary()                 Disable binary (Unicode) support
  isDefaultEncodingErrors()       Is encoding/errors the default?
  getDefaultEncoding()            Get the default file encoding
  open(filename, [mode], ...)     Open a file
  significatorReString()          Regular expression string for significators
  significatorRe()                Regular expression pattern for significators
  significatorFor(key)            Significator variable name for key
  setContextFormat(format)        Set the context format
  renderContext(context)          Render context using format
  calculateIconsSignature()       Calculate icons signature
  signIcons()                     Sign the icons dictionary
  transmogrifyIcons()             Process the icons dictionary
  validateIcons()                 Process the icons dictionaray if necessary
  intializeEmojiModules([names])  Initialize emoji module support
  substituteEmoji(text)           Substitute emoji
  isSuccessCode(code)             Does this exit code indicate success?
  isExitError(error)              Is this exception instance an exit?
  errorToExitCode(error)          Return exit code for exception instance
  isNotAnError(error)             Is this exception instance not an error?
  formatError(error[, p, s])      Render an error string from instance
```

## Hook methods summary

```text
HOOKS:
The following hook methods are supported.  The return values are ignored except
for the `pre...` methods which, when they return a true value, signal that the
following token handling should be skipped:
  atInstallProxy(proxy, new)          Proxy being installed
  atUninstallProxy(proxy, new)        Proxy being uninstalled
  atStartup()                         Interpreter started up
  atReady()                           Interpreter ready
  atFinalize()                        Interpreter finalizing
  atShutdown()                        Interpreter shutting down
  atParse(scanner, loc)               Interpreter parsing
  atToken(token)                      Interpreter expanding token
  atHandle(info, fatal, contexts)     Interpreter encountered error
  atInteract()                        Interpreter going interactive
  pushContext(context)                Context being pushed
  popContext(context)                 Context was popped
  setContext(context)                 Context was set or modified
  restoreContext(context)             Context was restored
  prePrefix()                         Pre prefix token
  preWhitespace()                     Pre whitespace token
  preString(string)                   Pre string literal token
  preLineComment(comment)             Pre line comment
  postLineComment()                   Post line comment
  preInlineComment(comment)           Pre inline comment
  postInlineComment()                 Post inline comment
  preBackquote(literal)               Pre backquote literal
  postBackquote()                     Post backquote literal
  preSignificator(key, value, s)      Pre significator
  postSignificator()                  post significator
  preContextName(name)                Pre context name
  postContextName()                   Post context name
  preContextLine(line)                Pre context line
  postContextLine()                   Post context line
  preExpression(pairs, except, loc)   Pre expression
  postExpression(result)              Post expression
  preSimple(code, sub, loc)           Pre simple expression
  postSimple(result)                  Post simple expression
  preInPlace(code, loc)               Pre in-place expression
  postInPlace(result)                 Post in-place expression
  preStatement(code, loc)             Pre statement
  postStatement()                     Post statement
  preControl(type, rest, loc)         Pre control
  postControl()                       Post control
  preEscape(code)                     Pre escape
  postEscape()                        Post escape
  preDiacritic(code)                  Pre diacritic
  postDiacritic()                     Post diacritic
  preIcon(code)                       Pre icon
  postIcon()                          Post icon
  preEmoji(name)                      Pre emoji
  postEmoji()                         Post emoji
  preCustom(contents)                 Pre custom
  postCustom()                        Post custom
  beforeProcess(command, n)           Before command processing
  afterProcess()                      After command processing
  beforeInclude(file, loc, name)      Before file inclusion
  afterInclude()                      After file inclusion
  beforeExpand(string, loc, name)     Before expand call
  afterExpand(result)                 After expand call
  beforeTokens(tokens, loc)           Before processing tokens
  afterTokens(result)                 After processing tokens
  beforeFileLines(file, loc)          Before reading file by lines
  afterFileLines()                    After reading file by lines
  beforeFileChunks(file, loc)         Before reading file by chunks
  afterFileChunks()                   After reading file by chunks
  beforeFileFull(file, loc)           Before reading file in full
  afterFilFull()                      After reading file in full
  beforeString(string, loc)           Before processing string
  afterString()                       After processing string
  beforeQuote(string)                 Before quoting string
  afterQuote()                        After quoting string
  beforeEscape(string)                Before escaping string
  afterEscape()                       After escaping string
  beforeSignificate(key, value, loc)  Before significator
  afterSignificate()                  After significator
  beforeCallback(contents)            Before custom callback
  afterCallback()                     Before custom callback
  beforeAtomic(name, value, loc)      Before atomic assignment
  afterAtomic()                       After atomic assignment
  beforeMulti(names, values, loc)     Before complex assignment
  afterMulti()                        After complex assignment
  beforeImport(name, loc)             Before module import
  afterImport()                       After module import
  beforeFunctional(code, lists, loc)  Before functional expression
  afterFunctional(result)             After functional expression
  beforeEvaluate(code, loc, write)    Before expression evaluation
  afterEvaluate(result)               After expression evaluation
  beforeExecute(statements, loc)      Before statement execution
  afterExecute()                      After statement execution
  beforeSingle(source, loc)           Before single execution
  afterSingle(result)                 After single execution
  beforeFinalizer(final)              Before finalizer processing
  afterFinalizer()                    After finalizer processing
```

## Named escapes summary

```text
NAMED:
The following named escapes (control codes) (`@\^{...}`) are supported:
  NUL     U+0000; null
  SOH     U+0001; start of heading
  STX     U+0002; start of text
  ETX     U+0003; end of text
  EOT     U+0004; end of transmission, end of data
  ENQ     U+0005; enquiry
  ACK     U+0006; acknowledge
  BEL     U+0007; bell, alert
  BS      U+0008; backspace
  HT      U+0009; horizontal tabulation, tab
  LF      U+000A; linefeed, newline
  NL      U+000A; linefeed, newline
  LT      U+000B; line tabulation, vertical tab
  VT      U+000B; line tabulation, vertical tab
  FF      U+000C; form feed
  CR      U+000D; carriage return
  SO      U+000E; shift out
  SI      U+000F; shift in
  DLE     U+0010; data link escape
  DC1     U+0011; device control one, xon
  XON     U+0011; device control one, xon
  DC2     U+0012; device control two
  DC3     U+0013; device control three, xoff
  XOFF    U+0013; device control three, xoff
  DC4     U+0014; device control four
  NAK     U+0015; negative acknowledge
  SYN     U+0016; synchronous idle
  ETB     U+0017; end of transmission block
  CAN     U+0018; cancel
  EM      U+0019; end of medium
  SUB     U+001A; substitute
  ESC     U+001B; escape
  FS      U+001C; file separator, information separator four
  IS4     U+001C; file separator, information separator four
  GS      U+001D; group separator, information separator three
  IS3     U+001D; group separator, information separator three
  IS2     U+001E; record separator, information separator two
  RS      U+001E; record separator, information separator two
  IS1     U+001F; unit separator, information separator one
  US      U+001F; unit separator, information separator one
  SP      U+0020; space
  DEL     U+007F; delete
  PAD     U+0080; padding character
  HOP     U+0081; high octet preset
  BPH     U+0082; break permitted here
  IND     U+0084; index
  NEL     U+0085; next line
  SSA     U+0086; start of selected area
  ESA     U+0087; end of selected area
  HTS     U+0088; character tabulation set
  HTJ     U+0089; character tabulation with justification
  VTS     U+008A; line tabulation set
  PLD     U+008B; partial line forward
  PLU     U+008C; partial line backward
  RI      U+008D; reverse line feed
  SS2     U+008E; single shift two
  SS3     U+008F; single shift three
  DCS     U+0090; device control string
  PV1     U+0091; private use one
  PV2     U+0092; private use two
  STS     U+0093; set transmission state
  CHC     U+0094; cancel character
  MW      U+0095; message waiting
  SPA     U+0096; start guarded area
  EPA     U+0097; end guarded area
  SOS     U+0098; start of string
  SCI     U+009A; single character introducer
  CSI     U+009B; control sequence introducer
  ST      U+009C; string terminator
  OSC     U+009D; operating system command
  PM      U+009E; privacy message
  APC     U+009F; application program command
  NBSP    U+00A0; no-break space
  SHY     U+00AD; soft hyphen, discretionary hyphen
  CGJ     U+034F; combining grapheme joiner
  NQSP    U+2000; en quad
  MQSP    U+2001; em quad, mutton quad
  ENSP    U+2002; en space, nut
  EMSP    U+2003; em space, mutton
  3MSP    U+2004; three-per-em space, thick space
  4MSP    U+2005; four-per-em space, mid space
  6MSP    U+2006; six-per-em space
  FSP     U+2007; figure space
  PSP     U+2008; punctuation space
  THSP    U+2009; thin space
  HSP     U+200A; hair space
  ZWSP    U+200B; zero width space
  ZWNJ    U+200C; zero width non-joiner
  ZWJ     U+200D; zero width joiner
  LRM     U+200E; left-to-right mark
  RLM     U+200F; right-to-left mark
  NBH     U+2011; non-breaking hyphen: ‑
  LSEP    U+2028; line separator
  PSEP    U+2029; paragraph separator
  LRE     U+202A; left-to-right encoding
  RLE     U+202B; right-to-left encoding
  PDF     U+202C; pop directional formatting
  LRO     U+202D; left-to-right override
  RLO     U+202E; right-to-left override
  NNBSP   U+202F; narrow no-break space
  MMSP    U+205F; medium mathematical space
  WJ      U+2060; word joiner
  FA      U+2061; function application (`f()`)
  IT      U+2062; invisible times (`x`)
  IS      U+2063; invisible separator (`,`)
  ISS     U+206A; inhibit symmetric swapping
  ASS     U+206B; activate symmetric swapping
  IAFS    U+206C; inhibit arabic form shaping
  AAFS    U+206D; activate arabic form shaping
  NADS    U+206E; national digit shapes
  NODS    U+206F; nominal digit shapes
  IDSP    U+3000; ideographic space
  IVI     U+303E; ideographic variation indicator
  VS1     U+FE00; variation selector 1
  VS2     U+FE01; variation selector 2
  VS3     U+FE02; variation selector 3
  VS4     U+FE03; variation selector 4
  VS5     U+FE04; variation selector 5
  VS6     U+FE05; variation selector 6
  VS7     U+FE06; variation selector 7
  VS8     U+FE07; variation selector 8
  VS9     U+FE08; variation selector 9
  VS10    U+FE09; variation selector 10
  VS11    U+FE0A; variation selector 11
  VS12    U+FE0B; variation selector 12
  VS13    U+FE0C; variation selector 13
  VS14    U+FE0D; variation selector 14
  TEXT    U+FE0E; variation selector 15, text display
  VS15    U+FE0E; variation selector 15, text display
  EMOJI   U+FE0F; variation selector 16, emoji display
  VS16    U+FE0F; variation selector 16, emoji display
  BOM     U+FEFF; zero width no-break space, byte order mark
  ZWNBSP  U+FEFF; zero width no-break space, byte order mark
  IAA     U+FFF9; interlinear annotation anchor
  IAS     U+FFFA; interlinear annotation separator
  IAT     U+FFFB; interlinear annotation terminator
  ORC     U+FFFC; object replacement character
  RC      U+FFFD; replacement character: �
```

## Diacritic combiners summary

```text
DIACRITICS:
The following diacritic combining characters (`@^C...`) are supported:
  `       U+0300; grave: ◌̀
  '       U+0301; acute: ◌́
  ^       U+0302; circumflex accent: ◌̂
  ~       U+0303; tilde: ◌̃
  -       U+0304; macron: ◌̄
  _       U+0305; overline: ◌̅
  (       U+0306; breve: ◌̆
  .       U+0307; dot: ◌̇
  :       U+0308; diaeresis: ◌̈
  ?       U+0309; hook above: ◌̉
  o       U+030A; ring above: ◌̊
  "       U+030B; double acute accent: ◌̋
  v       U+030C; caron: ◌̌
  s       U+030D; vertical line above: ◌̍
  S       U+030E; double vertical line above: ◌̎
  @       U+0310; candrabinu: ◌̐
  )       U+0311; inverted breve: ◌̑
  1       U+0312; turned comma above: ◌̒
  2       U+0313; comma above: ◌̓
  3       U+0314; reversed comma above: ◌̔
  4       U+0315; comma above right: ◌̕
  ]       U+0316; grave accent below: ◌̖
  [       U+0317; acute accent below: ◌̗
  <       U+0318; left tack below: ◌̘
  >       U+0319; right tack below: ◌̙
  A       U+031A; left angle above: ◌̚
  h       U+031B; horn: ◌̛
  r       U+031C; left half ring below: ◌̜
  u       U+031D; up tack below: ◌̝
  d       U+031E; down tack below: ◌̞
  +       U+031F; plus sign below: ◌̟
  m       U+0320; minus sign below: ◌̠
  P       U+0321; palatalized hook below: ◌̡
  R       U+0322; retroflex hook below: ◌̢
  D       U+0323; dot below: ◌̣
  E       U+0324; diaeresis below: ◌̤
  O       U+0325; ring below: ◌̥
  c       U+0326; comma below: ◌̦
  ,       U+0327; cedilla: ◌̧
  K       U+0328; ogonek: ◌̨
  V       U+0329; vertical line below: ◌̩
  $       U+032A; bridge below: ◌̪
  W       U+032B; inverted double arch below: ◌̫
  H       U+032C; caron below: ◌̬
  C       U+032D; circumflex accent below: ◌̭
  B       U+032E; breve below: ◌̮
  N       U+032F; inverted breve below: ◌̯
  T       U+0330; tilde below: ◌̰
  M       U+0331; macron below: ◌̱
  l       U+0332; low line: ◌̲
  L       U+0333; double low line: ◌̳
  &       U+0334; tilde overlay: ◌̴
  !       U+0335; short stroke overlay: ◌̵
  |       U+0336; long stroke overlay: ◌̶
  %       U+0337; short solidays overlay: ◌̷
  /       U+0338; long solidus overlay: ◌̸
  g       U+0339; right half ring below: ◌̹
  *       U+033A; inverted bridge below: ◌̺
  #       U+033B; square below: ◌̻
  G       U+033C; seagull below: ◌̼
  x       U+033D; x above: ◌̽
  ;       U+033E; vertical tilde: ◌̾
  =       U+033F; double overline: ◌̿
```

## Icons summary

```text
ICONS:
The following icon sequences (`@|...`) are supported:
  !       U+2757 U+FE0F; exclamation mark: ❗️
  ""      U+0022; quotation mark: "
  "(      U+201C; left double quotation mark: “
  ")      U+201D; right double quotation mark: ”
  $       U+1F4B2; heavy dollar sign: 💲
  %%      U+1F3B4; flower playing cards: 🎴
  %c      U+2663 U+FE0F; club suit: ♣️
  %d      U+2666 U+FE0F; diamond suit: ♦️
  %e      U+1F9E7; red gift envelope: 🧧
  %h      U+2665 U+FE0F; heart suit: ♥️
  %j      U+1F0CF; joker: 🃏
  %r      U+1F004; Mahjong red dragon: 🀄
  %s      U+2660 U+FE0F; spade suit: ♠️
  &!      U+1F396 U+FE0F; military medal: 🎖️
  &$      U+1F3C6; trophy: 🏆
  &0      U+1F3C5; sports medal: 🏅
  &1      U+1F947; first place medal: 🥇
  &2      U+1F948; second place medal: 🥈
  &3      U+1F949; third place medal: 🥉
  ''      U+0027; apostrophe: '
  '(      U+2018; left single quotation mark: ‘
  ')      U+2019; right single quotation mark: ’
  '/      U+00B4; acute accent: ´
  '\      U+0060; grave accent: `
  **      U+2716 U+FE0F; heavy multiplication sign: ✖️
  *+      U+2795 U+FE0F; heavy plus sign: ➕️
  *-      U+2796 U+FE0F; heavy minus sign: ➖️
  */      U+2797 U+FE0F; heavy division sign: ➗️
  +       U+1F53A; red triangle pointed up: 🔺
  ,+      U+1F44D; thumbs up: 👍
  ,-      U+1F44E; thumbs down: 👎
  ,a      U+261D U+FE0F; point above: ☝️
  ,d      U+1F447; point down: 👇
  ,f      U+1F44A; oncoming fist: 👊
  ,l      U+1F448; point left: 👈
  ,o      U+1FAF5; point out: 🫵
  ,r      U+1F449; point right: 👉
  ,s      U+1F91D; handshake: 🤝
  ,u      U+1F446; point up: 👆
  -       U+1F53B; red triangle pointed down: 🔻
  .d      U+2B07 U+FE0F; down arrow: ⬇️
  .l      U+2B05 U+FE0F; left arrow: ⬅️
  .r      U+27A1 U+FE0F; right arrow: ➡️
  .u      U+2B06 U+FE0F; up arrow: ⬆️
  /       U+2714 U+FE0F; check mark: ✔️
  :$      U+1F911; money-mouth face: 🤑
  :(      U+1F61E; disappointed face: 😞
  :)      U+1F600; grinning face: 😀
  :*      U+1F618; face blowing a kiss: 😘
  :/      U+1F60F; smirking face: 😏
  :0      U+1F636; face without mouth: 😶
  :1      U+1F914; thinking face: 🤔
  :2      U+1F92B; shushing face: 🤫
  :3      U+1F617; kissing face: 😗
  :4      U+1F605; grinning face with sweat: 😅
  :5      U+1F972; smiling face with tear: 🥲
  :6      U+1F602; face with tears of joy: 😂
  :7      U+1F917; smiling face with open hands: 🤗
  :8      U+1F910; zipper-mouth face: 🤐
  :9      U+1F923; rolling on the floor laughing: 🤣
  :D      U+1F601; beaming face with smiling eyes: 😁
  :O      U+1F62F; hushed face: 😯
  :P      U+1F61B; face with tongue: 😛
  :S      U+1FAE1; saluting face: 🫡
  :T      U+1F62B; tired face: 😫
  :Y      U+1F971; yawning face: 🥱
  :Z      U+1F634; sleeping face: 😴
  :[      U+1F641; frowning face: 🙁
  :\      U+1F615; confused face: 😕
  :]      U+263A U+FE0F; smiling face: ☺️
  :|      U+1F610; neutral face: 😐
  ;)      U+1F609; winking face: 😉
  <3      U+2764 U+FE0F; red heart: ❤️
  ?       U+2753 U+FE0F; question mark: ❓️
  B)      U+1F60E; smiling face with sunglasses: 😎
  E       U+2130; script capital E: ℰ
  F       U+2131; script capital F: ℱ
  M       U+2133; script capital M: ℳ
  \       U+274C U+FE0F; cross mark: ❌️
  ^       U+26A0 U+FE0F; warning sign: ⚠️
  {!!}    U+203C U+FE0F; double exclamation mark: ‼️
  {!?}    U+2049 U+FE0F; exclamation question mark: ⁉️
  {()}    U+1F534; red circle: 🔴
  {[]}    U+1F7E5; red square: 🟥
  {{}}    U+2B55 U+FE0F; hollow red circle: ⭕️
  |       U+1F346; aubergine: 🍆
  ~       U+3030 U+FE0F; wavy dash: 〰️
```

## Usage hints summary

```text
HINTS:
Whitespace immediately inside parentheses of `@(...)` are ignored.  Whitespace
immediately inside braces of `@{...}` are ignored, unless ... spans multiple
lines.  Use `@{ ... }@` to suppress newline following second `@`.  Simple
expressions ignore trailing punctuation; `@x.` means `@(x).`, not a parse
error.  A `#!` at the start of a file is treated as a comment.
```

## Topic list

```text
TOPICS:
Need more help?  Add more -h options (-hh, -hhh) for more help.  Use -H <topic>
for help on a specific topic, or specify a comma-separated list of topics.  Try
`default` (-h) for default help, `more` (-hh) for more common topics, `all`
(-hhh) for all help topics, or `topics` for this list.  Use -V for version
information, -W for version and system information, or -Z for all debug
details.  Available topics:
  usage       Basic command line usage
  options     Command line options
  markup      Markup syntax
  escapes     Escape sequences
  environ     Environment variables
  pseudo      Pseudomodule attributes and functions
  config      Configuration variable attributes
  methods     Configuration methods
  hooks       Hook methods
  named       Named escapes
  diacritics  Diacritic combiners
  icons       Icons
  hints       Usage hints
  topics      This list of topics
```
