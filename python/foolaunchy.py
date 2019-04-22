import launchy
import httplib

class FooLaunchy(launchy.Plugin):
    CMD_MAPPING = {
        'play'     : 'play',
        'pl'       : 'play',
        'y'        : 'play',
        'stop'     : 'stop',
        's'        : 'stop',
        'pause'    : 'pause',
        'p'        : 'pause',
        'next'     : 'next',
        'n'        : 'next',
        'previous' : 'previous',
        'prev'     : 'previous',
        'pr'       : 'previous'
    }
    
    REST_MAPPING = {
        'play'     : '/api/player/play',
        'stop'     : '/api/player/stop',
        'pause'    : '/api/player/pause/toggle',
        'next'     : '/api/player/next',
        'previous' : '/api/player/previous'
    }
    
    PLUGIN_KEYWORD = 'foo '
    
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
            resultsList.push_back( launchy.CatItem(text,
                'foobar2000: ' + cmdText,
                self.getID(), self.getIcon()) )
        
    def getCatalog(self, resultsList):
        pass

    def launchItem(self, inputDataList, catItemOrig):   
        catItem = inputDataList[-1].getTopResult()
        fullCmd = catItem.fullPath
        keyword = fullCmd[:4]
        cmd = fullCmd[4:]
        if self.PLUGIN_KEYWORD == keyword and cmd in self.CMD_MAPPING and self.CMD_MAPPING[cmd] in self.REST_MAPPING:
            self.postFooBarAPICommand(self.REST_MAPPING[self.CMD_MAPPING[cmd]])

    def postFooBarAPICommand(self, apiCommand):
        conn = httplib.HTTPConnection('localhost', 8880)
        req = conn.request('POST', apiCommand)
        conn.close()
        
        
launchy.registerPlugin(FooLaunchy)
