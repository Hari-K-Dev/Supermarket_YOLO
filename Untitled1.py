import os
import subprocess
from datetime import datetime, timedelta
import random

# === Configuration ===
repo_path = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(repo_path, 'log.txt')

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

# === Ask User for Dates ===
date_format = "%Y-%m-%d"
while True:
    try:
        start_input = input("Enter the start date (YYYY-MM-DD): ")
        end_input = input("Enter the end date (YYYY-MM-DD): ")

        start_date = datetime.strptime(start_input, date_format)
        end_date = datetime.strptime(end_input, date_format)

        if start_date > end_date:
            raise ValueError("Start date must be before end date.")
        break
    except ValueError as ve:
        print(f"❌ Invalid input: {ve}. Please try again.")

# === Commit Loop ===
current_date = end_date
while current_date >= start_date:
    if random.random() < 0.3:
        commits_today = get_random_int(1, 4)
        for j in range(commits_today):
            msg = f"Random Changes on {current_date.strftime('%a %b %d %Y')} #{j + 1}"
            make_commit(current_date, msg)
    current_date -= timedelta(days=1)

print("✅ Commits created. Now push to GitHub!")
