# OctoPrint PSU Control - openHAB3
Adds openHAB3 support to OctoPrint-PSUControl as a sub-plugin.
Massive Credits go to the original plugin for Home Assistant:
https://github.com/edekeijzer/OctoPrint-PSUControl-HomeAssistant

## Setup
- Install the plugin using Plugin Manager from Settings
- Configure this plugin
- Select this plugin as Switching *and* Sensing method in [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl)

## Configuration
* Enter the URL of your openHAB3 Installation
* Go to your openHAB3 Administration Site
* At the bottom left, click on your Username
* Scroll down to "API Tokens" and click *Create new API Token*, enter your Admin Username, Admin Password and give the token a name (suggestion: OctoPrint PSUControl) and click *OK*
* Copy the token and paste it into the *Access token* field in the plugin settings
* Alternatively, you can use Basic Authorization (e.g. your Username and Password for openHAB3). Careful, you'll may need to enable *Allow Basic Authentication* in Settings -> API Settings in openHAB3.
* At *Item Name* enter the Name of the openHAB3 Item you want to control (for example: *my_smart_outlet*). IMPORTANT: we need the Item Name, not the Label! This can be checked when going to Items -> *your_item* -> Edit and see the Name of the Item.
* If your openHAB3 installation is running HTTPS with a self-signed certificate, uncheck the *Verify certificate* option

## FAQ
### The plugin is not working! / No actions to the device are done!
Check if you really used the correct settings - Portnumber, Item Name (not Label!). Otherwise please see down below at support.

### Help, my openHAB3 Instance is behind a proxy (NGINX, traefik, caddy), which cares for Authorization!
Just use the Basic Authorization of your proxy in the settings.

### Does this work with openHAB2?
Maybe. I developed it for openHAB3, but I guess the API is still the same, so it may work. Though, this plugin comes with no warranty!

## Support
Please check your logs first. If they do not explain your issue, open an issue in GitHub. Please set *octoprint.plugins.psucontrol* and *octoprint.plugins.psucontrol_openhab3* to **DEBUG** and include the relevant logs. Feature requests are welcome as well.