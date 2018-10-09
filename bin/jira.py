import sys
import json
import requests
from jira_helpers import get_jira_password

# creates outbound message from alert payload contents
# and attempts to send to the specified endpoint
def send_message(payload):
    config = payload.get('configuration')

    ISSUE_REST_PATH = "/rest/api/latest/issue"
    url = config.get('jira_url')
    jira_url = url + ISSUE_REST_PATH
    username = config.get('jira_username')
    password = config.get('jira_password')
    if not password:
        password = get_jira_password(payload.get('server_uri'), payload.get('session_key'))
    if config.get('component'):
        component = [ { "name": config.get('component') } ]
    else:
        component = []
    if config.get('labels'):
        labels = config.get('labels').split(',')
    else:
        labels = []
    if config.get('assignee'):
        assignee = config.get('assignee')
    else:
        assignee = config.get('assignee_list')

    # create outbound JSON message body
    body = json.dumps({
        "fields": {
            "project": {
                "key" : config.get('project_key')
            },
            "issuetype": {
                "name": config.get('issue_type')
            },
            "summary": config.get('summary'),
            "description": config.get('description'),
            "components" : component,
            "labels": labels,
            "priority": {
                "name": config.get('priority')
            },
            "timetracking": {
                "originalEstimate": config.get('timetracking_original')
            },
            "assignee": {
                "name": assignee
            }
        }
    })

    # create outbound request object
    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(url=jira_url, data=body, headers=headers, auth=(username, password))
        print >>sys.stderr, "INFO Jira server HTTP status= %s" % result.text
        print >>sys.stderr, "INFO Jira server response: %s" % result.text
    except Exception, e:
        print >> sys.stderr, "ERROR Error sending message: %s" % e
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        try:
            # retrieving message payload from splunk
            raw_payload = sys.stdin.read()
            payload = json.loads(raw_payload)
            send_message(payload)
        except Exception, e:
            print >> sys.stderr, "ERROR Unexpected error: %s" % e
            sys.exit(3)
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
