from github_application import RepositoryInstance

token = input("Insert github token: ")

searched_repo_full_name = "fga-gpp-mds/2018.1-Reabilitacao-Motora"

repo = RepositoryInstance(authorization_token=token, repository_name=searched_repo_full_name)
issues = repo.getOpenIssues()
for issue in issues:
        print("Issue #" + str(issue.number) + " - " + issue.title)
prs = repo.getOpenPullRequests()
for pr in prs:
        print("Pull Request #" + str(pr.number) + " - " + pr.title)
