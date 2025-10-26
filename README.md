# PyOmron FINS

A Python wrapper for OMRON FINS protocol communication with OMRON PLCs.

This library provides a clean, Pythonic interface to communicate with OMRON PLCs using the FINS (Factory Interface Network Service) Ethernet protocol. It's based on the functionality from the popular [node-red-contrib-omron-fins](https://github.com/Steve-Mcl/node-red-contrib-omron-fins) Node.js library.

## Features

- **Pure Python**: No external dependencies - uses only Python standard library
- **Protocol Support**: Both UDP and TCP FINS communication
- **Memory Operations**: Read, write, fill, and transfer operations
- **Multiple Address Types**: Support for all OMRON memory areas (DM, CIO, WR, HR, etc.)
- **Batch Operations**: Read multiple disparate addresses in single command
- **PLC Control**: Start/stop PLC, read status and system information
- **Clock Operations**: Read and write PLC clock
- **Thread Safe**: Proper locking for concurrent access
- **Context Manager**: Easy resource management with `with` statements
- **Comprehensive Error Handling**: Detailed exception hierarchy

## Installation

```bash
pip install pyomron-fins
```

## Quick Start

```python
from pyomron_fins import FinsClient

# Create client (UDP by default)
client = FinsClient('192.168.1.10')

# Read single value
value = client.read('DM1000')[0]
print(f"DM1000 = {value}")

# Write single value
client.write('DM1001', 1234)

# Read multiple words
values = client.read('DM1000', count=5)
print(f"DM1000-1004 = {values}")

# Read bit
bit_value = client.read('CIO100.05')[0]
print(f"CIO100.05 = {bit_value}")

# Disconnect
client.disconnect()
```

## Using Context Manager

```python
with FinsClient('192.168.1.10') as client:
    # Read some values
    dm_values = client.read('DM1000', count=10)
    cio_status = client.read('CIO100', count=5)
    
    # Write results
    client.write('DM2000', dm_values)
    
# Connection automatically closed
```

## Advanced Usage

### Multiple Address Read

```python
# Read multiple disparate addresses efficiently
addresses = ['DM1000', 'DM1500', 'CIO100', 'WR200']
results = client.read_multiple(addresses)

for addr, value in results.items():
    print(f"{addr} = {value}")
```

### Memory Operations

```python
# Fill memory area with same value
client.fill('DM1000', value=0, count=100)

# Transfer data within PLC memory
client.transfer('DM1000', 'DM2000', count=50)
```

### PLC Control

```python
# Get PLC status
status = client.get_status()
print(f"Run mode: {status['run_mode']}")
print(f"Program mode: {status['program_mode']}")

# Start/Stop PLC
client.run()   # Set to RUN mode
client.stop()  # Set to PROGRAM mode

# Read PLC information
info = client.get_cpu_unit_data()
print(f"Controller: {info.get('controller_model', 'Unknown')}")
```

### Clock Operations

```python
# Read PLC clock
clock = client.read_clock()
print(f"PLC Time: {clock['year']}-{clock['month']:02d}-{clock['day']:02d} {clock['hour']:02d}:{clock['minute']:02d}:{clock['second']:02d}")

# Write PLC clock (set to current time)
import datetime
now = datetime.datetime.now()
client.write_clock(
    year=now.year,
    month=now.month, 
    day=now.day,
    hour=now.hour,
    minute=now.minute,
    second=now.second,
    day_of_week=now.weekday()
)
```

## Configuration Options

```python
client = FinsClient(
    host='192.168.1.10',
    port=9600,              # FINS port (default 9600)
    protocol='udp',         # 'udp' or 'tcp'
    timeout=5.0,            # Socket timeout in seconds
    auto_connect=True,      # Auto-connect on first operation
    # FINS header options:
    DNA=0x00,              # Destination Network Address
    DA1=0x00,              # Destination Node Address
    DA2=0x00,              # Destination Unit Address
    SNA=0x00,              # Source Network Address
    SA1=0x00,              # Source Node Address  
    SA2=0x00               # Source Unit Address
)
```

## Supported Memory Areas

| Area Code | Description | Address Format |
|-----------|-------------|----------------|
| CIO | Core I/O Area | CIO0000-CIO6143 |
| WR | Work Area | WR0000-WR511 |
| HR | Holding Area | HR0000-HR511 |
| AR | Auxiliary Area | AR0000-AR447 |
| DM | Data Memory Area | DM0000-DM32767 |
| EM | Extended Memory Area | EM0000-EM32767 |
| TIM | Timer Area | TIM000-TIM4095 |
| CNT | Counter Area | CNT000-CNT4095 |
| DR | Data Register Area | DR0000-DR32767 |
| IR | Index Register Area | IR0000-IR32767 |

### Address Formats

- **Word Access**: `DM1000`, `CIO100`, `WR200`
- **Bit Access**: `CIO100.05`, `WR200.15`, `DM1000.08`
- **Address Ranges**: All addresses support the full range for each area

## Error Handling

```python
from pyomron_fins import FinsClient, FinsError, ConnectionError, TimeoutError

try:
    with FinsClient('192.168.1.10') as client:
        values = client.read('DM1000', count=10)
except ConnectionError:
    print("Failed to connect to PLC")
except TimeoutError:
    print("Operation timed out")
except FinsError as e:
    print(f"FINS protocol error: {e}")
```

## Exception Hierarchy

- `FinsError` - Base exception for all FINS-related errors
  - `ConnectionError` - Connection-related errors
  - `TimeoutError` - Timeout errors
  - `ReadError` - Read operation errors
  - `WriteError` - Write operation errors
  - `InvalidAddressError` - Address format/range errors

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on [node-red-contrib-omron-fins](https://github.com/Steve-Mcl/node-red-contrib-omron-fins) by Steve McLaughlin
- OMRON FINS Protocol documentation
- Python community for excellent libraries and tools

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
