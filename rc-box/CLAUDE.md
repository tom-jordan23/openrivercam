# RC-Box design effort

We are working to adapt the OpenRiverCam approach to humanitarian river monitoring, and we want to build a hardware package that will be easily deployable by National Societies that may not have specialized training in hydrology, GIS, survey processes or electronics / electrical systems.

The platform should consist of a raspberry pi 5 (with PiJuice / PiSugar to control a regular startup and shutdown process) running the ORC-OS sofware. It should include 2 Pi V3 camera modules that could be mounted separately and connected via USB. The device must be easily deployable with basic training, and needs to be weatherproof in all environments and able to withstand the abuse of shipping, warehousing and being handled by untrained staff. Everything must be field serviceable. The device needs to be able to connect via wireless or cellular modem.

In a recent deployment in Indonesia, we assembled the following list of improvements for a future hardware platform:

Don't depend on local procurement for specialized items. Maybe minimize local procurement wherever we can.
Make sure hardware is resilient against shipping damage
Ship consumables that might be even remotely hard to source - we spent lots of time driving around to find little things that I could have easily packed or shipped
Include extras of fittings, terminals, fuses, etc. to leave behind in the box for later service
Mark all connections distinctly and then photograh to help with remote troubleshooting
Provide better engineering specs in advance for the pole or mast - diameter, material, rigidity, lateral load, etc.
If using an arm, calculate moment to factor into vibration or sway
Give time for at least two full surveys. Save original source data from both.
Hardware needs a visual indicator of whether it's on or not, and it needs to be visible from the ground while on the pole
Hardware soft power switch makes it impossible to know if the device has been turned on or not
We need a better way to capture the intended video orientation and angle, especially for steep banks. 
There's not an obvious way in the software to change the orientation of the video (portrait / landscape / rotate).
Need a mounting system that allows for easier changes in orientation to find a proper picture
Consider a different approach to cameras - something simpler, off the shelf and easily field replaceable.
Create a hardware switch we can use to turn on a local wireless hotspot for configuration.
Create a hardware switch we can use to put the device into maintenance mode / cycling mode / power on / power off
Provide a configuration that uses commercial power and / or network if available
Maybe a way to communicate what the startup / shutdown sequence is other than trying the website over and over again
Hardware should have a lot more local storage than what they appear to have - we need to make sure they can operate for a long time without a stable connection without losing data
Device should show in the UI whether it is in maintenance mode or not, and how long the timer. Should also give an option to extend maintenance mode.
