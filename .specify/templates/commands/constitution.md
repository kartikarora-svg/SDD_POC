---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync
---

# Command: speckit.constitution

## Purpose

This command creates or updates the project constitution at `.specify/memory/constitution.md`. The constitution is a living document that defines the project's core principles, governance, and architectural constraints. All project decisions, features, and implementations must align with constitutional principles.

## User Input Processing

The command accepts natural language input describing:
- Project name and mission
- Core principles (numbered or unnumbered)
- Architectural constraints
- Governance requirements
- Quality attributes

## Execution Flow

### 1. Load Existing Constitution

- Read `.specify/memory/constitution.md` if it exists
- Identify all placeholder tokens in format `[ALL_CAPS_IDENTIFIER]`
- Note: User may require fewer or more principles than in template—adapt accordingly

### 2. Collect/Derive Values

**Project Metadata**:
- `PROJECT_NAME`: From user input or existing value
- `CONSTITUTION_VERSION`: Increment using semantic versioning
- `RATIFICATION_DATE`: Original adoption date (ask if unknown, or use today for new)
- `LAST_AMENDED_DATE`: Today's date if making changes

**Principles**:
- `PRINCIPLE_N_NAME`: Short, descriptive principle name
- `PRINCIPLE_N_STATEMENT`: Clear, declarative statement of the principle
- `PRINCIPLE_N_REQUIREMENTS`: Bulleted list of MUST/SHOULD requirements
- `PRINCIPLE_N_RATIONALE`: Why this principle exists

**Version Increment Rules**:
- **MAJOR**: Backward-incompatible changes, principle removals, redefinitions
- **MINOR**: New principles added, material expansions
- **PATCH**: Clarifications, wording, typo fixes, non-semantic changes

### 3. Draft Updated Constitution

- Replace all placeholders with concrete values
- No bracketed tokens should remain (unless explicitly marked TODO)
- Preserve heading hierarchy
- Ensure each principle section includes:
  - Succinct name line
  - Clear statement
  - Bulleted requirements (MUST/SHOULD/MAY)
  - Explicit rationale
- Include Governance section with:
  - Amendment procedure
  - Versioning policy
  - Compliance review expectations

### 4. Consistency Propagation

Validate and update dependent files:

**Templates** (`.specify/templates/`):
- [ ] `plan-template.md`: Constitution check section aligns with principles
- [ ] `spec-template.md`: Scope/requirements align with principles
- [ ] `tasks-template.md`: Task categories reflect principle-driven work

**Commands** (`.specify/templates/commands/`):
- [ ] All command files reference principles correctly
- [ ] No outdated references to removed principles

**Documentation**:
- [ ] `README.md`: Update if principles changed
- [ ] `docs/`: Update any architectural or governance docs

### 5. Generate Sync Impact Report

Prepend as HTML comment at top of constitution file:

```html
<!--
Sync Impact Report - Constitution vX.Y.Z
========================================
Version Change: vA.B.C → vX.Y.Z
Ratification Date: YYYY-MM-DD
Last Amended: YYYY-MM-DD

PRINCIPLES MODIFIED:
  - Principle N: [Old Title] → [New Title]
  - Added: Principle M: [Title]
  - Removed: Principle K: [Title]

TEMPLATES STATUS:
  ✅ plan-template.md - Updated
  ✅ spec-template.md - Updated
  ⚠️  tasks-template.md - Requires manual review
  ✅ commands/ - All updated

FOLLOW-UP ITEMS:
  - TODO(FIELD): [Explanation if deferred]
  - Manual review needed for [file]

NOTES:
  [Any additional context about this version]
-->
```

### 6. Validation Checklist

Before writing final output:
- [ ] No unexplained bracket tokens remain
- [ ] Version line matches report
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Principles are declarative and testable
- [ ] MUST/SHOULD used appropriately with rationale
- [ ] All dependent templates reviewed and updated

### 7. Write Constitution

Write completed constitution to `.specify/memory/constitution.md` (overwrite).

### 8. Output Summary

Provide user with:
- **New version**: X.Y.Z
- **Bump rationale**: Why this version increment
- **Files flagged**: Any requiring manual follow-up
- **Suggested commit**: `docs: amend constitution to vX.Y.Z (principle additions + governance update)`

## Formatting Requirements

- Use Markdown headings as specified (do not change levels)
- Wrap long lines to <100 characters for readability
- Single blank line between sections
- No trailing whitespace
- ISO 8601 dates (YYYY-MM-DD)

## Partial Updates

If user supplies partial updates (e.g., only one principle revision):
- Still perform full validation
- Still update version appropriately
- Still check template consistency

## Missing Information

If critical info is missing:
- Insert `TODO(FIELD_NAME): explanation`
- Include in Sync Impact Report under "FOLLOW-UP ITEMS"
- Clearly communicate to user what needs resolution

## Important Notes

- DO NOT create a new template; always operate on existing `.specify/memory/constitution.md`
- This command is the single source of truth for constitutional updates
- All changes must be traceable through version history and Sync Impact Reports
- When in doubt about version increment, propose reasoning to user before finalizing

## Example Invocation

```
/speckit.constitution Add a new principle about API-first design: 
All features must expose programmatic APIs before building UI components.
```

This would:
1. Read current constitution
2. Add new principle as Principle N+1
3. Increment MINOR version
4. Update LAST_AMENDED_DATE
5. Check template consistency
6. Generate Sync Impact Report
7. Write updated constitution
8. Report back to user

---

**Command Version**: 1.0  
**Last Updated**: 2025-10-28  
**Maintained By**: Speckit Framework

