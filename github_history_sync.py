"""
Generate fake GitHub contribution commits and push to GitHub.

Fixes:
  - Sets remote origin to https://github.com/Yash-Chindam/<repo_name>.git
  - Uses `git push -u origin main` to set upstream (fixes "Publish branch" prompt)
"""

import os
import subprocess
import random
from datetime import datetime, timedelta
from collections import defaultdict

REPO_PATH = r"C:\Users\yash\Downloads\projects\git codes repos\ML-project"
GITHUB_USERNAME = "Yash-Chindam"


def setup_remote(repo_path: str) -> None:
    """Set the remote origin to the correct GitHub URL using Yash-Chindam username."""
    repo_name = os.path.basename(repo_path)
    remote_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"

    # Remove existing origin if present
    subprocess.run(
        ["git", "remote", "remove", "origin"],
        cwd=repo_path,
        capture_output=True
    )

    # Add correct remote
    result = subprocess.run(
        ["git", "remote", "add", "origin", remote_url],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✓ Remote set to: {remote_url}")
    else:
        print(f"✗ Failed to set remote: {result.stderr}")


def generate_commits(days=365):
    commits = defaultdict(int)
    today = datetime.now()

    for _ in range(days // 7):
        d = today - timedelta(days=random.randint(0, days))
        commits[d.strftime("%Y-%m-%d")] += 1

    return commits


def make_commit(date: str) -> None:
    hour = random.randint(9, 20)
    minute = random.randint(0, 59)
    full_date = f"{date} {hour}:{minute}:00"

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = full_date
    env["GIT_COMMITTER_DATE"] = full_date

    file = os.path.join(REPO_PATH, "activity.txt")
    with open(file, "a") as f:
        f.write(full_date + "\n")

    subprocess.run(["git", "add", "."], cwd=REPO_PATH)
    subprocess.run(
        ["git", "commit", "-m", f"update {date}"],
        cwd=REPO_PATH,
        env=env
    )


def push() -> None:
    """Push with -u to set upstream and fix the 'Publish branch' prompt."""
    result = subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✓ Pushed to GitHub successfully.")
    else:
        print(f"✗ Push failed: {result.stderr}")
        print("Tip: Make sure the repo exists at "
              f"https://github.com/{GITHUB_USERNAME}/{os.path.basename(REPO_PATH)}")


def main():
    print("Setting up remote...")
    setup_remote(REPO_PATH)

    print("Generating commits...")
    commits = generate_commits()
    for d in sorted(commits.keys()):
        make_commit(d)

    print("Pushing to GitHub...")
    push()

    print("Done.")


if __name__ == "__main__":
    main()