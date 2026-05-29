# Contributing

## Branches

Create a new branch for every change. Use a short, descriptive name prefixed by the change type:

| Prefix | Use for |
|--------|---------|
| `feat/` | new content or features (e.g. `feat/add-jane-doe`) |
| `fix/` | corrections to existing content (e.g. `fix/broken-publication-link`) |
| `docs/` | README or documentation updates |
| `chore/` | dependencies, config, or tooling |

When a GitHub issue exists, prefix the branch name with the issue number:

```bash
git checkout -b feat/42-add-jane-doe
```

If there is no associated issue:

```bash
git checkout -b feat/add-jane-doe
```

Open a pull request against `main` when ready.

## Closing issues automatically

Reference the related issue in your pull request description using a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) so GitHub closes it automatically when the PR is merged:

```
Closes #42
```

Supported keywords: `Closes`, `Fixes`, `Resolves` (case-insensitive). Place the reference in the PR body, not in a commit message.

## Commit messages

This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard:

```
<type>: <short description>
```

Examples:

```
feat: add Jane Doe to people
fix: correct publication year for doe2024saferl
docs: update setup instructions in README
chore: bump jekyll dependency
```

Keep the description short and written in the imperative ("add", "fix", "update" — not "added" or "fixes").
