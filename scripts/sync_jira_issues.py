import os
import requests

# Get credentials from environment variables
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")

# API URLs
JIRA_API_URL = "https://karendouglas.atlassian.net/rest/api/3/search"
GITHUB_API_URL = "https://api.github.com/repos/KarenDouglas/KarenDev/issues"

# Fetch JIRA Issues
response = requests.get(JIRA_API_URL, headers={"Authorization": f"Bearer {JIRA_API_TOKEN}"})
# Check the response status and content
print(f"Response Status Code: {response.status_code}")
print(f"Response Content: {response.text}")
jira_issues = response.json()

# Loop through JIRA issues and create GitHub issues
for issue in jira_issues['issues']:
    title = issue['fields']['summary']
    description = issue['fields']['description']

    # Create a GitHub issue
    github_response = requests.post(GITHUB_API_URL, json={
        "title": title,
        "body": description,
    }, headers={"Authorization": f"token {GITHUB_TOKEN}"})
