# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcaddon
import xbmcgui

if sys.version_info >= (2, 7):
    import json
else:
    import simplejson as json

# Import the common settings
from resources.lib.settings import log
from resources.lib.core import SuitabilityCore

ADDON = xbmcaddon.Addon(id='script.suitability')


def getIsTvShow():
    if xbmc.getCondVisibility("Container.Content(tvshows)"):
        return True
    if xbmc.getCondVisibility("Container.Content(Seasons)"):
        return True
    if xbmc.getCondVisibility("Container.Content(Episodes)"):
        return True
    if xbmc.getInfoLabel("container.folderpath") == "videodb://tvshows/titles/":
        return True  # TvShowTitles

    return False


#########################
# Main
#########################
if __name__ == '__main__':
    log("Suitability: Started")

    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "params": { "addonid": "repository.robwebset", "properties": ["enabled", "broken", "name", "author"]  }, "id": 1}')
    json_response = json.loads(json_query)

    displayNotice = True
    if ("result" in json_response) and ('addon' in json_response['result']):
        addonItem = json_response['result']['addon']
        if (addonItem['enabled'] is True) and (addonItem['broken'] is False) and (addonItem['type'] == 'xbmc.addon.repository') and (addonItem['addonid'] == 'repository.robwebset') and (addonItem['author'] == 'robwebset'):
            displayNotice = False

    if displayNotice:
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "params": { "addonid": "repository.urepo", "properties": ["enabled", "broken", "name", "author"]  }, "id": 1}')
        json_response = json.loads(json_query)

        if ("result" in json_response) and ('addon' in json_response['result']):
            addonItem = json_response['result']['addon']
            if (addonItem['enabled'] is True) and (addonItem['broken'] is False) and (addonItem['type'] == 'xbmc.addon.repository') and (addonItem['addonid'] == 'repository.urepo'):
                displayNotice = False

    if displayNotice:
        xbmc.executebuiltin('Notification("robwebset of URepo Repository Required","github.com/robwebset/repository.robwebset",10000,%s)' % ADDON.getAddonInfo('icon'))
    else:
        videoName = None
        isTvShow = getIsTvShow()

        # First check to see if we have a TV Show of a Movie
        if isTvShow:
            videoName = xbmc.getInfoLabel("ListItem.TVShowTitle")

        # If we do not have the title yet, get the default title
        if videoName in [None, ""]:
            videoName = xbmc.getInfoLabel("ListItem.Title")

        # If there is no video name available prompt for it
        if videoName in [None, ""]:
            # Prompt the user for the new name
            keyboard = xbmc.Keyboard('', ADDON.getLocalizedString(32032), False)
            keyboard.doModal()

            if keyboard.isConfirmed():
                try:
                    videoName = keyboard.getText().decode("utf-8")
                except:
                    videoName = keyboard.getText()

        if videoName not in [None, ""]:
            log("Suitability: Video detected %s" % videoName)
            SuitabilityCore.runForVideo(videoName, isTvShow)
        else:
            log("Suitability: Failed to detect selected video")
            xbmcgui.Dialog().ok(ADDON.getLocalizedString(32001), ADDON.getLocalizedString(32011))

    log("Suitability: Ended")
