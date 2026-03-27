# Contributing to cq

Thank you for your interest in contributing to cq. This guide explains how to get involved.

---

## **Guidelines for Contributions**

### Ground Rules

- Review issue discussion fully before starting work. Engage in the thread first when an issue is under discussion.
- PRs must build on agreed direction where ones exist. If there is no agreed direction, seek consensus from the core maintainers.
- PRs with "drive-by" unrelated changes or untested refactors will be closed.
- Untested or failing code is not eligible for review.
- PR description **must** follow the PR template and explain **what** changed, **why**, and **how to test**.
- Links to related issues are required.
- Duplicate PRs will be automatically closed.
- Only have 1-2 PRs open at a time. Any further PRs will be closed.

**Maintainers reserve the right to close issues and PRs that do not align with the library roadmap.**

### Code Clarity and Style

- **Readability first:** Code must be self-documenting—if it is not self-explanatory, it should include clear, concise comments where logic is non-obvious.
- **Consistent Style:** Follow existing codebase style (e.g., function naming, Go conventions)
- **No dead/debug code:** Remove commented-out blocks, leftover debug statements, unrelated refactors
- Failure modes must be documented and handled with robust error handling.

### Testing Requirements

- **Coverage:** All new functionality must include unit tests covering both happy paths and relevant edge cases.
- **Passing tests:** All linting and formatting checks must pass (see below on how to run).
- **No silent failures:** Tests should fail loudly on errors. No placeholder tests.

### Scope and Size

- **One purpose per PR:** No kitchen-sink PRs mixing bugfixes, refactors, and features.
- **Small, reviewable chunks:** If your PR is too large to review in under 30 minutes, break it up into chunks.
- Each chunk must be independently testable and reviewable
- If you can't explain why it can't be split, expect an automatic request for refactoring.
- Pull requests that are **large** (>500 LOC changed) or span multiple subsystems will be closed with automatic requests for refactoring.
- If the PR is to implement a new feature, please first make a GitHub issue to suggest the feature and allow for discussion. We reserve the right to close feature implementations and request discussion via an issue.

## How to Contribute

### **Browse Existing Issues** 🔍
- Check the Issues page to see if there are any tasks you'd like to tackle.
- Look for issues labeled **`good first issue`** if you're new to the project—they're a great place to start.

### **Report Issues** 🐛
- **Bugs:** Please use our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yaml) to provide clear steps to reproduce and environment details.
- **Search First:** Before creating a new issue, please search existing issues to see if your topic has already been discussed.
- Provide as much detail as possible, including the steps to reproduce the issue and expected vs. actual behavior.

### **Suggest Features** 🚀
- **Features:** Please use our [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yaml) to describe the problem your idea solves and your proposed solution.
- Share why the feature is important and any alternative solutions you've considered.
- If the PR is to implement a new feature, please first make a GitHub issue to suggest the feature and allow for discussion.

## Before You Start

- **Search for duplicates.** Check [existing issues](https://github.com/mozilla-ai/cq-python/issues) and [open pull requests](https://github.com/mozilla-ai/cq-python/pulls) before starting work.
- **Discuss major changes first.** Open an issue before starting work on: new features, API changes, architectural changes, breaking changes, or new dependencies. This avoids wasted effort and helps maintainers provide early guidance.
- **Set up your development environment.** See the [README](README.md) for prerequisites, installation, and how to run tests and linters.

## Making Changes

### Branch Naming

Use descriptive branch names with one of these prefixes:

| Prefix      | Use case              |
|-------------|-----------------------|
| `feature/`  | New features          |
| `fix/`      | Bug fixes             |
| `refactor/` | Code improvements     |
| `docs/`     | Documentation changes |
| `chore/`    | Maintenance tasks     |

### Tests and Commits

- Write tests for every change. Bug fixes should include a test that reproduces the issue.
- Write clear commit messages that explain *why* the change was made, not just *what* changed.
- Keep commits atomic; each commit should represent one logical change.
- 
## Submitting Your Contribution

1. Fork the repository and clone your fork.
2. Add the upstream remote: `git remote add upstream https://github.com/mozilla-ai/cq-python.git`
3. Create a branch from `main` following the naming conventions above.
4. Make your changes, including tests.
5. Push your branch to your fork and open a pull request against `main`.

Your PR description should include:

- What changed and why.
- How to test the change.
- Links to related issues (use `Fixes #123` or `Closes #456` to auto-close them).

## Review Process

- Expect an initial response within 5 business days.
- Simple fixes typically take around 1 week to merge; complex features may take 2-3 weeks.
- Address review comments with new commits rather than force-pushing during review. This makes it easier for reviewers to see incremental changes.
- Pull requests with no activity for 30 or more days may be closed. You are welcome to reopen or re-submit if you return to the work.

## Your First Contribution

- Look for issues labeled [`good-first-issue`](https://github.com/mozilla-ai/cq-python/labels/good-first-issue) or [`help-wanted`](https://github.com/mozilla-ai/cq-python/labels/help-wanted).
- Comment on the issue to claim it so others know you are working on it.
- Ask questions early; maintainers are happy to help.
- Start small. A well-scoped first PR is easier to review and merge.

## Code of Conduct

This project follows Mozilla's [Community Participation Guidelines](https://www.mozilla.org/about/governance/policies/participation/).

See our full [Code of Conduct](CODE_OF_CONDUCT.md) for details.

## Security

If you discover a security vulnerability, do **not** open a public issue. See [SECURITY.md](SECURITY.md) for responsible disclosure instructions.

## License

By contributing code to this project, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers the project.