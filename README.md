# IDeA — Industrial Decision Analytics — Research Group Website

Static website for the IDeA (Industrial Decision Analytics) research group, built with [Jekyll](https://jekyllrb.com/) and deployed to GitHub Pages.

## Prerequisites

- **Ruby** 4+

Verify your Ruby version:

```bash
ruby --version
```

## Setup

```bash
# Clone the repository
git clone git@github.com:SasCezar/IDeA.git
cd IDeA

# Install dependencies
bundle install
```

## Running the local server

```bash
bundle exec jekyll serve
```

The site will be available at [http://localhost:4000](http://localhost:4000). Jekyll watches for file changes and rebuilds automatically.

To also reload the browser on changes, add `--livereload`:

```bash
bundle exec jekyll serve --livereload
```

## Project structure

```
IDeA/
├── _config.yml          # Site configuration and navigation
├── _data/
│   └── people/          # One YAML file per person
├── _projects/           # One Markdown file per project
├── _publications/       # One Markdown file per publication
├── _layouts/            # HTML page templates
├── _includes/           # Reusable HTML components (header, footer)
├── _sass/               # Stylesheets
├── assets/              # Images and compiled CSS
├── index.html           # Home page
├── people.html          # People listing page
├── projects.html        # Projects listing page
└── publications.html    # Publications listing page
```

## Adding content

### Adding a person

Create a new YAML file in `_data/people/` named `firstname_lastname.yml`:

```yaml
name: Jane Doe
role: PhD Student          # e.g. Professor, Postdoc, PhD Student, Research Engineer
email: jane.doe@example.com
website: https://janedoe.example.com
photo:                     # /assets/images/people/jane_doe.jpg  (leave blank if none)
orcid:                     # https://orcid.org/0000-0000-0000-0001
scholar:                   # https://scholar.google.com/citations?user=XXXXXXX
linkedin:                  # https://linkedin.com/in/janedoe
github:                    # https://github.com/janedoe
bio: Short biography in one or two sentences.
interests:
  - Machine Learning
  - Natural Language Processing
former: false              # Set to true to move person to the "Former Members" section
```

The person will appear automatically on the People page. The page sorts members by role seniority (Professor → Postdoc → PhD Student → …) and separates current from former members.

Place profile photos in `assets/images/people/` and set the `photo` field to the relative path.

### Adding a project

Create a new Markdown file in `_projects/` named after the project (use underscores, e.g. `my_project.md`):

```markdown
---
layout: project
title: My Project Title
status: active             # active | completed
start: 2024
end:                       # Leave blank if ongoing
description: >
  One-paragraph description shown on the projects listing page.
image:                     # /assets/images/projects/my_project.jpg
tags:
  - Tag One
  - Tag Two
members:
  - Jane Doe               # Must match the `name` field in _data/people/
funding: Grant or funder name
plotly: false              # Set to true to enable Plotly chart support
---

## Overview

Write the full project description in Markdown here.
```

The project will appear on the Projects listing page and get its own page at `/projects/my_project/`. The Markdown content below the front matter is optional.

### Adding a publication

Create a new Markdown file in `_publications/` using a citation-key style name (e.g. `doe2024mywork.md`):

````markdown
---
layout: publication
title: "Full Paper Title"
authors:
  - Jane Doe
  - John Smith
venue: ICML 2024
year: 2024
type: conference           # conference | journal | workshop | preprint
abstract: >
  Abstract text shown on the publications listing page.
pdf:                       # URL to PDF (arXiv link works)
code:                      # URL to code repository
arxiv: "2401.00000"        # arXiv ID only (no URL prefix)
doi:                       # DOI string
tags:
  - Machine Learning
plotly: false
---

## Key Contributions

- Contribution one
- Contribution two

## BibTeX

```bibtex
@inproceedings{doe2024mywork,
  title     = {Full Paper Title},
  author    = {Doe, Jane and Smith, John},
  booktitle = {Proceedings of ICML},
  year      = {2024}
}
```
````

The publication will appear on the Publications listing page, grouped by year, and get its own page at `/publications/doe2024mywork/`. The Markdown content below the front matter is optional.

## Deployment

The site deploys automatically to GitHub Pages on every push to `main` via the GitHub Actions workflow defined in [.github/workflows/deploy.yml](.github/workflows/deploy.yml). No manual steps are required.

To trigger a manual deployment, go to **Actions → Deploy Jekyll site → Run workflow** in the GitHub repository UI.
