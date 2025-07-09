# ZeroMQ 

Easy installation:

`sudo apt-get install libzmq3-dev`

# Google Protocol Buffers 

Installation:

`sudo apt install python3-protobuf`

# Protocol Buffer message format

Prepare `my_point.proto` file:

```
syntax = "proto3";

message Point {
  float x = 1;
  float y = 2;
  float z = 3;
}
```

Then generate code for Python:

`protoc --python_out=. my_point.proto`

Use it in the sender and receiver with `from my_point_pb2 import Point`, examples in the ZIP (`sender_zmq.py`, `receiver_zmq.py`).

