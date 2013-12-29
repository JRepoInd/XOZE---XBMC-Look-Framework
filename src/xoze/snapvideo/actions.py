'''
Created on Dec 22, 2013

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''


def addVideoHostingInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoHostingInfo_in_item'), items, 'Retrieving video info', 'Video is either removed or not available. Use other links.')

def addVideoHostingInfoInPlayableItems(request_obj, response_obj):
    items = response_obj.get_item_list()
    playable_items = []
    for item in items:
        if item.get_next_action_name() == 'Play':
            playable_items.append(item)
    try:
        XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoHostingInfo_in_item'), playable_items, 'Retrieving video info', failure_message=None)
    except Exception, e:
        Logger.logFatal(e)

def __addVideoHostingInfo_in_item(item):
    videoHostingInfo = findVideoHostingInfo(item.get_moving_data()['videoUrl'])
    item.set_xbmc_list_item_obj(XBMCInterfaceUtils.updateListItem_With_VideoHostingInfo(videoHostingInfo, item.get_xbmc_list_item_obj()))
        
def addVideoInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoInfo_in_item'), items, 'Retrieving video info', 'Video is either removed or not available. Use other links.')

def addVideoInfoInPlayableItems(request_obj, response_obj):
    items = response_obj.get_item_list()
    playable_items = []
    for item in items:
        if item.get_next_action_name() == 'Play':
            playable_items.append(item)
    try:
        XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addVideoInfo_in_item'), playable_items, 'Retrieving video info', failure_message=None)
    except Exception, e:
        Logger.logFatal(e)

def __addVideoInfo_in_item(item):
    __processAndAddVideoInfo__(item, item.get_moving_data()['videoUrl'])


def addEmbeddedVideoInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addEmbeddedVideoInfo_in_item__'), items, 'Retrieving video info', 'Failed to retrieve video information, please try again later')

def addEmbeddedVideoInfoInPlayableItems(request_obj, response_obj):
    items = response_obj.get_item_list()
    playable_items = []
    for item in items:
        if item.get_next_action_name() == 'Play':
            playable_items.append(item)
    try:
        XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addEmbeddedVideoInfo_in_item__'), playable_items, 'Retrieving video info', 'Failed to retrieve video information, please try again later')
    except Exception, e:
        Logger.logFatal(e)

def __addEmbeddedVideoInfo_in_item__(item):
    video_url = item.get_moving_data()['videoUrl']
    if findVideoHostingInfo(video_url) == None:
        html = HttpClient().getHtmlContent(video_url)
        __processAndAddVideoInfo__(item, html)
    else:
        __processAndAddVideoInfo__(item, video_url)


def __processAndAddVideoInfo__(item, data):
    video_info = findVideoInfo(data)
    if video_info is None:
        raise Exception(ExceptionHandler.VIDEO_PARSER_NOT_FOUND, 'Video information is not found. Please check other sources.')
    if video_info.is_video_stopped():
        raise Exception(ExceptionHandler.VIDEO_STOPPED, 'Video is either Removed by hosting website. Please check other links.')
    if video_info.get_video_link(DataObjects.XBMC_EXECUTE_PLUGIN) is not None:
        item.get_moving_data()['pluginUrl'] = video_info.get_video_link(DataObjects.XBMC_EXECUTE_PLUGIN)
    else:
        if Container().getAddonContext().addon.getSetting('ga_video_title') == 'true':
            Container().ga_client.reportContentUsage(video_info.get_video_hosting_info().get_video_hosting_name(), video_info.get_video_name())
        XBMCInterfaceUtils.updateListItem_With_VideoInfo(video_info, item.get_xbmc_list_item_obj())
        qual_set = Container().getAddonContext().addon.getSetting('playbackqual')
        if qual_set == '':
            qual_set = '0'
        qual = int(qual_set)
        video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_HD_1080)
        if video_strm_link is None or qual != 0:
            video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_HD_720)
            if video_strm_link is None or qual == 2:
                video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_SD)
                if video_strm_link is None:
                    video_strm_link = video_info.get_video_link(DataObjects.VIDEO_QUAL_LOW)
        item.get_moving_data()['videoStreamUrl'] = video_strm_link
    
    
def addPlaylistVideosInfo(request_obj, response_obj):
    items = response_obj.get_item_list()
    for item in items:
        videoItems = __processPlaylistAndAddVideoItem__(item)
        if videoItems is not None and len(videoItems) > 0:
            items.remove(item)
            items.extend(videoItems)
            
            
def addPlaylistVideosInfoInPlayableItems(request_obj, response_obj):
    items = response_obj.get_item_list()
    try:
        for item in items:
            if item.get_next_action_name() == 'Play':
                videoItems = __processPlaylistAndAddVideoItem__(item)
                if videoItems is not None and len(videoItems) > 0:
                    items.remove(item)
                    items.extend(videoItems)
    except Exception, e:
        Logger.logFatal(e)
            
    
def __processPlaylistAndAddVideoItem__(item):
    playlist = findPlaylistInfo(item.get_moving_data()['videoUrl'])
    if playlist is not None:
        videoItems = []
        part = 0
        for videoUrl in playlist:
            part = part + 1
            item = ListItem()
            item.add_moving_data('videoUrl', videoUrl)
            item.set_next_action_name('Play')
            xbmcListItem = xbmcgui.ListItem(label='Video ' + str(part))
            item.set_xbmc_list_item_obj(xbmcListItem)
            videoItems.append(item)
        return videoItems