# Project Refinement Process

This document outlines the official process for documenting changes and refinements to the Military-grade-quantum-encryption project. Adhering to this process ensures a clear, consistent, and auditable history of the project's evolution.

## 1. Refinement Principles

A "refinement" is any meaningful change to the project. The goal of this process is to capture the *what* and *why* of each change in a structured format. All refinements are stored as immutable records in the `Refinement history/` directory.

### 1.1. Refinement Categories

We use categories inspired by the [Conventional Commits](https://www.conventionalcommits.org/) specification. Each refinement must be assigned one of the following types:

- **feat**: A new feature or user-facing change.
- **fix**: A bug fix.
- **docs**: Changes to documentation only.
- **style**: Code style changes (formatting, white-space, etc.).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing ones.
- **build**: Changes that affect the build system or external dependencies.
- **ci**: Changes to our CI configuration files and scripts.
- **chore**: Other changes that don't modify `src` or `test` files.
- **security**: A change that addresses a security vulnerability.

### 1.2. Metadata and Documentation Standards

Each refinement entry must contain the following metadata and documentation:

- **Author**: The name and email of the person who made the change.
- **Date**: The date the refinement was completed (YYYY-MM-DD).
- **Type**: One of the categories from section 1.1.
- **Summary**: A one-sentence description of the change.
- **Description**: A more detailed explanation of the change, including the problem it solves and the approach taken.
- **Affected Components**: A list of files, modules, or components that were changed.
- **Related Links**: Links to relevant GitHub Issues, Pull Requests, or other external documentation.

## 2. Refinement Workflow

### 2.1. Submission Workflow

1.  **Create a Branch**: All work should be done on a separate Git branch.
2.  **Make Changes**: Implement your feature, fix, or other refinement.
3.  **Create a Refinement File**:
    - Before you commit, create a new Markdown file in the `Refinement history/` directory.
    - Name the file descriptively, e.g., `YYYY-MM-DD_feat_new-api-endpoint.md`.
    - Use the template provided in section 3 to fill out the file.
4.  **Commit Changes**:
    - Stage your code changes AND the new refinement file (`git add .`).
    - Commit your changes using the Conventional Commits format. The commit message should align with the refinement entry.
    - Example: `feat: add user authentication endpoint`
5.  **Open a Pull Request**: Push your branch to the repository and open a Pull Request for review.

### 2.2. Review Process

- The refinement entry file will be reviewed as part of the Pull Request.
- Reviewers will check for clarity, completeness, and adherence to the standards defined in this document.
- Once the Pull Request is approved and merged, the refinement becomes a permanent part of the project's history.

## 3. Refinement Entry Template

Use this template to create new refinement entries.

```markdown
---
Author: Your Name <your.email@example.com>
Date: YYYY-MM-DD
Type: [feat|fix|docs|style|refactor|perf|test|build|ci|chore|security]
---

### Summary

A brief, one-sentence summary of the change.

### Description

A detailed description of the changes. Explain the problem, the solution, and the reasoning behind the implementation.

### Affected Components

- `src/module/file.py`
- `tests/test_file.py`

### Related Links

- **GitHub Issue**: #123
- **Pull Request**: #124
```
