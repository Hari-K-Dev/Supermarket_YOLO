import os
import subprocess
from datetime import datetime, timedelta
import random

# === Configuration ===
repo_path = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(repo_path, 'log.txt')

days_back = 30
today = datetime.now()

def get_random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def format_git_date(date):
    return date.isoformat()

def make_commit(date, message):
    git_date = format_git_date(date)

    with open(log_file_path, 'a') as f:
        f.write(f'{git_date} - {message}\n')

    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = git_date
    env['GIT_COMMITTER_DATE'] = git_date

    subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
    subprocess.run(['git', 'commit', '-m', message, '--date', git_date],
                   cwd=repo_path, env=env, check=True)

# === Commit Loop ===
for i in range(days_back + 1):
    date = today - timedelta(days=i)

    # 30% chance to create commits on this day
    if random.random() < 0.2:
        commits_today = get_random_int(1, 4)
        for j in range(commits_today):
            msg = f"Random CHanges on {date.strftime('%a %b %d %Y')} #{j + 1}"
            make_commit(date, msg)

print("✅ Commits created. Now push to GitHub!")
