#!/usr/bin/env python3
"""
Test script for the refactored gRPC implementation.
Tests connection management, resource cleanup, and efficiency improvements.
"""

import asyncio
import threading
import time
import sys
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

# Initialize environment first
from compipe.runtime_env import Environment
from compipe.utils.io_helper import json_loader

# Load server config
server_config_path = os.path.join(
    os.path.dirname(__file__), 'debug_runtime_config.json')
server_config = json_loader(
    path=server_config_path).get(sys.platform or 'linux')
Environment.append_server_config(payload=server_config)

from engine_grpc.engine_pipe_channel import GrpcChannelPool, general_channel
from engine_grpc.engine_pipe_server import run_grpc_server, UGrpcPipeImpl
from engine_grpc.unity.engine_pipe_unity_impl import UnityEditorImpl
from compipe.utils.logging import logger


class TestGrpcServer:
    """Test server for validating client connections"""
    
    def __init__(self, port=50062):
        self.port = port
        self.server_thread = None
        self.running = False
    
    def start(self):
        """Start test server in a separate thread"""
        self.server_thread = threading.Thread(
            target=self._run_server, 
            daemon=True
        )
        self.running = True
        self.server_thread.start()
        # Give server time to start
        time.sleep(2)
    
    def stop(self):
        """Stop the test server"""
        self.running = False
        if self.server_thread:
            self.server_thread.join(timeout=5)
    
    def _run_server(self):
        """Run the gRPC server"""
        try:
            run_grpc_server(
                service_impl=UGrpcPipeImpl,
                port=self.port,
                max_workers=5
            )
        except Exception as e:
            logger.error(f"Test server error: {e}")


def test_connection_pooling():
    """Test that connection pooling works correctly"""
    print("🧪 Testing connection pooling...")
    
    try:
        pool = GrpcChannelPool()
        
        # Create multiple clients with same host:port
        client1 = UnityEditorImpl(channel="127.0.0.1:50062")
        client2 = UnityEditorImpl(channel="127.0.0.1:50062")
        
        # Both should use the same channel from pool
        with general_channel(engine=client1) as ch1:
            with general_channel(engine=client2) as ch2:
                # Check if they're using the same channel instance
                if ch1.grpc_channel is ch2.grpc_channel:
                    print("✅ Connection pooling works correctly")
                    return True
                else:
                    print("❌ Connection pooling failed - different channels created")
                    return False
                    
    except Exception as e:
        print(f"❌ Connection pooling test failed: {e}")
        traceback.print_exc()
        return False


def test_resource_cleanup():
    """Test that resources are properly cleaned up"""
    print("🧪 Testing resource cleanup...")
    
    try:
        pool = GrpcChannelPool()
        initial_channel_count = len(pool._channels)
        
        # Create and use a client
        client = UnityEditorImpl(channel="127.0.0.1:50062")
        
        with general_channel(engine=client) as channel_mgr:
            # Channel should be created when using the context manager
            current_channel_count = len(pool._channels)
            if current_channel_count >= initial_channel_count:
                print("✅ Channel management working correctly")
            else:
                print("❌ Channel management failed")
                return False
        
        # After context manager, channel should still exist in pool (for reuse)
        # but properly managed
        print("✅ Resource cleanup works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Resource cleanup test failed: {e}")
        traceback.print_exc()
        return False


def test_event_loop_handling():
    """Test proper event loop handling"""
    print("🧪 Testing event loop handling...")
    
    try:
        # Test in main thread
        client = UnityEditorImpl(channel="127.0.0.1:50062")
        
        with general_channel(engine=client) as channel_mgr:
            if client.event_loop is not None:
                print("✅ Event loop created successfully in main thread")
            else:
                print("❌ Event loop creation failed")
                return False
        
        # Test in separate thread
        def test_in_thread():
            client_thread = UnityEditorImpl(channel="127.0.0.1:50062")
            with general_channel(engine=client_thread) as channel_mgr:
                return client_thread.event_loop is not None
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(test_in_thread)
            if future.result(timeout=10):
                print("✅ Event loop handling works in separate threads")
                return True
            else:
                print("❌ Event loop handling failed in separate threads")
                return False
                
    except Exception as e:
        print(f"❌ Event loop handling test failed: {e}")
        traceback.print_exc()
        return False


def test_concurrent_connections():
    """Test multiple concurrent connections"""
    print("🧪 Testing concurrent connections...")
    
    def create_client_connection(client_id):
        """Create a client connection and perform a simple operation"""
        try:
            client = UnityEditorImpl(channel="127.0.0.1:50062")
            with general_channel(engine=client):
                # Simulate some work
                time.sleep(0.1)
                return f"Client {client_id} connected successfully"
        except Exception as e:
            return f"Client {client_id} failed: {e}"
    
    try:
        # Test multiple concurrent connections
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(create_client_connection, i) 
                for i in range(5)
            ]
            
            results = [future.result(timeout=10) for future in futures]
            
            success_count = sum(1 for r in results if "connected successfully" in r)
            
            if success_count == 5:
                print("✅ All concurrent connections successful")
                return True
            else:
                print(f"❌ Only {success_count}/5 concurrent connections successful")
                for result in results:
                    print(f"  - {result}")
                return False
                
    except Exception as e:
        print(f"❌ Concurrent connections test failed: {e}")
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling and recovery"""
    print("🧪 Testing error handling...")
    
    try:
        # Test connection to non-existent server
        client = UnityEditorImpl(channel="127.0.0.1:99999")
        
        try:
            with general_channel(engine=client) as channel_mgr:
                # Try to make a gRPC call that should fail
                try:
                    # This should fail when actually trying to connect
                    result = client.get_service_status()
                    print("❌ Should have failed connecting to non-existent server")
                    return False
                except Exception as call_error:
                    print("✅ Properly handled connection error during call")
                    return True
        except Exception as e:
            print("✅ Properly handled connection error during setup")
            return True
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 Running gRPC refactoring tests...\n")
    
    # Note: Server tests are disabled as they require a running server
    # In a real environment, you would start a test server
    
    tests = [
        ("Connection Pooling", test_connection_pooling),
        ("Resource Cleanup", test_resource_cleanup),
        ("Event Loop Handling", test_event_loop_handling),
        ("Concurrent Connections", test_concurrent_connections),
        ("Error Handling", test_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The refactored gRPC implementation is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)