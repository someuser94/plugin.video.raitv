import urllib
import urllib2
import json
import urlparse
import datetime
import StorageServer
from resources.lib.relinker import Relinker


class RaiReplay:
    

    def getProgramContent(self,data,index):
        #xbmc.log("leggo dalla cache"+cache.get('programs'))
        #exit(0)
        #if mode:
        #    programs = json.JSONDecoder().decode(cache.get('found'))
        #else:
        #    programs = json.JSONDecoder().decode(cache.get('programs'))
        program = data[int(index)]
        pathId = program['PathID'].replace('www.rai.it/raiplay','www.raiplay.it',1)
        response = urllib2.urlopen(pathId)
        data = json.JSONDecoder().decode(response.read())
        return data
        cache.set('program',json.JSONEncoder().encode(data['Blocks']))
        for i in range(len(data['Blocks'])):
            program_element = xbmcgui.ListItem(data['Blocks'][i]['Name'])
            xbmcplugin.addDirectoryItem(handle,sys.argv[0] + '?' + urllib.urlencode({'mode': 'program','index':i}),program_element,isFolder=True)
        xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.endOfDirectory(handle=handle, succeeded=True)    
     
    def exploreProgram(index):
        program = json.JSONDecoder().decode(cache.get('program'))
        #xbmc.log ("program="+cache.get('program'))
        detail = program[int(index)]['Sets']
        cache.set('detail',json.JSONEncoder().encode(detail))
        if len(detail) == 1:
            detailProgram(0)
        else:
            for i in range(len(detail)):
                detail_element = xbmcgui.ListItem(detail[i]['Name'])
                xbmcplugin.addDirectoryItem(handle,sys.argv[0] + '?' + urllib.urlencode({'mode': 'detail','index':i}),detail_element,isFolder=True)
            xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

    def getMediaContent(self,data,index):
        detail = data
        #xbmc.log ("program="+cache.get('program'))
        url = detail[int(index)]['url'].replace('/raiplay','http://www.raiplay.it',1)
        response = urllib2.urlopen(url)
        data = json.JSONDecoder().decode(response.read())
        #cache.set('items',json.JSONEncoder().encode(data['items']))
        data_content = {}
        for i in range(len(data['items'])):
            pathId = data['items'][index]['pathID'].replace('/raiplay','http://www.raiplay.it',1)
            response = urllib2.urlopen(pathId)
            item = json.JSONDecoder().decode(response.read())
            contentUrl = item['video']['contentUrl']
            data_content[i]={'title':data['items'][i]['subtitle'],'type':'Video','infoLabels':{'episode':i+1,'duration':data['items'][i]['duration']},'contentUrl':contentUrl}
            #items_element.setInfo(type='Video',infoLabels={'episode':i+1,'duration':data['items'][i]['duration']})
            #xbmcplugin.addDirectoryItem(handle,sys.argv[0] + '?' + urllib.urlencode({'mode': 'play','index':i}),items_element,isFolder=True)
        #xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
        #xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
        return data_content
        

#    if submode  == 'explore':
#        exploreLetters(param['letter'])
#    elif submode == 'programs':
#        explorePrograms(0,int(index))
#    elif submode == 'found':
#        explorePrograms(1,int(index))
#    elif submode == 'program':
#        exploreProgram(int(index))
#    elif submode == 'detail':
#        detailProgram(int(index))
    #elif submode=='play':
    #    play(int(param['index']))
#    elif submode=='search':
#        search()
#    else:
#        mainMenu()
    