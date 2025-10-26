# Changelog

All notable changes to PyOmron FINS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-20

### Added
- Initial release of PyOmron FINS
- Complete FINS protocol implementation for OMRON PLCs
- Support for both UDP and TCP connections
- FinsClient class with comprehensive PLC communication methods:
  - `read()` - Read single or multiple words from PLC memory
  - `write()` - Write single or multiple words to PLC memory
  - `read_multiple()` - Read multiple disparate addresses efficiently
  - `fill()` - Fill memory area with same value
  - `transfer()` - Transfer data within PLC memory
  - `get_status()` - Get PLC run/program status
  - `get_cpu_unit_data()` - Get PLC model and version information
  - `run()` - Set PLC to RUN mode
  - `stop()` - Set PLC to PROGRAM mode
  - `read_clock()` - Read PLC clock
  - `write_clock()` - Write PLC clock
- FinsAddress class for memory address handling:
  - Support for all OMRON memory areas (DM, CIO, WR, HR, AR, EM, TIM, CNT, DR, IR)
  - Word and bit addressing (e.g., DM1000, CIO100.05)
  - Address parsing from string format
  - Automatic byte conversion for FINS protocol
- Comprehensive exception hierarchy:
  - `FinsError` - Base exception for all FINS-related errors
  - `ConnectionError` - Connection-related errors
  - `TimeoutError` - Timeout errors
  - `ReadError` - Read operation errors
  - `WriteError` - Write operation errors
  - `InvalidAddressError` - Address format/range errors
- Thread-safe implementation with proper locking
- Context manager support for automatic connection management
- Pure Python implementation (no external dependencies)
- Comprehensive documentation and examples
- Complete test suite for local development

### Features
- **Protocol Support**: Full FINS Ethernet protocol over UDP/TCP
- **Memory Areas**: Support for all OMRON PLC memory areas
- **Address Formats**: Flexible string-based addressing (DM1000, CIO100.05)
- **Batch Operations**: Efficient multiple address reading
- **PLC Control**: Start/stop PLC and read status information
- **Clock Operations**: Read and write PLC real-time clock
- **Error Handling**: Detailed exception hierarchy with specific error types
- **Thread Safety**: Safe for concurrent access from multiple threads
- **Resource Management**: Context manager support for automatic cleanup
- **Configurable**: Extensive configuration options for FINS protocol parameters

### Documentation
- Complete README with installation and usage instructions
- Comprehensive examples covering all library features
- API reference with detailed parameter descriptions
- Memory area reference table
- Error handling guidelines
- Best practices and troubleshooting tips

### Development Tools
- Local testing script for development without PLC hardware
- Comprehensive test coverage for address parsing and protocol handling
- Setup.py for easy installation and distribution
- GitHub repository with complete project structure

### Based On
- Functionality inspired by [node-red-contrib-omron-fins](https://github.com/Steve-Mcl/node-red-contrib-omron-fins)
- OMRON FINS protocol specification
- Python best practices and conventions

## [Unreleased]

### Planned Features
- Support for FINS/UDP Node Address Table operations
- Enhanced error diagnostics with error code mapping
- Asynchronous (asyncio) client implementation
- Support for structured data types (arrays, structures)
- Built-in data logging and monitoring capabilities
- Configuration file support (JSON/YAML)
- CLI tools for PLC diagnostics and monitoring
- Web-based dashboard for PLC monitoring
- Integration with popular Python data analysis libraries
- Support for additional OMRON PLC models and protocols

### Future Considerations
- Integration with industrial IoT platforms
- OPC UA gateway functionality
- Historical data collection and analysis
- Alarm and event management
- Recipe management system
- Mobile app integration
- Cloud connectivity options

---

## Release Notes

### Version 1.0.0 Highlights

This is the initial stable release of PyOmron FINS, providing a complete Python interface for communicating with OMRON PLCs using the FINS Ethernet protocol. The library has been designed with simplicity, reliability, and performance in mind.

**Key Benefits:**
- **Easy to Use**: Simple, Pythonic API that feels natural to Python developers
- **Reliable**: Robust error handling and connection management
- **Efficient**: Optimized protocol implementation with batch operations
- **Flexible**: Support for both UDP and TCP, extensive configuration options
- **Safe**: Thread-safe design suitable for production applications
- **Complete**: Covers all major FINS operations and PLC control functions

**Getting Started:**
```python
from pyomron_fins import FinsClient

with FinsClient('192.168.1.10') as client:
    value = client.read('DM1000')[0]
    client.write('DM1001', value + 1)
    print(f"DM1000: {value}, DM1001: {value + 1}")
```

**Installation:**
```bash
pip install pyomron-fins
```

For detailed documentation, examples, and API reference, see the [README.md](README.md) file.
