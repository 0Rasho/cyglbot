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
        #"roll": commandslist['commands'].get("roll", None),
        #"ask": commandslist['commands'].get("ask", None),
        #"who": commandslist['commands'].get("who", None),
        "uptime": commandslist['commands'].get("uptime", None),
        #"rate": commandslist['commands'].get("rate", None),
        "add": commandslist['commands'].get("add", None),
        "random": commandslist['commands'].get("random", None),
        "stat": commandslist['commands'].get("stat", None),
        "hit": commandslist['commands'].get("hit", None),
        #"search": commandslist['commands'].get("search", None),
        #"q": commandslist['commands'].get("q", None),
        "pic": commandslist['commands'].get("pic", None),
        #"booru": commandslist['commands'].get("booru", None),
        #"4chan": commandslist['commands'].get("4chan", None),
        #"2ch": commandslist['commands'].get("2ch", None),
        #"alert": commandslist['commands'].get("alert", None),
        #"deny": commandslist['commands'].get("deny", None),
        #"allow": commandslist['commands'].get("allow", None),
        #"save": commandslist['commands'].get("save", None),
        "r": commandslist['commands'].get("r", None),
        #"h": commandslist['commands'].get("h", None),
        "m": commandslist['commands'].get("m", None),
        #"y": commandslist['commands'].get("y", None),
        #"cm": commandslist['commands'].get("cm", None),
        #"cy": commandslist['commands'].get("cy", None),
        #"t": commandslist['commands'].get("trivia_question", None),
        #"a": commandslist['commands'].get("trivia_answer", None)
    }
    return ruscommandsdict


def handle(cirno, username, msg):
    commandslist = loadplugins()
    splice = msg.split(' ')
    command = splice.pop(0)[1:]
    #if not command.startswith("bj"):
    #    return
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
    #if not command.startswith("bj"):
    #    return
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
