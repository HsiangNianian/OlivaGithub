import OlivOS
import OlivOSPluginTemplate

class Event(object):
    def init(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        poke_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

    def menu(plugin_event, Proc):
        if plugin_event.data.namespace == 'OlivOSPluginTemplate':
            if plugin_event.data.event == 'OlivOSPluginTemplate_Menu_001':
                pass
            elif plugin_event.data.event == 'OlivOSPluginTemplate_Menu_002':
                pass

def unity_reply(plugin_event, Proc):
    if plugin_event.data.message == '/bot' or plugin_event.data.message == '.bot' or plugin_event.data.message == '[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + '] .bot':
        plugin_event.reply('OlivOSPluginTemplate')

def poke_reply(plugin_event, Proc):
    if plugin_event.data.target_id == plugin_event.base_info['self_id']:
        plugin_event.reply('OlivOSPluginTemplate')
    elif plugin_event.data.target_id == plugin_event.data.user_id:
        plugin_event.reply('OlivOSPluginTemplate')
    elif plugin_event.data.group_id == -1:
        plugin_event.reply('OlivOSPluginTemplate')

