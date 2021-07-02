''' 
  Micropython mit ESP32
  Verbindung mit WLAN, RTC setzen und abfragen
  
  Version 0.10, 01.02.2020
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
'''

from microWebSrv import MicroWebSrv
from mynetzwerk import *


'''
  titel: wird als Überschrift und <title> eingesetzt
  content: der eigentliche Inhalt
  refresh: Refresh - Zeit in Sekunden
'''
def _html(titel,content,refresh):
    return """\
    <!DOCTYPE html>
    <html lang=de>
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="refresh" content="{}">
            <title>{}</title>
        </head>
        <body>
            <h1>{}</h1>
            <h3>
            {}
            </h3>
        </body>
    </html>
    """.format(refresh,titel,titel,content)
        

class BigScreen:
    
    '''
      titel: wird als Überschrift und <title> eingesetzt
      content: der eigentliche Inhalt
      refresh: Refresh - Zeit in Sekunden
    '''
    def __init__(self,titel,refresh):
        self.titel = titel
        self.refresh = refresh
        self.lines = []
     
    def set_refresh(self, refresh):
        self.refresh = refresh
     
    def add(self, line = ""):
        self.lines.append(line)
        
    def clear(self):
        self.lines.clear()
        
    def print(self):        
        for line in self.lines:
            print(line)
            
    def get_content(self):
        content = ""
        for line in self.lines:
            content += line + "<br>"
        return content
    
    def getHTML(self):
        return _html(self.titel,self.get_content(),self.refresh)



log = BigScreen("LOG",10)
hp = BigScreen("Mecanum Car - Homepage",300)
daten = BigScreen("Mecanum Car - aktuelle Daten",5)

@MicroWebSrv.route('/log')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = log.getHTML())

@MicroWebSrv.route('/')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = hp.getHTML())

@MicroWebSrv.route('/daten')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = daten.getHTML())


def startHTTP():
    srv = MicroWebSrv(webPath='www/')
    srv.MaxWebSocketRecvLen = 256
    srv.WebSocketThreaded = True
    srv.Start(True)
    
    
    