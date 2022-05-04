import importlib
import os


def importplugins(path):
    files = os.listdir(path)
    importpath = path.replace('/', '.')
    modulenames = [importpath + i[:-3] for i in files
                   if not i.startswith('_') and i.endswith('.py')]
    modules = list(map(importlib.import_module, modulenames))
    return modules


def loadplugins():
    modules = importplugins('cmds/')
    triggers = {'commands': {}}
    for module in modules:
        instance = module.setup()
        for method in dir(instance):
            if method.startswith('_cmd_'):
                trigger = '%s' % method[5:]
                triggers['commands'][trigger] \
                    = getattr(instance, method)
    return triggers


def ruscommands():
    commandslist = loadplugins()
    ruscommandsdict = {
        "pick": commandslist['commands'].get("pick", None),
        "uptime": commandslist['commands'].get("uptime", None),
        "add": commandslist['commands'].get("add", None),
        "random": commandslist['commands'].get("random", None),
        "stat": commandslist['commands'].get("stat", None),
        "hit": commandslist['commands'].get("hit", None),
        "pic": commandslist['commands'].get("pic", None),
        "r": commandslist['commands'].get("r", None),
        "m": commandslist['commands'].get("m", None),
    }
    return ruscommandsdict


def handle(cirno, username, msg):
    commandslist = loadplugins()
    splice = msg.split(' ')
    command = splice.pop(0)[1:]
    args = ' '.join("%s" % x for x in splice).strip()
    if command in ruscommands().keys():
        method = ruscommands().get(command, None)
    else:
        method = commandslist['commands'].get(command, None)
    if method:
        try:
            return method(cirno, username, args)
        except:
            if cirno.what:
                cirno.sendmsg("%s: %s" % (username, cirno.what))
            else:
                return
    else:
        return

def handle_pm_cmds(cirno, username, msg):
    cirno.pm_cmd_usr=username
    cirno.pm_cmd=msg
    commandslist = loadplugins()
    splice = msg.split(' ')
    command = splice.pop(0)[1:]
    args = ' '.join("%s" % x for x in splice).strip()
    if command in ruscommands().keys():
        method = ruscommands().get(command, None)
    else:
        method = commandslist['commands'].get(command, None)
    if method:
        return method(cirno, username, args)
        try:
            return method(cirno, username, args)
        except:
            if cirno.what:
                jmsg={ "to": username, "msg": cirno.what, "meta": {} } 
                cirno.sendraw("pm", jmsg)
            else:
                return
    else:
        return
