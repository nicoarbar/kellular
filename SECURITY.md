# Security policy

## Reporting a vulnerability or exposed data

Please **do not open a public issue**. Report it privately through GitHub:
**Security tab → "Report a vulnerability"** on this repository
(https://github.com/nicoarbar/kellular/security/advisories/new).

Include what you found, how to reproduce it, and the affected files or versions. You can expect an
acknowledgment within about 7 days. This is a small research project run by volunteers, so fix
times are best effort.

## What counts

- Vulnerabilities in the code or its dependencies.
- **Sensitive data committed by mistake**: patient-level data, credentials, API keys or tokens.
  If you find any, report it privately instead of posting it, so it can be removed and, where
  needed, rotated and purged from git history.

## Supported versions

Only the latest commit on `main` is supported while the project is pre-1.0.

## Scope note

Kellular is research software and is not intended for clinical use (see
[DISCLAIMER.md](DISCLAIMER.md)). Model errors or biased predictions are not security
vulnerabilities, but you are welcome to report them as regular issues.
