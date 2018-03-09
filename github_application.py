from github import Github

class RepositoryInstance(object):

    def __init__(self, authorization_token, repository_name):
        self.github_instance = Github(authorization_token)
        found_repositories = self.github_instance.search_repositories(repository_name)
        self.repository = found_repositories[0]

    def getOpenIssues(self):
        open_issues = self.repository.get_issues()
        result = []
        for issue in open_issues:
            if issue.pull_request == None:
                result.append(issue)
        return result

    def getOpenPullRequests(self):
        open_issues = self.repository.get_issues()
        result = []
        for issue in open_issues:
            if issue.pull_request != None:
                result.append(issue)
        return result
