import csv
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)])

def remove_non_ascii(filename):
    """
    Opens a file and rewrites it without any non-ASCII characters or BOM.
    """
    try:
        with open(filename, 'r', encoding='utf-8-sig') as file:
            contents = file.read()

        # Writing the content back to the file with ASCII encoding, ignoring non-ASCII characters
        with open(filename, 'w', encoding='ascii', errors='ignore') as file:
            file.write(contents)

        logging.info(f"File {filename} has been cleaned and converted to ASCII.")
    except Exception as e:
        logging.error(f"Failed to clean and convert {filename} to ASCII: {e}")
        raise

def read_protocol_numbers(filename):
    """
    Reads the protocol numbers from a CSV file and returns a dictionary mapping the protocol number to the protocol keyword.
    """
    protocol_map = {}
    try:
        with open(filename, mode='r', encoding='ascii') as file:
            reader = csv.reader(file)
            next(reader)  # Skipping header
            for row in reader:
                protocol_number = row[0].strip()
                protocol_keyword = row[1].strip()
                protocol_map[protocol_number] = protocol_keyword.lower()  # Converting to lower case for case insensitive matching
    except Exception as e:
        logging.error(f"Failed to read protocol numbers from {filename}: {e}")
        raise
    return protocol_map

def read_lookup_table(filename):
    """
    Reads the lookup table from a CSV file and returns a dictionary.
    """
    lookup = {}
    try:
        with open(filename, mode='r', encoding='ascii') as file:
            reader = csv.reader(file)
            next(reader)  # Skipping header
            for row in reader:
                dstport = row[0].strip()
                protocol = row[1].strip().lower()
                tag = row[2].strip()
                lookup[(dstport, protocol)] = tag
    except Exception as e:
        logging.error(f"Failed to read lookup table from {filename}: {e}")
        raise
    return lookup

def process_flow_logs(log_filename, lookup, protocol_map):
    """
    Processes the flow log file and returns counts for tags and port/protocol combinations.
    """
    tag_counts = {'Untagged': 0}  # Always having initialized 'Untagged'
    port_protocol_counts = {}
    try:
        with open(log_filename, mode='r', encoding='ascii') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                dstport = parts[5]
                protocol_number = parts[7]
                protocol = protocol_map.get(protocol_number, 'unknown')

                key = (dstport, protocol)
                port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1

                tag = lookup.get(key, 'Untagged')
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    except Exception as e:
        logging.error(f"Failed to process flow logs from {log_filename}: {e}")
        raise
    return tag_counts, port_protocol_counts


def write_counts_to_csv(filename, counts_dict, headers):
    try:
        with open(filename, mode='w', newline='', encoding='ascii') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in sorted(counts_dict.items()):
                row = list(key) + [value] if isinstance(key, tuple) else [key, value]
                writer.writerow(row)
    except Exception as e:
        logging.error(f"Failed to write to {filename}: {e}")
        raise

def main():
    protocol_filename = 'input_data/protocol_numbers.csv'
    lookup_filename = 'input_data/lookup_table.csv'
    log_filename = 'input_data/flow_logs.txt'
    
    # Cleaning and converting files to ASCII
    remove_non_ascii(protocol_filename)
    remove_non_ascii(lookup_filename)
    remove_non_ascii(log_filename)

    tag_output_filename = 'output_data/tag_counts.csv'
    port_protocol_output_filename = 'output_data/port_protocol_counts.csv'
    
    try:
        protocol_map = read_protocol_numbers(protocol_filename)
        lookup_table = read_lookup_table(lookup_filename)
        tag_counts, port_protocol_counts = process_flow_logs(log_filename, lookup_table, protocol_map)
        
        write_counts_to_csv(tag_output_filename, tag_counts, ['Tag', 'Count'])
        write_counts_to_csv(port_protocol_output_filename, port_protocol_counts, ['Port', 'Protocol', 'Count'])

        logging.info("Processing complete. Output files generated.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()