# Resume Project

## Overview
Markdown-first resume management: master resume as single source of truth, tailored per job requirement, exported to docx/pdf.

## Directory Structure
```
.
├── CLAUDE.md                # How the coworker should behave
├── PROJECT_CONTEXT.md       # Profile, constraints, style preferences
├── resume/
│   ├── master.md            # Single source of truth (edit this)
│   ├── templates/           # Role-based tailoring guides
│   │   ├── ai-engineer.md
│   │   ├── data-eng-lead.md
│   │   └── solutions-arch.md
│   ├── history/             # Snapshots of master at key milestones
│   │   └── 2026-03-20-master-v1.md
│   └── *.docx               # Exported docx versions
├── requirements/            # Job descriptions / role requirements
│   └── {date}-{company}-{role}.md
├── outputs/                 # Tailored resumes per application
│   └── {date}-{company}/
│       ├── resume-tailored.md
│       ├── recruiter-reply-email.md
│       └── keywords-extracted.json
└── scripts/
    └── export_to_pdf.sh     # Pandoc export helper
```

## Workflow

### Editing Master Resume
1. Edit `resume/master.md`
2. Review changes with user
3. When approved, export: `./scripts/export_to_pdf.sh resume/master.md Vamshi_Resume_2026_V{N}`
4. Commit and push to GitHub

### Tailoring for a Job
1. Save job description to `requirements/{date}-{company}-{role}.md`
2. Pick a template from `resume/templates/` as a guide
3. Create tailored resume in `outputs/{date}-{company}/resume-tailored.md`
4. Optionally draft recruiter reply and extract keywords
5. Export tailored version via `./scripts/export_to_pdf.sh`

## Conversion Commands
- **docx → md**: `pandoc resume/FILE.docx -f docx -t gfm -o resume/master.md`
- **md → docx**: `pandoc resume/master.md -f gfm -t docx -o resume/OUTPUT.docx`
- **Export script**: `./scripts/export_to_pdf.sh [input.md] [output-name]`

## Versioning
- `resume/master.md` — always the latest version, git tracks history
- `resume/history/` — manual snapshots at key milestones
- Docx files: filename includes version or company name

## Rules
- Do NOT use internal pipeline names (e.g., KH_PL_Master_Main), schema names (e.g., replica_par, kh_core), internal project codes (e.g., I&DP, VCS&O, NRD), or company-specific abbreviations that an external recruiter would not understand. Always generalize to descriptive terms (e.g., "curated analytical layer", "parent-child pipeline patterns", "value chain optimization platform").
- Do NOT put specific content in README.md
- `resume/master.md` is the single source of truth
- Always convert md → docx when user approves changes
- Tailored resumes go in `outputs/`, never overwrite master
- Resume must NOT exceed 10 pages. If content pushes beyond 10 pages, reduce font size in the pandoc reference doc or export command — never cut content.
- Every page of the docx must have a header containing: Name, LinkedIn profile URL, and GitHub URL. Footer must contain page number (centered). Use `resume/reference-compact.docx` as the pandoc reference doc to enforce this.
- Refer to `PROJECT_CONTEXT.md` for profile, style, and constraints
