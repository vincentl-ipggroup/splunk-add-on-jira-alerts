[jira]
* Please refer to the Jira API Documentation for Further Details about Jira Rest API 
* https://docs.atlassian.com/software/jira/docs/api/REST/7.12.2/?_ga=2.226934429.1412021697.1538460253-230921612.1532996192#api/2/project-getAllProjects

param.jira_url = <string>
* URL of your Jira instance, example: http://my-jira.example.com:8080

param.jira_username = <string>
* Username to connect to Jira, require enough privilege to create Issues in the desired Project

param.jira_password = <string>
* Password associate to your Username. 
* Setup password will be encrypted in local/password.
* Override password will NOT be encrypted in the savedsearches.conf

param.project_key = <string>
* Project Key required to create a Jira Issue. Please refer to your Jira Projects.
* Related API Call + JQuery Filtering:
* curl -s -u username:password -X GET 'http://my-jira.example.com:8080/rest/api/2/project' | jq -r '.[]|"\(.name): \(.key)"'

param.issue_type = <string>
* IssueType Required to create a Jira Issue. Please refer to your Jira IssueTypes.
* Related API Call + JQuery Filtering:
* curl -s -u username:password -X GET 'http://my-jira.example.com:8080/rest/api/2/issuetype' | jq -r '.[].name'

param.summary = <string>
* Custom Alert Summary. [Default associate Splunk Search name: $name$]

param.description = <string>
* Custom Alert Description. [Default: short message including Splunk Token: $Description$, $name$, $trigger_date$, $trigger_timeHMS$, $results_link$]

param.component = <string>
* Component related to your Jira Issue.
* Component are Project Base and can not easily proposed as a list

param.labels = <string>
* Labels you want to associate your Jira Issue with.
* Labels must be composed by one word and multiples labels can be separated by ','
* Example: Splunk2Jira, Test

param.priority = <string>
* Priority of the Issue [default: Minor (Normal)]

param.timetracking_original = <string> | 10 | 30 | 60 | 90 | 120 | 180
* Set a Original Time Tracking value [Default: None]

param.assignee = <string>
* Field to set the assignee, written in the Alert
* Override param.assignee_list

param.assignee_list = <string>
* Field to select the Assignee from a list.
* Is superseded by param.assignee
