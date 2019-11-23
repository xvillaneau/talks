#!/usr/bin/env bash

# Testing tool to measure the speed of N iterations of various
# implementations of deep look-and-say methods.
# N is the first argument to the script, defaults to 25.

HERE=$(dirname "$0")
pushd "$HERE/.." > /dev/null || exit 1

# Make Python recognize the modules in this directory
PYTHONPATH=$(realpath .):$PYTHONPATH
export PYTHONPATH

# Extract and test the DEPTH argument
DEPTH=$(python -c "print(int(${1:-25}))") || exit 1

# for cmd in list recursive parallel cached cosmology; do
 for cmd in parallel cached cosmology; do
#for cmd in cosmology; do
  echo "Time for ${cmd} length at a depth of ${DEPTH}:"
  python -m timeit -s 'from look_and_say.timing import make_length_test' \
                   -s "call = make_length_test('${cmd}', depth=${DEPTH})" \
                   'call()'
done

popd > /dev/null || exit 1
