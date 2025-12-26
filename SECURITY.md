# Security Policy

## 🛡️ Philosophy
Q-SSP (Quantum-Stable Sanitization Protocol) is a security-critical tool. We prioritize the integrity of our entropy-injection and data-destruction logic. As this is a **Research Prototype**, we follow a coordinated disclosure model to ensure user safety while we bridge the gap between quantum theory and forensic practice.

## 📊 Supported Versions
| Version | Status | Security Updates |
| :--- | :--- | :--- |
| v1.0.0 | Research Prototype | ✅ Active |
| < v1.0.0 | Pre-release | ❌ End of Life |

## 🚨 Reporting a Vulnerability
**Do not open public issues for security vulnerabilities.**

If you discover a flaw in the entropy engine or hardware interaction layer, please use:
1. **GitHub Private Vulnerability Reporting:** [Repository Security Tab]
2. **Direct Email:** `aaronlijo6a+security@gmail.com`
   * **Subject:** `[SECURITY] Q-SSP Vulnerability Report`

### Response Timeline
* **Acknowledgment:** Within 48 hours.
* **Initial Assessment:** Within 7 days.
* **Coordinated Disclosure:** Usually 7 days after a patch is released.

## 🎯 Scope

### ✅ In Scope (The Logic)
* **Entropy Acquisition:** Flaws in the ANU QRNG API integration or validation.
* **CSEE Engine:** Cryptographic weaknesses in the expansion logic (`core/csee.py`).
* **Hardware Seizure:** Failure to bypass OS-level cache or direct sector access errors.
* **Validation:** Flaws in the Shannon Entropy calculation or SHA-256 audit chain.

### ❌ Out of Scope (Externalities)
* **API Availability:** Downtime of the ANU Quantum API.
* **NAND Architecture:** Physical wear-leveling or over-provisioning residual data (documented in the whitepaper).
* **Social Engineering:** User error in drive selection.

## 🏆 Hall of Fame (Recognition)
As a student-led project, we do not currently offer financial bounties. However, researchers who report valid, critical vulnerabilities will be:
1. **Publicly credited** in the `SECURITY.md` Hall of Fame.
2. **Attested** in future academic publications related to the protocol.
3. **Featured** in release notes.

---
### Hall of Fame
*Your name could be here. Help us harden quantum sanitization.*

---
**Last Updated:** December 26, 2025  
**Version:** 1.0
