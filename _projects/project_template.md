---
layout: project
published: false # Set to true when the project is ready to be published

project_name: "Project Name" # The name of the project
status: active # active | completed
start: 2024 # Start year (or YYYY-MM-DD)
end: # End year — leave blank if ongoing

short_summary: >
    A one or two sentence summary of the project shown on the project
    cards and in search engine previews.

cover_image: # Path to cover image, e.g. /assets/images/projects/my_project.jpg
    # Can also be a URL.

website: # Official project website, if any
code_repository: # URL to the code repository (GitHub, GitLab, etc.)
project_coordinator: # Name of the project coordinator if not IDeA

funding: # Funding source, e.g. Swiss National Science Foundation
aramis_url: # URL to the ARAMIS project page, e.g. https://www.aramis.admin.ch/...

plotly: false # Set to true if the project page uses Plotly charts

# Keywords to improve search engine visibility and help users find the project.
keywords:
    - Keyword One
    - Keyword Two

# IDeA team members contributing to the project.
contributors:
    - Contributor One
    - Contributor Two

# External partners, if any.
partners:
    - Partner One
    - Partner Two
---

Write the detailed project description here using standard Markdown.

You can use:

- **Bold**, _italic_, `code`
- Tables, bullet lists, numbered lists
- Mermaid diagrams (fenced code blocks with ```mermaid)
- Plotly charts (set plotly: true in the frontmatter, then add a <div id="..."> and a <script> block)

## Example Mermaid Diagram

```mermaid
graph LR
    A[Input] --> B[Model]
    B --> C[Output]
```

## Example Table

| Method   | Metric ↑ |
| -------- | -------- |
| Baseline | 0.72     |
| Ours     | 0.89     |
