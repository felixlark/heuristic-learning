# Security and Sensitive Sources

This repository is a public course and research artifact. Do not open issues, pull requests, commits, or discussion comments that contain secrets or sensitive internal material.

## Do Not Share

- API keys, access tokens, cookies, OAuth device codes, app secrets, or private URLs.
- Feishu/Lark message bodies, document contents, meeting notes, task details, or personal data that are not already public.
- X/Twitter cookies, bearer tokens, API keys, raw bookmark exports, or private account data.
- Private logs, screenshots, videos, or replay files that include credentials, personal data, or confidential business context.
- `.env` files or local machine paths that expose secrets.

## How to Report Safely

For public source signals, use the `Source signal` issue template and provide only public URLs or sanitized summaries.

For internal Feishu/Lark or private X/FieldTheory material:

1. Reduce the material to a sanitized case card or minimal environment.
2. Mark it as an internal clue or source signal.
3. Do not paste the original private content.
4. Provide a verification path that can be run from public repository files.

## Course Boundary

Internal signals can guide course examples only after they are transformed into non-sensitive minimal examples, tests, and feedback reports. Public claims still need public sources or explicit research-hypothesis wording.

## Local Files

Keep credentials in local environment variables or secret managers. `.env` files are ignored by `.gitignore`; do not commit them.

If a secret is accidentally committed, rotate it immediately and remove it from history before publishing.
