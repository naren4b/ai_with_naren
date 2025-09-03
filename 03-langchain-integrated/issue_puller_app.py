import json
import requests
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "goharbor-issues.json")
all_issues = []
page = 1
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set as environment variable

headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"
    headers["Accept"] = "application/vnd.github.v3+json"
while True:
    api_url = f"https://api.github.com/repos/goharbor/harbor/issues?state=open&page={page}&per_page=100"  # Example API URL
    print(f"Fetching page {page}...")
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if not data:
            break
        all_issues.extend(data)
        page += 1
    elif response.status_code == 403:
        print("Rate limit exceeded. Consider using a GitHub token.")
        print(
            f"Remaining requests: {response.headers.get('X-RateLimit-Remaining', 'Unknown')}"
        )
        break
    else:
        print(f"Failed to fetch data: {response.status_code}")
        break

print(f"Total Issue Collected: {len(all_issues)}")
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_issues, f, ensure_ascii=False, indent=4)
print("Completed")
