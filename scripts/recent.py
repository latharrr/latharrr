"""Rebuild the "Recent commits" list in README.md from public GitHub data.

Fixed allowlist of repositories, public API only, no private fetches.
If a repository cannot be read or its data looks wrong, its previous line is kept.
If nothing changed, or the README does not have the expected shape, nothing is written.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime

OWNER = "latharrr"
REPOS = [  # (repo, label)
    ("linkedin-bot", "linkedin-bot"),
    ("Proofmart.shop", "ProofMart"),
    ("gapl", "Gapl"),
    ("lpuconnect", "LpuTV"),
]
START = "Updated daily from the GitHub API, latest commit per project."
END = "<sub>Open to"
SHA = re.compile(r"^[0-9a-f]{40}$")


def fetch(repo):
    url = f"https://api.github.com/repos/{OWNER}/{repo}/commits?per_page=1"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme-recent",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {}),
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    c = data[0]
    sha = c["sha"]
    msg = c["commit"]["message"].splitlines()[0].strip()
    when = datetime.strptime(c["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
    if not SHA.match(sha) or not msg:
        raise ValueError("malformed entry")
    return sha, msg, when


def esc(text):
    text = re.sub(r"\s+", " ", text)
    if len(text) > 80:
        text = text[:79].rstrip() + "\u2026"
    return re.sub(r"([\\`*_{}\[\]<>()#+!|~&])", r"\\\1", text)


def line(repo, label, sha, msg, when):
    day = f"{when.day:02d} {when.strftime('%b')}"
    return f"- `{day}` **{label}**: [{esc(msg)}](https://github.com/{OWNER}/{repo}/commit/{sha})"


def main():
    text = open("README.md", encoding="utf-8").read()
    a = text.find(START)
    b = text.find(END)
    if a < 0 or b < 0 or b < a:
        print("README shape unexpected; leaving it alone")
        return 0
    head, body, tail = text[: a + len(START)], text[a + len(START): b], text[b:]
    old = {}
    for ln in body.splitlines():
        m = re.match(r"- `[^`]+` \*\*([^*]+)\*\*:", ln)
        if m:
            old[m.group(1)] = ln
    entries = []
    for repo, label in REPOS:
        try:
            sha, msg, when = fetch(repo)
            entries.append((when, line(repo, label, sha, msg, when)))
        except Exception as e:  # keep the last good line for this repo
            print(f"{repo}: {type(e).__name__}, keeping previous line")
            if label in old:
                entries.append((datetime.min, old[label]))
    if not entries:
        print("nothing usable; leaving README alone")
        return 0
    entries.sort(key=lambda x: x[0], reverse=True)
    new_body = "\n\n" + "\n".join(l for _, l in entries) + "\n\n"
    if new_body == body:
        print("unchanged")
        return 0
    open("README.md", "w", encoding="utf-8").write(head + new_body + tail)
    print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
