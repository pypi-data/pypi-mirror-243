#!/bin/sh

#
# defaults
#

export ROOT=${ROOT:=}
export PYTHON=${PYTHON:=python3}
export SCRIPT=${SCRIPT:=em.py}
export OPTIONS=${OPTIONS:=}

export EXT=${EXT:=.em}
export IN=${IN:=.in}
export OUT=${OUT:=.out}
export ERR=${ERR:=.err}
export XXX=${XXX:=.xxx}

export IGNORED=${IGNORED:=0}
export BLESSED=${BLESSED:=0}
export SUCCESS=${SUCCESS:=0}
export FAILURE=${FAILURE:=1}
export UNAVAIL=${UNAVAIL:=2}
export CURSED=${CURSED:=3}
export ABORTED=${ABORTED:=4}

export CALLOUT=${CALLOUT:=---}
export DELIMITER=${DELIMITER:=:::}
export DIFF=${DIFF:=diff}
export GREP=${GREP:=grep}
export NULL=${NULL:=/dev/null}
export TEMP=${TEMP:=/tmp/empy.test}

export MODE=${MODE:=test}

export DEBUG=${DEBUG:=false}
export CHECK=true
export BRIEF=false
export IGNORE=false
export KEEP=false
export QUIET=false
export REDIRECT=false
export VERBOSE=false

#
# functions
#

printUsage ()
{
    echo "Usage: $0 [<option>...] [--] (<file> | <directory> | @<suite>)..."

    if [ $# = 0 ]
    then
        return
    fi

    cat <<EOF
Run one or more EmPy tests, comparing the results to exemplars, and
return an exit code indicating whether all tests succeeded or whether
there were some failures.  If no tests are specified, this help is
displayed.  Test filenames, directory names, and suite names cannot
contain spaces.

A test is one of the following:
  - an individual $EXT test file to run;
  - a directory hierarchy containing $EXT test files to run; or
  - an at sign (\`@\`) followed immediately by a filename representing
    a test suite whose contents are a whitespace-separated list of
    individual tests, directories, or suites to run, with lines that
    start with \`#\` being ignored.

Before running tests, the interpreter is tested first to see if it is
functional (unless the --no-check option is provided).  If not, the
tests are skipped and an error is reported; if the --ignore option is
provided, this is not considered an error.

Each test is run with a separate interpreter invocation; any symbolic
links are followed.  If an $IN file is present, its contents are
divided into sections delimited with \`$DELIMITER SECTION $DELIMITER\`.  Allowed
input sections are:

  - arguments: A list of command line arguments to pass to EmPy
  - environment: A shell environment script to source before executing

An $OUT file must be present, and represents the exemplar test stdout.
If an $ERR file is present, then that represents the exemplar stderr
output; if no $ERR file is present, then no stderr output is expected.
If a $XXX file is present, its contents represent the exemplar exit
code; if none is present, the expected value is 0 (success).  If the
outputs differ from the exemplars, their diffs (first from stdout,
then from stderr) and the exit code are displayed.

Tests can be run in bless mode (with --bless), which will process the
$EXT files and set up necessary any $OUT, $ERR, and/or $XXX files,
marking the current outputs/exit codes as correct.  Subsequent
(non-blessing) test runs will then pass.

All corresponding environment variables (in brackets below) are
overridable from the environment, and all defaults are shown below.

Command line options:
  -h --help                Print this usage and exit
  -R --root DIRECTORY      cd here before running tests [ROOT]: $ROOT
  -D --diff COMMAND        Command to run to compare files [DIFF]: $DIFF
  -G --grep COMMAND        Command to run tog rep files [GREP]: $GREP
  -N --null FILE           File to use as an empty exemplar [NULL]: $NULL
  -p --python INTERP       Python interpreter to use [PYTHON]: $PYTHON
  -s --script SCRIPT       Python script to run [SCRIPT]: $SCRIPT
  -x --options OPTIONS     Script arguments to use [OPTIONS]: $OPTIONS
  -t --temp TEMP           The temporary file prefix [TEMP]: $TEMP
  -k --keep                Keep temporary output files
  -i --ignore              If present, a bad interpreter is not an error
  -v --verbose             Print stdout, stderr, and exit code of each test
  -b --brief               If present, do not print a summary
  -q --quiet               Only show failures
  -r --redirect            Use redirection rather than -o (non-standard scripts)
  -z --no-check            Don't check the interpreter before running tests
  -X --extension EXT       Filename extension for EmPy test files [EXT]: $EXT
  -I --input EXT           Filename extension for input [IN]: $IN
  -O --output EXT          Filename extension for stdout benchmark [OUT]: $OUT
  -E --error EXT           Filename extension for stderr benchmark [ERR]: $ERR
  -C --code EXT            Filename extension for exit code [XXX]: $XXX
  -m --mode MODE           Set run mode (test, bless, enuemrate) [MODE]: $MODE
  -0 --enumerate           Set mode: Enumerate tests instead of running
  -1 --test                Set mode: Run tests (default)
  -2 --bless               Set mode: Bless the specified tests as valid
  -3 --clean               set mode: Clean out results
     --debug               Show command line invocations before executing
  --                       Stop processing command line options

Tests can have the following possible results:
  - PASS: Test succeeded
  - FAIL.OUT: Script stdout output does not match $OUT
  - FAIL.ERR: Script stderr output does not match $ERR, if any
  - FAIL.XXX: EmPy process exited with error code not matching $XXX file, if any
  - BAD.GONE: Test $EXT file/directory is not present
  - BAD.MISS: Test $EXT file is present but with no corresponding $OUT file
  - BAD.FORM: Test $IN file is present but malformed
  - SKIP: Interpreter does not appear to be functional (not test-specific)

Sample usages:
  % ./test.sh [-h] # show this help
  % ./test.sh -p python2 # run Python 2.x (in the PATH)
  % ./test.sh -i -p python2.4 # missing interpreter is not an error
  % ./test.sh -p /usr/local/bin/jython3 sample.em # run custom interpreter
  % ./test.sh -q -s /path/to/em.py # run a different script; show only failures
  % ./test.sh tests # run all .em files under tests
  % ./test.sh --bless good # bless all these tests
  % ./test.sh @suites/all # run all .em files enumerated from suites/all

Exit codes:
  - Ignored; no tests were run [IGNORED]: $IGNORED
  - Blessed; all tests successfully blessed [BLESSED]: $BLESSED
  - Success; interpreter was present and EmPy passed [SUCCESS]: $SUCCESS
  - Failure; interpreter was present and EmPy failed [FAILURE]: $FAILURE
  - Unavailable; required interpreter was not available [UNAVAIL]: $UNAVAIL
  - Cursed; blessing failed, interpreter unavailable [CURSED]: $CURSED
  - Aborted; invalid command line options were detected [ABORTED]: $ABORTED
EOF
}

checkInterpreter ()
{
    if [ $CHECK = true ] && \
           ! $PYTHON -c "print(__import__('sys').version)" > $NULL 2> $NULL
    then
        echo "-- ($PYTHON) [SKIP]"
        summary=unavail
        return 1
    fi
}

initialize ()
{
    export stamp=$(date +'%Y%m%d%H%M%S')
    export prefix=$TEMP.$stamp.$$

    passes=0
    bads=0
    failures=0
    blesses=0
    cleans=0
    total=0
}

summarize ()
{
    # Report the summary.
    if [ $BRIEF = false ]
    then
        if [ $QUIET = false ]
        then
            echo
        fi

        if [ $MODE = bless ]
        then
            echo "BLESSES: $blesses/$total"
        elif [ $MODE = clean ]
        then
            echo "CLEANS: $cleans/$total"
        else
            [ $passes = 0 ] || echo "PASSES: $passes/$total"
            [ $failures = 0 ] || echo "FAILURES: $failures/$total"
            [ $bads = 0 ] || echo "BAD: $bads/$total"
        fi

        [ $summary = ignored ] && echo "No tests were run ($PYTHON)."
        [ $summary = blessed ] && echo "All tests blessed ($PYTHON)."
        [ $summary = success ] && echo "All tests passed ($PYTHON)."
        [ $summary = failure ] && echo "There were failures ($PYTHON)!"
        [ $summary = unavail ] && echo "No tests were run; interpreter unavailable ($PYTHON)!"
    fi

    # Figure out the test script exit code.
    [ $summary = ignored ] && CODE=$IGNORED
    [ $summary = blessed ] && CODE=$BLESSED
    [ $summary = success ] && CODE=$SUCCESS
    [ $summary = failure ] && CODE=$FAILURE
    [ $summary = unavail ] && CODE=$UNAVAIL

    # Goodbye.
    exit $CODE
}

unpackInputFile ()
{
    section=--

    while read -r line
    do
        if ! [ "$line" = "${line#$DELIMITER}" ]
        then
            section="${line#$DELIMITER}"
            section="${section%$DELIMITER}"
            section="${section# }" # remove the leading space, if present
            section="${section% }" # remove the trailing space, if present

            if ! [ $section = arguments ] && ! [ $section = environment ]
            then
                echo "*** Bad input file section: $section ($input)"
                return 1
            fi
        else
            if [ "$section" = "--" ]
            then
                echo "*** Input file does not start with \`$DELIMITER SECTION $DELIMITER\` ($input)"
                return 2
            fi

            echo "$line" >> $prefix.$total.$section
        fi
    done < $input
}

setupTest ()
{
    env=$NULL
    args=

    # Unpack any input file.
    if [ -f $input ]
    then
        if ! unpackInputFile
        then
            result=BAD.FORM
            bads=$((bads + 1))
            finalizeTest
            return
        fi
    fi

    # Check for a custom environment.
    if [ -f $prefix.$total.environment ]
    then
        env=$prefix.$total.environment
    fi

    # Check for custom args.
    if [ -f $prefix.$total.arguments ]
    then
        args=$(cat $prefix.$total.arguments)
    fi
}

executeTest ()
{
    if [ $DEBUG = true ]
    then
        echo DEBUG: $PYTHON $SCRIPT $OPTIONS $args -o $out $test
    fi

    # Run the test (possibly in a subshell).
    if [ $REDIRECT = true ]
    then
        if [ $env = $NULL ]
        then
            $PYTHON $SCRIPT $OPTIONS $args $test < $NULL > $out 2> $err
        else
            (. $env; $PYTHON $SCRIPT $OPTIONS $args $test < $NULL > $out 2> $err)
        fi
    else
        if [ $env = $NULL ]
        then
            $PYTHON $SCRIPT $OPTIONS -o $out $args $test < $NULL > $out2 2> $err
        else
            (. $env; $PYTHON $SCRIPT $OPTIONS -o $out $args $test \
                             < $NULL > $out2 2> $err)
        fi
    fi
    code=$?

    touch $out

    if [ -s $out2 ]
    then
        echo "$CALLOUT REDIRECTED STDOUT:" >> $out
        cat $out2 >> $out
    fi
}

verboseTest ()
{
    echo $CALLOUT $test STDOUT:
    cat $out

    if [ -s $err ]
    then
        echo $CALLOUT $test STDERR:
        cat $err
    fi

    if ! [ $code = 0 ]
    then
        echo $CALLOUT $test EXIT CODE: $code
    fi
    echo $CALLOUT
}

logTest ()
{
    # Log the result.
    if [ $result = ok ]
    then
        if [ $MODE = bless ]
        then
            result=BLESS
            blesses=$((blesses + 1))
        elif [ $MODE = clean ]
        then
            result=CLEAN
            cleans=$((cleans + 1))
        else
            result=PASS
            passes=$((passes + 1))
        fi
        [ $QUIET = false ] && echo "$test ($PYTHON) [$result]"
        if ! [ $summary = failure ]
        then
            if [ $MODE = bless ]
            then
                summary=blessed
            elif [ $MODE = clean ]
            then
                summary=cleaned
            else
                summary=success
            fi
        fi
    else
        echo "$test ($PYTHON) [$result]"
        summary=failure
    fi
}

wipeTest ()
{
    # Remove the temporary files, if desired.
    if [ $KEEP = false ]
    then
        rm -f $prefix*
    fi
}

finalizeTest ()
{
    logTest
    wipeTest
}

cleanTest ()
{
    # Clean the new exemplar .out, .err, and/or .xxx files.
    rm -f $stdout $stderr $stdcod
}

blessTest ()
{
    cleanTest

    # New exemplar .out.
    mv $out $stdout

    # New exemplar .err (if needed).
    if [ -s $err ]
    then
        mv $err $stderr
    fi

    # New exemplar .xxx (if needed).
    if ! [ $code = 0 ]
    then
        echo $code > $stdcod
    fi
}

checkTest ()
{
    if [ $DEBUG = true ]
    then
        echo DEBUG: $DIFF $stdout $out
    fi

    # Check exit code: Start by determining the expected
    # exit code.
    if [ -f $stdcod ]
    then
        # If there's a exemplar .xxx file, its contents are it.
        expected="$(cat $stdcod)"
    else
        # If not, it's 0 (success).
        expected=0
    fi

    # Check stdout output.
    if ! [ -f $stdout ]
    then
        # The exemplar stdout does not exist.
        $DIFF $NULL $out
        [ $result = ok ] && bads=$((bads + 1))
        [ $result = ok ] && result=BAD.MISS
    elif ! $DIFF $stdout $out
    then
        # The exemplar stdout differs.
        [ $result = ok ] && failures=$((failures + 1))
        [ $result = ok ] && result=FAIL.OUT
    fi
    # Check stderr output.
    if [ -f $stderr ]
    then
        if ! $DIFF $stderr $err
        then
            # The exemplar stderr exists and differs.
            [ $result = ok ] && failures=$((failures + 1))
            [ $result = ok ] && result=FAIL.ERR
        fi
    else
        if [ -s $err ]
        then
            # The exemplar stderr does not exist but stderr is not
            # empty.
            $DIFF $NULL $err
            [ $result = ok ] && failures=$((failures + 1))
            [ $result = ok ] && result=FAIL.ERR
        fi
    fi

    # Finally, check the error code.
    if ! [ $code = $expected ]
    then
        # The exemplar code differs.
        echo "* $code (should be $expected)"
        [ $result = ok ] && failures=$((failures + 1))
        [ $result = ok ] && result=FAIL.XXX
    fi
}

runTest ()
{
    test="$1"
    total=$((total + 1))

    if [ $MODE = enumerate ]
    then
        echo $test
        return
    fi

    result=ok
    name="${test%.*}"
    base=$(basename "$name")
    input=$name$IN
    stdout=$name$OUT
    stderr=$name$ERR
    stdcod=$name$XXX

    export out=$prefix.$total$OUT
    export out2=$prefix.$total$OUT.redirect
    export err=$prefix.$total$ERR

    setupTest
    executeTest

    if [ $VERBOSE = true ]
    then
        verboseTest
    fi

    if ! [ -e $test ]
    then
        # Test does not exist.
        result=BAD.GONE
        bads=$((bads + 1))
    else
        if [ $MODE = bless ]
        then
            blessTest
        elif [ $MODE = clean ]
        then
            cleanTest
        else
            checkTest
        fi
    fi

    finalizeTest
}

runTests ()
{
    for test in "$@"
    do
        runTest $test
    done
}

runSuites ()
{
    for suite in "$@"
    do
        if ! [ "${suite#@}" = "$suite" ]
        then
            # If it starts with an @, it's a file containing a list of
            # test suites; get the list and run them.
            suite="${suite#@}"
            if [ -f $suite ]
            then
                tests=$($GREP -v '^#' "$suite")
                runSuites $tests
            else
                # Suite file does not exist, so report a missing test.
                runTest @$suite
            fi
        elif [ -d "$suite" ]
        then
            # If it's a directory, then it's a directory (hierarchy);
            # find the list of tests.
            tests=$(find -L "$suite" -name "*$EXT" -type f | sort)
            runTests $tests
        else
            # Otherwise it's just an individual test.
            runTest $suite
        fi
    done
}

#
# run
#

summary=ignored

if [ $# = 0 ] || [ "$1" = "-h" ] || [ "$1" = "-?" ] || [ "$1" = "--help" ]
then
    printUsage "$@"

    exit $SUCCESS
fi

while ! [ "${1#-}" = "$1" ]
do
    if [ "$1" = "--" ]
    then
        shift
        break
    elif [ "$1" = "-R" ] || [ "$1" = "--root" ]
    then
        shift
        ROOT="$1"
        shift
    elif [ "$1" = "-D" ] || [ "$1" = "--diff" ]
    then
        shift
        DIFF="$1"
        shift
    elif [ "$1" = "-G" ] || [ "$1" = "--grep" ]
    then
        shift
        GREP="$1"
        shift
    elif [ "$1" = "-N" ] || [ "$1" = "--null" ]
    then
        shift
        NULL="$1"
        shift
    elif [ "$1" = "-p" ] || [ "$1" = "--python" ]
    then
        shift
        PYTHON="$1"
        shift
    elif [ "$1" = "-s" ] || [ "$1" = "--script" ]
    then
        shift
        SCRIPT="$1"
        shift
    elif [ "$1" = "-x" ] || [ "$1" = "--options" ]
    then
        shift
        OPTIONS="$1"
        shift
    elif [ "$1" = "-t" ] || [ "$1" = "--temp" ] || [ "$1" = "--prefix" ]
    then
        shift
        TEMP="$1"
        shift
    elif [ "$1" = "-k" ] || [ "$1" = "--keep" ]
    then
        shift
        KEEP=true
    elif [ "$1" = "-i" ] || [ "$1" = "--ignore" ]
    then
        shift
        IGNORE=true
        UNAVAIL=$SUCCESS
    elif [ "$1" = "-v" ] || [ "$1" = "--verbose" ]
    then
        shift
        VERBOSE=true
    elif [ "$1" = "-b" ] || [ "$1" = "--brief" ]
    then
        shift
        BRIEF=true
    elif [ "$1" = "-q" ] || [ "$1" = "--quiet" ]
    then
        shift
        QUIET=true
    elif [ "$1" = "-r" ] || [ "$1" = "--redirect" ]
    then
        shift
        REDIRECT=true
    elif [ "$1" = "-z" ] || [ "$1" = "--no-check" ]
    then
        shift
        CHECK=false
    elif [ "$1" = "-X" ] || [ "$1" = "--extension" ]
    then
        shift
        EXT="$1"
        shift
    elif [ "$1" = "-I" ] || [ "$1" = "--input" ]
    then
        shift
        IN="$1"
        shift
    elif [ "$1" = "-O" ] || [ "$1" = "--output" ]
    then
        shift
        OUT="$1"
        shift
    elif [ "$1" = "-E" ] || [ "$1" = "--error" ]
    then
        shift
        ERR="$1"
        shift
    elif [ "$1" = "-C" ] || [ "$1" = "--code" ]
    then
        shift
        XXX="$1"
        shift
    elif [ "$1" = "-m" ] || [ "$1" = "--mode" ]
    then
        shift
        MODE="$1"
        shift
    elif [ "$1" = "-0" ] || [ "$1" = "--enumerate" ]
    then
        shift
        MODE=enumerate
        BRIEF=true
    elif [ "$1" = "-1" ] || [ "$1" = "--test" ]
    then
        shift
        MODE=test
    elif [ "$1" = "-2" ] || [ "$1" = "--bless" ]
    then
        shift
        MODE=bless
        UNAVAIL=$CURSED
    elif [ "$1" = "-3" ] || [ "$1" = "--clean" ]
    then
        shift
        MODE=clean
        UNAVAIL=$CURSED
    elif [ "$1" = "--debug" ]
    then
        shift
        DEBUG=true
    else
        echo "Option not recognized: $1" 1>&2
        exit $ABORTED
    fi
done

if [ -n "$ROOT" ]
then
    cd "$ROOT"
fi

initialize

if checkInterpreter
then
    suites="$@"

    runSuites $suites
fi

summarize
