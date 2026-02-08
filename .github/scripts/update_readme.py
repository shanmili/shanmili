import requests
import re

USERNAME = "shanmili"
README_PATH = "README.md"

def fetch_top_repos():
    """Fetch top repositories by stars"""
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=stars&per_page=100"
    response = requests.get(url)
    repos = response.json()
    
    # Filter out forks, sort by stars
    my_repos = [r for r in repos if not r['fork']]
    top_repos = sorted(my_repos, key=lambda x: x['stargazers_count'], reverse=True)[:6]
    
    return top_repos

def generate_projects_markdown(repos):
    """Generate markdown for projects"""
    lines = []
    for repo in repos:
        name = repo['name']
        url = repo['html_url']
        desc = repo['description'] or "No description"
        stars = repo['stargazers_count']
        
        lines.append(f"- **[{name}]({url})** - {desc} ⭐ {stars}")
    
    return "\n".join(lines)

def update_readme(projects_md):
    """Update README with new projects"""
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace content between markers
    pattern = r'<!-- AUTO-GENERATED-CONTENT:START \(PROJECTS\) -->.*?<!-- AUTO-GENERATED-CONTENT:END -->'
    replacement = f'<!-- AUTO-GENERATED-CONTENT:START (PROJECTS) -->\n{projects_md}\n<!-- AUTO-GENERATED-CONTENT:END -->'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README updated successfully!")

if __name__ == "__main__":
    repos = fetch_top_repos()
    projects_md = generate_projects_markdown(repos)
    update_readme(projects_md)
