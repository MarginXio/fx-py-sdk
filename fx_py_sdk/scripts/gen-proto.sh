#!/usr/bin/env bash

OUT=codec

rm -rf "$OUT"

if [ ! -d "$OUT" ]; then
  mkdir "$OUT"
fi

proto_dirs=$(find ./proto -path -prune -o -name '*.proto' -print0 | xargs -0 -n1 dirname | sort | uniq)
for dir in $proto_dirs; do
  python3 -m grpc_tools.protoc \
    -I=./proto \
    --python_out=$OUT \
    --grpc_python_out=$OUT \
  $(find "${dir}" -maxdepth 10 -name '*.proto')
done

find codec -type d -exec touch {}/__init__.py \;
