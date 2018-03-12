from slackclient import SlackClient
from github_application import RepositoryInstance
from zenhub_application import BoardInstance
import re
import os

GITHUB_AUTH_TOKEN = os.environ['GITHUB_AUTH_TOKEN']
GITHUB_REPO_NAME = os.environ['GITHUB_REPO_NAME']
ZENHUB_AUTH_TOKEN = os.environ['ZENHUB_AUTH_TOKEN']
ZENHUB_REPO_ID = os.environ['ZENHUB_REPO_ID']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

class SlackInstance(object):

    def __init__(self, slack_token):

        self.repo = RepositoryInstance(authorization_token=GITHUB_AUTH_TOKEN, repository_name=GITHUB_REPO_NAME)
        self.board = BoardInstance(authorization_token=ZENHUB_AUTH_TOKEN, repository_id=ZENHUB_REPO_ID)
        self.slack_instance = SlackClient(SLACK_BOT_TOKEN)
        
        if self.slack_instance.rtm_connect(with_team_state=False):
            # Read bot's user ID by calling Web API method `auth.test`
            self.starterbot_id = self.slack_instance.api_call("auth.test")["user_id"]
            
            print("Starter Bot connected and running with id", self.starterbot_id)
            
            while True:
                command, channel = self.parse_bot_commands(self.slack_instance.rtm_read())
                if command:
                    self.handle_command(command, channel)
        else:
            print("Connection failed. Exception traceback printed above.")

    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.starterbot_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        """
            Executes bot command if the command is known
        """

        default_response = "Not sure what you mean. Try *{}*.".format('help')
        response = None
        
        if command.startswith('help'):
            response = '''The possible commands are:\n
            *move issue* "issue number" to "kanban status"\n
            *list open issues*\n
            *list open pull requests*'''

        elif command.startswith('move issue'):
            #not implemented yet
            split_command = command.split()
            
            issue_number = int(split_command[2])
            pipeline_name = ' '.join(split_command[4:])
            
            response = "Ok, moving issue #" + str(issue_number) + " to " + pipeline_name
            
            self.slack_instance.api_call(
                "chat.postMessage",
                channel=channel,
                text=response or default_response
            )

            self.board.moveIssueTo(issue_number, pipeline_name)

            response = "Done!"

        elif command.startswith('list open issues'):
            issues = self.repo.getOpenIssues()
            response = 'The open issues are:\n\n'
            for issue in issues:
                text = "Issue #" + str(issue.number) + " - " + issue.title + "\n"
                response = response + text
            if response == 'The open pull requests are:\n\n':
                response = 'There are no open issues.'
        
        elif command.startswith('list open pull requests'):
            prs = self.repo.getOpenPullRequests()
            response = 'The open pull requests are:\n\n'
            for pr in prs:
                text = "Pull Request #" + str(pr.number) + " - " + pr.title + "\n"
                response = response + text
            if response == 'The open pull requests are:\n\n':
                response = 'There are no open pull requests.'

        # Sends the response back to the channel
        self.slack_instance.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )