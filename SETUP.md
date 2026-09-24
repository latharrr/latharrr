# How the card works

`today.py` draws `dark_mode.svg` and `light_mode.svg` from a template, filling in live numbers from GitHub's GraphQL API. The workflow in `.github/workflows/build.yaml` runs it every morning at 04:00 UTC, on pushes that touch the generator, and on demand from the Actions tab. It commits the SVGs only when they change. If the API fails, the script exits before writing, so the card keeps its last good numbers.

## Editing

- **Profile rows** (Host, Role, Stack, Shipped…): edit `PROFILE` near the top of `today.py`, then push. Don't edit the SVGs by hand; the next run overwrites them.
- **Colours**: `THEMES` in `today.py`.
- **Portrait**: `art/portrait.txt` is ASCII art made from a photo. To regenerate it from a new photo:
  `pip install pillow && python art/portrait.py path/to/photo.jpg` (adjust `CROP` in that file to frame the head and shoulders).

## Live stats

| Row | Source |
|:--|:--|
| Contributions, Commits | Sum of `contributionsCollection` for every year since the account was created |
| Repositories | Repos you own, forks excluded |
| Merged PRs | Pull requests you authored that were merged |
| Language bar | Bytes per language across repos you own, forks, HTML/CSS and config files excluded |
| Uptime | Days since `BIRTHDAY` in `today.py` |

## Token

The workflow reads two repository secrets (Settings → Secrets and variables → Actions):

- `ACCESS_TOKEN`: a fine-grained personal access token with **All repositories** access and read-only **Metadata** and **Contents** permissions. Private repos then count toward the language bar and contributions. Without this secret the script falls back to the workflow's own token and only sees public data.
- `USER_NAME`: `latharrr`.

Run it locally with `ACCESS_TOKEN=$(gh auth token) python today.py`.
