#!/usr/bin/env python3
"""
Integration test for packing struct data on server side and unpacking on client side.
This simulates the complete flow described in the user's example.
"""

import sys
from google.protobuf import any_pb2, struct_pb2
from betterproto.lib.google import protobuf
from ugrpc_pipe import ugrpc_pipe_pb2
from engine_grpc.engine_pipe_impl import BaseEngineImpl


def create_server_response_with_struct(payload_dict: dict):
    """
    Simulate server-side packing of dict data into GenericResp with struct payload.
    This follows the pattern described by the user.
    """
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


def test_pack_unpack_integration():
    """Test the complete pack/unpack flow"""
    print("🧪 Testing complete pack/unpack integration...")
    
    # Test data
    test_payload = {
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
            {"metric": "purchases", "value": 3},
            {"metric": "rating", "value": 4.8}
        ]
    }
    
    try:
        # Step 1: Server-side packing (simulate server creating response)
        print("📦 Step 1: Server-side packing...")
        server_response = create_server_response_with_struct(test_payload)
        print(f"✅ Server created GenericResp with status: {server_response.status.code}")
        
        # Step 2: Convert to betterproto format (as it would be received by client)
        print("🔄 Step 2: Converting to client format...")
        betterproto_any = protobuf.Any()
        betterproto_any.type_url = server_response.payload.type_url
        betterproto_any.value = server_response.payload.value
        print(f"✅ Converted to betterproto Any with type_url: {betterproto_any.type_url}")
        
        # Step 3: Client-side unpacking (using updated unpack method)
        print("📤 Step 3: Client-side unpacking...")
        unpacked_result = BaseEngineImpl.unpack(betterproto_any)
        print(f"✅ Unpacked result type: {type(unpacked_result)}")
        
        # Step 4: Validate the results
        print("✅ Step 4: Validating results...")
        
        if not isinstance(unpacked_result, dict):
            print(f"❌ Expected dict, got {type(unpacked_result)}")
            return False
        
        # Check basic fields
        checks = [
            ("user_id", "12345"),
            ("user_name", "John Doe"),
            ("user_score", 95.5),
            ("is_active", True),
        ]
        
        for key, expected in checks:
            actual = unpacked_result.get(key)
            if actual == expected:
                print(f"✅ {key}: {actual} ✓")
            else:
                print(f"❌ {key}: expected {expected}, got {actual}")
                return False
        
        # Check nested dict
        metadata = unpacked_result.get("metadata")
        if isinstance(metadata, dict):
            print("✅ metadata is dict ✓")
            if metadata.get("last_login") == "2024-01-15":
                print("✅ metadata.last_login ✓")
            else:
                print(f"❌ metadata.last_login: expected '2024-01-15', got {metadata.get('last_login')}")
                return False
            
            preferences = metadata.get("preferences")
            if isinstance(preferences, dict) and preferences.get("theme") == "dark":
                print("✅ nested preferences ✓")
            else:
                print(f"❌ nested preferences failed: {preferences}")
                return False
        else:
            print(f"❌ metadata is not dict: {metadata}")
            return False
        
        # Check list
        tags = unpacked_result.get("tags")
        if isinstance(tags, list) and len(tags) == 3 and "premium" in tags:
            print("✅ tags list ✓")
        else:
            print(f"❌ tags list failed: {tags}")
            return False
        
        # Check list of dicts
        stats = unpacked_result.get("stats")
        if isinstance(stats, list) and len(stats) == 3:
            if all(isinstance(item, dict) for item in stats):
                if stats[0].get("metric") == "logins" and stats[0].get("value") == 42:
                    print("✅ stats list of dicts ✓")
                else:
                    print(f"❌ stats content failed: {stats[0]}")
                    return False
            else:
                print(f"❌ stats items not all dicts: {stats}")
                return False
        else:
            print(f"❌ stats list failed: {stats}")
            return False
        
        print("🎉 All integration tests passed!")
        print(f"📊 Original payload size: {len(str(test_payload))} chars")
        print(f"📊 Unpacked payload size: {len(str(unpacked_result))} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_empty_payload():
    """Test handling of empty payload"""
    print("\n🧪 Testing empty payload handling...")
    
    try:
        # Create response with empty payload
        server_response = create_server_response_with_struct({})
        
        # Check if payload is empty (None payload case)
        if server_response.payload.type_url == "":
            print("✅ Empty dict created empty Any - this is correct behavior")
            return True
        
        # Convert and unpack
        betterproto_any = protobuf.Any()
        betterproto_any.type_url = server_response.payload.type_url
        betterproto_any.value = server_response.payload.value
        
        result = BaseEngineImpl.unpack(betterproto_any)
        
        if isinstance(result, dict) and len(result) == 0:
            print("✅ Empty payload handled correctly")
            return True
        else:
            print(f"❌ Empty payload failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Empty payload test failed: {e}")
        return False


def test_null_payload():
    """Test handling of null payload"""
    print("\n🧪 Testing null payload handling...")
    
    try:
        # Create response with None payload
        server_response = create_server_response_with_struct(None)
        
        # The payload should be empty
        if server_response.payload.type_url == "":
            print("✅ Null payload handled correctly (empty Any)")
            return True
        else:
            print(f"❌ Null payload failed: {server_response.payload}")
            return False
            
    except Exception as e:
        print(f"❌ Null payload test failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests"""
    print("🚀 Running pack/unpack integration tests...\n")
    
    tests = [
        ("Pack/Unpack Integration", test_pack_unpack_integration),
        ("Empty Payload", test_empty_payload),
        ("Null Payload", test_null_payload),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! The pack/unpack flow works correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)