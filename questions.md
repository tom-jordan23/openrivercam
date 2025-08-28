# Questions from first review of OpenRiverCam Materials

## Site Access
    - Specifics of the site (GPS location, etc)
    - Who owns the site? Who manages access?
    - Do we need to inform someone before being onsite?
    - Is access limited to certain hours of the day or days of the week?
    - Is the installation point accessible via vehicle? If not, how far to the closest parking?

## Site Preparation
    - Is there site preparation needed? If so, whose responsibility will that be?
        - Is there a need to clear vegetation
        - Do we need to dig and set a post? How deep?
        - How high a post is needed, and what dimensions / diameters?
        - What setback from the riverbank is required / recommended for the mounting location?
    - Do we need to have a grounding post available for the station?
    - Does site alteration require permits?

## Mounting
    - Are there tolerances we need to meet for placement?
        - Height above the water surface
        - Horizontal or vertical field of view without disruption?
        - Tolerance of obstructions on near or far bank (e.g. branches obscuring water surface)
    - What security / anti-tampering measures are needed based on the site surroundings? Is it accessible to the public?
    - What mounting hardware should we plan for the PtBox?
    - What mounting hardware to plan for power (solar panel + charge controller)?
    - What mounting hardware to plan for IR emittter?


## Camera positioning
    - What should be the specific aiming point for the camera?
    - is there an optimal camera angle that we're looking to achieve? What are the min/max recommended angles to the water surface?
    - What advice for avoiding glare in the mornings / evenings?

## Installing markers
    - Will we need transport to the other riverside? Or is it walkable / is there a bridge nearby?
    - Do we want to attempt both depth and position markers?
    - Who will define the specs for the markers?
    - Who will procure?
    - Likelihood that the river will be safe for a person to traverse?

## Measuring and Calibrating
    - Do we want to take the Ardusimple + fishfinder approach?
    - Is renting the equipment an option? There appear to be places in Jakarta and Sukabumi.
    - Does AmRC Domestic have equipment they could lend us?
    - Are we ok with the risk of building a low cost RTK rig in-country? Or should we build and test here, then ship?
    - If not that approach, what others are realistic?
    - Will there be more documentation / instructions provided?
    - Do we need to make sure we train the local team on the calibration process?
    - Will the local team need to periodically recalibrate the instrument?


## Software configuration
    - What services should we expect to be running on the PtBox? What ports should we expect to be open?
    - Will we have a shell account on it?
    - What firewalling / security is needed?
    - Do you typically configure automated updates on the device?

## NodeORC questions
    - Will the PtBox be preconfigured for image capture, or do we need to do that?
    - Is there a preferred way to schedule image capture (e.g. Cron job?)
    - Do we have specifics on the camera used in the PtBox?
    - Will we need to generate the device config for NodeORC, or will that be provided with the PtBox?
    - 


## Uplink Connectivity
    - Are we supplying the cell modem, or is that included in the PtBox?
    - Will the local team obtain a SIM card or eSIM locally? And will eSIMs work with the ptBox?
    - Do we know if there will be any port restrictions on the cellular internet service?
    - Do we need a VPN connection to post information to the LiveORC server, or is this generally open to any IP?
    - Will the Pi / PxBox Ethernet interface be available to us? (in the event that we need to bridge the PtBox through something else during setup or troubleshooting)
