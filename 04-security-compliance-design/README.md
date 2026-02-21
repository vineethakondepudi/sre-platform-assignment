Secure Deployment Design for a FinTech Microservice
1. Overview

This document describes a secure, compliant deployment architecture for a FinTech microservice handling sensitive financial and personal data. The design focuses on:

Secure CI/CD pipeline

Strong IAM and least-privilege access

Service-to-service mTLS

Compliance-aligned logging (PCI-DSS, SOC2, ISO27001)

Audit logging aligned with PMLA-style requirements

Secrets management and rotation

SBOM generation and supply-chain security

The goal is to ensure confidentiality, integrity, availability, and auditability of the system across the entire software lifecycle.

2. Secure CI/CD Pipeline
2.1 Pipeline Stages

Source Control (GitHub/GitLab)

Protected branches (main/release)

Mandatory code reviews

Signed commits (where possible)

Pre-Merge Checks

SAST (Static Application Security Testing)

Tools: Semgrep, SonarQube, Snyk Code

Fails build on high/critical issues

Dependency scanning

Tools: Snyk, Dependabot, Trivy

Secrets scanning

Tools: GitGuardian, TruffleHog

Prevents committing API keys, tokens, certificates

Build Stage

Build container image in isolated CI runner

Use minimal base images (distroless/alpine where possible)

Pin dependencies and base image digests

Container Security

Image scanning (Trivy/Grype)

Fail pipeline on critical/high vulnerabilities

Sign images (Cosign) and store signatures in registry

DAST (Dynamic Testing)

Run against staging environment

Tools: OWASP ZAP, Burp (automated)

Check for common OWASP Top 10 issues

Deployment

Only signed and scanned images allowed (admission controller / policy)

Progressive delivery (canary/blue-green)

Rollback on SLO or error-rate breach

2.2 Pipeline Security Controls

CI runners use short-lived credentials (OIDC to cloud provider)

No long-lived secrets in CI

All artifacts are immutable and traceable

Full audit trail of who deployed what and when

3. IAM Design (Least Privilege)
3.1 Principles

One service = one IAM role

No shared roles between services

Permissions are:

Minimal

Explicit

Time-bound where possible

3.2 Example Permissions

Microservice IAM role:

Read secrets from Secrets Manager (specific path only)

Write logs to logging service

Read/write to its own database tables

No access to:

Other services’ data

IAM management APIs

Infrastructure APIs

CI/CD IAM role:

Push image to container registry

Deploy to Kubernetes (limited namespace scope)

No access to production data

3.3 Human Access

Engineers use SSO + MFA

Role-based access (ReadOnly, Operator, Admin)

Break-glass access is:

Logged

Time-limited

Requires approval

4. Service-to-Service mTLS
4.1 Why mTLS

Prevents impersonation

Ensures:

Mutual authentication

Encrypted traffic

Strong service identity

4.2 Implementation Options

Service mesh (Istio/Linkerd)

Or application-level TLS using:

Short-lived certificates

Internal CA (Vault / SPIFFE/SPIRE)

4.3 Certificate Management

Certificates are:

Automatically issued

Automatically rotated

Valid for short duration (e.g., 24 hours)

No manual certificate handling by developers

5. Logging and Monitoring (PCI-DSS, SOC2, ISO27001)
5.1 PCI-DSS Logging Requirements

Log:

Authentication events

Authorization failures

Access to sensitive data

Configuration changes

Logs must include:

Timestamp (UTC)

User / service identity

Action performed

Result (success/failure)

Source IP / service

5.2 Log Security

Logs are:

Immutable (WORM storage or append-only)

Centralized (SIEM)

Retained as per policy (e.g., 1 year online, 7 years archive)

Access to logs is restricted and audited

5.3 Observability

Metrics: latency, error rate, throughput, saturation

Traces: request flow across services

Alerts:

SLO burn rate

Security anomalies

Auth failures spikes

6. Audit Log Structure (PMLA-Aligned)
6.1 Audit Log Fields

Each audit event includes:

event_id

timestamp

actor_type (user/service/admin)

actor_id

action (READ/WRITE/DELETE/LOGIN/etc.)

resource_type (ACCOUNT, TRANSACTION, USER_PROFILE, etc.)

resource_id

result (SUCCESS/FAILURE)

reason_code (if failure)

source_ip / source_service

correlation_id / request_id

6.2 Audit Log Properties

Tamper-evident

Write-only for applications

Read access only for:

Compliance

Security

Audit teams

Regular reviews and automated anomaly detection

7. Secrets Management and Rotation
7.1 Storage

All secrets stored in:

Cloud Secrets Manager / HashiCorp Vault

No secrets in:

Git

Docker images

CI variables (long-term)

7.2 Access

Services fetch secrets at runtime using IAM identity

Secrets are scoped per service and per environment

7.3 Rotation

Automatic rotation:

Database passwords

API keys

Certificates

Rotation frequency:

High-risk secrets: 30–60 days

Certificates: hours to days

Zero-downtime rotation using:

Dual credentials

Grace periods

8. SBOM and Supply Chain Security
8.1 SBOM Generation

Generate SBOM at build time:

Tools: Syft, CycloneDX, SPDX

Store SBOM artifact with build

8.2 Usage

Track vulnerable dependencies

Support incident response:

“Where is log4j used?”

Enforce policies:

Block builds with banned components

8.3 Image Provenance

Sign images (Cosign)

Verify signatures at deploy time

Only trusted build pipelines can produce deployable artifacts

9. Common Anti-Patterns to Avoid

Hardcoded secrets in code or YAML

Shared IAM roles across services

Long-lived credentials in CI/CD

No mTLS or plain-text internal traffic

No audit logs for sensitive actions

No vulnerability scanning in pipeline

No image signing or provenance checks

10. Conclusion

This design provides a defense-in-depth security posture:

Secure-by-default CI/CD

Strong identity and least privilege

Encrypted and authenticated service communication

Compliance-aligned logging and auditing

Automated secrets management

Strong supply-chain security with SBOM and image signing

This approach aligns well with PCI-DSS, SOC2, and ISO27001 expectations and is suitable for a production-grade FinTech environment.
