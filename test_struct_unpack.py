#!/usr/bin/env python3
"""
Test script for the updated unpack method to handle struct_pb2.Struct payloads.
"""

import sys
from google.protobuf import any_pb2, struct_pb2
from betterproto.lib.google import protobuf
from engine_grpc.engine_pipe_impl import BaseEngineImpl


def create_test_struct_payload():
    """Create a test payload with struct_pb2.Struct"""
    # Create a test dict
    test_data = {
        "string_field": "test_string",
        "number_field": 42.0,
        "bool_field": True,
        "null_field": None,
        "nested_dict": {
            "nested_string": "nested_value",
            "nested_number": 123.456
        },
        "list_field": [
            "item1",
            2.0,
            True,
            {"nested_in_list": "value"}
        ]
    }
    
    # Convert dict to protobuf Struct
    struct_pb = struct_pb2.Struct()
    for key, value in test_data.items():
        if value is None:
            struct_pb[key] = None
        else:
            struct_pb[key] = value
    
    # Pack into Any
    payload_any = any_pb2.Any()
    payload_any.Pack(struct_pb)
    
    return payload_any, test_data


def test_struct_unpack():
    """Test that the unpack method correctly handles struct_pb2.Struct payloads"""
    print("🧪 Testing struct_pb2.Struct unpack functionality...")
    
    try:
        # Create test payload
        payload_any, expected_data = create_test_struct_payload()
        
        # Convert to betterproto Any format (as it would come from gRPC)
        betterproto_any = protobuf.Any()
        betterproto_any.type_url = payload_any.type_url
        betterproto_any.value = payload_any.value
        
        # Test the unpack method
        result = BaseEngineImpl.unpack(betterproto_any)
        
        print(f"Expected: {expected_data}")
        print(f"Result:   {result}")
        
        # Verify the results
        if isinstance(result, dict):
            print("✅ Unpack returned a dictionary")
            
            # Check string field
            if result.get("string_field") == "test_string":
                print("✅ String field unpacked correctly")
            else:
                print(f"❌ String field mismatch: {result.get('string_field')}")
                return False
            
            # Check number field
            if result.get("number_field") == 42.0:
                print("✅ Number field unpacked correctly")
            else:
                print(f"❌ Number field mismatch: {result.get('number_field')}")
                return False
            
            # Check bool field
            if result.get("bool_field") is True:
                print("✅ Bool field unpacked correctly")
            else:
                print(f"❌ Bool field mismatch: {result.get('bool_field')}")
                return False
            
            # Check null field
            if result.get("null_field") is None:
                print("✅ Null field unpacked correctly")
            else:
                print(f"❌ Null field mismatch: {result.get('null_field')}")
                return False
            
            # Check nested dict
            nested = result.get("nested_dict")
            if isinstance(nested, dict):
                print("✅ Nested dict unpacked correctly")
                if nested.get("nested_string") == "nested_value":
                    print("✅ Nested string unpacked correctly")
                else:
                    print(f"❌ Nested string mismatch: {nested.get('nested_string')}")
                    return False
            else:
                print(f"❌ Nested dict mismatch: {nested}")
                return False
            
            # Check list field
            list_field = result.get("list_field")
            if isinstance(list_field, list) and len(list_field) == 4:
                print("✅ List field unpacked correctly")
                if list_field[0] == "item1" and list_field[1] == 2.0 and list_field[2] is True:
                    print("✅ List items unpacked correctly")
                    
                    # Check nested dict in list
                    if isinstance(list_field[3], dict) and list_field[3].get("nested_in_list") == "value":
                        print("✅ Nested dict in list unpacked correctly")
                    else:
                        print(f"❌ Nested dict in list mismatch: {list_field[3]}")
                        return False
                else:
                    print(f"❌ List items mismatch: {list_field[:3]}")
                    return False
            else:
                print(f"❌ List field mismatch: {list_field}")
                return False
            
            print("🎉 All struct_pb2.Struct unpack tests passed!")
            return True
        else:
            print(f"❌ Unpack did not return a dictionary: {type(result)}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_types():
    """Test that existing simple type unpacking still works"""
    print("\n🧪 Testing existing simple type unpack functionality...")
    
    from google.protobuf import wrappers_pb2
    
    try:
        # Test string value
        string_wrapper = wrappers_pb2.StringValue(value="test_string")
        string_any = any_pb2.Any()
        string_any.Pack(string_wrapper)
        
        betterproto_any = protobuf.Any()
        betterproto_any.type_url = string_any.type_url
        betterproto_any.value = string_any.value
        
        result = BaseEngineImpl.unpack(betterproto_any)
        if result == "test_string":
            print("✅ String value unpack still works")
        else:
            print(f"❌ String value unpack failed: {result}")
            return False
        
        # Test int value
        int_wrapper = wrappers_pb2.Int32Value(value=123)
        int_any = any_pb2.Any()
        int_any.Pack(int_wrapper)
        
        betterproto_any = protobuf.Any()
        betterproto_any.type_url = int_any.type_url
        betterproto_any.value = int_any.value
        
        result = BaseEngineImpl.unpack(betterproto_any)
        if result == 123:
            print("✅ Int32 value unpack still works")
        else:
            print(f"❌ Int32 value unpack failed: {result}")
            return False
        
        print("🎉 All simple type unpack tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple type test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all unpack tests"""
    print("🚀 Running struct_pb2.Struct unpack tests...\n")
    
    tests = [
        ("Struct Unpack", test_struct_unpack),
        ("Simple Types", test_simple_types),
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
        print("🎉 All tests passed! The updated unpack method works correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)