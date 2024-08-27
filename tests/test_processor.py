import unittest
import os
import csv
import sys

sys.path.append('..')  
from main import remove_non_ascii, read_protocol_numbers, read_lookup_table, process_flow_logs, write_counts_to_csv

class TestFlowLogProcessor(unittest.TestCase):
    def setUp(self):
        # Creating test files
        self.setup_files()

    def setup_files(self):
        with open('test_protocol_numbers.csv', 'w', newline='', encoding='ascii') as file:
            writer = csv.writer(file)
            writer.writerow(['Protocol_Number', 'Protocol'])
            writer.writerow(['6', 'tcp'])
            writer.writerow(['17', 'udp'])

        with open('test_lookup_table.csv', 'w', newline='', encoding='ascii') as file:
            writer = csv.writer(file)
            writer.writerow(['dstport', 'protocol', 'tag'])
            writer.writerow(['80', 'tcp', 'web'])
            writer.writerow(['443', 'tcp', 'secure_web'])
            writer.writerow(['53', 'udp', 'dns'])

        with open('test_flow_logs.txt', 'w', encoding='ascii') as file:
            file.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
            file.write("2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 53 49154 17 15 12000 1620140761 1620140821 REJECT OK\n")

    def tearDown(self):
        files = ['test_protocol_numbers.csv', 'test_lookup_table.csv', 'test_flow_logs.txt', 'test_tag_counts.csv', 'test_port_protocol_counts.csv']
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_file_cleaning(self):
        remove_non_ascii('test_protocol_numbers.csv')
        with open('test_protocol_numbers.csv', 'r') as file:
            contents = file.read()
            self.assertFalse(any(ord(char) > 127 for char in contents))

    def test_read_protocol_numbers(self):
        protocol_map = read_protocol_numbers('test_protocol_numbers.csv')
        self.assertEqual(protocol_map, {'6': 'tcp', '17': 'udp'})

    def test_read_lookup_table(self):
        lookup_table = read_lookup_table('test_lookup_table.csv')
        self.assertEqual(lookup_table, {('80', 'tcp'): 'web', ('443', 'tcp'): 'secure_web', ('53', 'udp'): 'dns'})

    def test_process_flow_logs(self):
        protocol_map = {'6': 'tcp', '17': 'udp'}
        lookup_table = {('443', 'tcp'): 'secure_web', ('53', 'udp'): 'dns'}
        tag_counts, port_protocol_counts = process_flow_logs('test_flow_logs.txt', lookup_table, protocol_map)
        self.assertEqual(tag_counts, {'secure_web': 1, 'dns': 1, 'Untagged': 0})
        self.assertEqual(port_protocol_counts, {('443', 'tcp'): 1, ('53', 'udp'): 1})

    def test_write_counts_to_csv(self):
        counts_dict = {'web': 1, 'secure_web': 1}
        write_counts_to_csv('test_tag_counts.csv', counts_dict, ['Tag', 'Count'])
        with open('test_tag_counts.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertIn(['Tag', 'Count'], rows)
            self.assertIn(['web', '1'], rows)
            self.assertIn(['secure_web', '1'], rows)

if __name__ == '__main__':
    unittest.main()