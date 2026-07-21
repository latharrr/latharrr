# Setup

## One-time setup (~5 min)

1. **Push these files** to `latharrr/latharrr` (replace current contents).

2. **Create a fine-grained PAT** — GitHub → Settings → Developer settings → Fine-grained tokens:
   - Repository access: All repositories
   - Account permissions: `Followers`, `Starring`, `Watching` → Read
   - Repository permissions: `Commit statuses`, `Contents`, `Issues`, `Metadata`, `Pull requests` → Read

3. **Add repo secrets** — `latharrr/latharrr` → Settings → Secrets → Actions:
   - `ACCESS_TOKEN` = the PAT from step 2
   - `USER_NAME` = `latharrr`

4. **Run it** — Actions tab → "README build" → Run workflow.

## Editing the card

- **Static fields** (Host, Role, Languages, etc.): edit `dark_mode.svg` and `light_mode.svg` directly.
- **Dynamic stats** (repos, stars, commits, followers, LOC, uptime): auto-update daily at 04:00 UTC via `today.py`.
- **Keep all `id="..."` attributes** in the SVGs — the script writes dynamic values into those elements.

## Credit

Design and automation adapted from [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant).
