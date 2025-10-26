#!/usr/bin/env python3
"""
Local Testing Script for PyOmron FINS Library

This script provides local testing capabilities without requiring
a physical PLC connection. Useful for development and debugging.
"""

import sys
import os

# Add the package directory to Python path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyomron_fins'))

from fins_client import FinsClient, FinsAddress
from exceptions import FinsError, InvalidAddressError


def test_address_parsing():
    """Test FINS address parsing functionality"""
    print("=== Testing Address Parsing ===")
    
    test_cases = [
        ('DM1000', 'DM', 1000, None),
        ('CIO100.05', 'CIO', 100, 5),
        ('WR200', 'WR', 200, None),
        ('HR300.15', 'HR', 300, 15),
        ('DM0', 'DM', 0, None),
        ('CIO0.00', 'CIO', 0, 0),
    ]
    
    for addr_str, expected_area, expected_addr, expected_bit in test_cases:
        try:
            fins_addr = FinsAddress.from_string(addr_str)
            
            # Check parsing results
            assert fins_addr.area == expected_area, f"Area mismatch: {fins_addr.area} != {expected_area}"
            assert fins_addr.address == expected_addr, f"Address mismatch: {fins_addr.address} != {expected_addr}"
            assert fins_addr.bit == expected_bit, f"Bit mismatch: {fins_addr.bit} != {expected_bit}"
            
            print(f"✓ {addr_str} -> {fins_addr}")
            
            # Test byte conversion
            addr_bytes = fins_addr.to_bytes()
            print(f"  Bytes: {' '.join(f'{b:02X}' for b in addr_bytes)}")
            
        except Exception as e:
            print(f"❌ {addr_str} -> Error: {e}")
    
    # Test invalid addresses
    print("\nTesting invalid addresses:")
    invalid_cases = [
        'INVALID1000',
        'DM',
        '1000',
        'DM1000.16',  # Bit > 15
        'DM1000.99',  # Invalid bit
        '',
    ]
    
    for invalid_addr in invalid_cases:
        try:
            FinsAddress.from_string(invalid_addr)
            print(f"❌ {invalid_addr} -> Should have failed!")
        except InvalidAddressError:
            print(f"✓ {invalid_addr} -> Correctly rejected")
        except Exception as e:
            print(f"❌ {invalid_addr} -> Unexpected error: {e}")


def test_fins_header_building():
    """Test FINS header building"""
    print("\n=== Testing FINS Header Building ===")
    
    # Create a client (won't connect)
    client = FinsClient('192.168.1.10', auto_connect=False)
    
    # Test header building
    command = 0x0101  # Memory Area Read
    data_length = 6
    
    header = client._build_fins_header(command, data_length)
    
    print(f"Header length: {len(header)} bytes")
    print(f"Header bytes: {' '.join(f'{b:02X}' for b in header)}")
    
    # Verify header structure
    expected_length = 12  # Standard FINS header length
    assert len(header) == expected_length, f"Header length mismatch: {len(header)} != {expected_length}"
    
    # Check ICF (first byte)
    assert header[0] == client.icf, f"ICF mismatch: {header[0]:02X} != {client.icf:02X}"
    
    print("✓ Header building test passed")


def test_memory_area_codes():
    """Test memory area code mappings"""
    print("\n=== Testing Memory Area Codes ===")
    
    expected_codes = {
        'CIO': 0x30,
        'WR': 0x31,
        'HR': 0x32,
        'AR': 0x33,
        'DM': 0x02,
        'EM': 0x20,
        'TIM': 0x09,
        'CNT': 0x09,
        'DR': 0x2C,
        'IR': 0x2D,
    }
    
    for area, expected_code in expected_codes.items():
        try:
            addr = FinsAddress(area, 100)
            actual_code = addr.area_code
            
            assert actual_code == expected_code, f"Code mismatch for {area}: {actual_code:02X} != {expected_code:02X}"
            print(f"✓ {area}: 0x{actual_code:02X}")
            
        except Exception as e:
            print(f"❌ {area} -> Error: {e}")


def test_client_initialization():
    """Test client initialization with various options"""
    print("\n=== Testing Client Initialization ===")
    
    # Test default options
    client1 = FinsClient('192.168.1.10')
    print(f"✓ Default client: {client1.host}:{client1.port} ({client1.protocol})")
    assert client1.port == 9600
    assert client1.protocol == 'udp'
    assert client1.timeout == 5.0
    
    # Test custom options
    client2 = FinsClient(
        host='192.168.1.20',
        port=9601,
        protocol='tcp',
        timeout=10.0,
        DNA=0x01,
        DA1=0x02
    )
    print(f"✓ Custom client: {client2.host}:{client2.port} ({client2.protocol})")
    assert client2.port == 9601
    assert client2.protocol == 'tcp'
    assert client2.timeout == 10.0
    assert client2.dna == 0x01
    assert client2.da1 == 0x02


def test_command_codes():
    """Test FINS command code definitions"""
    print("\n=== Testing Command Codes ===")
    
    expected_commands = {
        'MEMORY_AREA_READ': 0x0101,
        'MEMORY_AREA_WRITE': 0x0102,
        'MEMORY_AREA_FILL': 0x0103,
        'MULTIPLE_MEMORY_AREA_READ': 0x0104,
        'MEMORY_AREA_TRANSFER': 0x0105,
        'CONTROLLER_DATA_READ': 0x0501,
        'CONTROLLER_STATUS_READ': 0x0601,
        'RUN': 0x0401,
        'STOP': 0x0402,
        'CLOCK_READ': 0x0720,
        'CLOCK_WRITE': 0x0721,
    }
    
    for cmd_name, expected_code in expected_commands.items():
        actual_code = FinsClient.FINS_COMMANDS.get(cmd_name)
        assert actual_code == expected_code, f"Command code mismatch for {cmd_name}: {actual_code:04X} != {expected_code:04X}"
        print(f"✓ {cmd_name}: 0x{actual_code:04X}")


def test_error_hierarchy():
    """Test exception hierarchy"""
    print("\n=== Testing Error Hierarchy ===")
    
    # Import all exception types
    from exceptions import (
        FinsError, ConnectionError, TimeoutError, 
        ReadError, WriteError, InvalidAddressError
    )
    
    # Test inheritance
    exceptions_to_test = [
        (ConnectionError, FinsError),
        (TimeoutError, FinsError),
        (ReadError, FinsError),
        (WriteError, FinsError),
        (InvalidAddressError, FinsError),
    ]
    
    for exc_class, parent_class in exceptions_to_test:
        assert issubclass(exc_class, parent_class), f"{exc_class.__name__} should inherit from {parent_class.__name__}"
        print(f"✓ {exc_class.__name__} -> {parent_class.__name__}")
        
        # Test exception creation
        try:
            raise exc_class("Test message")
        except exc_class as e:
            assert str(e) == "Test message"
            print(f"  Exception message: {e}")


def simulate_connection_test():
    """Simulate connection test (no actual network)"""
    print("\n=== Simulating Connection Test ===")
    
    # Test that connection attempts fail gracefully
    client = FinsClient('192.168.1.999', timeout=1.0, auto_connect=False)  # Invalid IP
    
    # Should not be connected initially
    assert not client.connected, "Client should not be connected initially"
    print("✓ Initial connection state: False")
    
    # Test connection attempt (will fail)
    try:
        client.connect()
        print("❌ Connection should have failed!")
    except Exception as e:
        print(f"✓ Connection failed as expected: {type(e).__name__}")
    
    # Test auto-connect behavior
    client_auto = FinsClient('192.168.1.999', timeout=1.0, auto_connect=True)
    
    try:
        # This should attempt auto-connect and fail
        client_auto.read('DM1000')
        print("❌ Auto-connect should have failed!")
    except Exception as e:
        print(f"✓ Auto-connect failed as expected: {type(e).__name__}")


def run_all_tests():
    """Run all local tests"""
    print("PyOmron FINS Local Testing")
    print("=" * 50)
    
    tests = [
        test_address_parsing,
        test_fins_header_building,
        test_memory_area_codes,
        test_client_initialization,
        test_command_codes,
        test_error_hierarchy,
        simulate_connection_test,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print(f"✓ {test.__name__} PASSED")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} FAILED: {e}")
        
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All tests passed!")
        return True
    else:
        print(f"❌ {failed} test(s) failed")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
