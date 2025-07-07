# Contributing to Military-Grade Quantum Encryption Framework

We welcome contributions to this project! To ensure a smooth and efficient collaboration, please follow these guidelines.

## Refinement Process

This project follows a structured refinement process to ensure all changes are documented consistently and transparently. Before making any contributions, you must familiarize yourself with this process.

**Please read the [Refinement Process](./REFINEMENT_PROCESS.md) documentation for detailed guidelines, workflows, and templates.**

## How to Contribute

1.  **Fork the Repository**: Start by forking the project repository to your GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/your-username/Military-Grade-Quantum-Encryption.git
    cd Military-Grade-Quantum-Encryption
    ```
3.  **Create a New Branch**: Create a new branch for your feature or bug fix. Use a descriptive name:
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/issue-description
    ```
4.  **Make Your Changes**: Implement your changes, ensuring they adhere to the project's coding style and conventions.
5.  **Test Your Changes**: Before submitting, make sure your changes pass all existing tests and add new tests for new functionalities.
6.  **Commit Your Changes**: Write clear and concise commit messages. A good commit message explains *what* was changed and *why*.
    ```bash
    git commit -m "feat: Add new quantum key distribution simulation"
    # or
    git commit -m "fix: Resolve issue with hybrid encryption decryption"
    ```
7.  **Push to Your Fork**: Push your local branch to your forked repository on GitHub:
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Create a Pull Request (PR)**: Go to the original repository on GitHub and create a new Pull Request from your forked branch. Provide a detailed description of your changes.

## Coding Style and Conventions

*   **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
*   **Docstrings**: Use [Google style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for all functions, classes, and modules.
*   **Type Hinting**: Use type hints for function arguments and return values.
*   **Comments**: Add comments where necessary to explain complex logic.

## Reporting Bugs

If you find a bug, please open an issue on GitHub. Include:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Actual behavior.
*   Screenshots or error messages (if applicable).
*   Your operating system and Python version.

## Feature Requests

If you have an idea for a new feature, please open an issue on GitHub to discuss it. Describe:

*   The problem you're trying to solve.
*   How your proposed feature would solve it.
*   Any alternatives you've considered.

## Security Vulnerabilities

If you discover a security vulnerability, please do NOT open a public issue. Instead, please contact [your-security-email@example.com] directly. We appreciate your responsible disclosure.

## Code Review Guidelines

Code reviews are a critical part of our development process, ensuring code quality, catching bugs, improving design, and sharing knowledge. Both authors and reviewers have responsibilities to make the process effective.

### For Authors (Those Submitting Code)

*   **Self-Review First**: Before opening a PR, review your own code. Check for obvious errors, adherence to style guides, and clarity.
*   **Clear Description**: Provide a clear and concise description in your Pull Request. Explain what problem it solves, how it solves it, and any relevant context or design decisions.
*   **Small, Focused PRs**: Aim for smaller, focused Pull Requests that address a single concern. This makes reviews easier and faster.
*   **Respond to Feedback**: Be open to feedback and engage in constructive discussions. Address comments promptly and update your PR as needed.
*   **Verify Changes**: Ensure all automated tests pass and manually verify your changes work as expected after addressing review comments.

### For Reviewers (Those Reviewing Code)

*   **Be Timely**: Try to review PRs in a timely manner to keep the development process flowing.
*   **Be Constructive**: Provide clear, actionable, and constructive feedback. Focus on the code, not the person.
*   **Understand the Goal**: Read the PR description to understand the intent of the changes.
*   **Check for**: 
    *   **Correctness**: Does the code do what it's supposed to do? Are there any edge cases missed?
    *   **Readability & Maintainability**: Is the code easy to understand? Does it follow coding conventions?
    *   **Efficiency**: Are there any obvious performance bottlenecks?
    *   **Security**: Are there any potential security vulnerabilities?
    *   **Tests**: Are there adequate tests for the changes? Do they cover critical paths?
*   **Ask Questions**: If something is unclear, ask for clarification rather than making assumptions.
*   **Approve or Request Changes**: Clearly indicate whether the PR is approved or if changes are required, providing specific reasons for the latter.

Thank you for contributing to the Military-Grade Quantum Encryption Framework!