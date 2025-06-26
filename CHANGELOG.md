# Changelog

All notable changes to the Disk Forensics Tool (SKAT) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Comprehensive documentation
- Test suite
- Contributing guidelines

### Changed
- Reorganized project structure for better maintainability
- Improved error handling and logging
- Enhanced documentation with examples

### Fixed
- Windows compatibility issues (tool designed for Linux/Unix)
- Import errors with pytsk3 module
- Directory structure inconsistencies

## [1.0.0] - 2024-06-26

### Added
- **Core Features**:
  - Disk image acquisition with integrity verification
  - Partition analysis using mmls
  - Filesystem statistics extraction using fsstat
  - Recursive file listing using fls
  - File extraction by inode using icat
  - Timeline analysis for forensic investigations
  - Autopsy integration capabilities

- **Security Features**:
  - MD5 and SHA1 hash verification
  - Comprehensive audit logging
  - Safe file handling with error recovery
  - Metadata preservation

- **Documentation**:
  - Comprehensive README with usage examples
  - Installation instructions for multiple platforms
  - Security and disclaimer information
  - Contributing guidelines

- **Project Structure**:
  - Organized directory structure (evidence/, reports/, samples/)
  - Proper .gitignore for sensitive files
  - MIT License
  - Test suite for validation

### Technical Details
- **Language**: Python 3.6+
- **Dependencies**: The Sleuth Kit (TSK), pytsk3
- **Platform**: Linux/Unix systems (primary), macOS support
- **Architecture**: Command-line interface with modular design

### Known Issues
- Limited Windows compatibility due to TSK tool dependencies
- Requires system-level installation of The Sleuth Kit tools
- Large disk images may require significant processing time

---

## Version History

### Version 1.0.0
- Initial release with core forensics capabilities
- Focus on Linux/Unix compatibility
- Comprehensive documentation and testing

### Future Versions
- Enhanced Windows compatibility
- GUI interface development
- Additional filesystem support
- Performance optimizations
- Plugin system architecture 