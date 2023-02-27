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
import OlivOS  # type: ignore
import OlivaGithub  # type: ignore
import os
from . import config as Config
from .webhook import Webhook
from flask import Flask
import json

app = Flask(__name__)

webhook = Webhook(app)
GlobalProc = None


class Event(object):
    def init(plugin_event, Proc):  # type: ignore
        global GlobalProc
        GlobalProc = Proc

        try:
            os.mkdir(f"./plugin/conf/{Config.PKG_NAME}")
        except:
            pass
        config = Config.default_config
        config['bot'] = {'hash': list(Proc.Proc_data['bot_info_dict'])[0]}
        config['settings'] = {
            'host': Config.host,
            'port': Config.port,
            'path': Config.path,
        }
        config['sent'] = {
            'private': [2753364619],
            'group': [971050440, 10005856]
        }

        if not os.path.exists(Config.file_path):
            with open(Config.file_path, 'w') as configfile:
                configfile.write(json.dumps(config))
        config = json.loads(open(Config.file_path, "r").read())
        pluginName = Config.PKG_NAME
        botHash = config['bot']['hash']
        plugin_event = OlivOS.API.Event(
            OlivOS.contentAPI.fake_sdk_event(
                bot_info=Proc.Proc_data['bot_info_dict'][botHash],
                fakename=pluginName
            ),
            Proc.log
        )

        def repost(obj: str, dic: dict):
            if obj:
                for qq in config['sent']['private']:
                    plugin_event.send("private", qq, obj.format(**dic))
                for group in config['sent']['group']:
                    plugin_event.send("group", group, obj.format(**dic))

        @app.route("/")
        def hello_world():
            return "<h1>Hi,I'm Listening...<h1>"

        @webhook.hook("member")
        def on_member(data):
            logg(json.dumps(data))
            repost(obj=config['member'], dic=data)

        @webhook.hook("commit_comment")
        def on_commit_comment(data):
            logg(json.dumps(data))
            repost(obj=config['commit_comment'], dic=data)

        @webhook.hook("star")
        def on_star(data):
            logg(json.dumps(data))
            repost(obj=config['star'][data['action']], dic=data)

        @webhook.hook("issues")
        def on_issue(data):
            logg(json.dumps(data))
            repost(obj=config['issues'], dic=data)

        @webhook.hook("issue_comment")
        def on_issue_comment(data):
            logg(json.dumps(data))
            repost(obj=config['issue_comment'], dic=data)

        @webhook.hook("create")
        def on_create(data):
            logg(json.dumps(data))
            repost(obj=config['create'], dic=data)

        @webhook.hook("delete")
        def on_delete(data):
            logg(json.dumps(data))
            repost(obj=config['delete'], dic=data)

        @webhook.hook("deployment")
        def on_deployment(data):
            logg(json.dumps(data))
            repost(obj=config['deployment'], dic=data)

        @webhook.hook("deployment_status")
        def on_deployment_status(data):
            logg(json.dumps(data))
            repost(obj=config['deployment_status'], dic=data)

        @webhook.hook("fork")
        def on_fork(data):
            logg(json.dumps(data))
            repost(obj=config['fork'], dic=data)

        @webhook.hook("gollum")
        def on_gollum(data):
            logg(json.dumps(data))
            repost(obj=config['gollum'], dic=data)

        @webhook.hook("membership")
        def on_membership(data):
            logg(json.dumps(data))
            repost(obj=config['membership'], dic=data)

        @webhook.hook("page_build")
        def on_page_build(data):
            logg(json.dumps(data))
            repost(obj=config['page_build'], dic=data)

        @webhook.hook("pull_request")
        def on_pull_request(data):
            logg(json.dumps(data))
            repost(obj=config['pull_request'], dic=data)

        @webhook.hook("pull_request_review")
        def on_pull_request_review(data):
            logg(json.dumps(data))
            repost(obj=config['pull_request_review'], dic=data)

        @webhook.hook("pull_request_review_comment")
        def on_pull_request_review_comment(data):
            logg(json.dumps(data))
            repost(obj=config['pull_request_review_comment'], dic=data)

        @webhook.hook("push")
        def on_push(data):
            logg(json.dumps(data))
            repost(obj=config['push'], dic=data)

        @webhook.hook("release")
        def on_release(data):
            logg(json.dumps(data))
            repost(obj=config['release'], dic=data)

        @webhook.hook("repository")
        def on_repository(data):
            logg(json.dumps(data))
            repost(obj=config['repository'], dic=data)

        @webhook.hook("status")
        def on_status(data):
            logg(json.dumps(data))
            repost(obj=config['status'], dic=data)

        @webhook.hook("team_add")
        def on_team_add(data):
            logg(json.dumps(data))
            repost(obj=config['team_add'], dic=data)

        @webhook.hook("watch")
        def on_watch(data):
            logg(json.dumps(data))
            repost(obj=config['watch'], dic=data)

    def menu(plugin_event, Proc):  # type: ignore
        if plugin_event.data.namespace == 'OlivaGithub':  # type: ignore
            if plugin_event.data.event == 'OlivaGithub_on':  # type: ignore
                config = json.loads(open(Config.file_path, "r").read())
                try:
                    app.run(host="0.0.0.0", port=3000)  # type: ignore[int]
                    logg(
                        f"flask Already Runns On {config['settings']['host']}{config['settings']['path']}:{config['settings']['port']}!")
                except:
                    logg("Already On!!")
            elif plugin_event.data.event == 'OlivaGithub_off':  # type: ignore
                pass

# # 对字典降级处理
# def flatten_dict(d):
#     result = {}
#     for key, value in d.items():
#         if isinstance(value, dict):
#             value = flatten_dict(value)
#             for subkey, subvalue in value.items():
#                 result[key + '.' + subkey] = subvalue
#         else:
#             result[key] = value
#     # results = {'res':{}}
#     # for key,value in result.items(): results['res'][key] = value
#     return result


def logg(msg, level=2):
    GlobalProc.log(level, f"[OlivaGithub] > {msg}")  # type: ignore

# # 使字典可以使用点表示法，暂时弃用
# class DotDict(dict):
#     def __init__(self, *args, **kwargs):
#         dict.__init__(self, *args, **kwargs)
#         self.__dict__ = self

#     def toDotDict(data):
#         if isinstance(data, dict):
#             for k, v in data.items():
#                 if isinstance(v, dict):
#                     data[k] = DotDict(v)
#                     DotDict.toDotDict(data[k])
#         else:
#             return data

#         return DotDict(data)
