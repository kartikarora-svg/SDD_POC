# Finalytics Speckit

This directory contains the **Speckit framework** for the Finalytics project—a structured approach to project governance, planning, and specification management.

## Directory Structure


```
.specify/
├── README.md                          # This file
├── memory/
│   └── constitution.md                # Project constitution (core principles & governance)
└── templates/
    ├── plan-template.md               # Template for feature plans
    ├── spec-template.md               # Template for technical specifications
    ├── tasks-template.md              # Template for task lists
    └── commands/
        └── constitution.md            # Constitution command documentation
```

## What is Speckit?

Speckit is a lightweight framework for maintaining project consistency through:

1. **Constitution**: A living document defining core principles, architectural constraints, and governance
2. **Templates**: Standardized formats for plans, specs, and tasks that ensure constitutional alignment
3. **Commands**: Structured workflows for creating and updating project artifacts

## Core Concepts

### The Constitution

The constitution (`.specify/memory/constitution.md`) is the foundational governance document for Finalytics. It defines:

- **Project Mission**: What Finalytics aims to achieve
- **Core Principles**: 5 non-negotiable principles that guide all decisions
- **Architectural Constraints**: Technical requirements and quality attributes
- **Governance**: How the constitution evolves and how compliance is ensured

**All project work must align with constitutional principles.**

### Templates

Templates ensure consistency and constitutional compliance across all project artifacts:

- **`plan-template.md`**: High-level feature plans with principle alignment checks
- **`spec-template.md`**: Detailed technical specifications with requirements traceability
- **`tasks-template.md`**: Categorized task lists organized by constitutional principles

### Commands

Commands provide structured workflows for common operations:

- **`/speckit.constitution`**: Create or update the project constitution

## Usage

### Creating a New Feature

1. **Check Constitutional Alignment**: Review `.specify/memory/constitution.md` to identify relevant principles
2. **Create a Plan**: Copy `plan-template.md` and fill in constitutional compliance checks
3. **Write a Spec**: Use `spec-template.md` to detail requirements, linking each to principles
4. **Generate Tasks**: Break down work using `tasks-template.md`, categorized by principle
5. **Implement & Validate**: Ensure implementation satisfies constitutional requirements

### Updating the Constitution

Use the `/speckit.constitution` command to propose amendments:

```
/speckit.constitution [description of changes]
```

The command will:
- Update the constitution
- Increment version appropriately (MAJOR/MINOR/PATCH)
- Check dependent templates for consistency
- Generate a Sync Impact Report

## Finalytics Constitutional Principles

The Finalytics platform is governed by 5 core principles:

1. **On-Demand Document Intelligence**: 10-K Analyzer with OCR and RAG-powered Q&A
2. **Actionable & Shareable Analysis**: Export to PDF/Doc and email sharing
3. **Real-Time Market Awareness**: Live news feed with AI summarization
4. **Live Ticker RAG Agent**: Yahoo Finance integration with natural language queries
5. **Seamless Comparative Analysis**: Stock comparison tool with side-by-side metrics

See `.specify/memory/constitution.md` for complete details.

## Contributing

### Before Starting Work

- [ ] Read the constitution to understand core principles
- [ ] Review relevant templates for the type of work
- [ ] Ensure your work aligns with at least one constitutional principle
- [ ] Include principle compliance statements in PRs

### When Making Changes

- Keep the constitution as the single source of truth
- Update templates when governance changes
- Maintain traceability from principles → specs → tasks → code
- Document architectural decisions with constitutional references

## Version History

- **v1.0.0** (2025-10-28): Initial constitution ratified with 5 core principles

## Questions?

Refer to:
- `.specify/memory/constitution.md` for governance and principles
- `.specify/templates/` for planning and specification guidance
- `.specify/templates/commands/` for command documentation

---

**Maintained By**: Finalytics Team  
**Framework Version**: Speckit 1.0

