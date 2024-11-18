#!/bin/bash
rm -rf ./pages/P114Aopticalclearing/{*,.*}
rm -rf ./prep/output/{*,.*}
python3 ./prep/make-slicers.py
OUTPUT="$(ruff check output)"

if [ "$OUTPUT" = "All checks passed!" ]
pwd
then
  ruff format output
  # mv ./prep/output/* ./pages/P114Aopticalclearing
  # echo "Files moved"
else
  echo $OUTPUT
fi
