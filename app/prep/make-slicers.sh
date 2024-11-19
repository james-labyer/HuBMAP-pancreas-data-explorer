#!/bin/bash
rm -rf ./pages/P17Aopticalclearing/{*,.*}
rm -rf ./pages/P114Aopticalclearing/{*,.*}
rm -rf ./pages/P119Aopticalclearing/{*,.*}
rm -rf ./prep/output/P1-7A/{*,.*}
rm -rf ./prep/output/P1-14A/{*,.*}
rm -rf ./prep/output/P1-19A/{*,.*}
python3 ./prep/make-slicers.py
OUTPUT="$(ruff check ./prep/output)"

if [ "$OUTPUT" = "All checks passed!" ]
then
  ruff format ./prep/output
  mv ./prep/output/P1-7A/* ./pages/P17Aopticalclearing
  mv ./prep/output/P1-14A/* ./pages/P114Aopticalclearing
  mv ./prep/output/P1-19A/* ./pages/P119Aopticalclearing
else
  echo $OUTPUT
fi
