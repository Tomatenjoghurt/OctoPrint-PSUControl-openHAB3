# OctoPrint PSU Control - openHAB3
Adds openHAb3 support to OctoPrint-PSUControl as a sub-plugin.
Massive Credits go to the original plugin for Home Assistant:
https://github.com/Tomatenjoghurt/OctoPrint-PSUControl-openHAB3

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
* At *Item Name* enter the Name of the openHAB3 Item you want to control (for example: *my_smart_outlet*)
* If your openHAB3 installation is running HTTPS with a self-signed certificate, uncheck the *Verify certificate* option

## Support
Please check your logs first. If they do not explain your issue, open an issue in GitHub. Please set *octoprint.plugins.psucontrol* and *octoprint.plugins.psucontrol_openhab3* to **DEBUG** and include the relevant logs. Feature requests are welcome as well.

## Todo
- [ ] Add images to documentation