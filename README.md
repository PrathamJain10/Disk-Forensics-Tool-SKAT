# Disk Forensics Tool (SKAT)

> **Note:** This tool is compatible with **Linux/Unix systems only**. Windows is **not supported out-of-the-box**. Significant changes would be required to make this tool work on Windows, due to dependencies on The Sleuth Kit command-line tools and Linux-specific system calls.

A comprehensive Python-based disk forensics automation tool using The Sleuth Kit (TSK) library. This tool simplifies digital forensics workflows by automating common tasks such as disk image acquisition, partition analysis, file extraction, and timeline analysis.

## 🚀 Features

- **Disk Image Acquisition**: Create forensic images with integrity verification (MD5/SHA1)
- **Partition Analysis**: Analyze partition structures and layouts
- **Filesystem Analysis**: Extract detailed filesystem statistics
- **File Listing**: Recursive file listing with metadata
- **File Extraction**: Extract specific files by inode
- **Timeline Analysis**: Create activity timelines for forensic analysis
- **Autopsy Integration**: Launch Autopsy with evidence
- **Comprehensive Logging**: Detailed logging for audit trails
- **Report Generation**: Automated report generation in multiple formats

## 🛠️ Technologies Used

- **Python 3.6+**: Core programming language
- **The Sleuth Kit (TSK)**: Industry-standard digital forensics library
- **Subprocess Management**: Secure command execution
- **JSON/CSV**: Data serialization and reporting
- **Logging**: Comprehensive audit trails

## 📋 Prerequisites

### Linux/Unix Systems
```bash
# Install The Sleuth Kit
sudo apt-get install sleuthkit

# Or on CentOS/RHEL
sudo yum install sleuthkit

# Or on macOS
brew install sleuthkit
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/disk-forensics-tool.git
   cd disk-forensics-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python skat.py verify
   ```

## 📖 Usage

### Basic Commands

```bash
# Verify TSK installation
python skat.py verify

# Analyze partition structure
python skat.py partitions <image_path>

# Extract filesystem statistics
python skat.py fsstat <image_path> [--offset <offset>]

# List files recursively
python skat.py list <image_path> [--offset <offset>]

# Extract file by inode
python skat.py extract <image_path> <inode> [--output <output_path>]

# Create timeline analysis
python skat.py timeline <image_path> [--offset <offset>]

# Run full analysis
python skat.py full <image_path> [--offset <offset>]
```

### Advanced Usage

```bash
# Create forensic image with verification
python skat.py acquire <source_device> [--output <output_path>]

# Launch Autopsy with evidence
python skat.py autopsy <evidence_path>
```

## 📁 Project Structure

```
disk-forensics-tool/
├── skat.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── evidence/           # Acquired forensic images
├── reports/            # Generated analysis reports
├── skat.log           # Application logs
└── samples/           # Sample disk images (not included in repo)
```

## 🔧 Configuration

The tool automatically creates `evidence/` and `reports/` directories for storing forensic images and analysis reports respectively. All operations are logged to `skat.log` for audit purposes.

## 📊 Output Examples

### Partition Analysis
```
Partition Analysis for disk.img
================================================================================
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Size    Description
000:  Meta      0000000000   0000000000   0000000001     512B   Primary Table (#0)
001:  -------   0000000000   0000000062   0000000063    31.5K   Unallocated
002:  000:000   0000000063   0000204799   0000204737  1000.0M   NTFS (0x07)
```

### Filesystem Statistics
```
Filesystem Analysis for disk.img (Offset: 63)
================================================================================
FILE SYSTEM INFORMATION
----------------------------------------
File System Type: NTFS
Volume Name: 
Volume ID: 0x1234567890abcdef
```

## 🛡️ Security Features

- **Integrity Verification**: All acquired images include MD5 and SHA1 hashes
- **Audit Logging**: Comprehensive logging of all operations
- **Safe File Handling**: Secure file operations with error handling
- **Metadata Preservation**: Maintains original file metadata

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for educational and authorized forensic analysis purposes only. Users are responsible for ensuring they have proper authorization before analyzing any disk images. The authors are not responsible for any misuse of this software.

## 📞 Support

For support, please open an issue on GitHub or contact the maintainers.

## 🔗 Related Projects

- [The Sleuth Kit](https://www.sleuthkit.org/) - Core forensics library
- [Autopsy](https://www.autopsy.com/) - GUI forensics platform
- [FTK Imager](https://accessdata.com/products-services/forensic-toolkit-ftk/ftk-imager) - Commercial forensics tool

---

**Note**: This tool is designed for Linux/Unix systems. For Windows forensics, consider using Windows-native tools like FTK Imager or Autopsy. 