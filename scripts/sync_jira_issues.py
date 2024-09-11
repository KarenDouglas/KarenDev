import os
import requests
import base64

# Get credentials from environment variables
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")  # Your JIRA account email
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")

# Encode credentials for Basic Authentication
auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
auth_bytes = auth_string.encode('utf-8')
auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

# API URLs with JQL to fetch issues from a specific project
JIRA_API_URL = "https://karendouglas.atlassian.net/rest/api/3/search?jql=project=KPW"

GITHUB_API_URL = "https://api.github.com/repos/KarenDouglas/KarenDev/issues"

# Fetch JIRA Issues
response = requests.get(
    JIRA_API_URL,
    headers={"Authorization": f"Basic {auth_b64}"}
)

# Check the response status and content
print(f"Response Status Code: {response.status_code}")
print(f"Response Content: {response.text}")

# Check for a successful response
if response.status_code != 200:
    print("Failed to fetch issues from JIRA. Exiting...")
    exit(1)

# Attempt to parse the JSON response
try:
    jira_issues = response.json()
except ValueError:
    print("Error parsing JSON response from JIRA. Exiting...")
    exit(1)

# Verify that the 'issues' key is in the response
if 'issues' not in jira_issues:
    print("Key 'issues' not found in the JIRA API response. Exiting...")
    exit(1)

# Loop through JIRA issues and create GitHub issues
for issue in jira_issues['issues']:
    title = issue['fields']['summary']
    description = issue['fields']['description'] if issue['fields']['description'] else "No description provided."

    # Create a GitHub issue
    github_response = requests.post(GITHUB_API_URL, json={
        "title": title,
        "body": description,
    }, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    # Print response for debugging
    print(f"Created GitHub issue for '{title}': {github_response.status_code} - {github_response.text}")
