#!/usr/bin/env bash
# Sanity-checks every task: the starter must FAIL the verifier and the
# reference solution must PASS it.
set -u
cd "$(dirname "$0")/.."
status=0
for task in task_*; do
  if IMPL_DIR=starter python -m pytest -q -x "$task/tests" >/dev/null 2>&1; then
    echo "FAIL  $task: starter unexpectedly passes the verifier"; status=1
  else
    echo "ok    $task: starter fails as intended"
  fi
  if IMPL_DIR=solution python -m pytest -q "$task/tests" >/dev/null 2>&1; then
    echo "ok    $task: reference solution passes"
  else
    echo "FAIL  $task: reference solution does not pass"; status=1
  fi
done
exit $status
