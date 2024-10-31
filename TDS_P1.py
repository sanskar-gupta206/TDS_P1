import requests
import pandas as pd
from time import sleep

# GitHub personal access token (replace 'your_token_here' with your actual token)
GITHUB_TOKEN = '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'
GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Function to fetch users in Bangalore with over 100 followers
def fetch_users_in_bangalore(min_followers=100, per_page=30, max_pages=10):
    users = []
    page = 1
    while page <= max_pages:
        query = f"location:Bangalore followers:>{min_followers}"
        url = f"{GITHUB_API_URL}/search/users?q={query}&page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            break

        data = response.json()
        users.extend(data['items'])
        
        if 'items' not in data or not data['items']:
            break
        
        page += 1
        sleep(1)  # Avoid hitting API rate limits

    return users

# Function to fetch repositories for each user
def fetch_user_repositories(username):
    repos = []
    page = 1
    per_page = 30
    
    while True:
        url = f"{GITHUB_API_URL}/users/{username}/repos?page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            break
        
        data = response.json()
        if not data:
            break
        
        repos.extend(data)
        page += 1
        sleep(0.5)

    return repos

# Main function to fetch users and their repositories and write to CSV files
def main():
    # Fetch users
    users = fetch_users_in_bangalore()
    users_data = []
    repos_data = []

    for user in users:
        username = user['login']
        print(f"Fetching data for user: {username}")
        
        # User details for users.csv
        user_data = {
            'login': username,
            'name': user.get('name', ''),
            'company': str(user.get('company', '')).strip().lstrip('@').upper(),
            'location': user.get('location', ''),
            'email': user.get('email', ''),
            'hireable': user.get('hireable', ''),
            'bio': user.get('bio', ''),
            'public_repos': user.get('public_repos', 0),
            'followers': user.get('followers', 0),
            'following': user.get('following', 0),
            'created_at': user.get('created_at', '')
        }
        users_data.append(user_data)

        # Repository details for repositories.csv
        repos = fetch_user_repositories(username)
        for repo in repos[:500]:
            repo_data = {
                'login': username,
                'full_name': repo.get('full_name', ''),
                'created_at': repo.get('created_at', ''),
                'stargazers_count': repo.get('stargazers_count', 0),
                'watchers_count': repo.get('watchers_count', 0),
                'language': repo.get('language', ''),
                'has_projects': repo.get('has_projects', False),
                'has_wiki': repo.get('has_wiki', False),
                'license_name': repo['license']['name'] if repo.get('license') else ''
            }
            repos_data.append(repo_data)
        
        sleep(1)

    # Writing to CSV files
    users_df = pd.DataFrame(users_data)
    repos_df = pd.DataFrame(repos_data)

    users_df.to_csv('users.csv', index=False)
    repos_df.to_csv('repositories.csv', index=False)

# Run the main function
if __name__ == "__main__":
    main()
