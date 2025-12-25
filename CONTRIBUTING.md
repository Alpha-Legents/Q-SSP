# Contributing to Q-SSP

Thank you for your interest in contributing to the Quantum-Stable Sanitization Protocol! This project aims to advance secure data sanitization through quantum entropy, and we welcome contributions from researchers, developers, and security professionals.

---

## 🎯 How You Can Help

We're particularly interested in contributions in these areas:

### 1. **Testing & Validation**
- Test Q-SSP on different hardware configurations
- Validate entropy measurements across various drive types
- Perform forensic recovery attempts and document results
- Benchmark performance on different systems

### 2. **Platform Support**
- Linux/Unix implementation (translating Windows-specific code)
- macOS support
- BSD variants
- Cross-platform testing and compatibility fixes

### 3. **Security Enhancements**
- Hardware QRNG integration (Quantis, IDQ devices)
- Additional entropy sources as fallbacks
- Enhanced SSD-specific sanitization methods
- Cryptographic improvements

### 4. **Performance Optimization**
- Multi-threaded overwrite operations
- Optimized I/O patterns for different drive types
- Memory usage optimization for large drives
- Caching strategies for quantum entropy

### 5. **Documentation**
- Improve code comments and docstrings
- Add tutorials and usage examples
- Translate documentation to other languages
- Create video demonstrations

### 6. **Research**
- Formal security proofs
- Comparative analysis with other sanitization methods
- Advanced entropy analysis techniques
- Academic paper reviews and feedback

---

## 🚀 Getting Started

### Prerequisites

Before contributing, make sure you have:
- Python 3.8 or higher
- Git installed and configured
- A GitHub account
- **Administrator/root access** for testing (use VMs!)
- Basic understanding of data sanitization concepts

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/Alpha-Legents/Q-SSP.git
   cd Q-SSP
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a new branch for your work:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 🧪 Testing Guidelines

### **CRITICAL: Safety First**

**NEVER test on production drives or drives containing important data.**

- ✅ Use virtual disks (VirtualBox, VMware, Hyper-V)
- ✅ Use dedicated test drives you can safely wipe
- ✅ Double-check drive selection before running
- ✅ Keep backups of everything important
- ❌ NEVER run on your primary OS drive

### Creating Test Environments

**Option 1: Virtual Disk (Recommended for beginners)**
```bash
# Windows (PowerShell as Administrator)
$vhdPath = "C:\test-disk.vhdx"
New-VHD -Path $vhdPath -SizeBytes 1GB -Dynamic
Mount-VHD -Path $vhdPath

# Linux
dd if=/dev/zero of=test-disk.img bs=1M count=1024
sudo losetup /dev/loop0 test-disk.img
```

**Option 2: USB Flash Drive**
- Use a cheap USB drive you don't need
- Clearly label it "TEST ONLY"
- Verify it contains no important data

**Option 3: Old/Spare Drives**
- Repurpose old hard drives or SSDs
- Physically label them as test drives
- Keep them separate from production hardware

### What to Test

When testing Q-SSP, please document:

1. **System Configuration:**
   - OS version (e.g., Windows 11 22H2)
   - CPU and RAM
   - Drive type (HDD/SSD/NVMe)
   - Drive capacity

2. **Performance Metrics:**
   - Time to complete
   - Throughput (MB/s)
   - Memory usage during operation
   - CPU utilization

3. **Entropy Results:**
   - Measured Shannon entropy (should be ~7.99 bits/byte)
   - Any anomalies or patterns detected
   - Pre/post SHA-256 hashes

4. **Recovery Testing:**
   - Tools used (PhotoRec, Foremost, Scalpel, etc.)
   - Recovery success rate (should be 0%)
   - Any partial data recovered

5. **Issues Encountered:**
   - Error messages
   - Unexpected behavior
   - Edge cases or corner cases

---

## 📝 Code Contribution Guidelines

### Code Style

- Follow **PEP 8** Python style guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Comment complex logic

**Example:**
```python
def calculate_entropy(data: bytes) -> float:
    """
    Calculate Shannon entropy of byte sequence.
    
    Args:
        data: Byte sequence to analyze
        
    Returns:
        Entropy value in bits per byte (0-8)
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Cannot calculate entropy of empty data")
    
    # Count byte frequency
    frequency = {}
    for byte in data:
        frequency[byte] = frequency.get(byte, 0) + 1
    
    # Calculate Shannon entropy
    entropy = 0.0
    length = len(data)
    for count in frequency.values():
        p = count / length
        entropy -= p * math.log2(p)
    
    return entropy
```

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
Add Linux support for hardware seizure layer

- Implement /dev/sdX device handling
- Add root permission checks
- Update documentation for Linux usage
```

**Bad:**
```
fixed stuff
```

### Pull Request Process

1. **Update documentation** if you changed functionality
2. **Add tests** for new features (when applicable)
3. **Update CHANGELOG.md** with your changes
4. **Ensure all tests pass** before submitting
5. **Write a clear PR description** explaining:
   - What problem does this solve?
   - What changes did you make?
   - How did you test it?

---

## 🔬 Research Contributions

### Academic Feedback

If you're reviewing Q-SSP from an academic perspective:

1. **Open an issue** with the "research-feedback" label
2. Reference specific sections of the whitepaper
3. Cite relevant literature if applicable
4. Suggest improvements with justification

### Empirical Studies

If you conduct independent testing:

1. Document your methodology thoroughly
2. Share raw data (when appropriate)
3. Include statistical analysis
4. Submit findings as an issue or discussion post

### Formal Verification

If you work on formal proofs or security analysis:

1. Clearly state assumptions and threat models
2. Use standard cryptographic notation
3. Reference established security definitions
4. Consider submitting to academic venues

---

## 🐛 Bug Reports

### Before Submitting a Bug Report

- Check if the bug has already been reported
- Verify you're using the latest version
- Test on a clean installation
- Gather system information

### What to Include

```markdown
**Describe the bug:**
A clear description of what went wrong.

**To Reproduce:**
Steps to reproduce the behavior:
1. Run 'python main.py'
2. Select drive '...'
3. Observe error '...'

**Expected behavior:**
What you expected to happen.

**System Information:**
- OS: [e.g., Windows 11 22H2]
- Python Version: [e.g., 3.11.2]
- Q-SSP Version: [e.g., 1.0.0]
- Drive Type: [e.g., Samsung 970 EVO NVMe 500GB]

**Logs:**
```
Paste relevant log output here
```

**Additional context:**
Any other information that might be relevant.
```

---

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** - why is this feature needed?
3. **Propose a solution** - how might it work?
4. **Consider trade-offs** - what are the downsides?

---

## 📚 Documentation Contributions

Documentation improvements are highly valued:

- Fix typos or grammatical errors
- Clarify confusing sections
- Add examples and tutorials
- Improve code comments
- Translate to other languages

Even small documentation fixes are welcome! No change is too minor.

---

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** - treat others with courtesy and professionalism
- **Be constructive** - offer solutions, not just criticism
- **Be patient** - remember this is a research project, not commercial software
- **Give credit** - acknowledge others' contributions
- **Stay on topic** - keep discussions focused on Q-SSP

### Communication Channels

- **GitHub Issues** - bug reports and feature requests
- **GitHub Discussions** - general questions and ideas
- **Pull Requests** - code contributions
- **Email** - sensitive security disclosures (aaronlijo6a@gmail.com)

---

## 🔒 Security Disclosures

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. **Email directly** to aaronlijo6a@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

We'll respond within 48 hours and work with you on disclosure.

---

## 📄 License

By contributing to Q-SSP, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Recognition

Contributors will be:
- Listed in the project README
- Acknowledged in release notes
- Credited in academic publications (where applicable)

---

## ❓ Questions?

If you have questions about contributing:

1. Check the [FAQ in the README](README.md#-frequently-asked-questions)
2. Search existing [GitHub Issues](https://github.com/Alpha-Legents/Q-SSP/issues)
3. Open a [new discussion](https://github.com/Alpha-Legents/Q-SSP/discussions)
4. Email aaronlijo6a@gmail.com

---

## 🎓 Learning Resources

New to data sanitization or quantum entropy? Here are some resources:

- **NIST SP 800-88 Rev. 1** - Media Sanitization Guidelines
- **Shannon's "A Mathematical Theory of Communication"** - Information Theory basics
- **ANU QRNG API Documentation** - Understanding quantum random numbers
- **Python Cryptography Library Docs** - Understanding CSEE implementation

---

**Thank you for contributing to Q-SSP! Every contribution, no matter how small, helps advance secure data sanitization research.**

---

*Last updated: December 2024*
