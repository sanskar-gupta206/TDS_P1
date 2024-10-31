### GitHub Users and Repositories in Bangalore

- This project scrapes GitHub users in Bangalore with over 100 followers and their repository details using the GitHub API.
- The most interesting finding: A surprising number of developers have repositories primarily in languages other than JavaScript or Python.
- Recommendation: Developers may want to diversify their public repositories across trending languages to attract broader audiences.

#### Overview

This repository includes:
- `users.csv`: Details of GitHub users in Bangalore with over 100 followers.
- `repositories.csv`: Details of the repositories owned by these users.
- Python script used for data extraction.

#### Data Fields

- **users.csv**:
  - `login`, `name`, `company`, `location`, `email`, `hireable`, `bio`, `public_repos`, `followers`, `following`, `created_at`

- **repositories.csv**:
  - `login`, `full_name`, `created_at`, `stargazers_count`, `watchers_count`, `language`, `has_projects`, `has_wiki`, `license_name`
