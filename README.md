# Static Site Generator

A minimal static site generator implemented from scratch in Python with a small Bash wrapper. It converts Markdown to HTML using a hand-rolled parser based on regular expressions (no external Markdown libraries), and handles asset copying and base-path handling for deployment.

Example output (built from the `content/` directory via `build.sh`):  
[Sample pages](https://geometricgrouptheorydev.github.io/static-site-generator/)

---

## Features

- Custom Markdown to HTML conversion using regular expressions
- Simple templating for consistent layout
- Configurable base path for GitHub Pages and other hosts
- Single-command local preview and build
- Zero third-party Python dependencies

---

## Installation and Usage

**Requirements**

- Unix-like environment (Linux, macOS, or WSL)
- Python 3
- Bash / POSIX shell

**Steps**

1. Clone this repository.
2. Make `main.sh` and `build.sh` executable:
   ```bash
   chmod +x main.sh build.sh
   ```
3. Replace the contents of the content/ directory with your own Markdown
(tables and nested bold/italics are not yet supported).
4. Replace the images in static/images/ as needed.
5. (Optional) Adjust styling in static/index.css.
6. Run ```./main.sh``` Then visit http://localhost:8888 for a local preview.

## Building

General build:

- ```./build.sh [basepath]``` outputs the static site to docs/.
- For GitHub project pages (e.g. USERNAME.github.io/REPO_NAME): ```./build.sh github```
(Automatically detects /REPO_NAME/ as the base path.)
- GitHub user/organization site (USERNAME.github.io): ```./build.sh "/"``` Then push to the USERNAME.github.io repository.

Other hosts:

- Pass the base path for your host (often /).
- With no argument, the default base path is /.

Note: build.sh only builds the site; deployment is handled by your hosting provider (e.g. GitHub Pages on push).

## Dependencies

- Python 3 (standard library only)
- Bash / POSIX-compatible shell
- Unix-like OS (Linux, macOS, WSL)
- No third-party Python packages are required.

## Roadmap / Future Enhancements

- Support for nested bold/italics/strikethrough
- Basic Markdown table support
- Optional MathJax integration for LaTeX-style math (would introduce a JS dependency)
- Additional templating and layout options

## Contributions

This is currently a personal exploration, so I’m not accepting external pull requests.

Bug reports: please open a GitHub issue.
Suggestions and ideas: also welcome via issues.