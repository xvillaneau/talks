#!/usr/bin/env bash

# Testing tool to measure the speed of N iterations of various
# implementations of the core look-and-say logic.
# N is the first argument to the script, defaults to 25.

HERE=$(dirname "$0")
pushd "$HERE" > /dev/null || exit 1

# Make Python recognize the modules in this directory
PYTHONPATH=$(realpath .):$PYTHONPATH
export PYTHONPATH

# Extract and test the DEPTH argument
DEPTH=$(python -c "print(int(${1:-25}))") || exit 1

for cmd in imperative regex groupby; do
  echo "Time for ${DEPTH} iterations of ${cmd}_look_and_say:"
  python -m timeit -s 'from look_and_say.timing import make_lns_test' \
                   -s "call = make_lns_test('${cmd}', depth=${DEPTH})" \
                   'call()'
done

popd > /dev/null || exit 1
