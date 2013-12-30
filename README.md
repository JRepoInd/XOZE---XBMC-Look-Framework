XOZE - XBMC ADD-ON with LOOK Framework
=======================================

XOZE has all necessary modules to develop XMBC add-ons supporting its own UI and provides fastest response of all. Few important features that matters:
	XBMC skin module integration.
	Provides XML-based configuration: enables you to modularize your add-on logic by reusing or organizing functions among multiple python modules. Split event handlers, main business logic and setting view content among independent modules.
	Internal In-Memory CacheManager.
	Python logging module integration. 
	Video url resolver - URLResolver module.
	Web service ready: create XBMC service add-on with JSON-RPC support.
	HTTP connection utils: support for cookie and beautifulSoup parsing of HTML content.
	
I might have missed few points which I will be adding soon. I will also document the process to use XOZE framework though its very easy to understand. I have converted one of my add-on using XOZE that is available at https://github.com/ajdeveloped/plugin.video.tvondesizonexl

The project src folder has xoze module which needs to be used as library inside your add-on. It requires following dependency to be added to your add-on: 

				<requires>
                <import addon="xbmc.python" version="2.1.0" />
                <import addon="script.module.simplejson" />
                <import addon="script.module.beautifulsoup" />
                <import addon="script.module.elementtree" />
        </requires>
	
The add-on should be defined as python script:
				<extension point="xbmc.python.script" library="main.py">

To initialize the add-on, you need to initlize the AddonContext class:

from xoze.context import AddonContext
import logging

try:
    addon_context = AddonContext(addon_id='plugin.video.tvondesizonexl', conf={'contextFiles':['actions.xml','dr_actions.xml','dtf_actions.xml'], 'webServiceEnabled':False})
    addon_context.get_current_addon().get_action_controller().do_action('start')
    addon_context.do_clean()
    del addon_context
except Exception, e:
    logging.getLogger().exception(e)
    raise e
    
    
The XBMC add-on skin should be located at its default path: addon/resources/skins/Default/720p/AddonWindow.xml. The window XML should be named: AddonWindow.xml. 

The multiple views can be controlled by grouping the controls and show/hide control using python. DONOT set visible inside XML as false, it will not be loaded. 

I know this documentation is getting unorganized and I definitely need to work on it. :)




	
