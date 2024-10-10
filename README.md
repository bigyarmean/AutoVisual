# AutoVisual

## Project Summary

### Overview:
AutoVisual is a complementary tool designed to work hand-in-hand with Tib3rius' AutoRecon. It enhances the visualization and analysis of AutoRecon's output by generating an interactive HTML report. AutoVisual is aimed at cybersecurity professionals, penetration testers, and CTF enthusiasts who want to quickly interpret and navigate through the wealth of information gathered by AutoRecon.

### Key Features:
- Generates interactive HTML reports from AutoRecon output
- Integrates various scan results into a unified view
- Provides a visually appealing interface with Tailwind CSS styling
- Includes dark mode toggle for improved readability
- Implements search functionality within the report
- Uses collapsible sections for organized information display
- Offers copy-to-clipboard functionality for scan results

### Technologies Used:
- Python 3.x
- Jinja2 templating engine
- Tailwind CSS for styling
- JavaScript for interactive features
- HTML5 for report structure

### Use Cases:
- Enhance AutoRecon output visualization for penetration testing
- Quickly navigate and analyze reconnaissance data in CTF competitions
- Improve reporting capabilities for network security audits
- Facilitate the teaching of network reconnaissance interpretation

### Skills Demonstrated:
- Data Parsing and Analysis
- Web Development (HTML, CSS, JavaScript)
- Python Programming
- Report Generation and Documentation
- Integration with Existing Security Tools

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/bigyarmean/autovisual.git
   cd autovisual
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage with AutoRecon

1. First, run Tib3rius' AutoRecon on your target(s). If you haven't installed AutoRecon, you can find it here: [AutoRecon GitHub](https://github.com/Tib3rius/AutoRecon)

   Example AutoRecon command:
   ```
   autorecon 192.168.1.100
   ```

2. After AutoRecon completes, navigate to the results directory:
   ```
   cd results
   ```

3. Place the AutoVisual script in this results directory.

4. Run AutoVisual:
   ```
   python autovisual.py
   ```

5. AutoVisual will generate an HTML report named `autovisual_report.html` in the same directory.

## Features

### Interactive HTML Report
- **Tabbed Interface**: Easy navigation between different IP addresses scanned by AutoRecon.
- **Collapsible Sections**: Organize scan results for better readability.
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing.
- **Search Functionality**: Quickly find specific information within the report.

### Comprehensive Data Visualization
- Visualizes Nmap scan results, including open ports and services
- Shows severity ratings for identified services (in beta)

## Configuration

- Modify the `report_template.html` file to customize the HTML report layout.
- Adjust the parsing methods in the script to extract additional information from AutoRecon's output as needed.

## Contributing

Contributions to improve AutoVisual are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

[MIT License](LICENSE)

## Acknowledgments

- [AutoRecon by Tib3rius](https://github.com/Tib3rius/AutoRecon): The primary reconnaissance tool that AutoVisual is designed to complement.
- [Nmap](https://nmap.org/): The powerful network scanning tool used by AutoRecon.
- [Tailwind CSS](https://tailwindcss.com/): For styling the HTML report.

---

For any questions or issues, please open an issue on the GitHub repository.
