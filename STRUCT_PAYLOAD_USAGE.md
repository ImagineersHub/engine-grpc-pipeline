# Struct Payload Support in engine_grpc

This document explains the enhanced support for `struct_pb2.Struct` payloads in the gRPC engine implementation.

## Overview

The `BaseEngineImpl.unpack()` method has been updated to properly handle `struct_pb2.Struct` payloads, which allows for more flexible JSON-like data exchange between client and server.

## Server-Side Usage

When creating a gRPC response with dictionary data, you can now pack it as a protobuf Struct:

```python
from google.protobuf import any_pb2, struct_pb2
from ugrpc_pipe import ugrpc_pipe_pb2

def create_response_with_dict_payload(payload_dict: dict):
    """Create a GenericResp with dict payload packed as Struct"""
    
    # Create status
    pb_status = ugrpc_pipe_pb2.Status(code=0, message="OK")
    
    # Create payload_any
    payload_any = any_pb2.Any()
    if payload_dict:
        # Convert dict to protobuf Struct (which can hold JSON-like data)
        struct_pb = struct_pb2.Struct()
        for key, value in payload_dict.items():
            struct_pb[key] = value
        payload_any.Pack(struct_pb)

    return ugrpc_pipe_pb2.GenericResp(
        status=pb_status,
        payload=payload_any
    )
```

## Client-Side Usage

The client automatically unpacks struct payloads using the enhanced `unpack()` method:

```python
from engine_grpc.engine_pipe_impl import BaseEngineImpl

# When receiving a response with struct payload
response = some_grpc_call()

# The unpack method automatically handles struct_pb2.Struct payloads
if isinstance(response.payload, protobuf.Any):
    unpacked_data = BaseEngineImpl.unpack(response.payload)
    # unpacked_data is now a Python dict with the original data
```

## Supported Data Types

The enhanced unpack method supports:

### Simple Types
- `StringValue` → `str`
- `Int32Value` → `int`
- `Int64Value` → `int`
- `UInt32Value` → `int`
- `UInt64Value` → `int`
- `FloatValue` → `float`
- `DoubleValue` → `float`
- `BoolValue` → `bool`
- `BytesValue` → `bytes`

### Complex Types
- `Struct` → `dict` (with recursive unpacking)
- `ListValue` → `list` (with recursive unpacking)

### Nested Structures
- Nested dictionaries are fully supported
- Lists containing mixed types (strings, numbers, bools, dicts, lists)
- Null values are properly handled

## Example Usage

### Server Response Creation
```python
# Complex data structure
user_data = {
    "user_id": "12345",
    "user_name": "John Doe",
    "user_score": 95.5,
    "is_active": True,
    "metadata": {
        "last_login": "2024-01-15",
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    },
    "tags": ["premium", "active", "verified"],
    "stats": [
        {"metric": "logins", "value": 42},
        {"metric": "purchases", "value": 3}
    ]
}

# Pack into response
response = create_response_with_dict_payload(user_data)
```

### Client Data Unpacking
```python
# Client receives and unpacks the response
unpacked_user_data = BaseEngineImpl.unpack(response.payload)

# Access the data naturally
print(f"User: {unpacked_user_data['user_name']}")
print(f"Theme: {unpacked_user_data['metadata']['preferences']['theme']}")
print(f"First tag: {unpacked_user_data['tags'][0]}")
print(f"Login count: {unpacked_user_data['stats'][0]['value']}")
```

## Backward Compatibility

All existing functionality remains unchanged. The enhancement only adds support for `struct_pb2.Struct` payloads while maintaining full compatibility with existing wrapper types.

## Error Handling

- Unsupported payload types will log a warning and return `None`
- Malformed struct data is handled gracefully
- The type URL is logged for debugging unsupported types

## Testing

Comprehensive tests are available:
- `test_struct_unpack.py` - Tests basic struct functionality
- `test_pack_unpack_integration.py` - Tests complete server-to-client flow

Run tests with:
```bash
python3 test_struct_unpack.py
python3 test_pack_unpack_integration.py
```