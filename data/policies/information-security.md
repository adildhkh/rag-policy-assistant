# Information Security Policy
**Effective Date:** 1 January 2026
**Applies To:** All employees, contractors, and authorized third parties
**Company Context:** Mid-size technology company (200–500 employees)

## 1. Purpose and Objectives
The purpose of this Information Security Policy is to protect the confidentiality, integrity, and availability of the Company’s information assets. As a technology-driven organization, the Company relies heavily on digital systems, cloud services, and distributed work environments, making strong information security controls essential.
This policy establishes minimum security requirements to reduce risks related to data breaches, cyberattacks, misuse of systems, and regulatory non-compliance.

## 2. Scope
This policy applies to: - All Company employees (full-time and part-time) - Contractors, consultants, and temporary staff - Third-party vendors with access to Company systems or data - All Company-owned and approved personal devices
It covers all information assets, including data, systems, networks, applications, and physical facilities.

## 3. Password Requirements and Multi-Factor Authentication (MFA)
### 3.1 Password Standards
All users must comply with the following password requirements:
Minimum length: **12 characters**
Must include at least:
One uppercase letter
One lowercase letter
One number
One special character
Passwords must not include:
Usernames or email addresses
Common dictionary words
Previously used passwords (last 10 passwords)
Passwords must be changed every **90 days** for privileged accounts and every **180 days** for standard user accounts.
### 3.2 Multi-Factor Authentication (MFA)
MFA is mandatory for: - Email systems - VPN access - Cloud platforms (e.g., Git repositories, CRM, cloud consoles)
Accepted MFA methods include: - Authenticator apps (preferred) - Hardware security keys - SMS (allowed only where other methods are not feasible)
**Example:**
An engineer accessing the production cloud console must authenticate using a password and a time-based one-time password (TOTP) from an authenticator app.

## 4. Data Classification
All Company data must be classified according to sensitivity and risk.
### 4.1 Handling Requirements
**Public:** No restrictions
**Internal:** Access limited to employees
**Confidential:** Access granted on a need-to-know basis; encryption required
**Restricted:** Strict access control, logging, encryption at rest and in transit

## 5. Acceptable Use of Company Devices and Networks
### 5.1 Permitted Use
Company devices and networks may be used for: - Business-related activities - Limited personal use that does not interfere with work or security
### 5.2 Prohibited Activities
Installing unauthorized software
Downloading pirated or illegal content
Circumventing security controls
Using Company systems for personal commercial gain
**Example:**
Installing unauthorized torrent software on a Company laptop is strictly prohibited.

## 6. Bring Your Own Device (BYOD)
### 6.1 Eligibility and Approval
BYOD is permitted only with written IT approval and enrollment in the Company’s device management system.
### 6.2 BYOD Security Requirements
Device-level encryption enabled
Screen lock with PIN/password or biometric authentication
Ability to remotely wipe Company data
Up-to-date operating system and security patches
Company reserves the right to revoke BYOD access at any time.

## 7. Cloud Storage and File Sharing
### 7.1 Approved Platforms
Only Company-approved platforms may be used, such as: - Google Workspace / Microsoft 365 - Approved cloud storage and repositories
### 7.2 Restrictions
Sharing confidential or restricted data via personal cloud accounts is prohibited
Public sharing links must not be used for confidential data
**Example:**
Sharing a customer database via a personal Google Drive link is a policy violation.

## 8. Email Security and Phishing Awareness
### 8.1 Email Usage Rules
Do not open suspicious attachments or links
Verify sender identity before sharing sensitive information
### 8.2 Phishing Reporting
Suspected phishing emails must be reported immediately using the “Report Phishing” tool or by contacting IT Security
Regular phishing simulation training may be conducted.

## 9. Incident Reporting Procedures
All security incidents must be reported immediately, including: - Lost or stolen devices - Suspected malware infections - Unauthorized system access
Reports should be made within **1 hour** of discovery to the IT Security team.

## 10. Social Media Usage Guidelines
Employees must: - Avoid sharing confidential or internal information - Clearly state opinions are personal when referencing the Company - Refrain from engaging in hostile or misleading discussions on behalf of the Company

## 11. Physical Security
### 11.1 Badge Access
Employees must wear ID badges at all times in Company offices
Badge sharing is prohibited
### 11.2 Visitor Policy
All visitors must sign in and be escorted
Visitors must wear temporary badges

## 12. Data Breach Response Protocol
### 12.1 Immediate Actions
Isolate affected systems
Notify IT Security and management
Preserve logs and evidence
### 12.2 Investigation and Notification
Conduct root cause analysis
Notify affected customers or authorities where legally required

## 13. Encryption Requirements
Encryption at rest using **AES-256** or equivalent
Encryption in transit using **TLS 1.2 or higher**
Full disk encryption required for all laptops and mobile devices

## 14. Third-Party Vendor Security Requirements
Third-party vendors must: - Comply with Company security standards - Sign data protection and confidentiality agreements - Notify the Company of any security incidents within **24 hours**
Vendors handling restricted data may be subject to security audits.

## 15. Compliance and Enforcement
Violations of this policy may result in disciplinary action, up to and including termination of employment or contract. This policy will be reviewed annually and updated as needed.
**Approved By:** IT Security, Legal, and Executive Management

| Classification | Description | Examples |
| --- | --- | --- |
| Public | Approved for public release | Marketing website content, job postings |
| Internal | For internal use only | Internal policies, project documentation |
| Confidential | Sensitive business or personal data | Employee records, client contracts |
| Restricted | Highly sensitive, critical data | Source code, credentials, financial data |
