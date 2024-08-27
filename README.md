# Network Flow Log Processor

## Overview
This Python application parses network flow logs (AWS VPC) and a lookup table to assign tags based on port and protocol combinations. It counts the occurrences of each tag and port/protocol combination, outputting the results to respective CSV files.

## Key Specifications
1. **Input Files**: All input files (flow logs and lookup tables) are handled in plain text ASCII format with robust error handling.
2. **Tag Mapping**: Allows multiple port/protocol combinations to map to the same tag.
3. **Case Insensitivity**: Matching of tags based on port and protocol is case insensitive.

## Files Description
- **`protocol_numbers.csv`**: Contains mappings from protocol numbers to protocol names, downloaded from the [IANA Protocol Numbers Assignment](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) using the reference link shared by Tyler.
- **`lookup_table.csv`**: Contains mappings of destination ports and protocols to tags. This is user-provided and must adhere to ASCII format.
- **`flow_logs.txt`**: Log file containing network flow data. Each entry must be in ASCII format and structured according to specified log version.

## Installation
This script was developed using Python 3.8.

## Usage
To run the script, navigate to the script's directory and execute:
```
python main.py
```

For running tests, navaigate to /tests directory and execute:
```
python test_processor.py
```

## Outputs
The application generates an app.log file and two CSV files in the `output_data` directory which is currently empty:
- **`tag_counts.csv`**: Counts of each tag found in the logs.
- **`port_protocol_counts.csv`**: Counts of each port/protocol combination found in the logs.

## When things go wrong
The script includes robust error handling to manage file access issues, non-ASCII content, and unexpected data formats. Errors are logged to `app.log`, which is managed by a rotating file handler to avoid excessive log file sizes.

## Data Cleaning
As a compliance measure with the ASCII file requirement, the script includes a preprocessing step that converts input files to ASCII, removing any non-ASCII characters such as BOMs.

## Logging
Operational messages are logged to `app.log`, providing insights into the process, including any issues encountered during execution.

## Assumptions
- **Log Format**: The program only supports the default log format and not custom formats.
- **Log Version**: The only supported version of logs is version 2 as described in AWS documentation.

## Unit Testing
Key unit tests have been performed to ensure that each component of the application functions correctly:
- Tests to validate the file cleaning process.
- Tests to ensure accurate reading of protocol numbers and lookup tables.
- Tests to confirm the correct processing of flow logs against lookup table mappings.
- Tests for proper writing of output CSV files.

All tests help in validating the integrity of data processing and error handling within the application.