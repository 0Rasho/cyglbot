from configparser import ConfigParser
import uuid

parser = ConfigParser()
parser.read('cfg/conf.cfg')
config = dict()
for section in parser.sections():
    config[section] = dict(parser.items(section))
config['Iamjoined'] = False
config['disablecmds'] = True
config['autobot'] = False
config['autousers'] = []
config['AIdatafile'] = "AI-data-WW"
#config['AIdatafile'] = "AI-"+ str(uuid.uuid4().hex)
