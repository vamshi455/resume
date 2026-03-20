# Resume Project

## Overview
Markdown-first resume management: edit in markdown, convert to docx for distribution.

## Directory Structure
- `resume/Vamshi_Resume.md` — Working resume file (always latest, edit this)
- `resume/*.docx` — Versioned docx outputs (do not edit directly)
- `projects/` — Per-project/application context files

## Workflow
1. Edit `resume/Vamshi_Resume.md`
2. Review changes with user
3. When approved, convert to docx: `pandoc resume/Vamshi_Resume.md -f gfm -t docx -o resume/Vamshi_Resume_2026_V{N}.docx`
4. Commit and push to GitHub

## Conversion Commands
- **docx → md**: `pandoc resume/FILE.docx -f docx -t gfm -o resume/Vamshi_Resume.md`
- **md → docx**: `pandoc resume/Vamshi_Resume.md -f gfm -t docx -o resume/Vamshi_Resume_2026_V{N}.docx`

## Versioning
- Markdown file: single file, git tracks history
- Docx files: filename includes version number (V7 is the original, V8 next, etc.)
- Increment version number on each approved conversion

## Project Contexts
- Store in `projects/{company}_{role}.md`
- Each file contains: job description, tailoring notes, technologies, status

## Rules
- Do NOT put specific content in README.md
- Always convert md → docx when user approves changes
- Keep project contexts updated as needed
