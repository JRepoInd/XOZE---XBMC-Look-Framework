'''
Created on Nov 30, 2013

@author: ajju
'''
import json
import re

video_info_link="jwplayer('flvplayer').setup({file:'http://31.207.20.187/d/pl3jefwcfhfk5moxa5tixwptqnhksvcfdn5wz3b7mtdy4djdu4cnzroley/video.mp4',flashplayer:'http://hostingbulk.com/player/player.swf',skin:'http://hostingbulk.com/player/blueratio.zip',image:'http://31.207.20.187/i/00055/vii7cf4vcw25.jpg',duration:'2612',width:1024,height:562,provider:'http',modes:[{type:'flash',src:'http://hostingbulk.com/player/player.swf'},{type:'html5',config:{file:'http://31.207.20.187/d/pl3jefwcfhfk5moxa5tixwptqnhksvcfdn5wz3b7mtdy4djdu4cnzroley/video.mp4','provider':'http'}},{type:'download'}]});"

img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
if len(img_data) == 1:
    print img_data
video_link_data = re.compile(r"file:\'(.+?)\'").findall(video_info_link)
print video_link_data
if len(video_link_data[0]) == 2:
    video_link = video_link_data[0][0]
    print video_link