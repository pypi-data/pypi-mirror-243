@%title "User's guide"
@%module 'em'
@{
import glob

import em
import emdoc

info = emdoc.init(empy, __module__)
}@
# @info.ident.title

## Introduction:  Welcome to EmPy!

[@info.ident](@info.ident.url) is a powerful, robust and mature
templating system for inserting Python code in template text.  EmPy
takes a source document, processes it, and produces output.  This is
accomplished via expansions, which are signals to the EmPy system
where to act and are indicated with markup.  Markup is set off by a
customizable prefix (by default the at sign, @`@`).  EmPy can expand
arbitrary Python expressions, statements and control structures in
this way, as well as a variety of additional special forms.  The
remaining textual data is sent to the output, allowing Python to be
used in effect as a markup language.

EmPy also supports hooks, which can intercept and modify the behavior
of a running interpreter; diversions, which allow recording and
playback; filters, which are dynamic and can be chained together; and
a dedicated user-customizable callback markup.  The system is highly
configurable via command line options, configuration files, and
environment variables.  An extensive API is also available for
embedding EmPy functionality in your own Python programs.

EmPy also has a supplemental library for additional non-essential
features (`emlib`), a documentation building library used to create
this documentation (`emdoc`), and an extensive help system (`emhelp`)
which can be queried from the command line with the main executable
`em.py` (@info.option('-h'), @info.option('-H')).  The base EmPy
interpreter can function with only the `em.py`/`em` file/module
available.

EmPy can be used in a variety of roles, including as a templating
system, a text processing system (preprocessing and/or
postprocessing), a simple macro processor, a frontend for a content
management system, annotating documents, for literate programming, as
a souped-up text encoding converter, a text beautifier (with macros
and filters), and many other purposes.


### Markup overview

Expressions are embedded in text with the @`@(...)` notation;
variations include conditional expressions with @`@(...?...!...)`  and
the ability to handle thrown exceptions with @`@(...$...)`.  As a
shortcut, simple variables and expressions can be abbreviated as
@`@variable`, @`@object.attribute`, @`@sequence[index]`,
@`@function(arguments...)`, @`@function{markup}{...}` and
combinations.  Full-fledged statements are embedded with @`@{...}`.
Control flow in terms of conditional or repeated expansion is
available with @`@[...]`.  A @`@` followed by any whitespace character
(including a newline) expands to nothing, allowing string
concatenations and line continuations.  Line comments are indicated
with @`@#` to the end of the line, up to and including the trailing
newline.  @`@* ... *` allows inline comments.  Escapes are indicated
with @`@\...`; diacritics with @`@^...`; icons with @`@|...`; and
emoji with @`@:...:`.  @`@% ...` indicate "significators," which are
distinctive forms of variable assignment intended to specify
per-document identification information in a format easy to parse
externally, _e.g._, to indicate metadata.  In-place expressions are
specified with @`@$...$...$`.  Context name and line number changes
can be done with @`@?` and @`@!`, respectively.  @`@<...>` markup is
customizable by the user and can be used for any desired purpose.  @``
@`...` `` allows literal escaping of any EmPy markup.  And finally, a
@`@@` sequence (the prefix repeated once) expands to a single literal
at sign.

The prefix (which defaults to `@info.config.prefix`) can be changed
with @info.option('--prefix', True).


### Getting the software

The current version of @info.ident is @info.ident.version.

The official URL for this Web site is <@info.ident.url>.

The latest version of the software is available in a tarball here:
<@info.ident.tarball()>.

The software can be installed through PIP via this shell command:

@info.shell{python3 -m pip install @info.ident.program}{...}

For information about upgrading from 3._x_ to 4.0, see
<@info.ident.path{ANNOUNCE.html}>.


### Requirements

EmPy works with any modern version of Python.  Python version 3._x_ is
expected to be the default and all source file references to the
Python interpreter (_e.g._, the bangpath of the .py scripts) use
`python3`.  EmPy also has legacy support for versions of Python going
back all the way to 2.3, with special emphasis on 2.7 regardless of
its end-of-life status.  It has no dependency requirements on any
third-party modules and can run directly off of a stock Python
interpreter.

EmPy will run on any operating system with a full-featured Python
interpreter; this includes, but is probably not limited to, Linux,
Windows, and macOS (Darwin).  Using EmPy requires knowledge of the
[Python language](https://www.python.org/).

EmPy is also compatible with several different Python implementations:

| Implementation | Supported versions | Description |
| --- | --- | --- |
| CPython | 2.3 to 2.7; 3.0 and up | Standard implementation in C |
| PyPy | 2.7; 3.2 and up | Implementation with just-in-time compiler |
| IronPython | 2.7; 3.4 and up | Implementation for .NET CLR and Mono |
| Jython | 2.7 (and up?) | Implementation for JVM |

It's probable that EmPy is compatible with earlier versions than those
listed here (potentially going all the way back to 2.3), but this has
not been tested.

Only a few .py module file(s) are needed to use EmPy; they can be
installed system-wide through a distribution package, a third-party
module/executable, or just dropped into any desired directory in the
`PYTHONPATH`.  A minimal installation need only install the em.py
file, either as an importable module and an executable, or both,
depending on the user's needs.

EmPy also has optional support for several [third-party
modules](#third-party-emoji-modules); see [Emoji
markup](#emoji-markup) for details.

The testing system included (the test.sh script and the tests and
suites directories) is intended to run on Unix-like systems with a
Bourne-like shell (_e.g._, sh, bash, zsh, etc.).  EmPy is routinely
tested with all supported versions of all available interpreters.

If you find an incompatibility with your Python interpreter or
operating system, [let me know](#reporting-bugs).


### License

This software is licensed under
[BSD (3-Clause)](https://opensource.org/licenses/bsd-3-clause/).


## Getting started

This section serves as a quick introduction to the EmPy system.  For
more details and a reference, see the sections below.

:::{hint}

As an introduction to the terminology, the following names are used
throughout:

| Name | Description |
| --- | --- |
| `EmPy` | The name of the software |
| `em.py` | The name of the executable and main source file |
| `em` | The name of the main module |
| `empy` | The name of the [pseudomodule](#pseudomodule-and-interpreter), as well as the PyPI package |
| `.em` | The conventional filename extension for EmPy documents |

:::


### Starting EmPy

After installing EmPy (see [Getting the
software](#getting-the-software)), EmPy is easily invoked by executing
the EmPy interpreter, `em.py`.  If it is invoked without arguments, it
will accept input from `sys.stdin`.  You can use this as an
interactive session to familiarize yourself with EmPy when starting
out:

@info.shell{em.py}{@
... accepts input from stdin and results written to stdout ...
}@

If an EmPy document is specified (which by convention has the
extension .em, though this is not enforced), then that document is
used as input:

@info.shell{em.py document.em}{@
... document.em is processed and results written to stdout ...
}@

:::{warning}

If your document filename begins with a `-`, it will be interpreted as
a command line argument and cause command line option processing
errors.  Either precede it with a relative path (_e.g._, `em.py
./-weirdname.em`) or the GNU-style `--` option which indicates there
are no further options (_e.g._, `em.py -- -weirdname.em`).

:::

Any number of command line arguments (beginning with a `-`) can
precede the document name.  For instance, this command writes its
output to document.out:

@info.shell{em.py -o document.out document.em}{@
... document.em is processed and results written to document.out ...
}@

Many options are available to change the behavior of the EmPy system.
This command will open the input file as UTF-8, write the output file
as Latin-1, show raw errors if they occur, and delete the output file
if an error occurs:

@info.shell{em.py --input-encoding=utf-8 --output-encoding=latin-1 -r -d -o document.out document.em}{@
... you get the idea ...
}@

EmPy documents can also take arguments, which are an arbitrary
sequence of strings that follow after the document, and are analogous
to the Python interpreter arguments `sys.argv`:

@info.shell{em.py document.em run test}{@
... empy.argv is ['document.em', 'run', 'test'] ...
}@

:::{tip}
  
You can create executable EmPy scripts by using a bangpath:
  
```shell
#!/usr/bin/env em.py

... EmPy code here ...
```

By default, bangpaths are treated as EmPy comments unless
@info.option('--no-ignore-bangpaths', True) is specified.

:::

:::{tip}

If you wish to run EmPy under Python 2._x_ for some reason on a system
that also has Python 3 installed, explicitly invoke the Python 2
interpreter before running it (`python2 em.py ...`).  If you wish to
make this more streamlined, edit the first line ("bangpath") of em.py
and change it to read `#!/usr/bin/env python2` (or whatever your
Python 2._x_ interpreter is named).

:::

:::{note}

In some distribution packages, the EmPy interpreter may be named
`empy` rather than `em.py`.  In the [official release
tarballs](#getting-the-software), and throughout this documentation,
it is `em.py`.  This is to distinguish it from the pseudomodule
`empy`.

:::

:::{seealso}

See the [Command line options section](#command-line-options) for a
list of command line options that EmPy supports.

:::


### The prefix and markup expansion

EmPy markup is indicated with a configurable prefix, which is by
default the at sign (@`@`).  The character (Unicode code point)
following the prefix indicates what type of markup it is.  There are a
wide variety of markups available, from comments to expression
evaluation to statement execution, and from prefixes, literals and
escapes to diacritics, icons and emojis.  Here is a long EmPy code
sample illustrating some of the more essential markups in EmPy, though
there are several not shown here:

@<<<[Markup sample]
Comments:
The line below will not render.
@# This is a line comment, up to and including the newline.
If a line comment appears in the middle of a line, @# this is a comment!
the line will be continued.
Inline comments can be @*placed inline* (this phrase did not render, 
but note the double space due to the spaces before and after it).
@**
  * Or it can span multiple lines.
  **@
Whitespace markup consumes the following space.
So two@ words becomes one word.
And this @
is a line continuation.
@* Inline comments can be used as a line comment. *@
Note the use of the trailing prefix to consume the final newline; this 
is a common idiom.

Literals:
Double the prefix to render it: @@.
String literals can be used to render escaped Python strings: @
@"A is also \N{LATIN CAPITAL LETTER A}".
Escape markup can render arbitrary characters:
These are all Latin capital letter A: @
A, @\B{1000001}, @\q1001, @\o101, @\x41, @\u0041, @\U00000041, @\N{LATIN CAPITAL LETTER A}.
Backquotes can be used to escape EmPy markup.
This is not evaluated: @`@(!@#$%^&*()`.

Expressions:
Python expressions can be evaluated like this: 1 + 2 = @(1 + 2).
Expressions can be arbitrary complex: @
This is Python @('.'.join(str(x) for x in __import__('sys').version_info[:3])).
Expressions can contain builtin ternary operators:
Seven is an @(7 % 2 == 0 ? 'even' ! 'odd') number.
They can even handle exceptions: @
Division by zero is @(1/0 $ 'illegal').

Statements:
@{
print("Hello, world!")
x = 123
}@
x is now @(x), which can be simplified to @x.
Statements can execute arbitrarily complex Python code,
including defining functions and classes.

Back to expressions, they can be simplified:
@{
# Define some variables.
class Person:

    def __init__(self, name):
        self.name = name

a = [4, 5, 6]
p = Person('Fred')
}@
x is @x.
a[1] is @a[1].
The name of p is @p.name.
You can even call functions this way:
p's name when shouted is @p.name.upper().
Note that the parser does not try to evaluate end-of-sentence punctuation.

Control structures:
Iterate over some numbers and classify them, but stop after 5:
@[for n in range(-1, 10)]@
@[if n > 5]@
And done.
@[break]@
@[end if]@
@n is @
@[if n < 0]@
negative@
@[elif n == 0]@
zero@
@[elif n % 2 == 0]@
even@
@[else]@# odd
odd@
@[end if]@
.
@[end for]@
Note the use of whitespace markup (a prefix with trailing 
whitespace is consumed) to make things more clear.

You can even define your own EmPy functions:
@[def officer(name, species, rank, role)]@
@# The definition is EmPy, not Python!
@name (@species, @rank, @role)@
@[end def]@
Some of the bridge crew of the USS Enterprise (NCC-1701):
- @officer("James T. Kirk", "Human", "captain", "commanding officer")
- @officer("Spock", "Vulcan-Human hybrid", "commander", "science officer")
- @officer("Montgomery Scott", "Human", "commander", "chief engineer")
- @officer("Nyota Uhura", "Human", "lieutenant commander", "communications officer")
- @officer("Hikaru Sulu", "Human", "commander", "astrosciences/helmsman")

Diacritics: Libert@^e', égalit@^e', fraternit@^e'!
Icons for curly quotes: @|"(these are curly quotes.@|")
This is an emoji: @:pile of poo:.  (Of course I would choose that one.)
>>>

:::{tip}

If you wish to change the prefix, use @info.option('-p', True).

:::

:::{seealso}

See the [Markup section](#markup) for detailed specifications on all
support EmPy markup.

:::


### Pseudomodule and interpreter

The interpreter instance is available to a running EmPy system through
the globals; by default, it is named
`@info.config.pseudomoduleName`.  When it is referenced this
way, it is called a pseudomodule (since it acts like a module but it
is not actually a module you can import):

@<<<[Pseudomodule sample]
This version of EmPy is @empy.version.
The prefix in this interpreter is @empy.getPrefix() @
and the pseudomodule name is @empy.config.pseudomoduleName.
Do an explicit write: @empy.write("Hello, world!").
The context is currently @empy.getContext().
Adding a new global in a weird way: @empy.updateGlobals({'q': 789})@
Now q is @q!
You can do explicit expansions: @empy.expand("1 + 1 = @(1 + 1)").
q is @(empy.defined('q') ? 'defined' ! 'undefined').
>>>

:::{seealso}

See the [Pseudomodule/interpreter section](#pseudomodule-interpreter)
for details on the pseudomodule/interpreter.

:::


### Diversions, filters & hooks

Diversions can defer and replay output at a desired time:

@<<<[Diversions sample]
This text is output normally.
@empy.startDiversion('A')@
(This text was diverted!)
@empy.stopDiverting()@
This text is back to being output normally.
Now playing the diversion:
@empy.playDiversion('A')@
And now back to normal output.
>>>

Filters can modify output before sending it to the final stream:

@<<<[Filters sample]
@{
# For access to the filter classes.

import emlib
}@
This text is normal.
@empy.appendFilter(emlib.FunctionFilter(lambda x: x.upper()))@
This text is in all uppercase!
@empy.appendFilter(emlib.FunctionFilter(lambda x: '[' + x + ']'))@
Now it's also surrounded by brackets!
(Note the brackets are around output as parsed, 
not at the beginning and end of each line.)
@empy.resetFilter()@
Now it's back to normal.
>>>

Hooks can intercept and even alter the behavior of a running system:

@<<<[Hooks sample]
@# Modify the backquote markup to prepend and append backquotes
@# (say, for a document rendering system, cough cough).
@{
import emlib

class BackquoteHook(emlib.Hook):

    def __init__(self, interp):
        self.interp = interp
    
    def preBackquote(self, literal):
        self.interp.write('`' + literal + '`')
        return True # return true to skip the standard behavior

empy.addHook(BackquoteHook(empy))
}@
Now backquote markup will render with backquotes: @
@`this is now in backquotes`!
>>>

:::{seealso}

See the [Diversions section](#diversions), [Filters
section](#filters), or the [Hooks section](#hooks) for more
information.

:::


### Embedding

EmPy is modular and can be embedded in your Python programmers, rather
than running it standalone.  Simply import the `em` module and create
an `Interpreter`:

```python
import sys

import em

config = em.Configuration(...)
output = sys.stdout
with em.Interpreter(config=config, output=output) as interp:
    ... do things with interp ...
```

For one-off uses, you can use the `em.expand` function:

```python
import em

result = em.expand(source)
```

:::{important}

When you create an interpreter, you must call its `shutdown` method
when you are done.  This can be accomplished by creating the
interpreter in a `with` statement -- interpreters are also context
managers -- or by creating it and shutting it down in a
`try`/`finally` statement.

:::

:::{seealso}

See the [Embedding EmPy section](#embedding-empy) section for more
details on embedding EmPy in your Python programs.

:::


### Getting help

For basic help, use the @info.option('-h') option:

@info.execute(['em.py', '-h', '# or: --help'], lines=9)@

For more help, repeat the @info.option('-h') option (up to three times
for the full help).  For help on a particular topic, use the
@info.option('-H') option, where `TOPICS` is a comma-separated list of
topics.  The list of available topics can be shown by using the topic
`topics`:

@info.execute(['em.py', '-H', 'topics', '# or: --topics=topics'])@

:::{tip}

Repeating the help option once (`-hh`) is the same as requesting the
`more` topic (`-H more`).  Repeating it three times (`-hhh`) is the
same as requesting the `all` topic (`-H all`).

:::

:::{warning}

The builtin help system requires the presence of the `emhelp` module.
If you have a minimal EmPy installation, this module may not be
available.  You can get it from the [release
tarball](#getting-the-software).

:::

:::{seealso}

See the rest of this document for details and specifications on all
the markup and features, and see the [Help topics
section](#help-topics) for the output of all the builtin help topics.

:::


## Markup

EmPy markup always begins with the EmPy prefix, which defaults to
@`@`.  The character (Unicode code point) following the prefix
indicates what type of markup it is, and the different types of markup
are parsed differently.

It is legal to set the EmPy prefix to `None`; then, no markup will be
parsed or expanded and EmPy will merely process filters and encoding
conversions.  This can be done from the command line with the
@info.option('--no-prefix') option, or by indicating a prefix that is an
empty string (`''`) or the word `none`.

Using a non-default prefix that is also the first character of an
existing markup will swap that markup character with the default.  For
example, setting the prefix to `$` would otherwise collide with the
in-place token (@`@$ ... $ ... $` with a default prefix).  On startup
it will be adjusted so that with a `$` prefix the in-place markup can
be accessed as @`$@ ... @ ... @`.

The following subsections list the types of markup supported by EmPy
and in which version they were introduced, organized by category.

:::{important}

All of the following code snippets and examples below assume that the
prefix is the default, @`@`.  It can be changed with
@info.option('-p', True).

:::

| Markup | Syntax | Description | Ver. |
| --- | --- | --- | --- |
| [Line comment](#line-comment-markup) | @`@# ... NL` | Consumes text up to and including newline | 1.0 |
| [Inline comment](#inline-comment-markup) | @`@* ... *` | Consumes text up to and including the final asterisk(s) | 4.0 |
| [Whitespace](#whitespace-markup) | @`@ WS` | Consumes the following whitespace character | 1.0 |
| [Prefix](#prefix-markup) | @`@@` | Produces the prefix character | 1.0 |
| [String](#string-markup) | @`@'...'`, @`@"..."`, @`@'''...'''`, @`@"""..."""` | Produces a string from a literal | 3.1.1 |
| [Backquote](#backquote-markup) | @`` @` ... ` `` | Quotes contained markup up to final backquote(s) | 4.0 |
| [Escape](#escape-markup) | @`@\...` | Render an escape character | 1.5 |
| [Named escape](#named-escape-markup) | @`@\^{...}` | Render an escape control character by name | 4.0 |
| [Expression](#expression-markup) | @`@( ... )` | Evaluates an expression | 1.0 |
| [Simple expression](#simple-expression-markup) | @`@variable`, @`@object.attribute`, @`@array[index]`, @`@function(args...)`, etc. | Evaluates a simple expression | 1.0 |
| [Functional expression](#functional-expression-markup) | @`@function{...}` | Evaluates a functional expression | 4.0 |
| [Extended expression](#extended-expression-markup) | @`@( ... ? ... ! ... $ ... )` | Expression evaluation with if-else-finally | 3.0 |
| [In-place expression](#in-place-expression-markup) | @`@$ ... $ ... $` | Copies and evaluates an expression | 1.4 |
| [Statement](#statement-markup) | @`@{ ... }` | Executes a statement or statements | 1.0 |
| [If control](#if-control-markup) | @`@[if C]`@:...:@`@[elif C]`@:...:@`@[else]`@:...:@`@[end if]` | Branching control structure | 3.0 |
| [Break control](#break-and-continue-control-markup) | @`@[break]` | Break out of repeating control structure | 3.0 |
| [Continue control](#break-and-continue-control-markup) | @`@[continue]` | Continue with next iteration of repeating structure | 3.0 |
| [For control](#for-control-markup) | @`@[for N in E]`@:...:@`@[else]`@:...:@`@[end for]` | Iterating control structure | 3.0 |
| [While control](#while-control-markup) | @`@[while E]`@:...:@`@[else]`@:...:@`@[end while]` | Looping control structure | 3.0 |
| [Dowhile control](#dowhile-control-markup) | @`@[dowhile E]`@:...:@`@[else]`@:...:@`@[end dowhile]` | Do/while analog control structure from C, C++ | 4.0 |
| [Try control](#try-control-markup) | @`@[try]`@:...:@`@[except E as N]`@:...:@`@[else]`@:...:@`@[finally]`@:...:@`@[end try]` | Exception handling control markup | 3.0 |
| [With control](#with-control-markup) | @`@[with E as N]`@:...:@`@[end with]` | Handle a context manager | 4.0 |
| [Defined control](#defined-control-markup) | @`@[defined N]`@:...:@`@[else]`@:...:@`@[end defined]` | Branch on whether a variable is defined | 4.0 |
| [Def control](#def-control-markup) | @`@[def F(...)]`@:...:@`@[end def]` | Define an EmPy function | 3.0 |
| [Diacritic](#diacritic-markup) | @`@^...` | Normalize and render a diacritic | 4.0 |
| [Icon](#icon-markup) | @`@\|...` | Render a customizable icon | 4.0 |
| [Emoji](#emoji-markup) | @`@:...:` | Render a customizable emoji | 4.0 |
| [Significator](#significator-markup) | @`@%[!] ... NL`, @`@%%[!] ... %% NL` | Declare a significator | 1.2 |
| [Context name](#context-name-markup) | @`@?... NL` | Set the context filename | 3.0.2 |
| [Context line](#context-line-markup) | @`@!... NL` | Set the context line | 3.0.2 |
| [Custom](#custom-markup) | @`@< ... >` | Fully-customizable markup with no set definition | 3.3 |

:::{seealso}

The list of supported markup is available in the `markup` help topic
and is summarized [here](@info.ident.path{HELP.html#markup-summary}).

:::


### Comments

Comment markup consumes its contents and performs no output.  A few
variants of comment markup are available.


#### Line comment markup: @`@# ... NL`

**Line comment markup** consists of a starting @`@#` and consumes up
until (and including) the following newline.  Note that if the markup
appears in the middle of a line, that line will be continued since it
consumes the ending newline.

@<<<[Line comments]
@# This is a comment.  It will not render in the output.
@# Even would-be EmPy markup is consumed by a comment: @(!@#$%^&*()
Welcome to EmPy!
Here's some text @# This will consume the rest of the line
on the same line.
>>>

:::{note}

Line comment markup was introduced in EmPy version 1.0.

:::


#### Inline comment markup: @`@* ... *`

**Inline comment markup** (@`@* ... *`) is a form of comment markup
that can appear anywhere in text and can even span multiple lines.  It
consumes everything up to and including the final asterisk(s).

@<<<[Inline comments, basic]
This is text.  @* This is a comment in the text. *  This is continuing text.
(Note the extra spaces around where the comment was.)
@* A trailing whitespace markup consumes the whole line. *@
There is no extraneous blank line here.
>>>

Multiple asterisks can be used as long as they are matched with the
end of the markup.  This allows asterisks to appear in the comment:

@<<<[Inline comments, advanced]
@** Here's an asterisk inside the comment: * **@
@*** There can * be any number of asterisks ** as
     long as it's * less than ** the delimiters. ***@
@**
  * This is a multiline inline comment.
  **@
@*************************************
 * This comment thinks it's so cool. *
 *************************************@
So many comments!
>>>

@empy.startDiversion('idiom')@
:::{attention}

Note that when markup which has starting and ending delimiters appears
alone on a line, the trailing newline will be rendered in the output.
To avoid these extra newlines, use a trailing @`@` to turn it into
whitespace markup which consumes that trailing newline, so _e.g._ @`@{
... }` followed by a newline becomes @`@{ ... }@` followed by a
newline.  This is idiomatic for suppressing unwanted newlines.  See
[here](#idiom) for more details.

:::
@empy.stopDiverting()@
@empy.replayDiversion('idiom')@

:::{note}

Inline comment markup was introduced in EmPy version 4.0.

:::


#### Whitespace markup: @`@ WS`

While not quite a comment, **whitespace markup** is sufficiently
common and useful that it warrants introduction early on.  The
interpreter prefix followed by any whitespace character, including a
newline, is consumed.  This allows a way to concatenate two strings,
create a line continuation, or create a line separator:

@<<<[Whitespace, basic]
This was two@ words.  Now it is one.
Note that this consumes the newline @
so that this is on the same line.
@
Note there is no blank line above.
>>>

::::{tip}

{#idiom}
A trailing prefix after markup which has beginning and ending
delimiters -- for instance, inline comment (@`@* ... *`), expression
(@`@( ... )`), statement (@`@{ ... }`), control (@`@[ ... ]`), and
custom (@`@< ... >`) -- is idiomatic for suppressing the newline when
there is nothing at the end of the line after the markup.  The
trailing prefix will consume the final newline, eliminating unwanted
newlines.

For example, using a statement markup (see below) on a whole line will
result in a seemingly spurious newline:

@<<<[Whitespace, idiom]
Statement markup:
@{x = 123}
Note there's an extra newline above from the EmPy code after the
statement markup.  The markup itself doesn't print anything; it's from
the trailing newline after the markup.

To suppress the extra newline:
@{x = 456}@
The trailing prefix above consumes the trailing newline, eliminating it.
>>>

::::

:::{note}

Whitespace markup was introduced in EmPy version 1.0.

:::

### Literals

**Literals** are a category of markup that evaluate to some form of
themselves.


#### Prefix markup: @`@@`

To render the **prefix** character literally in the output, duplicate
it.  For the default, @`@`, it will be @`@@`:

@<<<[Prefix literals]
This becomes a single at sign: @@.
>>>

:::{tip}

The prefix markup is not indicated by the prefix followed by an at
sign, but rather the prefix repeated twice.  So if the prefix has been
changed to `$`, the prefix markup is `$$`, not @`$@`.

:::

:::{note}

Prefix markup was introduced in EmPy version 1.0.

:::

#### String markup: @`@'...'`, @`@"..."`, @`@'''...'''`, @`@"""..."""`

The interpreter prefix followed by a Python **string** literal
(_e.g._, @`@'...'`) evaluates the Python string literal and expands
it.  All variants of string literals with single and double quotes, as
well as triple quoted string literals (with both variants) are
supported.  This can be useful when you want to use Python string
escapes (not EmPy escapes) in a compact form:

@<<<[String]
This is a string: @'A single-quoted string'.
This is also a string: @"A double-quoted string".
This is another string: @'''A triple single-quoted string'''.
This is yet another string: @"""A triple double-quoted string""".
This is a multiline string: @"""Triple quotes containing newlines
will be preserved."""
This is a string using escapes: @
@'Welcome to \U0001d53c\U0001d55e\u2119\U0001d56a!'.
>>>

:::{note}

String markup was introduced in EmPy version 3.1.1.

:::


#### Backquote markup: @`` @` ... ` ``

**Backquote** markup (@`` @` ... ` ``) can be used to escape any text,
including EmPy markup.  Multiple opening backquotes can be used as
long as they are matched by an equal number in order to allow quoting
text which itself has backquotes in it:

@<<<[Backquote]
This is literal text: @`some text`.
This is a prefix: @`@`.
This would be expanded if it were not backquoted: @`@(1 + 1)`.
This would be an error if expanded: @`@(!@#$%^&*())`.
This contains backquotes: @```here's one: ` and here's two: `` ```.
>>>

:::{warning}

To use the backquote markup with content containing backquotes which
are adjacent to the start or end markup, you need to pad it with
spaces.  So when quoting a single backquote, it needs to be written as
@```@`` ` `` ```.  This also means you cannot use backquote markup to
specify a completely empty string.  It must always contain at least
one non-backquote character, e.g., @`` @` ` ``.  If you really need
backquotes without whitespace padding, you can use a [hook](#hooks) to
intercept the backquote markup and strip it out.

:::

@empy.replayDiversion('idiom')@

:::{note}

Backquote markup was introduced in EmPy version 4.0.

:::


### Escape markup: @`@\...`

**Escape markup** allows specifying individual non-printable
characters with a special readable syntax: @`@\...`.  It is inspired
by and extends the string literal escape codes from languages such as
C/C++ and Python.

@<<<[Escapes]
@# These are all a Latin uppercase A:
Binary: @\B{1000001}
Quaternary: @\q1001, @\Q{1001}
Octal: @\o101, @\O{101}
Hexadecimal (variable bytes): @\X{41}
Hexadecimal (one-byte): @\x41
Hexadecimal (two-byte): @\u0041
Hexadecimal (eight-byte): @\U00000041
By Unicode name: @\N{LATIN CAPITAL LETTER A}
>>>

The escape sequence type is indicated by the first character and then
consumes zero or more characters afterward, depending on the escape
sequence.  Some sequence sequences support a variable number of
characters, delimited by curly braces (`{...}`).

:::{seealso}

The list of all valid escape sequences is available in the `escapes`
help topic and is summarized
[here](@info.ident.path{HELP.html#escape-sequences-summary}).

:::

:::{note}

Escape markup was introduced in EmPy version 1.5, and then reworked in
EmPy version 4.0.

:::


#### Named escape markup: @`@\^{...}`

The escape control markup @`@\^...` has an extended usage where the
character can be specified by a control code name.  The resulting
**named escape markup** takes the form of @`@\^{...}` with the escape
code name between the curly braces.  The name of the escape code used
in the markup is case insensitive.

The mapping of escape names to characters is specified in the
configuration variable @info.variable('controls').  The keys of this
dictionary must be in uppercase and the values can be integers
(Unicode code point values), lists of integers, or strings.  They can
also take the form of a 2-tuple, where the first element is one of the
above values and the second element is a description string used for
displaying in help topics.

@<<<[Named escapes]
Normal space: [ ]
Normal space by name: [@\^{SP}]
No-break space: [@\^{NBSP}]
Thin space: [@\^{THSP}]
En space: [@\^{ENSP}]
Em space: [@\^{EMSP}]
(Well, these would look right if it this were in a proportional font.)
>>>

:::{seealso}

The list of all valid control code names is available in the
`controls` help topic and is summarized
[here](@info.ident.path{HELP.html#named-escapes-summary}).

:::

:::{note}

Named escape markup was introduced in EmPy version 4.0.

:::


### Expression markup: @`@( ... )`

EmPy mainly processes markups by evaluating expressions and executing
statements.  Expressions are bits of Python code that return a value;
that value is then rendered into the output stream.  Simple examples
of Python expressions are `1 + 2`, `abs(-2)`, or `"test"*3`.

In EmPy, expressions are evaluated and expanded with the **expression
markup** @`@( ... )`.  By default, an expression that evaluates to
`None` does not print anything to the underlying output stream; it is
equivalent to it having returned `''`.

:::{tip}

If you want to change this behavior, specify your preferred value with
@info.option('--none-symbol', True).

:::

@<<<[Expressions]
The sum of 1 and 2 is @(1 + 2).
The square of 3 is @(3**2).
The absolute value of -12 is @(abs(-12)).
This prints "test" but does not print None: @(print("test", end='')).
This, however, does: @(repr(None)).
>>>

@empy.replayDiversion('idiom')@

:::{note}

Expression markup was introduced in EmPy version 1.0.

:::

### Additional expression markup

Several expression markup variants are available.

#### Simple expression markup: @`@variable`, _etc._

Often expressions are "simple" and unambiguous enough that needing to
use the full @`@( ... )` syntax is unnecessary.  In cases where a
single variable is being referenced unambiguously, the parentheses can
be left off to create **simple expression markup**:

@<<<[Simple expressions, basic]
@# Set a variable to use.
@{x = 16309}@
The value of x is @x.
>>>

@`@x` is precisely the same thing as @`@(x)`.  Attribute references
(@`@x.y`), indexing (@`@x[y]`), and function calls (@`@x(y, ...)`) can
also be simplified in this way.  They can also be chained together
arbitrarily, so @`@object.attribute.subattribute`,
@`@object.method(argument...)`, @`@object[index].attribute`, and
@`@object[index].method(argument...)` are all valid examples of simple
expression markup.  These simple expressions can be extended
arbitrarily.

@<<<[Simple expressions, chaining]
@# Define some variables to use.
@{
import time

def mean(seq): # a function
    return sum(seq)/len(seq)

class Person: # a class

    def __init__(self, name, birth, scores):
        self.name = name
        self.birth = birth
        self.scores = scores

    def age(self):
        current = time.localtime(time.time()).tm_year
        return current - self.birth

person = Person("Fred", 1984, [80, 100, 70, 90]) # an instance of that class
}@
The name of person is @(person.name), or more simply @person.name.
The first letter is @(person.name[0]), or more simply @person.name[0].
He has @(len(person.scores)) scores, or more simply @len(person.scores).
His first score is @(person.scores[0]), or more simply @person.scores[0].
His average score is @(mean(person.scores)), or more simply @mean(person.scores).
His age is @(person.age()), or more simply @person.age().
>>>

:::{note}

Final punctuation which is a period (`.`) is not interpreted as an
attribute reference and thus does not result in a parse error.  Thus
you can use end-of-sentence punctuation naturally after a simple
expression markup.

:::

If you wish to concatenate an expression with immediately following
text so that it will not be parsed incorrectly, either use whitespace
markup or just fall back to a full expression markup:

@<<<[Simple expressions, concatenation]
@# Define a variable for use.
@{thing = 'cat'}@
@# Referencing `@things` to pluralize `@thing` will not work.  But:
The plural of @thing is @(thing)s.
Or:  The plural of @thing is @thing@ s.
>>>

:::{note}

Simple expression markup was introduced in EmPy version 1.0.

:::


##### Functional expression markup: @`@function{markup...}`

Arguments to function calls in EmPy expression markups use Python
expressions, not EmPy markup (_e.g._, @`@f(x)` calls the function `f`
with the variable `x`).  To specify EmPy markup which is expanded and
then passed in to the function, there is **functional expression
markup** as an extension of simple expression markup.  Since each
argument to the function is expanded, the arguments are always
strings:

@<<<[Functional expressions, one argument]
@{
def f(x):
    return '[' + x + ']'
}@
@# Note that the argument is expanded before being passed to the function:
This will be in brackets: @f{1 + 1 is @(1 + 1)}.
>>>

Functional expressions support the application of multiple arguments
by repeating the `{...}` suffix for as many arguments as is desired:

@<<<[Functional expressions, multiple arguments]
@{
def f(x, y, z):
    return x.lower() + ', ' + y.upper() + ', ' + z.capitalize()
}@
@# Multiple arguments are possible by repeating the pattern:
These expansions are separated by commas: @
@f{lowercase: @(1)}{uppercase: @(1 + 1)}{capitalized: @(1 + 1 + 1)}.
>>>

:::{warning}

Functional expression markup is an extension of simple expression
markup so cannot be surrounded in parentheses.  Further, it cannot be
seemlessly combined with normal function call, so @`@f(1){a}{b}` is
equivalent to @`@(f(1)('a', 'b'))`, not @`@(f(1, 'a', 'b'))`.
Functional argument calls will end simple expression, so
@`@f{a}{b}(3)` is the same as @`@(f('a', 'b'))(3)`, not @`@f('a', 'b',
3)`; that is, trailing function calls are not applied.

:::

:::{note}

Functional expression markup was introduced in EmPy version 4.0.

:::


#### Extended expression markup: @`@( ... ? ... ! ... $ ... )`

Expression markup has an **extended expression markup** form which
allows more powerful manipulation of expressions.

The first form allows for a compact form of an @`@[if]` statement with
a ternary operator, similar to C/C++'s `?` and `:` operators.  In
EmPy, however, these are represented with `?` and `!`, respectively.

:::{note}

C/C++'s use of `:` was changed to `!` for EmPy since `:` already has
special meaning in Python.  This syntax was originally added before
Python supported the `if/else` ternary expression, although EmPy's
syntax is more general and powerful.

:::

If a `?` is present in the expression, then the Python (not EmPy)
expression before the `?` is tested; if it is true, then the Python
expression following it is evaluated.  If a `!` is present afterward
and the originally expression was false, then the Python expression
following it is expanded (otherwise, nothing is).  It thus acts as an
if-then-else construct:

@<<<[Extended expressions, if-else]
Four is an @(4 % 2 == 0 ? 'even' ! 'odd') number.
Seven is an @(7 % 2 == 0 ? 'even' ! 'odd') number.
@# Whitespace is not required:
Eleven is an @(11 % 2 == 0?'even'!'odd') number.
>>>

These `?` and `!` sequences can be repeated indefinitely, forming an
if-else chain, with the last `!` expression serving as the conditional
test for the next `?`:

@<<<[Extended expressions, chained if-else]
@# Define a variable for use.
@{x = 3}@
x is @(x == 1 ? 'one' ! x == 2 ? 'two' ! x == 3 ? 'three' ! x == 4 ? 'four').
>>>

Finally, a `$` present at the end of any if-else chain represents an
except Python (not EmPy) expression: If the main expression throws an
exception, swallow it and evaluate the except expression instead.
This can be combined with the chained if-else notation:

@<<<[Extended expressions, except]
No exception:  2 + 2 = @(2 + 2 $ 'oops').
Division by zero is @(1/0 $ 'illegal').
Two divided by zero is @(2/0 % 2 == 0 ? 'even' ! 'odd' $ 'also illegal').
>>>

@empy.replayDiversion('idiom')@

:::{note}

Extended expression markup was introduced in EmPy version 3.0, and was
expanded to support if-else chaining in 4.0.

:::


### In-place expression markup: @`@$ ... $ ... $`

Occasionally it's desirable to designate an expression that will be
evaluated alongside its evaluation which may change, but which will be
re-evaluated with subsequent updates, or identify exactly what is
being evaluated at the same time.  This is similar to the notion of
CVS or SVN keywords such as `$Date ...$`.  For this, there is
**in-place expression markup** (@`@$ ... $ ... $`).  They consist of two
segments: first, the Python (not EmPy) expression to evaluate, and the
second, the result of that evaluation.  When evaluating the markup,
the second (result) section is ignored and replaced with the
evaluation of the first and a new in-place markup is rendered.  For
example:

@<<<[In-place expressions]
This could be a code comment indicating the version of EmPy:
# @$empy.version$this text is replaced with the result$
Arbitrary Python expressions can be evaluated:
# @$__import__('time').asctime()$$
>>>

:::{note}

The `$` character is a common choice for an alternate prefix.  If it
is chosen instead of the default @`@`, the in-place expression markup
will be remapped to have the form @`$@ ... @ ... @`; that is, the @`@`
and `$` are swapped.  (This is done automatically for any prefix
collision with a markup indicator.)

:::

:::{note}

In-place markup was introduced in EmPy version 1.4.

:::


### Statement markup: @`@{ ... }`

Again, EmPy mainly processes markups by evaluating expressions and
executing statements.  Statements include assignments, control
structures (`if`, `for`, function and class definitions, etc.)
Statements do not yield a value; they are used for side effects,
whether that's changing the state of the interpreter (setting or
changing variables, defining objects, calling functions, etc.) or
printing output.  Statements can also consist of expressions, so an
expression (such as `print("Hello, world!")`) can be used solely for
its side effects with the statement markup.  **Statement markup** sets
off a series of statements to be executed inside the @`@{ ... }`
markup.  Since statements do not yield a value, they are executed but
the markup itself does not implicitly write anything.  Since the
executed statements are Python, they must be formatted and indented
according to Python's parsing rules:

@<<<[Statements]
@# Note the use of whitespace markup below to consume trailing newlines.
@{x = 16309}@
x is now @x.
@{
if x > 0:
    category = 'positive'
else:
    category = 'non-positive'
}@
x is @category.
@{
# Since statement markup does not write anything itself, this
# statement has no effect.
x + 123
}@
>>>

@empy.replayDiversion('idiom')@

:::{note}

Simple expression markup was introduced in EmPy version 1.0.

:::


### Control markup: @`@[ ... ]`

EmPy supports a variety of control structures, analogous to the
builtin Python control structures (`if`, `while`, `for`, etc.), with
some additional markups for convenience.  This is done with **control
markup** indicated by @`@[ ... ]`.

Since EmPy cannot rely on source indentation to delimit control
structure syntax, all primary control markups must end with an
explicit `end` markup (_e.g._, @`@[if ...]...@[end if]`).  The clauses
surrounded by control markup are EmPy (Python) markup and are expanded
according to the logic of each control markup; see below.

Unlike the Python control structures, the code that is expanded within
each subclause is EmPy code, not Python code.  Thus, controls markups
can be nested arbitrarily (_e.g._, @`@[for ...]@[if ...]...@[end
if]@[end for]`).

::::{attention}

To use nested control markup that spans multiple lines and is more
readable, you can rely on whitespace markup to console the newline
after a control markup.  As an example:

@<<<[Controls, idiom]
@# Note the user of whitespace markup to consume the trailing newlines.
Counting:
@[for i, x in enumerate(range(0, 5))]@
@x is @
@[if x % 2 == 0]@
even@
@[else]@
odd@
@[end if]@
.
@[end for]@
>>>

This method of writing organizing control markup with @`@[ ... ]@` all
on a single line for clarity is idiomatic EmPy.  (This applies to all
markup with starting and ending delimiters.)  See [here](#idiom) for
more details.

::::

:::{note}

Control markups were introduced in EmPy version 3.0 unless otherwise
noted below.

:::


#### If control markup: @`@[if E]...@[end if]`

The simplest control markup is the **if control markup**.  It
precisely mimics the Python `if` branching control structure.  The
test expressions are Python expressions.  Like the native Python
control structure, it takes on the following forms:

- @`@[if E]...@[end if]`
- @`@[if E]...@[else]...@[end if]`
- @`@[if E]...@[elif E2]...@[end if]`
- @`@[if E]...@[elif E2]...@[else]...@[end if]`
- @`@[if E]...@[elif E2]... ... @[else]...@[end if]`

Thus, as with the builtin Python `if` control structure, zero or more
@`@[elif]` clauses can be used and the @`@[else]` clause (only valid
at the end of the chain) is optional.  If there is no @`@[else]`
clause and all the test expressions are false, nothing will be
expanded.

@<<<[If controls]
@{
def even(x):
    return x % 2 == 0
}@
0 is @[if even(0)]even@[end if].
1 is @[if even(1)]even@[else]odd@[end if].
2 is @[if even(2)]even@[else]odd@[end if].
3 is @[if even(3)]even@[elif not even(3)]not even@[end if].
4 is @[if 0 == 1]wrong@[elif 1 == 2]wrong@[else]fine@[end if].
>>>


##### Break and continue control markup: @`@[break]`, @`@[continue]`

The looping control markup structures below (@`@[for]`, @`@[while]`,
and @`@[dowhile]`) all support **break** and **continue control
markup**.  These markups follow the native Python forms; @`@[break]`
will exit out of the innermost looping control structure, and
@`@[continue]` will restart the innermost looping control structure.

They take the following forms:

- @`@[break]`
- @`@[continue]`

The following is an example using a @`@[while]` loop:

@<<<[Continue controls]
@# Print even numbers.
@[for n in range(10)]@
@[if n % 2 != 0]@
@[continue]@
@[end if]@
@n is even.
@[end for]@
>>>

@<<<[Break controls]
@# Print numbers up to (but not including) 5.
@[for n in range(10)]@
@[if n >= 5]@
@[break]@
@[end if]@
@n is less than 5.
@[end for]@
>>>


#### For control markup: @`@[for N in E]...@[end for]`

A basic iteration markup is the **for control markup**.  It precisely
mimics the Python `for` looping control structure.  The iterator
expression is a Python expression.  Like the native Python control
structure, it takes on the following forms:

- @`@[for N in E]...@[end for]`
- @`@[for N in E]...@[else]...@[end for]`

As with the native Python control structure, an @`@[else]` clause is
supported; this is expanded if the loop exits without an intervening
break.

@<<<[For controls]
@[for x in range(1, 6)]@
@x squared is @(x*x).
@[else]@
... and done.
@[end for]@
>>>


#### While control markup: @`@[while E]...@[end while]`

The most general looping markup is the **while control markup**.  It
precisely mimics the Python `while` looping control structure.  The
test expression is a python expression.  Like the native Python
control structure, it takes on the following forms:

- @`@[while E]...@[end while]`
- @`@[while E]...@[else]...@[end while]`

As with the native Python control structure, an @`@[else]` clause is
supported; this is invoked if the loop exits without an intervening
break.

@<<<[While controls]
@{a = 1}@
@[while a <= 5]@
@a pound signs: @('#'*a).
@{a += 1}@
@[else]@
... and done.
@[end while]@
>>>


#### Dowhile control markup: @`@[dowhile E]...@[end dowhile]`

An alternate `while` control structure is provided by EmPy: **dowhile
control markup**.  This differs from the standard `while` markup only
in that the loop is always entered at least once; that is, the test
expression is not checked before the first iteration.  In this way, it
is similar to the `do ... while` control structure from C/C++.  It
takes the following forms:

- @`@[dowhile E]...@[end dowhile]`
- @`@[dowhile E]...@[else]...@[end dowhile]`

Like the native Python `while` control structure, an @`@[else]` clause
is supported; this is invoked if the loop exits without an intervening
break.

@<<<[Dowhile controls]
@# Stop when divisible by 5, but include 0 since it's the first iteration:
@{n = 0}@
@[dowhile n % 5 != 0]@
@n works@[if n % 5 == 0] (even though it's divisible by 5)@[end if].
@{n += 1}@
@[else]@
... and done.
@[end dowhile]@
>>>

:::{note}

Dowhile control markup was introduced in EmPy version 4.0.

:::


#### Try control markup: @`@[try]...@[end try]`

**Try control markup** is the EmPy equivalent of a `try` statement.
As with the native Python statement, this markup can take on the
widest variety of forms.  They are:

- @`@[try]...@[except]...@[end try]`
- @`@[try]...@[except C]...@[end try]`
- @`@[try]...@[except C as N]...@[end try]`
- @`@[try]...@[except C, N]...@[end try]`
- @`@[try]...@[except (C1, C2, ...) as N]...@[end try]`
- @`@[try]...@[except C1]...@[except C2]...@[end try]`
- @`@[try]...@[except C1]...@[except C2]... ... @[end try]`
- @`@[try]...@[finally]...@[end try]`
- @`@[try]...@[except ...]...@[finally]...@[end try]`
- @`@[try]...@[except ...]...@[else]...@[end try]`
- @`@[try]...@[except ...]...@[else]...@[finally]...@[end try]`

Its behavior mirrors in every way the native Python `try` statement.
The try clause will be expanded, and if an exception is thrown, the
first @`@[except]` clause that matches the thrown exception (if there
are any) will be expanded.  If a @`@[finally]` clause is present, that
will be expanded after any possible exception handling, regardless of
whether an exception was in fact thrown.  Finally, if there is at
least one @`@[except]` clause, an @`@[else]` may be present which will
be expanded in the event that no exception is thrown (but before any
@`@[finally]` clause).

The argument to the @`@[except]` markup indicates which type(s) of
exception should be handled and with what name, if any.  No argument
indicates that it will handle any exception.  A simple expression will
indicate an exception class, or a tuple of exception classes, that
will be handled.  The variable name of the thrown exception can be
captured and passed to the expansion with the `as` keyword, or a comma
(this latter notation is invalid in modern Python versions but is
still supported in EmPy regardless of the underlying Python version).

For example:

@<<<[Try controls]
Garbage is @[try]@hugalugah@[except NameError]not defined@[end try].
Division by zero is @[try]@(1/0)@[except ZeroDivisionError]illegal@[end try].
An index error is @[try]@([][3])@[except IndexError as e]@e.__class__.__name__@[end try].
And finally: @[try]@(nonexistent)@[except]oops, @[finally]something happened@[end try].
>>>

:::{note}

Try control markup was introduced in EmPy version 3.0, and was
expanded in 4.0 to include all modern valid uses of @`@[else]` and
@`@[finally]`.

:::


#### With control markup: @`@[with E as N]...@[end with]`

EmPy supports a version of the `with` statement, which was introduced
in Python 2.5.  In EmPy, the **with control markup** is written as
@`@[with]` and mirrors the behavior of the native `with` statement.
It takes the following forms:

- @`@[with E as N]...@[end with]`
- @`@[with N]...@[end with]`
- @`@[with E]...@[end with]`

All forms use context managers, just as with the native statement.
Context managers are objects which have `__enter__` and `__exit__`
methods, and the @`@[with]` markup ensures that the former is called
before the markup's contents are expanded and that the latter is
always called afterward, whether or not an exception has been thrown.

The three forms of the @`@[with]` markup mirror the uses of the `with`
keyword:  The user can specify an expression and a variable name with
the `as` keyword, or just a variable name, or just an expression (it
will be entered and exited, but the name of the resulting object will
not be available).  For example:

@<<<[With controls]
@{
import os, sys

with open('/tmp/with.txt', 'w') as f:
    print("Hello, world!", file=f)
}@
@[with open('/tmp/with.txt') as f]@f.read()@[end with]@
>>>

:::{note}

Although the `with` keyword was only introduced in Python 2.5, the 
@`@[with]` markup will work in any supported version of Python.

:::

:::{note}

With control markup was introduced in EmPy version 4.0.

:::

#### Defined control markup: @`@[defined N]...@[end defined]`

Sometimes it's useful to know whether a name is defined in either the
locals or globals dictionaries.  EmPy provides a dedicated markup for
this purpose: **defined control markup**.  It takes the following
forms:

- @`@[defined N]...@[end defined]`
- @`@[defined N]...@[else]...@[end defined]`

When provided a name, it will expand the contained markup if that name
is defined in either the locals or globals.  @`@[defined NAME]...@[end
defined]` is equivalent to @`@[if 'NAME' in globals() or 'NAME' in
locals()]...@[end if]`.  An @`@[else]` clause is also supported; if
present, this will be expanded if the name does _not_ appear in the
locals or globals.  If no @`@[else]` clause is present and the name is
not defined, nothing will be expanded.

@<<<[Defined controls]
@{cat = 'Boots'}@
Cat is @[defined cat]@cat@[else]not defined@[end defined].
Dog is @[defined dog]@dog@[else]not defined@[end defined].
>>>

:::{note}

Defined control markup was introduced in EmPy version 4.0.

:::

#### Def control markup: @`@[def F(...)]...@[end def]`

EmPy supports defining functions which expand EmPy code, not Python
code as with the standard `def` Python statement.  This is called
**def control markup**.  It takes on the following form:

- @`@[def F(...)]...@[end def]`

Def control markup involves specifying the signature of the resulting
function (such as with the standard Python `def` statement) and
encloses the EmPy code that the function should expand.  It is then
defined in the interpreter's globals/locals and can be called like any
other Python function.

It is best demonstrated with a simple example:

@<<<[Def controls]
@# Define an EmPy-native function.
@[def element(name, symbol, atomicNumber, group)]@
Element @name (symbol @symbol, atomic number @atomicNumber) is a @group@
@[end def]@
@# Now use it.
@element('hydrogen', 'H', 1, 'reactive nonmetal').
@element('helium', 'He', 2, 'noble gas').
@element('lithium', 'Li', 3, 'alkali metal').
@element('beryllium', 'Be', 4, 'alkaline earth metal').
@element('boron', 'B', 5, 'metalloid').
@element('carbon', 'C', 6, 'reactive nonmetal').
>>>

:::{hint}

The markup @`@[def FUNC(...)]DEFN@[end def]` is equivalent to the
following Python code:

```python
def FUNC(...):
    r"""DEFN"""
    return empy.expand(r"""DEFN""", locals())
```

It simply defines a Python function with the provided signature, a
docstring indicating its EmPy definition, and the function calls
`expand` on the pseudomodule/interpreter with the definition and
returns the results.

:::

:::{tip}

Functions defined with def control markup are callable Python objects
like any other.  They can be called through any mechanism, whether
Python (`f(...)`), through EmPy markup (@`@f(...)`), or even via
[functional expression markup](#functional-expression-markup)
(@`@f{...}`).

:::


### Diacritic markup: @`@^...`, @`@^CHAR{...}`

EmPy provides a quick and convenient way to combine diacritics
(accents) to characters with **diacritic markup**.  Diacritic markup
consists of the prefix @`@^`, followed by the base character, and then
either a single character representing the accent to apply or a
sequence of such characters enclosed in curly braces (`{...}`).

The first character is the base character to combine diacritics with,
and the remaining characters (possibly more than one if the curly
braces form is used) are diacritic codes corresponding to Unicode
combining characters that can be combined (or just appended) to the
base character.  These combining diacritics are simpler, more easily
entered characters that (at least in some cases) resemble the actual
desired combining character.  For instance, `'` (apostrophe)
represents the acute accent @\N{DOTTED CIRCLE}@\N{COMBINING ACUTE
ACCENT}; `` ` `` (backquote) represents the grave accent @\N{DOTTED
CIRCLE}@\N{COMBINING GRAVE ACCENT}; `^` represents the circumflex
accent @\N{DOTTED CIRCLE}@\N{COMBINING CIRCUMFLEX ACCENT}, and so on:

@<<<[Diacritics]
French: Voil@^a`, c'est ici que @^c,a s'arr@^e^te.
Spanish: Necesito ir al ba@^n~o ahora mismo.
Portuguese: Informa@^c,@^a~o @^e' poder.
Swedish: Hur m@^aonga kockar kr@^a:vs f@^o:r att koka vatten?
Vietnamese: Ph@^o{h?} b@^o` vi@^e^n ngon qu@^a'!
Esperanto: E@^h^o@^s^an@^g^e @^c^iu@^j^a@^u(de!
Shakespearean: All are punish@^e`d.
>>>

:::{tip}

Curly braces can enclose zero or more characters representing
diacritics.  If they enclose zero, the diacritic markup has no effect
(@`@^e{}` is no different from `e`).  If they enclose one, the results
are no different from not using curly braces (@`@^e{'}` and @`@^e'`
are have identical results).  Only for applying more than one
diacritic are curly braces required.

:::

By default, the base character and diacritics will be combined with
NFKC normalization -- this will, when possible, replace the base
character and its combiners with a single Unicode character
representing the combination, if one exists.  Normalization is not
required (and may sometimes fail when a suitable combined form does
not exist); in these cases, your system's Unicode renderer will cope
as best it can.  To change the normalization type, use
@info.option('--normalization-form', True).  To disable normalization,
set it to the empty string.

The dictionary mapping all diacritic codes to combining characters is
stored in the @info.variable('diacritics') configuration variable.
This can be modified or completely replaced as desired.  The values
can be integers (Unicode code point values), lists of integers, or
strings.  They can also take the form of a 2-tuple, where the first
element is one of the above values and the second element is a
description string used for displaying in help topics.

:::{seealso}

The list of all default diacritic codes is available in the
`diacritics` help topic and is summarized
[here](@info.ident.path{HELP.em#diacritics-combiners-summary}).

:::

:::{note}

Diacritic markup was introduced in EmPy version 4.0.

:::


### Icon markup: @`@|...`

A customizable brief way to map "icon" keys -- short, user-specified
strings -- to arbitrary Unicode strings exists in the form of **icon
markup**.  Icon markup is set off with @`@|...` and then followed by
an unambiguous, arbitrary-length sequence of characters (Unicode code
points) corresponding to one of its keys.

The icon keys can be any set of distinct strings, and are specified in
the @info.variable('icons') configuration variable whose keys are the
string keys as used in the markup, as well as all possible key
prefixes (more on this in a bit).  The values can be integers (Unicode
code point values), lists of integers, or strings.  They can also take
the form of a 2-tuple, where the first element is one of the above
values and the second element is a description string used for
displaying in help topics.  An (arbitrary) default set are provided by
default, but these can be modified or completely replaced as desired.

Keys can be arbitrary length and can consist of whatever characters
are desired (including letters, numbers, punctuation, or even Unicode
characters).  They are not delimited by whitespace; however, they must
be unambiguous, so if more than one key exists with the same prefixes
(say, `#+` and `#-`), a key cannot be defined as the common prefix
(`#`) as this would be found first and would hide the longer prefixes.
Such a common prefix key should be set to the value `None` (which
indicates to the parser that the icon is potentially valid but not yet
complete).

This validation is done automatically when the icon markup is first
used: The dictionary of icons is traversed and any common prefixes not
defined in the dictionary are set to `None`.  In the event that this
auto-validation may be expensive and the user wishes to do it manually
to avoid this step, specify the @info.option('--no-auto-validate-icons')
command line options to disable it.

@<<<[Icons]
These are @|"(curly quotes.@|")
This is a royal flush: A@|%s K@|%s Q@|%s J@|%s T@|%s.
This is a check mark @|/ and this is an X mark @|\.
Smile! @|:) Laugh! @|:9 Cry! @|:5 Sleep! @|:Z
>>>

To customize icons, modify or replace the @info.variable('icons')
configuration variable:

@<<<[Icons, customization]
@# Replace the icons with just a few very serious ones.
@{
empy.config.icons = {
    'kitty': '\U0001f431',
    'cat': '\U0001f408',
}
}@
Counting: one two @|kitty @|cat five.
>>>

:::{tip}

If you're finding problems with icons being ambiguous, you can add
delimiters at the end of the icon key to ensure that they are
unambiguous.  For example, the icons `!`, `!!` and `!?` would normally
be ambiguous.  However, wrapping them in, say, curly braces, will
remove the ambiguity: `{!}`, `{!!}`, `{!?}` are unambiguous and can be
used as icon keys.

:::

:::{seealso}

The list of all valid icon keys is available in the `icons` help topic
and is summarized [here](@info.ident.path{HELP.html#icons-summary}).

:::

:::{note}

The default set of icons were chosen by the author for his convenience
and to demonstrate what icon markup can do.  It is expected that users
using icon markup will modify/replace the icons dictionary.

:::

:::{note}

Icon markup was introduced in EmPy version 4.0.

:::


### Emoji markup: @`@:...:`

A dedicated **emoji markup** is available to translate Unicode emoji
names, and Unicode names more generally, into Unicode glyphs.  Using
the markup is simple: Use the @`@:...:` syntax and put the name of the
emoji character between the colons.  Since EmPy is often used in
wrapped text, any newlines in the emoji name will be replaced with
spaces.

By default it uses the builtin `unicodedata.lookup` function call
which allow the lookup of any Unicode code point by name, not just
emoji.  Whether names are case sensitive or not, or whether words are
separated by spaces or underscores or either, is module-dependent.
The builtin `unicodedata` module (the fallback if no emoji-specific
modules are installed) is case insensitive and requires spaces, not
underscores:

@<<<[Emojis]
Latin capital letter A: @:LATIN CAPITAL LETTER A:
Latin small letter O with diaeresis: @:latin small letter o with diaeresis:
White heavy check mark: @:WHITE HEAVY CHECK MARK:
Volcano: @:VOLCANO:
>>>

User-specified emoji can also be assigned to the configuration's
@info.variable('emojis') dictionary variable; this will be checked
before any emoji modules are queried.  The values of this dictionary
can be any string, not necessarily just a single character.  Emojis
in the `emojis` dictionary are case sensitive:

@<<<[Emojis, custom]
@# What's with this guy and cats?
@{
empy.config.emojis['kittycat'] = '\U0001f408'
}@
This is a kitty cat: @:kittycat:
>>>

{#third-party-emoji-modules} The emoji markup can also use third-party
emoji modules if they are present.  These can be installed in the
usual way with PyPI (e.g., `python3 -m pip install emoji`) or any
other preferred method.  The following emoji modules are supported:

| Module | Function | Parameter | Capitalization | Spaces or underscores |
| --- | --- | --- | --- | --- |
| `emoji` | `emojize` | `':%s:'` | lowercase | underscores |
| `emojis` | `encode` | `':%s:'` | lowercase | underscores |
| `emoji_data_python` | `replace_colons` | `':%s:'` | lowercase | underscores |
| `unicodedata` | `lookup` | `'%s'` | both | spaces |

On first usage, each module is checked to see if it is present and is
then registered in the order listed above.  When a lookup on a name is
performed, each module which is present is queried in order, and if it
finds the given name, that is used as output.  If no modules find the
name, by default an error is generated, but this behavior can be
changed with the @info.option('--ignore-emoji-not-found') command line
option.

The order in which modules are queried is also customizable with the
@info.option('--emoji-modules') command line option; specify the
sequence of emoji module names to test separated by commas.  Use the
@info.option('--no-emoji-modules') command line option to only enable
the builtin `unicodedata` module lookup, deactivating the use of any
custom modules which may be installed.  And use
@info.option('--disable-emoji-modules') to disable all emoji module
lookup; only the `emojis` configuration variable will be consulted.

If you're aware of other third-party emoji modules you'd like to see
supported, [contact the author](#contact).

:::{tip}

It's expected that the typical EmPy user will have at most one
third-party module installed, so no effort has been put in place to
avoid conflicts or redundancies regarding emoji names between them
other than specifying this desired lookup order.  Choose a third-party
module that works for you, or just rely on the builtin `unicodedata`
lookup table.

If you're relying on a third-party module to be present, you might
want to have your EmPy code explicitly import that module so that if
it's missing, the dependency will be more clear.

:::

@empy.replayDiversion('idiom')@

:::{note}

Emoji markup was introduced in EmPy version 4.0.

:::


### Significator markup: @`@%[!] ... NL`, @`@%%[!] ... %% NL`

**Significators** are ways to perform distinctive assignments within
an EmPy system which are easily parsed externally; for instance, for
specifying metadata for an EmPy source document.  In its simplest
form, it defines in a variable in the globals with the evaluation of a
Python value.  The significator @`@%KEY VALUE` is equivalent to the
Python assignment statement `__KEY__ = VALUE`.

The name of the assigned variable is preceded and ended with a double
underscore (`__`).  (This behavior can be changed with
configurations.)  Note that the value assigned can be any Python
expression, not just a string literal:

@<<<[Significators, basics]
@%title "A Tale of Two Cities"
@%author 'Charles Dickens'
@%year 1859
@%version '.'.join([str(x) for x in __import__('sys').version_info[0:2]])
The book is _@(__title__)_ (@__year__) by @__author__.
This version of Python is @__version__.
>>>

Whitespace is allowed between the @`@%` markup introducer and the key,
and any (non-newline) whitespace is allowed between the key and the
value.  The ending newline is always consumed.

A variant of significator markup can span multiple lines.  Instead of
using @`@%` and a newline to delimit the significator, use @`@%%` and
`%%` followed by a newline:

@<<<[Significators, multiline]
@%%longName "This is a potentially very long \
name which can span multiple lines." %%
@%%longerName """This is a triple quoted string
which itself contains newlines.  Note the newlines
are preserved.""" %%
@%%longExpression [[1, 2, 3],
[4, 5, 6],
[7, 8, 9]] %%
Long name: @__longName__
Longer name: @__longerName__
Long expression: @__longExpression__
>>>

::::{note}

When using multiline significators, the value must still be a valid
Python expression.  So the significator

@<<<empy
@%%bad 1 + 2 + 3 + 
4 + 5 + 6 %%
>>>

is a syntax error due to the intervening newline.  To correct this,
use a backslash character (`\`) to escape the newline or enclose the
value expression in parentheses:

@<<<empy
@%%good1 1 + 2 + 3 + \
4 + 5 + 6 %%
@%%good2 (1 + 2 + 3 +
4 + 5 + 6) %%
>>>

::::

Two more subvariants of significator markup exists, one for each of
these two variants.  Frequently significator values will just be
string literals and for uniformity users may wish to not deal with
full Python expressions.  For these purposes, significator values can
be **stringized**, or treated merely as strings with no Python
evaluation.  Simply insert a `!` after the @`@%` or @`@%%` markup
introducer and before the name of the key:

@<<<[Significators, stringized]
@# These values are all implicit strings.
@%!single This is on a single line.
@%%!multi This is on
multiple lines. %%
Single line: @__single__
Multiple lines: @__multi__
>>>

Finally, the values for both single and multiline significator markups
are optional.  If the markup is not stringized, the value will be
`None`; if stringized, it will be the empty string (`''`):

@<<<[Significators, optional values]
@%none
@%!empty
This is a None: @repr(__none__).
This is an empty string: @repr(__empty__).
>>>

:::{hint}

Significators can appear anywhere in an EmPy document, but typically
are used at the beginning.

:::

:::{tip}

A compiled regular expression object is returned by the
`significatorRe` configuration method and can be used to
systematically find all the significators in a given text.

:::

:::{note}

Significator markup was introduced in EmPy version 1.2.  Stringified
and multi-multiline variants were introduced in version 4.0.

:::


### Context markup

Contexts are objects which track the current progress of an EmPy
interpreter through its source document(s) for the purposes of error
reporting.  This is handled automatically by the EmPy system, but they
can be modified through the API or with context markup.

:::{note}

Context markups were introduced in EmPy version 3.0.2.

:::

#### Context name markup: @`@?... NL`

The **context name markup** can be used to change the current context
name with @`@?... NL`; it uses as the new name what follows on the
same line and consumes everything up to and including the newline.
Whitespace surrounding the context name is ignored.

@<<<[Context names]
@?Test
This context is now: @empy.getContext().
>>>


#### Context line markup: @`@!... NL`

The **context line markup** can be used to change the current context
line with @`@!... NL`; it uses as the new line what follows on the
same line and consumes everything up to and including the newline.
Whitespace surrounding the context name is ignored.  If the remaining
text is not parseable as an integer, it is a parse error.

@<<<[Context lines] 
@!1000
This context is now: @empy.getContext().
Note that the line is 1001 since it's the next line after the markup.
>>>


### Custom markup: @`@< ... >`

**Custom markup** is reserved for user-defined use.  Unlike the other
markups, this markup has no specified meaning on its own, and must be
provided a meaning by the user.  This meaning is provided with the use
of a Python callable object referred to as a **custom callback**, or
just "callback," which can be set, queried, or reset using
pseudomodule functions.  At most one custom callback can be registered
at a time.

When the custom markup @`@< ... >` is encountered, the contents inside
the markup are passed to the current custom callback.  Its return
value, if not `None`, is then written to the output stream.  The
custom callback may also perform operations with side effects
resulting in output, as well.  If there are multiple opening angle
brackets, an equal number of closing angle brackets will be required
to match.  This allows the embedding of `<` and `>` in the contents
passed to the callback.

The custom callback is a callable object which, when invoked, is
passed a single argument: a string representing the contents of what
was found inside the custom markup @`@< ... >`.  Only one custom
callback can be registered at a time.

To register a callback, call `empy.registerCallback`.  To remove it,
call `empy.deregisterCallback`.  To see if there is a callback
registered, use `empy.hasCallback`.  To retrieve the callback (if any)
registered with the interpreter, use `empy.getCallback`.  Finally, to
invoke the callback explicitly just as if the custom markup had been
encountered, call `empy.invokeCallback`.  For instance, @`@<This
text>` would be equivalent to the call @`@empy.invokeCallback("This
text")`.

By default, to invoke a callback (either explicitly with
`empy.invokeCallback` or by processing a @`@< ... >` custom markup) when
no callback has been registered is an error.  This behavior can be
changed with the @info.option('--no-callback-error') option; this
makes the use of the custom markup with no registered callback to
no-op.

@<<<[Custom markup]
@{
def callback(contents):
    return contents.upper()
empy.registerCallback(callback)
}@
This will be in uppercase: @<This is a test>.
This will also contain angle brackets: @<<This is <also a> test>>.
>>>

:::{tip}

It's typical to want to have an instance of the
interpreter/pseudomodule available to the callback, but it is neither
done automatically nor is it required.

:::

@empy.replayDiversion('idiom')@

:::{note}

Custom markup was introduced in EmPy version 3.3.

:::


## Features

Various additional features are available in a running EmPy system.

### Pseudomodule/interpreter

The pseudomodule/interpreter can be accessed by a running EmPy system by
referencing its name (which defaults to
`@info.config.pseudomoduleName`) in the globals:

@empy.replayDiversion('Pseudomodule sample')

:::{important}

The pseudomodule and interpreter are one and the same object; the
terms _pseudomodule_ and _interpreter_ are used interchangeably.  The
interpreter exposes itself as the pseudomodule
`@info.config.pseudomoduleName` in a running EmPy system; this
pseudomodule is never imported explicitly.

:::

:::{note}

The pseudomodule was introduced in EmPy version 1.0.

:::


#### Interpreter attributes and methods

##### Interpreter attributes

The following attributes are set on the pseudomodule after it is
initialized.

`version`

: The version of EmPy.

`compat`

: A list of strings indicating the "compatibility features" that were
  automatically enabled to support earlier versions of Python.
  Possible strings are:

| Feature | Description |
| --- | --- |
| `BaseException` | No `BaseException` class existed prior to Python 2.5 |
| `chr/decode` | Substituted an implementation of `chr` for narrow Unicode builds using `decode` |
| `chr/uliteral` | Substituted an implementation of `chr` for narrow Unicode builds using `uliteral` |
| `narrow` | Python was built with narrow Unicode (strings natively stored as UTF-16) |

`executable`

: The path to the EmPy interpreter that is being used by the system
  (analogous to `sys.executable`).

`argv`

: The arguments (analogous to `sys.argv`) used to start the
  interpreter.  The first element is the EmPy document filename and
  the remaining elements are the arguments, if any.  If no EmPy
  document was specified, `@info.config.unknownScriptName` is used.

`config`

: The [configuration](#configuration) instance that the interpreter is
  using.

##### Interpreter methods

These methods involve the interpreter directly.

:::{note}

Most interpreter methods return `None` so they can be called from
EmPy expression markup.

:::

{#constructor}
`__init__(**kwargs)`

: The constructor.  It takes the following keyword arguments, all of
  which are optional:

  | Argument | Meaning | Default |
  | --- | --- | --- |
  | `config` | The configuration instance to use | default |
  | `globals` | The globals dictionary to use | `{}` |
  | `output` | The output file to use | `sys.stdout` |
  | `input` | The input file to use for interactivity | `sys.stdin` |
  | `executable` | The path to the EmPy executable | `.../em.py` |
  | `argv` | The system arguments to use | `['<->']` |
  | `filespec` | A 3-tuple of the input filename, output mode, and buffering | `None` |
  | `hooks` | A list of hooks to install | `[]` |
  | `callback` | A custom callback to register | `None` |
  | `handler` | An error handler to use | default |
  | `evalFunc` | Function to evaluate expressions | `eval` |
  | `execFunc` | Function to execute statements | `exec` |
  | `immediately` | Declare the interpreter [ready](#ready) immediately after initialization | `True` |
  
  The ordering of the arguments does not matter.  Missing arguments
  have reasonable defaults and unrecognized arguments are ignored.
  
  _immediately_ is a `bool` which indicates whether the
  [`ready`](#ready) method will be called before the constructor
  exits.

  :::{tip}
  
  The order of the `Interpreter` constructor arguments has changed
  over time and is subject to change in the future, so you need to use
  keyword arguments to prevent any ambiguity, _e.g._:
  
  ```python
  import em

  myConfig = em.Configuration(...)
  myGlobals = {...}
  myOutput = open(...)
  interp = em.Interpreter(
      config=myConfig, 
      globals=myGlobals, 
      output=myOutput,
      ...)
  ```
  
  :::

{#context-management}
`__enter__()`/`__exit__(*exc)`

: The interpreter presents a context manager interface and so can be
  used with the `with` Python control structure, _e.g._:
  
  ```python
  import em

  with em.Interpreter(...) as interp:
      ... manipulate interp here ...
  ```

{#reset}
`reset()`

: Reset the interpreter to a pristine state.

{#ready}
`ready()`

: Declare the interpreter ready for processing.  This calls the
  `atReady` hook.  By default this is called before the
  [constructor](#constructor) exits, but the user can do this
  explicitly by passing `False` to the `immediately` constructor
  argument and calling it when they wish to declare the interpreter
  ready.

{#shutdown}
`shutdown()`

: Shutdown the interpreter.  No further expansion must be done.  This
  method is idempotent.

  :::{important}

  Any EmPy interpreter that is created must be shutdown properly by
  calling its `shutdown` method.  Not calling this method will likely
  cause a `ConsistencyError` to be raised.

  :::

#### Interpreter file-like methods

These methods mimic a file so the interpreter can be treated as a
file-like object in APIs.

`write(data)`

: Write the string data to the output stream.

`writelines(lines)`

: Write the sequence of strings to the output stream.

`flush()`

: Flush the output stream.

`serialize(object)`

: Write a string version of the object to the output stream.  This
  will reference @info.option('--none-symbol', True) if the object is
  `None`.

#### Interpreter context methods

These methods manipulate the interpreter's context stack.

`identify() -> tuple`

: Get a 4-tuple of the current context, consisting of the filename,
  the line number, the column number, and the number of characters
  (Unicode code points) processed.

`getContext() -> Context`

: Get the current context object.

`newContext([name, [line, [column]]]) -> Context`

: Create a new context and return it.

`pushContext(context)`

: Push the given context on top of the context stack.

`popContext()`

: Pop the top context off the context stack; do not return it.

`setContext(context)`

: Replace the context on the top of the context stack with the given
  context.

`setContextName(name)`

: Set the top context's name to the given value.

`setContextLine(line)`

: Set the top context's line to the given value.

`setContextColumn(column)`

: Set the top context's column to the given value.

`setContextData([name, [line, [column]]])`

: Set the top context's name, line, and/or column to the given value(s).

`restoreContext(oldContext)`

: Restore the top context on the stack to the given context.

#### Interpreter finalizer methods

These methods manipulate the interpreter's finalizers.

`clearFinalizers()`

: Clear all finalizers from this interpreter.

`appendFinalizer(finalizer)`/`atExit(finalizer)`

: Append the given finalizer to the finalizers list for this
  interpreter.  `atExit` is an alias.

`prependFinalizer(finalizer)`

: Prepend the given finalizer to the finalizers list for this
  interpreter.

#### Interpreter globals methods

These methods manipulate the interpreter's globals.

`getGlobals() -> dict`

: Get the current globals dictionary.

`setGlobals(globals)`

: Set the current globals dictionary,.

`updateGlobals(moreGlobals)`

: Update the current globals dictionary, adding this dictionary's
  entries to it.

`clearGlobals()`

: Clear the current globals dictionary completely.

`saveGlobals([deep])`

: Save a copy of the globals off to on the history stack.  If deep is
  true, do a deep copy (defaults to false).

`restoreGlobals([destructive])`

: Restore the globals dictionary on the top of the globals history
  stack.  If destructive is true (default), pop it off when done.

`flattenGlobals([skipKeys])`

: Flatten the interpreter namespace into the globals.  If `skipKeys`
  is specified, use those keys; otherwise use the defaults from the
  configuration.

#### Interpreter expansion methods

These methods are involved with markup expansion.

`include(fileOrFilename, [locals, [name]])`

: Include the given EmPy (not Python) document (or filename, which is
  opened) and process it with the given optional locals dictionary and
  name.

`expand(data, [locals, [name]]) -> str`

: Create a new context and stream to evaluate the EmPy data, with
  the given optional locals and name.  Return the result.

`defined(name, [locals]) -> bool`

: Return a Boolean indicating whether the given name is present in the
  interpreter globals (or the optional locals, if provided).
  
`lookup(name, [locals]) -> object`

: Lookup the value of a name in the globals (and optionally the
  locals, if provided) and return the value.

`evaluate(expression, [locals, [write]]) -> object | None`

: Evaluate the given Python expression in the interpreter, with the
  given optional locals dictionary.  If write is true, write it to the
  output stream, otherwise return it (defaults to false).

`execute(statements, [locals])`

: Execute the given Python statements in the interpreter, with the
  given optional locals dictionary.

`single(source, [locals]) -> object | None`

: Execute the given Python expression or statement, with the given
  optional locals dictionary.  This compiles the code with the
  `single` Python compilation mode which supports either.  Return the
  result or `None`.

`atomic(name, value, [locals])`

: Do an atomic assignment of the given name and value in the
  interpreter globals.  If the optional locals dictionary is provided,
  set it in the locals instead.

`assign(name, value, [locals])`

: Do a potentially complex assignment of the given name "lvalue" and
  "rvalue."  Unlike `atomic`, `assign` can support tuple assignment.

`significate(key, [value, [locals]])`

: Declare a significator with the given key and optional value (if not
  specified, defaults to `None`).  If the optional locals dictionary
  is provided, set it in the locals instead.

`quote(string) -> str`

: Given an EmPy string, return it quoted.

`escape(string) -> str`

: Given an EmPy string, escape non-ASCII characters in it and return.

`getPrefix() -> str`

: Get this interpreter's prefix.

`setPrefix(char)`

: Set this interpreter's prefix.

#### Interpreter diversion methods

These methods manipulate the interpreter's diversions.

`stopDiverting()`

: Stop any current diversion.

`createDiversion(name)`

: Create a new diversion with the given name but do not start diverting
  to it.

`retrieveDiversion(name) -> Diversion`

: Get the diversion with the given name.

`startDiversion(name)`

: Start diverting to a diversion with the given name, creating if it
  necessary.

`playDiversion(name, [drop])`

: Play the diversion with the given name, optionally dropping it
  (default).

`replayDiversion(name, [drop])`

: Play the diversion with the given name, optionally dropping it
  (default is false).

`dropDiversion(name)`

: Drop the diversion with the given name without playing it.

`playAllDiversions()`

: Play all diversions in sorted order by name, dropping them.

`replayAllDiversions()`

: Replay all diversions in sorted order by name, dropping them.

`dropAllDiversions()`

: Drop all diversions without playing them.

`getCurrentDiversionName() -> str | None`

: Get the name of the current diversion or `None` if there is no
  current diversion.

`getAllDiversionNames() -> list[str]`

: Get a list of the names of all diversions in sorted order.

`isExistingDiversionName(name) -> bool`

: Is the given name the name of an existing diversion?

#### Interpreter filter methods

These methods manipulate the interpreter's filters.

`resetFilter()`

: Reset the filtering system so there are no filters.

`getFilter() -> Filter`

: Get the top-most filter.

`getLastFilter() -> Filter`

: Get the bottom-most filter.

`setFilter(*filters)`

: Set the top-most filter(s) to the given filter chain, replacing any
  current chain.  More than one filter can be specified as separate
  arguments.

`prependFilter(filter)`

: Prepend the given filter to the current filter chain.

`appendFilter(filter)`

: Append the given filter to the current filter chain.

`setFilterChain(filters)`

: Set the filter chain to the given list of filters, replacing any
  current chain.

#### Interpreter hook methods

These methods manipulate the interpreter's hooks.

`invokeHook(_name, **kwargs)`

: Invoke the hooks associated with the given name and keyword
  arguments dictionary.  This is the primary method called when hook
  events are invoked.

`areHooksEnabled() -> bool`

: Are hooks currently enabled?

`enableHooks()`

: Enable hooks.

`disableHooks()`

: Disable hooks.  Any existing hooks will not be called until
  `enableHooks` is called.

`getHooks() -> list[Hook]`

: Get the current list of hooks.

`prependHook(hook)`

: Prepend the given hook to the list of hooks.

`appendHook(hook)`

: Append the given hook to the list of hooks.

`removeHook(hook)`

: Remove the given hook from the list of hooks.

`clearHooks()`

: Clear the list of hooks.

#### Interpreter callback methods

These methods manipulate the interpreter's custom callback.  A
callback is a callable object which takes one argument:  the content
to process.

`hasCallback() -> bool`

: Does this interpreter have a custom callback registered?

`getCallback() -> func | None`

: Return the interpreter's registered custom callback or `None` if
  none is registered.

`registerCallback(callback)`

: Register the given callback with the interpreter, replacing any
  existing callback.

`deregisterCallback()`

: Remove the current interpreter's registered callback, if any.

`invokeCallback(contents)`

: Manually invoke the interpreter's custom callback as if the custom
  markup @`@< ... >` were expanded.

#### Interpreter error handler methods

These methods manipulate the interpreter's error handler.  A handler
is a callable object which takes three arguments: the type of the
error, the error instance itself, and a traceback object.

`defaultHandler(type, error, traceback)`

: The default EmPy error handler.  This can be called manually by
  custom error handlers if desired.

`getHandler() -> object`

: Get the current error handler, or `None` for the default.

`setHandler(handler, [exitOnError])`

: Set the error handler.  If `exitOnError` is not `None` (defaults to
  false), also set the interpreter's configuration's `exitOnError`
  configuration variable.  This default is so that custom error
  handlers do not automatically exit which is usually the intent.

#### Interpreter emoji methods

`initializeEmojiModules([moduleNames])`

: Initialize the allowed emoji modules to use by name.  If the names
  list is not specified, use the defaults.

`getEmojiModule(moduleName) -> Module`

: Get the initialized module abstraction corresponding to the given
  module name.

`getEmojiModuleNames() -> list[str]`

: Return the list of available emoji modules by name in their proper
  order.

`substituteEmoji(text) -> str`

: Use the emoji facilities to lookup the given emoji name and return
  the result as if the emoji markup @`@:...:` were expanded.

:::{seealso}

The list of pseudomodule/interpreter attributes in methods is
available in the `hooks` help topic and is summarized
[here](@info.ident.path{HELP.html#pseudomodule-attributes-and-methods-summary}).

:::


### Diversions

EmPy supports an extended form of **diversions**, which are a
mechanism for deferring and playing back output on demand, similar to
the functionality included in [m4](https://www.gnu.org/software/m4/).
Multiple "streams" of output can be diverted (deferred) and played
back (undiverted) in this manner.  A diversion is identified with a
name, which is any immutable object such an integer or string.
Diversions can be played back multiple times ("replayed") if desired.
When recalled, diverted code is *not* resent through the EmPy
interpreter (although a [filter](#filters) could be set up to do
this).

By default, no diversions take place.  When no diversion is in effect,
processing output goes directly to the specified output file.  This
state can be explicitly requested at any time by calling the
`empy.stopDiverting` function.  It is always legal to call this
function, even when there is currently no active diversion.

When diverted, however, output goes to a deferred location which can
then be recalled later.  Output is diverted with the
`empy.startDiversion` function, which takes an argument that is the
name of the diversion.  If there is no diversion by that name, a new
diversion is created and output will be sent to that diversion; if the
diversion already exists, output will be appended to that preexisting
diversion.

Output send to diversions can be recalled in two ways.  The first is
through the `empy.playDiversion` function, which takes the name of the
diversion as an argument.  This plays back the named diversion, sends
it to the output, and then erases that diversion.  A variant of this
behavior is the `empy.replayDiversion`, which plays back the named
diversion but does not eliminate it afterwards; `empy.replayDiversion`
can be repeatedly called with the same diversion name, and will replay
that diversion repeatedly.  `empy.createDiversion` will create a
diversion without actually diverting to it, for cases where you want
to make sure a diversion exists but do not yet want to send anything
to it.

The diversion object itself can be retrieved with
`empy.retrieveDiversion`.  Diversions act as writable file-objects,
supporting the usual `write`, `writelines`, `flush`, and `close`
methods.  The data that has been diverted to them can be manually
retrieved in one of two ways; either through the `asString` method,
which returns the entire contents of the diversion as a single string,
or through the `asFile` method, which returns the contents of the
diversion as a readable (not writable) file-like object.

Diversions can also be explicitly deleted without playing them back
with the `empy.dropDiversion` function, which takes the desired
diversion name as an argument.

Additionally there are three functions which will apply the above
operations to all existing diversions: `empy.playAllDiversions`,
`empy.replayAllDiversions`, and `empy.dropAllDiversions`.  The
diversions are handled in lexicographical order by their name.  Also,
all three will do the equivalent of a `empy.stopDiverting` call before
they do their thing.

The name of the current diversion can be requested with the
`empy.getCurrentDiversionName` function; also, the names of all
existing diversions (in sorted order) can be retrieved with
`empy.getAllDiversionNames`.  `empy.isExistingDiversionName` will
return whether or not a diversion with the given name exists.

When all processing is finished, the equivalent of a call to
`empy.playAllDiversions` is done.  This can be disabled with the
@info.option('--no-auto-play-diversions', True) option.

@empy.replayDiversion('Diversions sample')

:::{note}

Diversions were introduced in EmPy version 1.0.

:::


### Filters

EmPy also supports dynamic **filters**.  Filters are put in place
immediately before the final output file, and so are only invoked
after all other processing has taken place (including interpreting and
diverting).  Filters take input, remap it, and then send it to the
output.  They can be chained together where a series of filters point
to each other in series and then finally to the output file.

The current top-level filter can be retrieved with `empy.getFilter`
(or `empy.getFirstFilter`).  The last filter in the chain (the one
just before the underlying file) can be retrieved with
`empy.getLastFilter`.  The filter can be set with `empy.setFilter`
(which allows multiple arguments to constitute a chain).  To append a
filter at the end of the chain (inserting it just before the
underlying output file), use `empy.appendFilter`.  To prepend it to
the top of the chain, use `empy.prependFilter`.  A filter chain can be
set directly with `empy.setFilterChain`.  And a filter chain can be
reset with `empy.resetFilter`, removing all filters.

Filters are, at their core, simply file-like objects (minimally
supporting `write`, `flush`, and `close` methods that behave in the
usual way) which, after performing whatever processing they need to
do, send their work to the next file-like object or filter in line,
called that filter's "sink."  That is to say, filters can be "chained"
together; the action of each filter takes place in sequence, with the
output of one filter being the input of the next.  The final sink of
the filter chain will be the output file.  Additionally, filters
support a `_flush` method (note the leading underscore) which will
always flush the filter's underlying sink; this method should be not
overridden.

Filters also support two additional methods, not part of the
traditional file interface: `attach`, which takes as an argument a
file-like object (perhaps another filter) and sets that as the
filter's "sink" -- that is, the next filter/file-like object in line.
`detach` (which takes no arguments) is another method which flushes
the filter and removes its sink, leaving it isolated.  Finally,
`next`, if present, is an attribute which references the filter's sink
-- or `None`, if the filter does not yet have a sink attached.

To create your own filter, you can create an object which supports the
above described interface, or simply derive from the `Filter` class
(or one of its subclasses) in the `emlib` module and override the
relevant methods.

@empy.replayDiversion('Filters sample')

:::{note}

Filters were introduced in EmPy version 1.3.

:::


### Hooks

The EmPy system allows for the registration of **hooks** with a
running EmPy interpreter.  Hooks are objects, registered with an
interpreter, whose methods represent specific hook events.  Any number
of hook objects can be registered with an interpreter, and when a hook
is invoked, the associated method on each one of those hook objects
will be called by the interpreter in sequence.  The method name
indicates the type of hook, and it is called with a keyword list of
arguments corresponding the event arguments.

To use a hook, derive a class from `emlib.Hook` and override the
desired methods (with the same signatures as they appear in the base
class).  Create an instance of that subclass, and then register it
with a running interpreter with the `empy.addHook` function.  A hook
instance can be removed with the `empy.removeHook` function.

More than one hook instance can be registered with an interpreter; in
such a case, the appropriate methods are invoked on each instance in
the order in which they were appended.  To adjust this behavior, an
optional `prepend` argument to the `empy.addHook` function can be used
dictate that the new hook should placed at the *beginning* of the
sequence of hooks, rather than at the end (which is the default).
Also there are explicit `empy.appendHook` and `empy.prependHook`
functions.

All hooks can be enabled and disabled entirely for a given
interpreter; this is done with the `empy.enableHooks` and
`empy.disableHooks` functions.  By default hooks are enabled, but
obviously if no hooks have been registered no hook callbacks will be
made.  Whether hooks are enabled or disabled can be determined by
calling `empy.areHooksEnabled`.  To get the list of registered hooks,
call `empy.getHooks`.  All the hooks can be removed with
`empy.clearHooks`.  Finally, to invoke a hook manually, use
`empy.invokeHook`.

For a list of supported hook callbacks, see the `Hook` class
definition in the `emlib` module.  (There is also an `AbstractHook`
class in this module which does not have blank stubs for existing hook
methods in case a user wishes to create them dynamically.)

For example:

@empy.replayDiversion('Hooks sample')

:::{note}

Hooks were originally introduced in EmPy version 2.0, much improved in
version 3.2, and revamped again in version 4.0.

:::


#### Hook methods

##### Hook `at...` methods

These hooks are called when a self-contained event occurs.

`atInstallProxy(proxy, new)`

: A `sys.stdout` proxy was installed.  The Boolean value `new`
  indicates whether or not the proxy was preexisting.

`atUninstallProxy(proxy, done)`

: A `sys.stdout` proxy was uninstalled.  The Boolean value `done`
  indicates whether the reference count went to zero (and so the proxy
  has been completely removed).

`atStartup()`

: The interpreter has started up.

`atReady()`

: The interpreter has declared itself ready for processing.

`atFinalize()`

: The interpreter is finalizing.

`atShutdown()`

: The interpreter is shutting down.

`atParse(scanner, locals)`

: The interpreter is initiating a parse action with the given scanner
  and locals dictionary (which may be `None`).

`atToken(token)`

: The interpreter is expanding a token.

`atHandle(info, fatal, contexts)`

: The interpreter has encountered an error.  The `info` parameter is a
  3-tuple error (error type, error, traceback) returned from
  `sys.exc_info`, `fatal` is a Boolean indicating whether the
  interpreter should exit afterwards, and `contexts` is the context
  stack.

`atInteract()`

: The interpreter is going interactive.

##### Hook context methods

`pushContext(context)`

: This context is being pushed.

`popContext(context)`

: This context has been popped.

`setContext(context)`

: This context has been set or modified.

`restoreContext(context)`

: This context has been restored.

##### Hook `pre...`/`post...` methods

The `pre...` hooks are invoked before a token expands.  The hook can
return a true value to indicate that it has intercepted the expansion
and the token should cancel native expansion.  Not explicitly
returning anything, as in standard Python, is equivalent to returning
`None`, which is a false value, which continues expansion:

@<<<[Hook `pre...` methods]
@{
import emlib
import sys

class Hook(emlib.Hook):

    def __init__(self, interp):
        self.interpreter = interp

    def preString(self, string):
        self.interpreter.write('[' + string + ']')
        return True

empy.addHook(Hook(empy))
}@
@# Now test it:
@"Hello, world!"
>>>

:::{tip}

It's typical to want to have an instance of the
interpreter/pseudomodule available to the hook, but it is neither done
automatically nor is it required.

:::

The `post...` hooks are invoked after a non-intercepted token finishes
expanding.  Not all `pre...` hooks have a corresponding `post...`
hook.  The `post...` hooks take at most one argument (the result of
the token expansion, if applicable) and their return value is ignored.

`preLineComment(comment)`, `postLineComment()`

: The line comment @`@# ... NL` with the given text.

`preInlineComment(comment)`, `postInlineComment()`

: The inline comment @`@* ... *` with the given text.

`preWhitespace(whitespace)`

: The whitespace token @`@ WS` with the given whitespace.

`prePrefix()`

: The prefix token @`@@`.

`preString(string)`, `postString()`

: The string token @`@'...'`, etc. with the given string.

`preBackquote(literal)`, `postBackquote(result)`

: The backquote token @`` @` ... ` `` with the given literal.

`preSignificator(key, value, stringized)`, `postSignificator()`

: The significator token @`@% ... NL`, etc. with the given key, value
  and a Boolean indicating whether the significator is stringized.

`preContextName(name)`, `postContentName()`

: The context name token @`@?...` with the given name.

`preContextLine(line)`, `postContextLine()`

: The context line token @`@!...` with the given line.

`preExpression(pairs, except, locals)`, `postExpression(result)`

: The expression token @`@( ... )` with the given if-then run pairs, the
  except run, and the locals dictionary (which may be `None`).

`preSimple(code, subtokens, locals)`, `postSimple(result)`

: The simple expression token @`@word` (etc.) with the given code,
  subtokens and locals.

`preInPlace(code, locals)`, `postInPlace(result)`

: The in-place expression token @`@$ ... $ ... $` with the given code
  (first section) and locals (which may be `None`).

`preStatement(code, locals)`, `postStatement()`

: The statement token @`@{ ... }` with the given code and locals (which
  may be `None`).

`preControl(type, rest, locals)`, `postControl()`

: The control token @`@[ ... ]` of the given type, with the rest run and
  locals (which may be None).

`preEscape(code)`, `postEscape()`

: The control token @`@\...` with the resulting code.

`preDiacritic(code)`, `postDiacritic()`

: The diacritic token @`@^...` with the resulting code.

`preIcon(code)`, `postIcon()`

: The icon token @`@|...` with the resulting code.

`preEmoji(name)`, `postEmoji()`

: The emoji token @`@:...:` with the given name.

`preCustom(contents)`, `postCustom()`

: The custom token @`@<...>` with the given contents.


##### Hook `before...`/`after...` methods

The `before...` and `after...` hooks are invoked before and after (go
figure) mid-level expansion activities are performed.  Any `locals`
argument indicates the locals dictionary, which may be `None`.

If the expansion returns something relevant, it is passed as a
`result` argument to the corresponding `after...` method.

`beforeProcess(command, n)`, `afterProcess()`

: The given command (with index number) is being processed.

`beforeInclude(file, locals, name)`, `afterInclude()`

: The given file is being processed with the given name.

`beforeExpand(string, locals, name)`, `afterExpand(result)`

: `empy.expand` is being called with the given string and name.

`beforeTokens(tokens, locals)`, `afterTokens(result)`

: The given list of tokens is being processed.

`beforeFileLines(file, locals)`, `afterFileLines()`

: The given file is being read by lines.

`beforeFileChunks(file, locals)`, `afterFileChunks()`

: The given file is being read by buffered chunks.

`beforeFileFull(file, locals)`, `afterFileFull()`

: The given file is being read fully.

`beforeString(string, locals)`, `afterString()`

: The given string is being processed.

`beforeQuote(string)`, `afterQuote(result)`

: The given string is being quoted.

`beforeEscape(string)`, `afterEscape(result)`

: The given string is being escaped.

`beforeSignificate(key, value, locals)`, `afterSignificate()`

: The given key/value pair is being processed.

`beforeCallback(contents)`, `afterCallback()`

: The custom callback is being processed with the given contents.

`beforeAtomic(name, value, locals)`, `afterAtomic()`

: The given atomic variable setting with the name and value is being
  processed.

`beforeMulti(names, values, locals)`, `afterMulti()`

: The given complex variable setting with the names and values is
  being processed.

`beforeImport(name, locals)`, `afterImport()`

: A module with the given name is being imported.

`beforeFunctional(code, lists, locals)`, `afterFunctional(result)`

: A functional markup is with the given code and argument lists (of
  EmPy code) is being processed.

`beforeEvaluate(expression, locals, write)`, `afterEvaluate(result)`

: An evaluation markup is being processed with the given code and a
  Boolean indicating whether or not the results are being written
  directly to the output stream or returned.

`beforeExecute(statements, locals)`, `afterExecute()`

: A statement markup is being processed.

`beforeSingle(source, locals)`, `afterSingle(result)`

: A "single" source (either an expression or a statement) is being
  compiled and processed.

`beforeFinalizer(final)`, `afterFinalizer()`

: The given finalizer is being processed.  If the `beforeFinalizer`
  hook returns true for a particular finalizer, then that finalizer
  will not be called.

:::{seealso}

The list of hook methods is available in the `hooks` help topic and is
summarized [here](@info.ident.path{HELP.html#hook-methods-summary}).

:::


## Customization

The behavior of an EmPy system can be customized in various ways.

### Command line options

EmPy uses a standard GNU-style command line options processor with
both short and long options (_e.g._, `-p` or `--prefix`).  Short
options can be combined into one word, and options can have values
either in the next word or in the same word separated by an `=`.  An
option consisting of only `--` indicates that no further option
processing should be performed.

EmPy supports the following options:

@info.option('-V', True)

: Print version information exit.  Repeat the option for more details
  (see below).

@info.option('-W', True)

: Print additional information, including the operating system, Python
  implementation and Python version number.
  
@info.option('-Z', True)

: Print all additional details about the running environment,
  including interpreter, system, platform, and operating system
  release details.

@info.option('-h', True)

: Print basic help and exit.  Repeat the option for more extensive
  help.  Specifying `-h` once is equivalent to `-H default`; twice to
  `-H more`, and three or more times to `-H all` (see below).

@info.option('-H', True)

: Print extended help by topic(s).  Topics are a comma-separated list
  of the following choices:
  
  | Topic | Description |
  | --- | --- |
  | `usage` | Basic command line usage |
  | `options` | Command line options |
  | `markup` | Markup syntax |
  | `escapes` | Escape sequences |
  | `environ` | Environment variables |
  | `pseudo` | Pseudomodule attributes and functions |
  | `config` | Configuration variable attributes |
  | `methods` | Configuration methods |
  | `hook` | Hook methods |
  | `controls` | Named escapes (control codes) |
  | `diacritics` | Diacritic combiners |
  | `icons` | Icons |
  | `emojis` | User-specified emojis (optional) |
  | `hints` | Usage hints |
  | `topics` | This list of topics |
  | `default` | `usage,options,markup,hints` and `topics` |
  | `more` | `usage,options,markup,escapes,environ,hints` and `topics` |
  | `all` | `usage,options,markup,escapes,environ,pseudo,config,controls,diacritics,icons,hints` |

  As a special case, `-H` with no topic argument is treated as `-H
  all` rather than error.

@info.option('--verbose', True)

: The EmPy system will print debugging information to `sys.stderr` as
  it is doing its processing.
  
@info.option('--prefix', True)

: Specify the desired EmPy prefix.  It must consistent of a single
  Unicode code point (or character), or an empty string for no prefix
  (see below).  Defaults to `@info.config.prefix`.

@info.option('--no-prefix', True)

: Specify that EmPy use no prefix.  In this mode, will only process
  text and perform no markup expansion.  This is equivalent to
  specyfing `-p ''`.

@info.option('--no-output', True)

: Use a null file for the output file.

@info.option('--pseudomodule', True)

: Specify the name of the EmPy pseudomodule/interpreter.  Defaults to
  `@info.config.pseudomoduleName`.
  
@info.option('--flatten', True)

: Before processing, move the contents of the
  `@info.config.pseudomoduleName` pseudomodule into the globals, just
  as if `empy.flattenGlobals()` were executed immediately after
  starting the interpreter.  This is the equivalent of executing `from
  empy import *` (though since the pseudomodule is not a real module
  that statement is invalid).  _e.g._, `empy.include` can be referred
  to simply as `include` when this flag is specified on the command
  line.

@info.option('--keep-going', True)

: Don't exit when an error occurs.  Execute the error handler but
  continue processing EmPy tokens.

@info.option('--ignore-errors', True)

: Ignore errors completely.  No error handler is executed and token
  processing continues indefinitely.

@info.option('--raw-errors', True)

: After logging an EmPy error, show the full Python traceback that
  caused it.  Useful for debugging.
  
@info.option('--interactive', True)

: Enter interactive mode (continue processing EmPy markup from
  `sys.stdin`) after processing is complete.  This is helpful for
  inspecting the state of the interpreter after processing.

@info.option('--delete-on-error', True)

: If an error occurs, delete the output file; requires the use of the
  one of the output options such as @info.option('-o').  This is
  useful when running EmPy under a build systemn such as GNU Make.  If
  this option is not selected and an error occurs, the output file
  will stop when the error is encountered.

@info.option('--no-proxy', True)

: Do not install a proxy in `sys.stdout`.  This will make EmPy thread
  safe but writing to `sys.stdout` will not be captured or processed
  in any way.

@info.option('--config', True)

: Perform the given configuration variable assignments.  This option
  can be specified multiple times.

@info.option('--config-file', True)

: Read and process the given configuration file(s), separated by the
  platform-specific path delimiter (`;` on Windows, `:` on other
  operating systems).  This option can be specified multiple times.
  
@info.option('--config-variable', True)

: Specify the variable name corresponding to the current configuration
  when configuration files are processed.  Defaults to
  `@info.config.configVariableName`.
  
@info.option('--ignore-missing-config', True)

: Ignore missing files while reading and processing configurations.
  By default, a missing file is an error.
  
@info.option('--output', True)

: Specify the file to write output to.  If this argument is not used,
  final output is written to the underlying `sys.stdout`.
  
@info.option('--append', True)

: Specify the file to append output to.  If this argument is not used,
  final output is appended to the underlying `sys.stdout`.

@info.option('--output-binary', True)

: Specify the file to write output to and open it as binary.

@info.option('--append-binary', True)

: Specify the file to append output to and open it as binary.

@info.option('--output-mode', True)

: Specify the output mode to use.

@info.option('--input-mode', True)

: Specify the input mode to use.  Defaults to `'r'`.

@info.option('--buffering', True)

: Specify the buffering to use.  Use an integer to specify the maximum
  number of bytes to read per block or one of the following string
  values:
  
  | Name | Value | Description |
  | --- | --- | --- |
  | `full` | @info.config.fullBuffering | Use full buffering |
  | `none` | @info.config.noBuffering | Use no buffering |
  | `line` | @info.config.lineBuffering | Use line buffering |
  | `default` | @info.config.defaultBuffering | Default buffering |

  If the choice of buffering is incompatible with other settings, a
  `ConfigurationError` is raised.  This option has no effect on
  interactive mode, as `sys.stdin` is already open.  Defaults to
  @info.config.buffering.

@info.option('--default-buffering', True)

: Use default buffering.

@info.option('--no-buffering', True)

: Use no buffering.

@info.option('--line-buffering', True)

: Use line buffering.

@info.option('--full-buffering', True)

: Use full buffering.

@info.option('--preprocess', True)

: Process the given EmPy (not Python) file before main document
  processing begins.

@info.option('--postprocess', True)

: Process the given EmPy (not Python) file after main document
  processing begins.

@info.option('--import', True)

: Import the given Python (not EmPy) module(s) into the interpreter
  globals before main document processing begins.

@info.option('--define', True)

: Define the given variable into the interpreter globals before main
  document processing begins.  This is executed as a Python assignment
  statement (`variable = ...`); if it does not contain a `=`
  character, then the variable is defined in the globals with the
  value `None`.

@info.option('--string', True)

: Define the given string variable into the interpreter globals before
  main document processing begins.  The value is always treated as a
  string and never evaluated; if it does not contain a `=` character,
  then the variable is defined as the empty string (`''`).

@info.option('--execute', True)

: Execute the given arbitrary Python (not EmPy) statement before main
  document processing begins.

@info.option('--file', True)

: Execute the given Python (not EmPy) file before main document
  processing begins.

@info.option('--postfile', True)

: Execute the given Python (not EmPy) file after main document
  processing begins.

@info.option('--pause-at-end', True)

: Prompt for a line of input after all processing is complete.  Useful
  for systems where the window running EmPy would automatically
  disappear after EmPy exits (_e.g._, Windows).  By default, the input
  file used is `sys.stdin`, so this will not work when redirecting
  stdin to an EmPy process.  This can be changed with the `input`
  interpreter attribute.

@info.option('--relative-path', True)

: Prepend the location of the EmPy script to Python's `sys.path`.
  This is useful when the EmPy scripts themselves import Python .py
  modules in that same directory.

@info.option('--no-callback-error', True)

: If the custom markup is used without a registered callback, do not
  report an error.

@info.option('--no-ignore-bangpaths', True)

: Do not treat bangpaths as comments.  By default, bangpaths (starting
  lines that begin with the characters `#!`) are treated as comments
  and ignored.

@info.option('--none-symbol', True)

: The string to write when expanding the value `None`.  Defaults to
  `None`, which will result in no output.

@info.option('--no-expand-user', True)

: Do not expand user constructions (`~user`) in pathnames.  By default
  they are expanded.

@info.option('--no-auto-validate-icons', True)

: Do not auto-validate icons when an icon markup is first used.  See
  below.

@info.option('--starting-line', True)

: Specify an integer representing the default starting line for
  contexts.  Default is @info.config.startingLine.

@info.option('--starting-column', True)

: Specify an integer representing the default starting column for
  contexts.  Default is @info.config.startingColumn.

@info.option('--emoji-modules', True)

: A comma-separated list of emoji modules to try to use for the emoji
  markup (@`@:...:`).  See below.  Defaults to
  `@(','.join(info.config.emojiModuleNames))`.

@info.option('--no-emoji-modules', True)

: Only use `unicodedata` as an emoji module; disable all other emoji
  modules.

@info.option('--disable-emoji-modules', True)

: Disable all emoji module usage; just rely on the `emojis` attribute
  of the configuration.  See below.

@info.option('--ignore-emoji-not-found', True)

: When using emoji markup (@`@:...:`), do not raise an error when an
  emoji is not found; just pass the `:...:` text through.

@info.option('--binary', True)

: Operate in binary mode; open files in binary mode and use the
  `codecs` module for Unicode support.  This is necessary in older
  versions of Python 2._x_.

@info.option('--encoding', True)

: Specify both input and output Unicode encodings.  Requires
  specifying both an input and an output file.

@info.option('--input-encoding', True)

: Specify the input Unicode encoding.  Requires specifying an input
  file rather than `sys.stdout`.

  :::{note}
  
  Specifying a non-default encoding when using interactive mode
  (`sys.stdin`) raises a `ConfigurationError`.
  
  :::

@info.option('--output-encoding', True)

: Specify the output Unicode encoding.  Requires specifying an output
  file rather than `sys.stdout`.
  
  :::{note}
  
  Specifying a non-default encoding when using `sys.stdout` raises a
  `ConfigurationError`.
  
  :::

@info.option('--errors', True)

: Specify both [input and output Unicode error
  handlers](https://docs.python.org/3/library/functions.html#open).

@info.option('--input-errors', True)

: Specify the [input Unicode error
  handler](https://docs.python.org/3/library/functions.html#open).

  :::{note}
  
  Specifying a non-default error handler when using interactive mode
  (`sys.stdin`) raises a `ConfigurationError`.
  
  :::

@info.option('--output-errors', True)

: Specify the [output Unicode error
  handler](https://docs.python.org/3/library/functions.html#open).

  :::{note}
  
  Specifying a non-default error handler when using `sys.stdout`
  raises a `ConfigurationError`.
  
  :::

@info.option('--normalization-form', True)

: Specify the Unicode normalization to perform when using the
  diacritics markup (@`@^...`).  Specify an empty string (`''`) to
  skip normalization.  Defaults to `@info.config.normalizationForm`
  for modern versions of Python and `''` for very old versions of
  Python 2._x_.

@info.option('--no-auto-play-diversions', True)

: Before exiting, do not automatically play back any remaining
  diversions.  By default such diversions are played back.

@info.option('--no-check-variables', True)

: When modifying configuration variables, normally the existence and
  types of these variables is checked and if it doesn't exist or it is
  attempting to be assigned to an incompatible type, it will raise a
  `ConfigurationError`.  To override this behavior, use this flag.

@info.option('--context-format', True)

: Specify the format for printing contexts.  See below.

@info.option('--success-code', True)

: Specify the exit code for the Python interpreter on success.
  Defaults to @info.config.successCode.

@info.option('--failure-code', True)

: Specify the exit code for the Python interpreter when a processing
  error occurs.  Defaults to @info.config.failureCode.

@info.option('--unknown-code', True)

: Specify the exit code for the Python interpreter when an invalid
  configuration (such as unknown command line options) is encountered.
  Defaults to @info.config.unknownCode.

:::{seealso}

The list of command line options is available in the `options` help
topic and is summarized
[here](@info.ident.path{HELP.html#command-line-options-summary}).

:::


### Environment variables

The following environment variables are supported:

@info.option(em.OPTIONS_ENV, None)

: Specify additional command line options to be used.  These are in
  effect added to the start of the command line and parsed before
  any explicit command line options and processing begins.
  
  For example, this will run the EmPy interpreter as if the `-r` and
  `-d` command line options were specified:
  
  @info.shell{export EMPY_OPTIONS='-r -d'; em.py ...}{}
  
@info.option(em.CONFIG_ENV, True)

: Specify the configuration file(s) to process before main document
  processing begins.

@info.option(em.PREFIX_ENV, True)

: Specify the prefix to use when processing.

@info.option(em.PSEUDO_ENV, True)

: Specify the name of the pseudomodule/interpreter to use when
  processing.

@info.option(em.FLATTEN_ENV, True)

: If defined, flatten the globals before processing.

@info.option(em.RAW_ERRORS_ENV, True)

: If defined, after an error occurs, show the full Python tracebacks
  of the exception.

@info.option(em.INTERACTIVE_ENV, True)

: If defined, enter interactive mode by processing markup from
  `sys.stdin` after main document processing is complete.

@info.option(em.DELETE_ON_ERROR_ENV, True)

: If defined, when an error occurs, delete the corresponding output
  file.

@info.option(em.NO_PROXY_ENV, True)

: If defined, do not install a `sys.stdout` proxy.

@info.option(em.BUFFERING_ENV, True)

: Specify the desired file buffering.

@info.option(em.BINARY_ENV, True)

: If defined, use binary mode.

@info.option(em.ENCODING_ENV, None)

: Specify the desired input and output Unicode encodings.

@info.option(em.INPUT_ENCODING_ENV, True)

: Specify the desired input Unicode encoding only.

@info.option(em.OUTPUT_ENCODING_ENV, True)

: Specify the desired output Unicode encoding only.

@info.option(em.ERRORS_ENV, None)

: Specify the desired input and output Unicode error handler.

@info.option(em.INPUT_ERRORS_ENV, True)

: Specify the desired input Unicode error handler.

@info.option(em.OUTPUT_ERRORS_ENV, True)

: Specify the desired output Unicode error handler.

:::{seealso}

The list of environment variables is available in the `environ` help
topic and is summarized
[here](@info.ident.path{HELP.html#environment-variables-summary}).

:::

:::{note}

Environment variables were first introduced in EmPy version 2.2, and
revamped in version 4.0.

:::


### Configuration

**Configurations** are objects which determine the behavior of an EmPy
interpreter.  They can be created with an instance of the
`Configuration` class and have a set of attributes (**configuration
variables**) which can be modified.  Most configuration variables
correspond to a command line option.  The configuration instance also
contains supporting methods which are used by the interpreter which
can be overridden.

When configuration variables are modified, they are by default checked
to make sure have a known name and that they have the correct type; if
not, a `ConfigurationError` will be raised.  This behavior can be
disabled with @info.option('--no-check-variables', True).

When a configuration is assigned to an interpreter, it exists as a
`config` attribute of the `empy` pseudomodule and can be modified by a
running EmPy system.  Configurations can be shared between multiple
interpreters if desired.

@<<<[Configuration instances]
@{
empy.config.prefix = '$'
}$
${
print("The EmPy prefix is now $, not @!")
}$
>>>

:::{tip}

This example shows a quirk of changing configurations in the middle of
processing an EmPy document; the prefix changes from a `@@` to a `$`
by the end of the first statement markup, so a `$` and a newline is
required to suppress the trailing newline; a `@@` would have been sent
to the output unchanged since it is no longer the prefix.  Use
[configuration files](#configuration-files) to avoid issues like this,
as they are processed before any EmPy document or commands such as
@info.option('-P').

:::


#### Configuration files

**Configuration files** are snippets of Python (not EmPy) code which
can be executed under an EmPy system to modify the current
configuration.  By convention they have the extension .conf. though
this is not a requirement.  Configuration files are processed before
any expansion begins and are specified with the @info.option('-c',
True) command line option; a list of configuration files can be
specified with a `:` delimiter (`;` on Windows); the delimiter can be
specified with @info.option('--path-separator', True).  A nonexistent
configuration file specified in this way is an error unless
@info.option('-C', True) is specified.

When a configuration file is processed, its contents are executed in a
Python (not EmPy) interpreter and then any resulting variable
assignments are assigned to the configuration instance.  So:

@<<<python
prefix = '$'
>>>

is a simple configuration file which will change the EmPy prefix to
`$`.

Any resulting variable beginning with an underscore will be ignored.
Thus these variables can be used as auxiliary variables in the
configuration file.  For example, this configuration file will define
custom emojis for the numbered keycaps:

@<<<python
emojis = {}
for _x in range(10):
    emojis[str(_x)] = '{}\ufe0f\u20e3'.format(_x)
>>>

Finally, when a configuration file is processed, the current
configuration instance is presented as a variable named `_` (this can
be changed with @info.option('--config-variable', True)).  The
following example does the same as the previous example but uses the
dedicated variable:

@<<<python
_.emojis.update(((str(_x), '{}\ufe0f\u20e3'.format(_x)) for _x in range(10)))
>>>

:::{tip}

To make a set of configuration files automatic loaded by EmPy, use the
@info.option('EMPY_CONFIG') environment variable in your startup
shell:

@info.shell{export EMPY_CONFIG=~/path/to/default.conf}{}

To make a more general set of _options_ available, set `EMPY_OPTIONS`.

:::


#### Configuration variables

The following configuration variables exist with the given types and
their corresponding command line options and environment variables.
Default values are shown in brackets.  When a corresponding command
line option exists, See the [command line
options](#command-line-options) for more detailed information.

@info.option('name', True, True)

: The name of this configuration.  It is for organizational purposes
  and is not used directly by the EmPy system.

@info.option('notes', True, True)

: Arbitrary data about this configuration.  It can be anything from an
  integer to a string to a dictionary to a class instance, or its
  default, `None`.  It is for organizational purposes and is not used
  directly by the EmPy system.
  
@info.option('prefix', True, True)

: The prefix the interpreter is using to delimit EmPy markup.  Must be
  a single Unicode code point (character).

@info.option('pseudomoduleName', True, True)

: The name of the pseudomodule for this interpreter.

@info.option('verbose', True, True)

: If true, print debugging information before processing each EmPy
  token.
  
@info.option('rawErrors', True, True)

: If true, print a Python traceback for every exception that is thrown.

@info.option('exitOnError', True, True)

: If true, exit the EmPy interpreter after an error occurs.  If false,
  processing will continue despite the error.

@info.option('contextFormat', True, True)

: The string format to use to render contexts.  EmPy will
  automatically determine whether or not it should use the `%`
  operator or the `str.format` method with this format.  See [Context
  formatting](#context-formatting) for more details.

@info.option('goInteractive', True, True)

: When done processing the main EmPy document (if any), go into
  interactive mode by running a REPL loop with `sys.stdin`.  If such
  document is specified (_i.e._, EmPy is invoked with no arguments),
  go into interactive mode as well.
  
@info.option('deleteOnError', True, True)

: If an output file is chosen (_e.g._, with @info.option('-o') or one
  of the other such options) and an error occurs, delete the output
  file.  If this is set to true with output set to `sys.stdout`, a
  ConfigurationError will be raised.
  
@info.option('doFlatten', True, True)

: Flatten the contents of the `@info.config.pseudomoduleName`
  pseudomodule into the globals rather than having them all under the
  pseudomodule name.
  
@info.option('useProxy', True, True)

: If true, install a proxy object for `sys.stdout`.  This should be
  true if any output is being done via `print` or `sys.stdout.write`.
  
@info.option('relativePath', True, True)

: If true, the directory of the EmPy script's path will be prepended
  to Python's `sys.path`.

@info.option('buffering', True, True)

: Specify the buffering for the input and output files.

@info.option('noCallbackIsError', True, True)

: By default, not having a custom callback set when using custom
  markup (@`@<...>`) is an error.  If this is set to true, that error
  will be suppressed.

@info.option('replaceNewlines', True, True)

: If true, newlines in emoji names, Unicode character name escape
  markup, and code evaluation will be changed to spaces.  This can
  help when writing EmPy with a word-wrapping editor.
  
@info.option('ignoreBangpaths', True, True)

: If true, a bangpath (the first line of a file which starts with
  `#!`) will be treated as an EmPy comment, allowing the creation of
  EmPy executable scripts.  If false, it will not be treated specially
  and will be rendered to the output.
  
@info.option('noneSymbol', True, True)

: When an EmPy expansion evaluates to None (_e.g._, @`@(None)`), this
  is the string that will be rendered to the output stream.  If set to
  `None` (the default), no output will be rendered.

@info.option('missingConfigIsError', True, True)

: If a configuration file is specified with @info.option('-c') but
  does not exist, if this variable is true an error will be raised.
  
@info.option('pauseAtEnd', True, True)

: When done processing EmPy files, read a line from `sys.stdin` before
  exiting the interpreter.  This can be useful when testing under
  consoles on Windows.

@info.option('startingLine', True, True)

: The line to start with in contexts.

@info.option('startingColumn', True, True)

: The column to start with in contexts.

@info.option('significatorDelimiters', True, True)

: A 2-tuple of strings representing the prefix and suffix to add to
  significator names in order to determine what name to give them in
  the globals.

@info.option('emptySignificator', True, True)

: The default value to use for non-stringized significators.

@info.option('autoValidateIcons', True, True)

: When icons are used with a custom dictionary, a preprocessing phase
  needs to be done to make sure that all icon starting substrings are
  marked in the `icons` dictionary.  If this variable is false, this
  extra processing step will not be done; this is provided if the user
  wants to specify their own properly-validated icons dictionary and
  wishes to avoid a redundant step.
  
@info.option('emojiModuleNames', True, True)

: The list of names of supported emoji modules that the EmPy system
  will attempt t use at startup.

@info.option('emojiNotFoundIsError', True, True)

: If true, a non-existing emoji is an error.

@info.option('useBinary', True, True)

: If true, open files in binary mode.

@info.option('inputEncoding', True, True)

: The file input encoding to use.  This needs to be set before files
  are opened to take effect.

@info.option('outputEncoding', True, True)

: The file output encoding to use.  This needs to be set before files
  are opened to take effect.
  
@info.option('inputErrors', True, True)

: the file input error handler to use.  This needs to be set before files
  are opened to take effect.

@info.option('outputErrors', True, True)

: The file output error handler to use.  This needs to be set before files
  are opened to take effect.

@info.option('normalizationForm', True, True)

: The normalization form to use when applying diacritic combiners.
  Set to `None` or `''` in order to skip normalization.
  
@info.option('autoPlayDiversions', True, True)

: If diversions are extant when an interpreter is ready to exist, if
  this variable is true then those diversions will be undiverted to
  the output stream in lexicographical order by name.

@info.option('expandUserConstructions', True, True)

: If true, when processing configuration files, call
  `os.path.expanduser` on each filename to expand `~` and `~user`
  constructions.
  
@info.option('configVariableName', True, True)

: When processing configuration files, the existing configuration
  object can be referenced as a variable.  This indicates its name.

@info.option('successCode', True, True)

: The exit code to return when a processing is successful.

@info.option('failureCode', True, True)

: The exit code to return when an error occurs during processing.

@info.option('unknownCode', True, True)

: The exit code to return when a configuration error is found (and
  processing never starts).
  
@info.option('checkVariables', True, True)

: If true, configuration variables will be checked for existing and
  proper type n assignment.

@info.option('pathSeparator', True, True)

: The path separator to use when specifying multiple filenames with
  @info.option('-c').  Defaults to `;` on Windows and `:` on other
  platforms.

@info.option('controls', True, True)

: The controls dictionary used by the [named escape
  markup](#named-escape-markup).

@info.option('diacritics', True, True)

: The diacritic combiners dictionary used by the [diacritic
  markup](#diacritic-markup).

@info.option('icons', True, True)

: The icons dictionary used by the [icon markup](#icon-markup).

@info.option('emojis', True, True)

: The custom emojis dictionary which is referenced first by the [emoji
  markup](#emoji-markup).  Defaults to an empty dictionary.

:::{seealso}

The list of configuration variables is available in the `config` help
topic and is summarized
[here](@info.ident.path{HELP.html#configuration-variables-summary}).

:::

:::{note}

Configuration objects were introduced in EmPy version 4.0; previously
an underused options dictionary was introduced in version 2.2.2.

:::


#### Configuration methods

The following methods are supported by configuration instances:

`__init__(**kwargs)`

: The constructor.  Takes a set of keyword arguments that are then set
  as attributes in the configuration instance.  So
  
  ```python
  config = em.Configuration(prefix='$')
  ```
  
  is a shorter form of
  
  ```python
  config = em.Configuration()
  config.prefix = '$'
  ```

`isInitialized() -> bool`

: Has this instance been initialized?  Before initialization, no
  typechecking is done even if @info.option('checkVariables') is set.

`check(inputFilename, outputFilename)`

: Check the file settings against these filenames and raise a
  `ConfigurationError` is there appears to be an inconsistency.

`has(name) -> bool`

: Is this name an existing configuration variable?

`get(name, default=None) -> bool`

: Get the value of this configuration variable or return this default
  if it does not exist.

`set(name, value)`

: Set the configuration variable to the given value.

`update(**kwargs)`

: Set a series of configuration variables via a set of keyword
  arguments.

`run(statements)`

: Execute a series of configuration commands.

`load(filename, required=None)`

: Load and execute a configuration file.  If `required` is true, raise
  an exception; if false, ignore; if `None`, use the default for this
  configuration.

`path(path, required=None)`

: Load and execute one or more configuration files separated by the
  path separator.  `required` argument is the same as for `load`
  above.

`hasEnvironment(name) -> bool`

: Is the given environment variable defined, regardless of its value?

`environment(name, default=None, blank=None)`

: Get the value of the environment variable.  If it is not defined,
  return `default`; if it is defined but is empty, return `blank`.

`hasDefaultPrefix() -> bool`

: Is the @info.option('prefix') configuration variable set to the
  default?

`has{Full|No|Line|Fixed}Buffering() -> bool`

: Is buffering set to full, none, line, or some fixed value,
  respectively?

`createFactory([tokens]) -> Factory`

: Create a token factory from the list of token classes and return it.
  If `tokens` is not specified, use the default list.

`adjustFactory()`

: Adjust an existing factory to take into account a non-default prefix.

`getFactory([tokens], [force])`

: Get a factory, creating one if one has not yet been created, with
  the given `tokens` list (if not specified, a default list will be
  used).  If `force` is true, then create a new one even if one
  already exists.

`resetFactory()`

: Clear the current factory, if any.

`hasBinary() -> bool`

: Is binary (formerly called Unicode) support enabled?

`enableBinary([major, minor])`

: Enable binary support, conditionally if `major` and `minor` (the
  major and minor versions of Python) are specified and binary support
  is needed for this version of Python.

`disableBinary()`

: Turn off binary/Unicode support.

`isDefaultEncodingErrors([encoding, errors, asInput]) -> bool`

: Are both the file encoding and file error handler the default?
  Check for input if `asInput` is true, otherwise check for output.

`getDefaultEncoding([default]) -> str`

: Get the current default encoding, overriding with `default` if
  desired.

`open(filename, mode=None, buffering=-1, encoding=None, errors=None, expand=None) -> file`

: The main wrapper around the `open`/`codecs.open` call, allowing for
  seamless file opening in both binary and non-binary mode across all
  supported Python versions.

`significatorReString() -> str`

: Return a regular expression string that will match significators in
  EmPy code with this configuration's prefix.
  
  :::{hint}
  
  It can be used in Python like this:
  
  ```python
  data = open('script.em', 'r').read()
  for result in empy.config.significatorRe().findall(data):
      string2, key2, value2, string1, key1, value1 = result
      if key1:
          print("Single line significator: {} = {}{}".format(
              key1, value1, ' (stringized)' if string1 else ''))
       else: # key2
          print("Multi-line significator: {} = {}{}".format(
              key2, value2, ' (stringized)' if string2 else ''))
  ```

  :::

`significatorRe([flags]) -> re.Pattern`

: Return a compiled regular expression pattern object for this
  configuration's prefix.  Override the `re` `flags` if desired.

`significatorFor(key) -> str`

: Return the significator variable name for this significator key.

`setContextFormat(rawFormat)`

: Set the context format for this configuration.  See [context
  formatting](#context-formatting).

`renderContext(context) -> str`

: Render the given context using the existing context format string.

`calculateIconsSignature() -> tuple`

: Calculate the icons signature to try to detect any accidental
  changes.

`signIcons()`

: Calculate the icons signature and update the configuration with it.

`transmogrifyIcons([icons])`

: Process the icons dictionary and make sure any keys' prefixes are
  backfilled with `None` values.  This is necessary for the
  functioning of the [icon markup](#icon-markup).  This method will be
  called automatically unless @info.option('autoValidateIcons') is
  false.

`validateIcons([icons])`

: Check whether the icons have possibly changed and transmogrify them
  if necessary.

`initializeEmojiModules([moduleNames])`

: Scan for existing emoji modules and set up the appropriate internal
  data structures.  Use the list of module names in the configuration
  if `moduleNames` is not specified.

`substituteEmoji(text) -> str`

: Perform emoji substitution with the detected emoji modules.

`isSuccessCode(code) -> bool`

: Is this exit code a success code?

`isExitError(error) -> bool`

: Is this exception instance an exit error rather than a real error?

`errorToExitCode(error) -> int`

: Return an appropriate exit code for this error.

`isNotAnError(error) -> bool`

: Does this exception instance not represent an actual error?

`formatError(error[, prefix, suffix]) -> str`

: Return a string representing the details of the given exception
  instance, with an optional prefix and suffix.

:::{seealso}

The list of configuration methods is available in the `methods` help
topic and is summarized
[here](@info.ident.path{HELP.html#configuration-methods-summary}).

:::


### Error handlers

When an error occurs in an EmPy system, it is handled with an **error
handler**.  An error handler is a callable object that will respond to
the error, typically logging in.  If no user-specified error handler
is set, the default error handler is used, which prints a formatted
EmPy error message to `sys.stderr`.

The error handler can be set with the `empy.setHandler` method on the
pseudomodule/interpreter.  Only one error handler can be set at a
time.  The current handler can be queried with `empy.getHandler` and
the handler can be explicitly invoked with `empy.invokeHandler`.

The signature of the handler object when called is:

`handler(type, error, traceback) -> bool`

It takes the error type, the error instance, and the traceback object
corresponding to an exception (the return value of `sys.exc_info()`)
and returns an optional Boolean.  If the return value is true, the
default handler will _also_ be invoked after the set error handler is
called.  Not explicitly returning anything will implicitly return
`None`, a false value, and so will _not_ result in the default handler
being called afterward.

The interpreter will exit after handling an error if the configuration
variable @info.option('exitOnError') is true; the corresponding
command line option is @info.option('-k') which sets it to false.


## Reference

The following reference material is available:

### Getting version and debugging information

To print the version of EmPy you have installed, run:

@info.execute(['em.py', '-V', '# or: --version'])@

To print additional information including the Python implementation
and version, operating system, and machine type, run:

@info.execute(['em.py', '-W', '# or: --info'])@

For diagnostic details (say, to report a potential problem to the
developer), run:

@info.execute(['em.py', '-Z', '# or: --details'], lines=7)@


### Examples and testing

For quick examples of EmPy code, check out the examples throughout
this document.  For a more expansive tour of examples illustrating
EmPy features, check out tests/sample/sample.em.  For a real-world
example, check out README.md.em, which is the EmPy source file from
which this documentation is generated.

EmPy has an extensive testing system.  (If you have EmPy installed via
an operating system package that does not include the test system and
you wish to use it, [download the tarball](#getting-the-software).)

EmPy's testing system consists of the shell script test.sh and two
directories: tests and suites.  The tests directory contains the
unit/system tests, and the suites directory contains files with lists
of tests to run.  The test.sh shell script will run with any modern
Bourne-like shell.

Tests can be run changing to the directory where test.sh and both the
tests and suites directories are located, and then executing
`./test.sh` followed by the tests desired to be run following on the
command line.  For example, this runs a quick test:

@info.execute(['./test.sh', 'tests/sample/sample.em'])@

Specifying a directory will run all the tests contained in that
directory and all its subdirectories:

@info.execute(['./test.sh', 'tests/sample'])@

:::{warning}

The tests directory contains a superset of all tests for Python
versions, so running all the tests with `./test.sh tests` will
generate test failures.

:::

Suites can be run by using the @`@` character before the filename.  A
suite is a list of tests, one per line, to run:

@info.shell{./test.sh @@suites/default}{@
tests/common/callbacks/deregister.em (python3) [PASS]
tests/common/callbacks/deregister_twice.em (python3) [PASS]
tests/common/callbacks/get_none.em (python3) [PASS]
...
PASSES: 315/315
All tests passed (python3).
}@

To test a version of Python other than the default (_i.e._, that is, a
Python 3._x_ interpreter named `python3`), specify it with the
`-p` option to the test script and use that version's test suite.  To
test CPython 2.7, for instance:

@info.shell{./test.sh -p python2.7 @@suites/python2.7}{@
tests/common/callbacks/deregister.em (python2.7) [PASS]
tests/common/callbacks/deregister_twice.em (python2.7) [PASS]
tests/common/callbacks/get_none.em (python2.7) [PASS]
...
}@

Suites for all supported interpreters and versions are provided.  For
example, if you have PyPy 2.7 installed:

@info.shell{./test.sh -p pypy2.7 @@suites/pypy2.7}{@
tests/common/callbacks/deregister.em (pypy2.7) [PASS]
tests/common/callbacks/deregister_twice.em (pypy2.7) [PASS]
tests/common/callbacks/get_none.em (pypy2.7) [PASS]
...
}@

To only report errors ("quiet mode"), use the `-q` option:

@{
import subprocess

tests = subprocess.check_output(
    '''find $(cat suites/default | grep -v '^#') -name '*.em' | wc -l''', 
    shell=True, text=True).strip()
}@
@info.shell{./test.sh -q @@suites/default}{@
PASSES: @tests/@tests
All tests passed (python3).
}@

For more information about the testing tool, run:

@info.execute(['./test.sh', '-h', '# or: --help'], lines=1)@

:::{note}

A simple benchmark test system was introduced in EmPy version 2.1, and
was extended to a full unit and system tests suites for all supported
versions of Python in EmPy version 4.0.

:::


### Embedding EmPy

EmPy can be easily embedded into your Python programs.  Simply ensure
that the em.py file is available in the `PYTHONPATH` and import `em`
as a module:

```python
import em

print(em)
```

To embed an interpreter, create an instance of the `Interpreter`
class.  The interpreter constructor requires keyword arguments; [see
here for the list](#constructor).  One important argument to an
interpreter is a [configuration](#configuration), which should be
constructed first and then passed into the interpreter.  If no
configuration is specified, a default instance will be created and
used:

```python
import em

config = em.Configuration(...)
interp = em.Interpreter(config=config, ...)
```

Then call interpreter methods on it such as `write`, `expand`,
`evaluate`, `execute`, and so on.  The full list of interpreter
methods is [here](#interpreter-methods).

:::{important}

Since the EmPy system requires replacing the `sys.stdout` object with
a proxy so it can track all output, it is important to call the
`shutdown` method on the interpreter when complete.

:::

This can be done either with a `try`/`finally` statement or a `with`
statement:

```python
import em

interp = em.Interpreter(...)
try:
    ... do some things with the interpreter ...
finally:
    interp.shutdown()
    
# or ...

with em.Interpreter(...) as interp:
    ... do other things with the interpreter ...
```

:::{warning}

If you receive a `ConsistencyError` mentioning the proxy when quitting
your program, you are likely not calling the `shutdown` method on the
interpreter.  Make sure to call `shutdown` so the interpreter can
clean up after itself.

:::

There is also a global `em.expand` function which will expand a single
string, creating and destroying an interpreter to do so.  You can use
this function to do a one-off expansion of, say, a large file:

```python
import em

data = open('tests/sample/sample.em').read()
print(em.expand(data))
```


### Modules

A fully-functional EmPy system contains the following modules and files.


#### `@info.config.pseudomoduleName` pseudomodule

The pseudomodule is not an actual module, but rather the instance of
the running EmPy interpreter exposed to the EmPy system.  It is
automatically placed into the interpreter's globals and cannot be
imported explicitly.  See
[Pseudomodule/interpreter](#pseudomodule-interpreter) for details.


#### `em` module

The primary EmPy module.  It contains the `Configuration` and
`Interpreter` classes as well as all supporting logic.  An EmPy system
can be functional with only this module present if needed.
  
It also includes the following global functions:

{#details}
`details(level, [prelim, postlim, file])`
  
: Write details about the running system to the given file, which
  defaults to `sys.stdout`.  The `level` parameter is an attribute
  of the `em.Version` class (effectively an enum).

{#expand}
`expand(data, [config, globals, argv, name, **locals]) -> str`
  
: Create an interpreter with the given configuration, globals, argv,
  and name, and expand data.  If additional keyword arguments are
  specified, use those as the locals dictionary.

{#invoke}
`invoke(args, [config, globals, output, callback, handler, errors])`
  
: Invoke the EmPy system with the given command line arguments and
  optional settings.  This is the entry point used by the main EmPy
  function.


#### `emlib` module

The EmPy supporting library.  It contains the base classes `Filter`
and `Hook` to assist in creating this supporting functionality.


#### `emhelp` module

The EmPy help system.  It can be accessed from the main executable
with the @info.option('-h', True) and @info.option('-H', True) command
line options.  If the emlib module is not available to the executable,
the help system will return an error.


#### `emdoc` module

The EmPy documentation system, used to create this document.


### Using EmPy with build tools

If you're using EmPy to process documents within a build system such
as GNU Make or Ninja, you'll want to use the @info.option('-o') (or
@info.option('-a')) and @info.option('-d') options together.  This
will guarantee that a file will be output (or appended) to a file
without shell redirection, and that the file will be deleted if an
error occurs.  This will prevent errors from leaving a partial file
around which subsequent invocations of the build system will mistake
as being up to date.  The invocation of EmPy should look like this
(the `--` is not required if the input filename never starts with a
dash):

```shell
em.py -d -o $output -- $input
```

For GNU Make:

```@`make

EMPY ?= em.py
EMPY_OPTIONS ?= -d

%: %.em
        $(EMPY) $(EMPY_OPTIONS) -o $@ -- $<
````

For Ninja:

```ninja
empy = em.py
empy_options = -d

rule empy
    command = $empy $empy_options -o $out -- $in
```


### Context formatting

**Contexts** are objects which contain the filename, the line number,
the column number, and the character (Unicode code point) number to
record the location of an EmPy error during processing.

These are formatted into human-readable strings with a **context
format**, a string specifiable with @info.option('--context-format',
True).  A few different mechanisms for formatting contexts are
available:

| Mechanism | Description | Example
| --- | --- | --- |
| format | Use the `str.format` method | `{name}:{line}:{column}` |
| operator | Use the `%` operator | `%(name)s:%(line)d:%(column)d` |
| variable | Use `$` variables | `$NAME:$LINE:$COLUMN` |

The default context format is `@info.config.defaultContextFormat` and
uses the operator mechanism for backward compatibility.

When a context format is set, EmPy will attempt to detect which of the above mechanisms is needed:

| Mechanism | Criteria |
| --- | --- |
| format | string begins with `format:` or does not contain a `%` |
| operator | string begins with `operator:` or contains a `%` | 
| variable | string begins with `variable:` |

  
### Data flow

**input @:-->: interpreter @:-->: diversions @:-->: filters @:-->: output**

Here, in summary, is how data flows through a working EmPy system:

1. Input comes from a source, such as an .em file on the command line,
   `sys.stdin`, or via an `empy.include` statement.

2. The interpreter processes this material as it comes in,
   processing EmPy expansions as it goes.

3. After interpretation, data is then sent through the diversion
   layer, which may allow it directly through (if no diversion is
   in progress) or defer it temporarily.  Diversions that are
   recalled initiate from this point.

4. Any filters in place are then used to filter the data and
   produce filtered data as output.

5. Finally, any material surviving this far is sent to the output
   stream.  That stream is `sys.stdout` by default, but can be changed
   with the @info.option('-o') or @info.option('-a') options.

6. If an error occurs, execute the error handler (which by default
   prints an EmPy error) If the @info.option('-r') option is
   specified, then print a full Python traceback.  If
   @info.option('-k') is specified, continue processing rather than
   exit; otherwise halt.

7. On unsuccessful exit, if @info.option('-d') is specified, delete any
   specified output file.


### Glossary

The following terms with their definitions are used by EmPy:

*callback*

: The user-provided callback which is called when the custom markup
  @`@<...>` is encountered.
  
*command*

: A processing step which is performed before or after main document
  processing.  Examples are @info.option('-D'), @info.option('-F') or
  @info.option('-P').

*configuration*

: An object encapsulating all the configurable behavior of an
  interpreter which passed into interpreter on creation.
  Configurations can be shared between multiple interpreters.

*context*

: An object which tracks the location of the parser in an EmPy file
  for tracking and error reporting purposes.

*control markup*

: A markup used to direct high-level control flow within an EmPy
  session.  Control markups are expressed with the @`@[...]` notation.

*custom*

: The custom markup invokes a callback which is provided by the user,
  allowing any desired behavior.  Custom markup is @`@<...>`.

*diacritic*

: A markup which joins together a letter and one or more combining
  characters from a dictionary in the configuration and outputs it.
  Diacritic markup is @`@^...`.

*diversion*

: A process by which output is deferred, and can be recalled later on
  demand, multiple times if desired.

*document*

: An EmPy file containing EmPy markup to expand.

*emoji*

: A markup which looks up a Unicode code point by name via a
  customizable set of installable emoji modules, or via a dictionary
  in the configuration.  Emoji markup is @`@:...:`.

*error*

: An exception thrown by a running EmPy system.  When these occur,
  they are passed to an error handler.

*escape*

: A markup designed to expand to a single (often non-printable)
  character, similar to escape sequences in C or other languages.
  Escape markup is @`@\...`.

*expansion*

: The process of processing EmPy markups and producing output.

*expression*

: An expression markup represents a Python expression to be evaluated,
  and replaced with the `str` of its value.  Expression markup is
  @`@(...)`.

*file*

: An object which exhibits a file-like interface (methods such as
  `write` and `close`).

*filter*

: A file-like object which can be chained to other filters or the
  final stream, and can buffer, alter, or manipulate in any way the
  data sent.  Filters can be chained together in arbitrary order.

*finalizer*

: A function which is called when an interpreter exits.  Multiple
  finalizers can be added to each interpreter.

*globals*

: The dictionary (or dictionary-like object) which resides inside the
  interpreter and holds the currently-defined variables.
  
*handler*

: An error handler which is called whenever an error occurs in the
  EmPy system.  The default error handler prints details about the
  error to `sys.stderr`.

*hook*

: A callable object that can be registered in a dictionary, and which
  will be invoked before, during, or after certain internal
  operations, identified by name with a string.  Some types of hooks
  can override the behavior of the EmPy interpreter.

*icon*

: A markup which looks up a variable-length abbreviation for a string
  from a lookup table in the configuration.  Icon markup is @`@|...`.

*interpreter*

: The application (or class instance) which processes EmPy markup.

*locals*

: Along with the globals, a locals dictionary can be passed into
  individual EmPy API calls.

*markup*

: EmPy substitutions set off with a prefix (by default @`@`) and
  appropriate delimiters.

*named escape*

: A control character referenced by name in an escape markup,
  @`@\^{...}`.

*output*

: The final destination of the result of processing an EmPy file.

*prefix*

: The Unicode code point (character) used to set off an expansions.
  By default, the prefix is @`@`.  If set to `None`, no markup will be
  processed.

*processor*

: An extensible system which processes a group of EmPy files, usually
  arranged in a filesystem, and scans them for significators.

*proxy*

: An object which replaces the `sys.stdout` file object and allows the
  EmPy system to intercept any indirect output to `sys.stdout` (say,
  by the `print` function).

*pseudomodule*

: The module-like object named `empy` (by default) which is exposed as
  a global inside every EmPy system.  The pseudomodule and the
  interpreter are in fact the same object, an instance of the
  `Interpreter` class.

*significator*

: A special form of an assignment markup in EmPy which can be easily
  parsed externally, primarily designed for representing uniform
  assignment across a collection of files.  Significator markup is
  @`@% ...`.

*statement*

: A line of code that needs to be executed; statements do not have
  return values.  Statement markup is @`@{...}`.

*stream*

: A file-like object which manages diversion and filtering.  A stack
  of these is used by the interpreter with the top one being active.
  
*system*

: A running EmPy environment.
  
*token*

: An element of EmPy parsing.  Tokens are parsed and then processed
  one at a time.


### Statistics

@{
files = (glob.glob('*.py') + glob.glob('*.sh') +
    glob.glob('*.md') + glob.glob('README.md.em'))

info.execute(['wc'] + files)
info.execute(['sha1sum'] + files)
}@


## End notes
### Author's notes

I originally conceived EmPy as a replacement for my [Web templating
system](http://www.alcyone.com/max/info/m4.html) which uses
[m4](https://www.gnu.org/software/m4/), a general macroprocessing
system for Unix.

Most of my Web sites use a variety of m4 files, some of which are
dynamically generated from databases, which are then scanned by a
cataloging tool to organize them hierarchically (so that, say, a
particular m4 file can understand where it is in the hierarchy, or
what the titles of files related to it are without duplicating
information); the results of the catalog are then written in database
form as an m4 file (which every other m4 file implicitly includes),
and then GNU Make converts each m4 to an HTML file by processing it.

As the Web sites got more complicated, the use of m4 (which I had
originally enjoyed for the challenge and abstractness) really started
to become an impediment to serious work; while I was very
knowledgeable about m4 -- having used it for so many years -- getting
even simple things done with it is awkward and often difficult.  Worse
yet, as I started to use Python more and more over the years, the
cataloging programs which scanned the m4 and built m4 databases were
migrated to Python and made almost trivial, but writing out huge
awkward tables of m4 definitions simply to make them accessible in
other m4 scripts started to become almost farcical.

It occurred to me what I really wanted was an all-Python solution.
But replacing what used to be the m4 files with standalone Python
programs would result in somewhat awkward programs normally consisting
mostly of unprocessed text punctuated by small portions where
variables and small amounts of code need to be substituted.  Thus the
idea was a sort of inverse of a Python interpreter: a program that
normally would just pass text through unmolested, but when it found a
special signifier would execute Python code in a normal environment.
I looked at existing Python templating systems, and didn't find
anything that appealed to me -- I wanted something where the desired
markups were simple and unobtrusive.  After considering choices of
prefixes, I settled on @`@` and EmPy was born.

As I developed the tool, I realized it could have general appeal, even
to those with widely varying problems to solve, provided the core tool
they needed was an interpreter that could embed Python code inside
templated text.  As I continue to use the tool, I have been adding
features as unobtrusively as possible as I see areas that can be
improved.

A design goal of EmPy is that its feature set should work on several
levels; at any given level, if the user does not wish or need to use
features from another level, they are under no obligation to do so --
in fact, they wouldn't even need to know they exist.  If you have no
need of diversions, for instance, you are under no obligation to use
them or even to know anything about them.  If significators will not
help you organize a set of EmPy scripts globally, then you can ignore
them.  New features that are being added are whenever feasible
transparently backward compatible (except for major version releases);
if you do not need them, their introduction should not affect you in
any way.  Finally, the use of unknown prefix and escape sequences
results in errors, ensuring that they are reserved for future use.


### Acknowledgements

Questions, suggestions, bug reports, evangelism, and even complaints
from many people over the years have helped make EmPy what it is
today.  Some, but by no means all, of these people are (in
alphabetical order by surname):

- Biswapesh Chattopadhyay
- Beni Cherniavsky
- Dr. S. Candelaria de Ram
- Eric Eide
- Dinu Gherman
- Grzegorz Adam Hankiewicz
- Robert Kroeger
- Bohdan Kushnir
- Kouichi Takahashi
- Ville Vainio


### Known issues and caveats

- A running EmPy system is just an alternate form of a Python
  interpreter; EmPy code is just as powerful as any Python code.  Thus
  it is vitally important that an EmPy system not expand EmPy markup
  from an untrusted source; this is just as unsafe and potentially
  dangerous as executing untrusted Python code.

- To function properly, EmPy must override `sys.stdout` with a proxy
  file object, so that it can capture output of side effects and
  support diversions for each interpreter instance.  It is important
  that code executed in an environment _not_ rebind `sys.stdout`,
  although it is perfectly legal to reference it explicitly (_e.g._,
  @`@sys.stdout.write("Hello world\n")`).  If one really needs to
  access the "true" stdout, then use `sys.__stdout__` instead (which
  should also not be rebound).  EmPy uses the standard Python error
  handlers when exceptions are raised in EmPy code, which print to
  `sys.stderr`.  `sys.stderr`, `sys.__stdout__`, and `sys.__stderr__`
  are never overridden by the interpreter; only `sys.stdout` is.

- Using EmPy with threads, each of which may be creating arbitrary
  output, can get messy (just like with any other threaded system).
  Either serialize everything yourself through the `sys.stdout` proxy,
  or use @info.option('--no-proxy') and process all output yourself
  through the `output` attribute of the interpreter.

- The `empy` "module" exposed through the EmPy interface (_e.g._,
  @`@empy`) is an artificial module.  It is automatically exposed in
  the globals of a running interpreter and it cannot be manually
  imported with the `import` statement (nor should it be -- it is an
  artifact of the EmPy processing system and does not correspond
  directly to any .py file).

- For an EmPy statement expansion all alone on a line, _e.g._, @`@{a =
  1}`, will include a blank line due to the newline following the
  closing curly brace.  To suppress this blank line, use the symmetric
  convention @`@{a = 1}@`, where the final @`@` markup precedes the
  newline, making it whitespace markup and thus consumed.  For
  instance:
  
  ```@`
  @{a = 1}
  There will be an extra newline above (following the closing brace).
  Compare this to:
  @{a = 1}@
  There will be no extra newline above.
  ````

- Contexts (such as `empy.identify`) track the context of executed
  _EmPy_ code, not Python code.  This means, for instance, that blocks
  of code delimited with @`@{` and `}` will identify themselves as
  appearing on the line at which the @`@{` appears.  If you're
  tracking errors and want more information about the location of the
  errors from the Python code, use the @info.option('-r') option, which
  will provide you with the full Python traceback.

- The @`@[for]` variable specification supports tuples for tuple
  unpacking, even recursive tuples.  However, it is limited in that
  the names included may only be valid Python identifiers, not
  arbitrary Python "lvalues."  Since the internal Python mechanism is
  very rarely used for this purpose, this is not thought to be a
  significant limitation.  As a concrete example:
  
  ```python
  a = [None]
  for a[0] in range(5):
      print(a)
  ```
  
  is valid Python but the EmPy equivalent with @`@[for a[0] in
  range(5)]...` is invalid in EmPy.

- The `:=` joint assignment/testing syntax for `while` and `for` loops
  is not supported in the EmPy equivalent control markups @`@[while]`
  and @`@[for]`.  This may be supported in the future.
  
- String exceptions are not handled properly, but they have been
  deprecated since Python 2.5 and invalid since Python 2.6.


### For package maintainers

EmPy can be made available as an operating system/distribution package
in several different ways.  Regardless of the high-level organization,
the installed .py Python files must be made available as an importable
Python module, with the additional requirement that em.py must be made
available as an executable in the default `PATH`.  If necessary, this
executable may also be named `empy`, but `em.py` is preferred -- and
either way it is still important that the em.py file be available for
importing as a Python module (`em`).

Here is a breakdown of the contents of a release tarball:

| File | Description |
| --- | --- |
| em.py | Main EmPy module and executable |
| emhelp.py | Help subsystem module |
| emlib.py | Supplementary EmPy facilities module |
| emdoc.py | Documentation subsystem module |
| LICENSE.md | Software license |
| README.md | README (this file) |
| README.md.em | README source file |
| doc | HTML documentation hierarchy |
| test.sh | Test shell script |
| tests | Tests directory hierarchy |
| suites | Test suites directory hierarchy |

They can either be bundled up into a single, monolithic package, or
divided into a series of subpackages:

`empy-minimal`

: Just the em.py file, available as a Python module as well as an
  executable.  Note that this will not allow the use of the EmPy help
  subsystem, unless the module emhelp.py is also included.

`empy-basic`

: The LICENSE.md and README.md files, all the .py files (em.py,
  emhelp.py, emlib.py, emdoc.py) available as Python modules, with the
  em.py file also available as an executable.

`empy-doc`

: Just the contents of the README source file README.md.em and the
  docs directory hierarchy.
  
`empy-test`

: The test script test.sh, the tests directory, and the suites
  directory.

`empy`

: All of the above.


### Reporting bugs

If you find a bug in EmPy, please follow these steps:

1. Whittle a reproducible test case down to the smallest standalone
   example which demonstrates the issue, the smaller the better;
   
2. Collect the output of `em.py -Z` (this will provide detailed
   diagnostic details about your environment), or at least `em.py -W`
   (which provides only basic details);
   
3. [Send me an email](mailto:software@@alcyone.com) with _EmPy_ in the
   Subject line including both files and a description of the problem.

Thank you!


### Release history

4.0 (2023 Nov 29)

: A very large refresh, revamp and expansion of the EmPy system and
  documentation with too many changes to summarize here.  See the
  [release announcement](@info.ident.path{ANNOUNCE.html}) and the
  [Full list of changes between EmPy 3._x_ and 4.0
  section](@info.ident.path{ANNOUNCE.html#full-list-of-changes-between-empy-3-x-and-4-0})
  for the full list.

3.3.4a (2021 Nov 19)

: Fix an error in the setup.py in the downloadable tarball (did not
  affect PIP downloads).

3.3.4 (2019 Feb 26)

: Minor fix for a Python 3 compatibility issue.

3.3.3 (2017 Feb 12)

: Fix for `empy.defined` interpreter method.

3.3.2 (2014 Jan 24)

: Additional fix for source compatibility between 2._x_ and 3.0.

3.3.1 (2014 Jan 22)

: Source compatibility for 2._x_ and 3.0; 1._x_ compatibility dropped.

3.3 (2003 Oct 27)

: Custom markup @`@<...>`; remove separate pseudomodule instance for
  greater transparency; deprecate `Interpreter` attribute of
  pseudomodule; deprecate auxiliary class name attributes associated
  with pseudomodule in preparation for separate support library in
  4.0; add @info.option('--no-callback-error') and
  `--no-bangpath-processing` [now @info.option('--no-ignore-bangpaths')]
  command line options; add `atToken` hook.

3.2 (2003 Oct 7)

: Reengineer hooks support to use hook instances; add @info.option('-v')
  and @info.option('--relative-path') option; reversed PEP 317 style;
  modify Unicode support to give less confusing errors in the case of
  unknown encodings and error handlers; relicensed under LGPL.

3.1.1 (2003 Sep 20)

: Add string literal @`@"..."` markup; add
  @info.option('--pause-at-end') option; fix improper globals collision
  error via the `sys.stdout` proxy.

3.1 (2003 Aug 8)

: Unicode support (Python 2.0 and above); add Document and Processor
  helper classes for processing significators [later moved to
  `emlib`]; add @info.option('--no-prefix') option for suppressing all
  markups.

3.0.4 (2003 Aug 7)

: Implement somewhat more robust "lvalue" parsing for @`@[for]`
  construct (thanks to Beni Cherniavsky for inspiration).

3.0.3 (2003 Jul 9)

: Fix bug regarding recursive tuple unpacking using @`@[for]`; add
  `empy.saveGlobals`, `empy.restoreGlobals`, and `empy.defined`
  functions.

3.0.2 (2003 Jun 19)

: @`@?` and @`@!` markups for changing the current context name and
  line, respectively; add `update` method to interpreter; new and
  renamed context operations, `empy.setContextName`,
  `empy.setContextLine`, `empy.pushContext`, `empy.popContext`.

3.0.1 (2003 Jun 9)

: Fix simple bug preventing command line preprocessing directives
  (@info.option('-I'), @info.option('-D'), @info.option('-E'),
  @info.option('-F'), @info.option('-P')) from executing properly;
  defensive PEP 317 compliance [defunct].

3.0 (2003 Jun 1)

: Replace substitution markup with control markup @`@[...]`; support
  @`@(...?...!...)` for conditional expressions; add acknowledgements
  and glossary sections to documentation; rename buffering option back
  to @info.option('-b'); add @info.option('-m', True) and
  @info.option('-n', True) for suppressing `sys.stdout` proxy; rename
  main error class to `Error`; add standalone `expand` function; add
  `--binary` and `--chunk-size` options [defunct]; reengineer parsing
  system to use Tokens for easy extensibility; safeguard curly braces
  in simple expressions [now used by functional expressions] by making
  them a parse error; fix bug involving custom Interpreter instances
  ignoring globals argument; distutils support.

2.3 (2003 Feb 20)

: Proper and full support for concurrent and recursive interpreters;
  protection from closing the true stdout file object; detect edge
  cases of interpreter globals or `sys.stdout` proxy collisions; add
  globals manipulation functions `empy.getGlobals`, `empy.setGlobals`,
  and `empy.updateGlobals` which properly preserve the `empy`
  pseudomodule; separate usage info out into easily accessible lists
  for easier presentation; have `-h` option show simple usage and `-H`
  show extended usage [defunct]; add `NullFile` utility class [defunct].

2.2.6 (2003 Jan 30)

: Fix a bug in the `Filter.detach` method (which would not normally be
  called anyway).

2.2.5 (2003 Jan 9)

: Strip carriage returns out of executed code blocks for DOS/Windows
  compatibility.

2.2.4 (2002 Dec 23)

: Abstract Filter interface to use methods only; add @`@[noop: ...]`
  substitution for completeness and block commenting [defunct].

2.2.3 (2002 Dec 16)

: Support compatibility with Jython by working around a minor
  difference between CPython and Jython in string splitting.

2.2.2 (2002 Dec 14)

: Include better docstrings for pseudomodule functions; segue to a
  dictionary-based options system for interpreters; add
  `empy.clearAllHooks` and `empy.clearGlobals`; include a short
  documentation section on embedding interpreters; fix a bug in
  significator regular expression.

2.2.1 (2002 Nov 30)

: Tweak test script to avoid writing unnecessary temporary file; add
  `Interpreter.single` method; expose `evaluate`, `execute`,
  `substitute` [defunct], and `single` methods to the pseudomodule;
  add (rather obvious) `EMPY_OPTIONS` environment variable support;
  add `empy.enableHooks` and `empy.disableHooks`; include optimization
  to transparently disable hooks until they are actually used.

2.2 (2002 Nov 21)

: Switched to -V option for version information;
  `empy.createDiversion` for creating initially empty diversion;
  direct access to diversion objects with `empy.retrieveDiversion`;
  environment variable support; removed `--raw` long argument (use
  @info.option('--raw-errors') instead); added quaternary escape code
  (well, why not).

2.1 (2002 Oct 18)

: `empy.atExit` [now `empy.appendFinalizer`] registration separate
  from hooks to allow for normal interpreter support; include a
  benchmark sample and test.sh verification script; expose
  `empy.string` directly; @info.option('-D') option for explicit defines
  on command line; remove ill-conceived support for @`@else:`
  separator in @`@[if ...]`  substitution [defunct]; handle nested
  substitutions properly [defunct]; @`@[macro ...]`  substitution for
  creating recallable expansions [defunct].

2.0.1 (2002 Oct 8)

: Fix missing usage information; fix `after_evaluate` hook not getting
  called [defunct]; add `empy.atExit` [now `empy.appendFinalizer`]
  call to register a finalizer.

2.0 (2002 Sep 30)

: Parsing system completely revamped and simplified, eliminating a
  whole class of context-related bugs; builtin support for buffered
  filters; support for registering hooks; support for command line
  arguments; interactive mode with @info.option('-i'); significator
  value extended to be any valid Python expression.

1.5.1 (2002 Sep 24)

: Allow @`@]` to represent unbalanced close brackets in @`@[...]`
  markups [defunct].

1.5 (2002 Sep 18)

: Escape codes (@`@\...`); conditional and repeated expansion
  substitutions [defunct]; replaced with control markups]; fix a few
  bugs involving files which do not end in newlines.

1.4 (2002 Sep 7)

: Add in-place markup @`@:...:...:` [now @`@$...$...$`]; fix bug with
  triple quotes; collapse conditional and protected expression
  syntaxes into the single generalized @`@(...)` notation;
  `empy.setName` and `empy.setLine` functions [now
  `empy.setContextName` and `empy.setContextLine`]; true support for
  multiple concurrent interpreters with improved `sys.stdout` proxy;
  proper support for `empy.expand` to return a string evaluated in a
  subinterpreter as intended; merged Context and Parser classes
  together, and separated out Scanner functionality.

1.3 (2002 Aug 24)

: Pseudomodule as true instance; move toward more verbose (and clear)
  pseudomodule functions; fleshed out diversions model; filters;
  conditional expressions; protected expressions; preprocessing with
  @info.option('-P') (in preparation for possible support for command
  line arguments).

1.2 (2002 Aug 16)

: Treat bangpaths as comments; `empy.quote` for the opposite process
  of `empy.expand`; significators (@`@%...`  sequences); add
  @info.option('-I') and @info.option('-f') options; much improved
  documentation.

1.1.5 (2002 Aug 15)

: Add a separate `invoke` function that can be called multiple times
  with arguments to simulate multiple runs.

1.1.4 (2002 Aug 12)

: Handle strings thrown as exceptions properly; use `getopt` to
  process command line arguments; cleanup file buffering with
  AbstractFile; very slight documentation and code cleanup.

1.1.3 (2002 Aug 9)

: Support for changing the prefix from within the `empy` pseudomodule.

1.1.2 (2002 Aug 5)

: Renamed buffering option [defunct], added @info.option('-F') option
  for interpreting Python files from the command line, fixed improper
  handling of exceptions from command line options (@info.option('-E'),
  @info.option('-F')).

1.1.1 (2002 Aug 4)

: Typo bugfixes; documentation clarification.

1.1 (2002 Aug 4)

: Added option for fully buffering output (including file opens),
  executing commands through the command line; some documentation
  errors fixed.

1.0 (2002 Jul 23)

: Renamed project to EmPy.  Documentation and sample tweaks; added
  `empy.flatten` [now `empy.flattenGlobals`]; added @info.option('-a')
  option.  First official release.

0.3 (2002 Apr 14)

: Extended "simple expression" syntax, interpreter abstraction, proper
  context handling, better error handling, explicit file inclusion,
  extended samples.

0.2 (2002 Apr 13)

: Bugfixes, support non-expansion of `None`s, allow choice of alternate
  prefix.

0.1.1 (2002 Apr 12)

: Bugfixes, support for Python 1.5._x_ [defunct], add
  @info.option('-r') option.

0.1 (2002 Apr 12)

: Initial early access release.


### Contact

This software was written by [Erik Max
Francis](http://www.alcyone.com/max/).  If you use this software, have
suggestions for future releases, or bug reports or problems with this
documentation, [I'd love to hear about
it](mailto:@info.ident.contact).

Even if you try out EmPy for a project and find it unsuitable, I'd
like to know what stumbling blocks you ran into so they can
potentially be addressed in a future version.

I hope you enjoy using @info.ident! @|E


### About this document

This document was generated with EmPy itself using the `emdoc` module.
Both the source (README.md.em) and the resulting Markdown text
(README.md) are included in the release tarball, as is the HTML
directory hierarchy generated with Sphinx (doc).

@info.summarize()@
