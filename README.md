OlivaGithub
===========
[![CI](https://github.com/HsiangNianian/OlivaGithub/actions/workflows/ci.yml/badge.svg)](https://github.com/HsiangNianian/OlivaGithub/actions/workflows/ci.yml)
<img src="https://img.shields.io/github/release/HsiangNianian/OlivaGithub.svg" alt="Latest version" />
> 利用webhook实时监控你的Github仓库

注意：插件仅适用**OlivOS 3.3.9+**

插件特性
-------
- 安装简单，仅需三步，一键式部署，不需要任何繁琐操作。
- 低延迟，高效率，利用`flask`微框架编写。
- 个性化程度高，可自定义`host`,`path`,`port`,以及任何事件的通报，支持转发多个好友与群聊。

使用方法
-------
1. 将`OlivaGithub.opk`放入`./plugin/app/`文件夹下，重载插件。
2. 此时配置文件`config.json`已经在`./plugin/conf/OlivaGithub/`生成，按需修改配置。
3. 右键`OlivOS`打开`OlivaGithub`插件菜单，单击`开启`。

配置示例
-------
这是`./plugin/conf/OlivaGithub/config.json`的一个示例。
```json
{
    "bot": {
        "hash": "43718c3b643*******ddfd95a0d013ae"
    },
    "settings": {
        "host": "0.0.0.0",
        "port": "3000",
        "path": "/webhook"
    },
    "sent": {
        "private": [
            2753364619
        ],
        "group": [
            971050440,
            10005856
        ]
    },
    "star": "{sender[login]} starred {repository[name]}",
    "issues": "{sender[login]} {action} issue #{issue[number]} in \"{repository[full_name]}\"",
    "issue_comment": "{sender[login]} commented on issue #{issue[number]} in \"{repository[full_name]}\"\n",
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
    "watch": "{sender[login]} {action} watch in repository \"{repository[full_name]}\""
}
```

参数说明
-------
`bot` _List_ 一个bot键，无实际用处。

`bot.hash` _str_ 这是一个由插件自动生成的键值对，请勿更改，否则无法发送消息。
```json
{
  "bot": {
        "hash": "43718c3b643*******ddfd95a0d013ae"
    }
}
```

-------

`settings` _List_ 存放一些基本配置的键。

`settings.host` _str_ 连接的域。

`settings.port` _str|int_ 连接的域的端口。

`settings.path` _str_ 连接域的路径。
```json
{
    "settings": {
        "host": "0.0.0.0",
        "port": "3000",
        "path": "/webhook"
    }
}
```
以上`host``port``path`组合便是`0.0.0.0:3000/webhook`。

-------

`sent` _List_ 发送消息的列表键。

`sent.private` _List_ 发送私聊消息的列表键。

`sent.group` _List_ 发送群聊消息的列表键。
```json
{
    "sent": {
        "private": [
            2753364619
        ],
        "group": [
            971050440,
            10005856
        ]
    }
}
```
以上参数代表有事件接收时将会发给QQ用户`2753364619`以及群聊`971050440`和`10005856`。

-------

其余键,均为Github Repo Webhook发送的事件名称，具体可参考[Webhook events and payloads](https://docs.github.com/zh/webhooks-and-events/webhooks/webhook-events-and-payloads)。

表达嵌套关系均用`xxx[xxx][xxx]`表示。

协议
----
如果想进行一些不同`action`的个性化操作可以更改源码。
```
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
```

