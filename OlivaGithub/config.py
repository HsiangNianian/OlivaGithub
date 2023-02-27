# -*- encoding: utf-8 -*-
'''
     ██╗██╗   ██╗██╗   ██╗███╗   ██╗██╗  ██╗ ██████╗ 
     ██║╚██╗ ██╔╝██║   ██║████╗  ██║██║ ██╔╝██╔═══██╗
     ██║ ╚████╔╝ ██║   ██║██╔██╗ ██║█████╔╝ ██║   ██║
██   ██║  ╚██╔╝  ██║   ██║██║╚██╗██║██╔═██╗ ██║   ██║
╚█████╔╝   ██║   ╚██████╔╝██║ ╚████║██║  ██╗╚██████╔╝
 ╚════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ 
                                                     
    Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


PKG_NAME: str = "OlivaGithub"
port: str = '3000'
host: str = "0.0.0.0"
path: str = "/webhook"
file_name: str = "config.json"
file_path: str = f"./plugin/conf/{PKG_NAME}/{file_name}"
default_config = {
    "bot": {},
    "settings": {},
    "sent": {},
    "star": "{sender[login]} starred {repository[name]}",
    "issues": "{sender[login]} {action} issue #{issue[number]} in \"{repository[full_name]}\"",
    "issue_comment": "{sender[login]} commented on issue #{issue[number]} in \"{repository[full_name]}\"",
    "commit_comment": "{comment[user][login]} commented on \"{comment[commit_id]}\" in \"{repository[full_name]}\"",
    "create": "{sender[login]} created {ref_type} ({ref}) in \"{repository[full_name]}\"",
    "delete": "{sender[login]} deleted {ref_type} ({ref}) in \"{repository[full_name]}\"",
    "deployment": "{sender[login]} deployed {deployment[ref]} to \"{deployment[environment]}\" in \"{repository[full_name]}\"",
    "deployment_status": "deployment of {deployement[ref]} to \"{deployment[environment]}\" \"{deployment_status[state]}\" in \"{repository[full_name]}\"",
    "fork": "{forkee[owner][login]} forked {forkee[name]}",
    "gollum": "{sender[login]} edited wiki pages in \"{repository[full_name]}\"",
    "member": "{sender[login]} {action} member {member[login]} in \"{repository[full_name]}\"",
    "membership": "{sender[login]} {action} member {member[login]} to team \"{team[name]} in {repository[full_name]}\"",
    "page_build": "{sender[login]} built pages in \"{repository[full_name]}\"",
    "ping": "ping from {sender[login]}",
    "public": "{sender[login]} publicized \"{repository[full_name]}\"",
    "pull_request": "{sender[login]} {action} pull #{pull_request[number]} in \"{repository[full_name]}\"",
    "pull_request_review": "{sender[login]} {action} {review[state]} \"review on pull #{pull_request[number]} in \"{repository[full_name]}\"",
    "pull_request_review_comment": "{comment[user][login]} {action} comment \"on pull #{pull_request[number]} in \"{repository[full_name]}\"",
    "push": "{pusher[name]} pushed {ref} in \"{repository[full_name]}\"",
    "release": "{release[author][login]} {action} {release[tag_name]} in \"{repository[full_name]}\"",
    "repository": "{sender[login]} {action} repository \"{repository[full_name]}\"",
    "status": "{sender[login]} set {sha} status to {state} in \"{repository[full_name]}\"",
    "team_add": "{sender[login]} added repository {repository[full_name]} to team \"{team[name]}\"",
    "watch": "{sender[login]} {action} watch in repository \"{repository[full_name]}\"",
}