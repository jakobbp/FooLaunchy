import launchy
import httplib
import urllib
import json

class FooLaunchy(launchy.Plugin):
    PLUGIN_KEYWORD = 'foo '

    BEEFWEB_HOST = 'localhost'
    BEEFWEB_PORT = 8880
    BEEFWEB_PLAYER_API_ROOT = '/api/player'

    BEEFWEB_PARAM_IS_MUTED = 'isMuted'
    BEEFWEB_PARAM_MAX = 'max'
    BEEFWEB_PARAM_MIN = 'min'
    BEEFWEB_PARAM_PLAYER = 'player'
    BEEFWEB_PARAM_VALUE = 'value'
    BEEFWEB_PARAM_VOLUME = 'volume'

    VOLUME_STEP = 2.0

    CMD_MAPPING = {
        'play'        : 'play',
        'pl'          : 'play',
        'y'           : 'play',
        'stop'        : 'stop',
        's'           : 'stop',
        'pause'       : 'pause',
        'p'           : 'pause',
        'next'        : 'next',
        'n'           : 'next',
        'previous'    : 'previous',
        'prev'        : 'previous',
        'pr'          : 'previous',
        'volume up'   : 'volume up',
        'vup'         : 'volume up',
        'vu'          : 'volume up',
        'volume down' : 'volume down',
        'vdn'         : 'volume down',
        'vd'          : 'volume down',
        'mute'        : 'mute',
        'm'           : 'mute'
    }

    REST_MAPPING = {
        'play'        : BEEFWEB_PLAYER_API_ROOT + '/play',
        'stop'        : BEEFWEB_PLAYER_API_ROOT + '/stop',
        'pause'       : BEEFWEB_PLAYER_API_ROOT + '/pause/toggle',
        'next'        : BEEFWEB_PLAYER_API_ROOT + '/next',
        'previous'    : BEEFWEB_PLAYER_API_ROOT + '/previous',
        'volume up'   : BEEFWEB_PLAYER_API_ROOT + '',
        'volume down' : BEEFWEB_PLAYER_API_ROOT + '',
        'mute'        : BEEFWEB_PLAYER_API_ROOT + ''
    }

    def __init__(self):
        launchy.Plugin.__init__(self)
        self.name = 'FooLaunchy'
        self.hash = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), 'foobar2000_64.png')

    def init(self):
        pass
       
    def getID(self):
        return self.hash

    def getName(self):
        return self.name

    def getIcon(self):
         return self.icon
       
    def getLabels(self, inputDataList):
        pass   
       
    def getResults(self, inputDataList, resultsList):
        text = inputDataList[0].getText()
        if self.PLUGIN_KEYWORD == text[:4]:
            cmd = text[4:]
            cmdText = self.CMD_MAPPING[cmd] if cmd in self.CMD_MAPPING else '???'
            resultsList.push_back(  launchy.CatItem(text,
                                    'foobar2000: ' + cmdText,
                                    self.getID(), self.getIcon()) )
       
    def getCatalog(self, resultsList):
        pass

    def launchItem(self, inputDataList, catItemOrig):  
        catItem = inputDataList[-1].getTopResult()
        fullCmd = catItem.fullPath
        keyword = fullCmd[:4]
        cmd = fullCmd[4:]
        if (self.PLUGIN_KEYWORD == keyword) and (cmd in self.CMD_MAPPING):
            apiKey = self.CMD_MAPPING[cmd]
            params = None
           
            if apiKey == 'volume up':
                volumeData = self.getPlayerVolumeData()
                volLevel = volumeData[self.BEEFWEB_PARAM_VALUE]
                volMax = volumeData[self.BEEFWEB_PARAM_MAX]
                volNew = min(volLevel + self.VOLUME_STEP, volMax)
                params = {self.BEEFWEB_PARAM_VOLUME : volNew}
            elif apiKey == 'volume down':
                volumeData = self.getPlayerVolumeData()
                volLevel = volumeData[self.BEEFWEB_PARAM_VALUE]
                volMin = volumeData[self.BEEFWEB_PARAM_MIN]
                volNew = max(volLevel - self.VOLUME_STEP, volMin)
                params = {self.BEEFWEB_PARAM_VOLUME : volNew}
            elif apiKey == 'mute':
                volumeData = self.getPlayerVolumeData()
                isMuted = volumeData[self.BEEFWEB_PARAM_IS_MUTED]
                params = {self.BEEFWEB_PARAM_IS_MUTED : str(not isMuted).lower()}
           
            if apiKey in self.REST_MAPPING:
                self.postFooBarAPICommand(self.REST_MAPPING[apiKey], params)

    def postFooBarAPICommand(self, apiCommand, params):
        conn = httplib.HTTPConnection(self.BEEFWEB_HOST, self.BEEFWEB_PORT)
        requestURL = apiCommand + '?' + urllib.urlencode(params) if params else apiCommand
        req = conn.request('POST', requestURL)
        conn.close()
   
    def getPlayerVolumeData(self):
        conn = httplib.HTTPConnection(self.BEEFWEB_HOST, self.BEEFWEB_PORT)
        req = conn.request('GET', self.BEEFWEB_PLAYER_API_ROOT)
        resp = conn.getresponse()
        volumeData = json.loads(resp.read())
        conn.close()
        return volumeData[self.BEEFWEB_PARAM_PLAYER][self.BEEFWEB_PARAM_VOLUME]
       
       
launchy.registerPlugin(FooLaunchy)
