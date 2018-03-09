from github_application import RepositoryInstance
import os

token = os.environ['GITHUB_AUTH_TOKEN']

searched_repo_full_name = os.environ['GITHUB_REPO_NAME']

repo = RepositoryInstance(authorization_token=token, repository_name=searched_repo_full_name)
issues = repo.getOpenIssues()
for issue in issues:
        print("Issue #" + str(issue.number) + " - " + issue.title)
prs = repo.getOpenPullRequests()
for pr in prs:
        print("Pull Request #" + str(pr.number) + " - " + pr.title)
