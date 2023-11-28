# EdgePi RPC Protobuf Python Library

EdgePi RPC Protobuf package for installation in a Python environment.

## Recompile Python-generated code for this package:

```
protoc -I=. --experimental_allow_proto3_optional --python_out=./python_rpc/protobufs <filename.proto>
```

## Importing python generated code

Install this package as:
```
pip install edgepi-rpc-protobuf
```

Import as:
```
from python_rpc.protobufs import <>
```