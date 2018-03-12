import requests
import os
import json

class BoardInstance(object):

    def __init__(self, authorization_token, repository_id):
        self.request_header = header = {'X-Authentication-Token': authorization_token}
        self.repo_id = repository_id
        self.board_data = getBoardData()

    def getIssueData(self, issue_number):
        link = 'https://api.zenhub.io/p1/repositories/' + str(self.repo_id) + '/issues/' + str(issue_number)
        r = requests.get(link, headers=self.request_header)
        json_data = json.loads(r.text)
        return json_data
    
    def getBoardData(self):
        link = 'https://api.zenhub.io/p1/repositories/' + str(self.repo_id) + '/board/'
        r = requests.get(link, headers=self.request_header)
        json_data = json.loads(r.text)
        return json_data

    def moveIssueTo(self, issue_number, pipeline_name):
        pipeline = self.getBoardData()
        pipeline_id = None

        for each in pipeline:
            if each['name'] == pipeline_name:
                pipeline_id = each['id']

        if pipeline_id:
            # there is an id
            link = 'https://api.zenhub.io/p1/repositories/' + str(self.repo_id) + '/issues/'+ str(issue_number) + '/moves'
            body = {"pipeline_id": pipeline_id, "position": "top"}
            r = requests.post(link, headers=self.request_header, body=body)
