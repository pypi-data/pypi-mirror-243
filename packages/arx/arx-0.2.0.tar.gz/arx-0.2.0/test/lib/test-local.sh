# declare prerequisites for external binaries used in tests
# test_declare_external_prereq python

if [ -z "$TEST_DIRECTORY" ] ; then
    TEST_DIRECTORY=$(cd $(dirname $0)/.. && pwd)
fi

export SRC_DIRECTORY=$(cd "$TEST_DIRECTORY"/.. && pwd)
export PYTHONPATH="$SRC_DIRECTORY":$PYTHONPATH
export PYTHON=python3
export LOG_LEVEL=DEBUG

arx() {
    python3 -m arx "$@"
}    
