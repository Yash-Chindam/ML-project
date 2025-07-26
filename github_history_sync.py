import os
import subprocess
import random
from datetime import datetime, timedelta
from collections import defaultdict

REPO_PATH = r"C:\Users\yash\Downloads\projects\git codes repos\ML-project"


def generate_commits(days=365):
    commits = defaultdict(int)
    today = datetime.now()

    for _ in range(days // 7):
        d = today - timedelta(days=random.randint(0, days))
        commits[d.strftime("%Y-%m-%d")] += 1

    return commits


def make_commit(date):
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
    subprocess.run(["git", "commit", "-m", f"update {date}"], cwd=REPO_PATH, env=env)


def push():
    subprocess.run(["git", "push"], cwd=REPO_PATH)


def main():

    print("Generating commits...")

    commits = generate_commits()

    for d in commits:
        make_commit(d)

    print("Pushing to GitHub...")
    push()

    print("Done.")


if __name__ == "__main__":
    main()