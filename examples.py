#!/usr/bin/env python3
"""
PyOmron FINS Examples

This file contains comprehensive examples showing how to use the PyOmron FINS library
to communicate with OMRON PLCs using the FINS protocol.
"""

import time
import datetime
from pyomron_fins import FinsClient, FinsError, ConnectionError, TimeoutError


def basic_read_write_example():
    """Basic read and write operations"""
    print("=== Basic Read/Write Example ===")
    
    try:
        # Create client with UDP (default)
        client = FinsClient('192.168.1.10')
        
        # Connect to PLC
        client.connect()
        print("Connected to PLC")
        
        # Read single word
        value = client.read('DM1000')[0]
        print(f"DM1000 = {value}")
        
        # Write single word
        client.write('DM1001', 1234)
        print("Written 1234 to DM1001")
        
        # Read multiple words
        values = client.read('DM1000', count=5)
        print(f"DM1000-1004 = {values}")
        
        # Write multiple words
        client.write('DM2000', [100, 200, 300, 400, 500])
        print("Written [100, 200, 300, 400, 500] to DM2000-2004")
        
        # Read bit
        bit_value = client.read('CIO100.05')[0]
        print(f"CIO100.05 = {bit_value}")
        
        client.disconnect()
        print("Disconnected from PLC")
        
    except ConnectionError:
        print("❌ Failed to connect to PLC")
    except Exception as e:
        print(f"❌ Error: {e}")


def context_manager_example():
    """Using context manager for automatic connection management"""
    print("\n=== Context Manager Example ===")
    
    try:
        with FinsClient('192.168.1.10', timeout=3.0) as client:
            print("Connected using context manager")
            
            # Read some process data
            process_data = {
                'temperature': client.read('DM1000')[0],
                'pressure': client.read('DM1001')[0],
                'flow_rate': client.read('DM1002')[0],
                'valve_status': client.read('CIO100.00')[0]
            }
            
            print("Process Data:")
            for name, value in process_data.items():
                print(f"  {name}: {value}")
            
            # Write control commands
            if process_data['temperature'] > 80:
                client.write('CIO200.00', 1)  # Turn on cooling
                print("Cooling activated")
            
        print("Connection automatically closed")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def multiple_read_example():
    """Reading multiple disparate addresses efficiently"""
    print("\n=== Multiple Address Read Example ===")
    
    try:
        with FinsClient('192.168.1.10') as client:
            # Define addresses to read
            addresses = [
                'DM1000',  # Temperature setpoint
                'DM1001',  # Pressure setpoint  
                'DM1500',  # Production counter
                'CIO100.00',  # Motor status
                'CIO100.01',  # Pump status
                'WR200',   # Working register
                'HR300'    # Recipe number
            ]
            
            # Read all addresses in one command
            results = client.read_multiple(addresses)
            
            print("Multiple Read Results:")
            for addr, value in results.items():
                print(f"  {addr} = {value}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def memory_operations_example():
    """Memory fill and transfer operations"""
    print("\n=== Memory Operations Example ===")
    
    try:
        with FinsClient('192.168.1.10') as client:
            # Fill memory area with zeros (initialize)
            client.fill('DM3000', value=0, count=100)
            print("Filled DM3000-3099 with zeros")
            
            # Write some test data
            test_data = [10, 20, 30, 40, 50]
            client.write('DM3000', test_data)
            print(f"Written test data {test_data} to DM3000-3004")
            
            # Transfer data within PLC memory
            client.transfer('DM3000', 'DM3100', count=5)
            print("Transferred DM3000-3004 to DM3100-3104")
            
            # Verify transfer
            original = client.read('DM3000', count=5)
            copied = client.read('DM3100', count=5)
            
            print(f"Original: {original}")
            print(f"Copied:   {copied}")
            print(f"Transfer successful: {original == copied}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def plc_control_example():
    """PLC control and status operations"""
    print("\n=== PLC Control Example ===")
    
    try:
        with FinsClient('192.168.1.10') as client:
            # Get PLC information
            try:
                info = client.get_cpu_unit_data()
                print("PLC Information:")
                print(f"  Model: {info.get('controller_model', 'Unknown')}")
                print(f"  Version: {info.get('controller_version', 'Unknown')}")
            except:
                print("Could not retrieve PLC information")
            
            # Get current status
            status = client.get_status()
            print("\nPLC Status:")
            print(f"  Run Mode: {status.get('run_mode', False)}")
            print(f"  Program Mode: {status.get('program_mode', False)}")
            print(f"  Fatal Error: {status.get('fatal_error', False)}")
            print(f"  Non-Fatal Error: {status.get('non_fatal_error', False)}")
            
            # Example: Controlled start/stop (be careful!)
            current_mode = status.get('run_mode', False)
            print(f"\nCurrent mode: {'RUN' if current_mode else 'PROGRAM'}")
            
            # Uncomment these lines only if you want to change PLC mode
            # WARNING: This will affect PLC operation!
            
            # if not current_mode:
            #     print("Setting PLC to RUN mode...")
            #     client.run()
            #     time.sleep(1)
            #     new_status = client.get_status()
            #     print(f"New mode: {'RUN' if new_status.get('run_mode', False) else 'PROGRAM'}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def clock_operations_example():
    """PLC clock read and write operations"""
    print("\n=== Clock Operations Example ===")
    
    try:
        with FinsClient('192.168.1.10') as client:
            # Read PLC clock
            clock = client.read_clock()
            
            if clock:
                print("PLC Clock:")
                print(f"  Date: {clock['year']}-{clock['month']:02d}-{clock['day']:02d}")
                print(f"  Time: {clock['hour']:02d}:{clock['minute']:02d}:{clock['second']:02d}")
                print(f"  Day of week: {clock['day_of_week']}")
                
                # Compare with system time
                now = datetime.datetime.now()
                print(f"\nSystem Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Calculate time difference
                plc_time = datetime.datetime(
                    clock['year'], clock['month'], clock['day'],
                    clock['hour'], clock['minute'], clock['second']
                )
                
                diff = abs((now - plc_time).total_seconds())
                print(f"Time difference: {diff:.1f} seconds")
                
                # Uncomment to sync PLC clock with system time
                # WARNING: This will change the PLC clock!
                
                # if diff > 60:  # If more than 1 minute difference
                #     print("Synchronizing PLC clock with system time...")
                #     client.write_clock(
                #         year=now.year,
                #         month=now.month,
                #         day=now.day,
                #         hour=now.hour,
                #         minute=now.minute,
                #         second=now.second,
                #         day_of_week=now.weekday()
                #     )
                #     print("Clock synchronized")
            else:
                print("Could not read PLC clock")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def tcp_connection_example():
    """Using TCP instead of UDP"""
    print("\n=== TCP Connection Example ===")
    
    try:
        # Create TCP client
        client = FinsClient(
            host='192.168.1.10',
            port=9600,
            protocol='tcp',  # Use TCP instead of UDP
            timeout=5.0
        )
        
        with client:
            print("Connected via TCP")
            
            # Same operations work with TCP
            value = client.read('DM1000')[0]
            print(f"DM1000 = {value}")
            
            # TCP provides reliable delivery
            client.write('DM1000', value + 1)
            new_value = client.read('DM1000')[0]
            print(f"DM1000 after increment = {new_value}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def error_handling_example():
    """Comprehensive error handling"""
    print("\n=== Error Handling Example ===")
    
    # Test with invalid IP to demonstrate connection error
    try:
        client = FinsClient('192.168.1.999', timeout=2.0)  # Invalid IP
        with client:
            value = client.read('DM1000')[0]
    except ConnectionError as e:
        print(f"✓ Caught ConnectionError: {e}")
    except TimeoutError as e:
        print(f"✓ Caught TimeoutError: {e}")
    
    # Test with valid connection but invalid address
    try:
        with FinsClient('192.168.1.10') as client:
            # This should work
            value = client.read('DM1000')[0]
            print(f"✓ Valid read: DM1000 = {value}")
            
            # This might cause an error depending on PLC configuration
            try:
                value = client.read('DM99999')[0]  # Very high address
                print(f"DM99999 = {value}")
            except FinsError as e:
                print(f"✓ Caught FinsError for invalid address: {e}")
                
    except ConnectionError as e:
        print(f"Could not connect for error testing: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def monitoring_loop_example():
    """Continuous monitoring loop"""
    print("\n=== Monitoring Loop Example ===")
    print("This will run for 30 seconds, monitoring DM1000-1002")
    print("Press Ctrl+C to stop early")
    
    try:
        with FinsClient('192.168.1.10') as client:
            start_time = time.time()
            
            while time.time() - start_time < 30:  # Run for 30 seconds
                try:
                    # Read monitoring addresses
                    values = client.read('DM1000', count=3)
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    print(f"[{timestamp}] DM1000={values[0]:5d}, DM1001={values[1]:5d}, DM1002={values[2]:5d}")
                    
                    # Check for alarm conditions
                    if values[0] > 1000:  # Example alarm condition
                        print(f"  ⚠️  WARNING: DM1000 value ({values[0]}) exceeds threshold!")
                    
                    time.sleep(2)  # Update every 2 seconds
                    
                except KeyboardInterrupt:
                    print("\nMonitoring stopped by user")
                    break
                except Exception as e:
                    print(f"  ❌ Monitoring error: {e}")
                    time.sleep(5)  # Wait longer on error
                    
    except Exception as e:
        print(f"❌ Failed to start monitoring: {e}")


def main():
    """Run all examples"""
    print("PyOmron FINS Library Examples")
    print("=" * 50)
    print("NOTE: These examples assume a PLC at 192.168.1.10")
    print("Modify the IP address to match your PLC")
    print("=" * 50)
    
    examples = [
        basic_read_write_example,
        context_manager_example,
        multiple_read_example,
        memory_operations_example,
        plc_control_example,
        clock_operations_example,
        tcp_connection_example,
        error_handling_example,
        # monitoring_loop_example,  # Uncomment to run monitoring
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\n\nExamples interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Example failed: {e}")
        
        time.sleep(1)  # Brief pause between examples
    
    print("\n=" * 50)
    print("Examples completed")


if __name__ == '__main__':
    main()
