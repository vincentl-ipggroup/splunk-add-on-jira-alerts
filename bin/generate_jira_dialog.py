import requests
import cgi
from jira_helpers import *

TEMPLATE = '''
<form class="form-horizontal form-complex">
    <div class="control-group">
        <label class="control-label" for="jira_integration_url">Integration URL</label>

        <div class="controls">
            <input type="text" name="action.jira.param.jira_url" id="jira_integration_url" />
            <span class="help-block">Override the global Jira Integration URL (refer to the application setup)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_username">JIRA Username</label>

        <div class="controls">
            <input type="text" name="action.jira.param.jira_username" id="jira_username" />
            <span class="help-block">Override the global Jira Username (refer to the application setup)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_password">JIRA Password</label>

        <div class="controls">
            <input type="password" name="action.jira.param.jira_password" id="jira_password" />
            <span class="help-block">Override the global Jira Password (will not be encrypted)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="project_key">Project</label>

        <div class="controls">
            <select name="action.jira.param.project_key" id="project_key">
                %(project_choices)s
            </select>
            <span class="help-block">Enter the project key to create Issues under.</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="issue_type">Type</label>

        <div class="controls">
            <select name="action.jira.param.issue_type" id="issue_type">
                %(issuetype_choices)s
            </select>
            <span class="help-block">Enter an Issue type.</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="summary">Issue Summary</label>

        <div class="controls">
            <input type="text" name="action.jira.param.summary" id="summary" />
            <span class="help-block">Enter a summary of the Issue.</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="description">Description</label>

        <div class="controls">
            <textarea name="action.jira.param.description" id="description" style="height: 120px;"></textarea>
            <span class="help-block">
                Enter a description of the issue. This text can include tokens that will resolve to text based on search results.
                <a href="{{SPLUNKWEB_URL_PREFIX}}/help?location=learnmore.alert.action.tokens" target="_blank"
                   title="Splunk help">Learn More <i class="icon-external"></i></a>
            </span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_component">Component</label>

        <div class="controls">
            <input type="text" name="action.jira.param.component" id="jira_component" />
            <span class="help-block">Override/Set a Component for the issue (optional)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_labels">Labels</label>

        <div class="controls">
            <input type="text" name="action.jira.param.labels" id="jira_labels" />
            <span class="help-block">Override/Set labels for the issue (optional)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_priority">Priority</label>

        <div class="controls">
            <select name="action.jira.param.priority" id="jira_priority">
                %(priority_choices)s
            </select>
            <span class="help-block">Select the issue priority.</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_timetracking">Original Estimate</label>

        <div class="controls">
            <select id="jira_timetracking" name="action.jira.param.timetracking_original">
                <option value=""></option>
                <option value="10m">10m</option>
                <option value="20m">20m</option>
                <option value="30m">30m</option>
                <option value="60m">60m</option>
                <option value="90m">90m</option>
                <option value="120m">180m</option>
                <option value="180m">180m</option>
            </select>
            <span class="help-block">Define an estimate time for the issue (optional)</span>
        </div>
    </div>
    <div class="control-group">
        <label class="control-label" for="jira_assignee">Assignee</label>

        <div class="controls">
            <select name="action.jira.param.assignee_list" id="jira_assignee">
                <option value=""></option>
                %(user_choices)s
            </select>
            <span class="help-block">Select user to assign the issue (optional)</span>
        </div>
        <div class="controls">
            <input type="text" name="action.jira.param.assignee" id="jira_assignee" />
            <span class="help-block">Or enter the username (optional - override list choice)</span>
        </div>
    </div>
</form>
'''

def generate_jira_dialog(jira_settings, server_uri, session_key):
    new_content = TEMPLATE % dict(
        project_choices="\n\t\t".join(map(lambda project: select_choice(value=project.get('key'), label='%(key)s - %(name)s' % project), get_projects(jira_settings))),
        issuetype_choices="\n\t\t".join(map(lambda issuetype: select_choice(value=issuetype.get('name'), label='%(name)s' % issuetype), get_issuetypes(jira_settings))),
        priority_choices="\n\t\t".join(map(lambda priority: select_choice(value=priority.get('name'), label='%(name)s' % priority), get_priorities(jira_settings))),
        user_choices="\n\t\t".join(map(lambda users: select_choice(value=users.get('key'), label='%(displayName)s' % users), get_usernames(jira_settings))),
    )
    update_jira_dialog(new_content, server_uri, session_key)


def get_projects(jira_settings):
    response = requests.get(
        url=jira_url(jira_settings, '/project'),
        auth=(jira_settings.get('jira_username'), jira_settings.get('jira_password')),
        verify=False)
    return response.json()

def get_issuetypes(jira_settings):
    response = requests.get(
        url=jira_url(jira_settings, '/issuetype'),
        auth=(jira_settings.get('jira_username'), jira_settings.get('jira_password')),
        verify=False)
    return response.json()

def get_priorities(jira_settings):
    response = requests.get(
        url=jira_url(jira_settings, '/priority'),
        auth=(jira_settings.get('jira_username'), jira_settings.get('jira_password')),
        verify=False)
    return response.json()

def get_usernames(jira_settings):
    response = requests.get(
        url=jira_url(jira_settings, '/user/search?username=.'),
        auth=(jira_settings.get('jira_username'), jira_settings.get('jira_password')),
        verify=False)
    return response.json()

def select_choice(value, label):
    # TODO: XML escape content
    return '<option value="%s">%s</option>' % (cgi.escape(value), cgi.escape(label))

