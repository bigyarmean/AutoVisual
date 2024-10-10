import os
import re
import html
from jinja2 import Environment, FileSystemLoader
import requests
from collections import Counter

class AutoReconReportGenerator:
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.data = {}
        self.env = Environment(loader=FileSystemLoader('.'))
        self.env.filters['most_common'] = self.most_common
        self.tailwind_css = self.get_tailwind_css()
        self.common_ports = {
            '21': 'FTP',
            '22': 'SSH',
            '23': 'Telnet',
            '25': 'SMTP',
            '53': 'DNS',
            '80': 'HTTP',
            '88': 'Kerberos',
            '110': 'POP3',
            '135': 'RPC Endpoint Mapper',
            '137': 'NetBIOS Name Service',
            '138': 'NetBIOS Datagram Service',
            '139': 'NetBIOS Session Service',
            '143': 'IMAP',
            '161': 'SNMP',
            '389': 'LDAP',
            '443': 'HTTPS',
            '445': 'SMB',
            '587': 'SMTP (submission)',
            '593': 'HTTP RPC Endpoint Mapper',
            '636': 'LDAPS',
            '993': 'IMAPS',
            '995': 'POP3S',
            '1433': 'Microsoft SQL Server',
            '2049': 'NFS',
            '2103': 'Microsoft Message Queue Server',
            '2105': 'Microsoft Message Queue Server',
            '2107': 'Microsoft Message Queue Server',
            '2121': 'FTP (alternative)',
            '3268': 'Global Catalog LDAP',
            '3269': 'Global Catalog LDAPS',
            '3306': 'MySQL',
            '3389': 'RDP',
            '5432': 'PostgreSQL',
            '5900': 'VNC',
            '5901': 'VNC',
            '5902': 'VNC',
            '5903': 'VNC',
            '5985': 'WinRM HTTP',
            '5986': 'WinRM HTTPS',
            '6379': 'Redis',
            '8080': 'HTTP Alternate',
            '8443': 'HTTPS Alternate',
            '11211': 'Memcached',
            '5040': 'WinRM',
            '47001': 'WinRM',
            '27017': 'MongoDB',
        }

    def get_tailwind_css(self):
        url = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch Tailwind CSS. Using default styles.")
            return ""

    def most_common(self, lst):
        return max(set(lst), key=lst.count)

    def parse_directories(self):
        for ip_folder in os.listdir(self.results_dir):
            ip_path = os.path.join(self.results_dir, ip_folder)
            if os.path.isdir(ip_path):
                scans_dir = os.path.join(ip_path, 'scans')
                if os.path.exists(scans_dir):
                    self.data[ip_folder] = {
                        'nmap_scans': {},
                        'port_scans': {}
                    }
                    self.parse_scans_directory(ip_folder, scans_dir)
                else:
                    print(f"Warning: 'scans' directory not found for IP {ip_folder}")

    def parse_scans_directory(self, ip, scans_dir):
        for item in os.listdir(scans_dir):
            item_path = os.path.join(scans_dir, item)
            if os.path.isfile(item_path) and item.endswith('.txt'):
                self.process_file(item_path, self.data[ip]['nmap_scans'], is_nmap=True)
            elif os.path.isdir(item_path):
                match = re.match(r'tcp(\d+)', item)
                if match:
                    port = match.group(1)
                    self.data[ip]['port_scans'][port] = {
                        'files': {},
                        'default_service': self.common_ports.get(port, 'Unknown')
                    }
                    for file in os.listdir(item_path):
                        if file.endswith('.txt'):
                            file_path = os.path.join(item_path, file)
                            self.process_file(file_path, self.data[ip]['port_scans'][port]['files'], is_nmap=False)

    def parse_nmap_output(self, content):
        ports_info = {}
        port_lines = re.findall(r'(\d+/\w+)\s+(\w+)\s+(.+)', content)
        for port, state, service in port_lines:
            port_number = port.split('/')[0]
            severity = 'Low'
            if service.lower() in ['http', 'https', 'ftp', 'ssh', 'telnet', 'smtp', 'pop3', 'imap', 'rdp', 'vnc', 'rpc']:
                severity = 'Medium'
            elif service.lower() in ['mssql', 'mysql', 'postgresql', 'mongodb', 'redis', 'memcached', 'ldap', 'smb', 'netbios']:
                severity = 'High'
            ports_info[port_number] = {
                'state': state,
                'service': service.strip(),
                'severity': severity
            }
        return ports_info

    def process_file(self, file_path, target_dict, is_nmap):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            file_name = os.path.basename(file_path)
            if is_nmap:
                target_dict[file_name] = {
                    'content': content,
                    'ports_info': self.parse_nmap_output(content)
                }
            else:
                target_dict[file_name] = {'content': content}
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

    def generate_html(self):
        template = self.env.get_template('report_template.html')
        return template.render(data=self.data, tailwind_css=self.tailwind_css)

    def save_html(self, html_content, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Report successfully generated: {output_file}")
        except Exception as e:
            print(f"Error saving HTML file: {str(e)}")

    def run(self, output_file):
        self.parse_directories()
        if not self.data:
            print("No data found. Make sure the directory structure is correct.")
            return
        html_content = self.generate_html()
        self.save_html(html_content, output_file)

if __name__ == "__main__":
    results_directory = os.getcwd()  # Use the current working directory
    output_file = "autovisual_report.html"
    
    generator = AutoReconReportGenerator(results_directory)
    generator.run(output_file)
