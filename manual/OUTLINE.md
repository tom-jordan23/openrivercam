# OpenRiverCam Manual - Draft Outline

## OpenRiverCam Background
- ORC Background
    - Description of OpenRiverCam
    - Brief History and Background
    - How it's being used today
    - Advantages of the approach, and where it's well suited
- Humanitarian Applications
    - Describe potential in humanitarian spaces
    - List examples of specific uses
    - Describe prior work in humanitarian settings
    - What specific problems can we use ORC to address?
- Goals of this research effort
    - Understand the tech
    - Understand how to apply it outside of an academic context
    - Make it reliable for humanitarian use
    - Make it deployable by a volunteer workforce
    - Understand partnerships and data sharing potential with other organizations

## OpenRiverCam Key Concepts
- Hyrology Concepts
    - Relationships between velocity, area, flow and discharge
    - Tracers and flow measurement
    - Comparison with conventional means
- Computer Imaging Concepts
    - Translating digital movement to physical movement (translating pixels moved to meters moved)
    - Different types of distortions and how to correct for them
        - Lens
        - Perspective
        - Atmospheric
- Geospatial Survey Concepts
    - Overview of centimeter-level survey strategies
    - Differential GNSS vs. Total Station
    - More complete explanation of RTK
        - Base and rover stations
        - RTK fixes
        - Logging, RINEX and PPP corrections
    - Physical and environmental factors affecting survey quality

## Site Selection
- Characteristics required
    - Visible tracers
    - Lighting / shadows
    - Uniform flow
    - Ability to survey at all water levels
- Hydrologic / Study Factors
    - Strategy to select where to place monitoring sites
    - Different types of hydrologic events and how they would influence placement
    - Accepted guidance around river gage placement and flow monitoring guidelines
    - Installation in conjunction with other instruments (rain collection, etc)
    - Installation in relation to other monitoring stations (coordinated data collection, verification of accuracy)

## Site Planning and Preparation
- Camera location and installation
- Power Requirements
- Network / Internet Connectivity
- Site security considerations

## Equipment Installation
- Power equipment installation
    - Solar
    - Utility Power
    - Hybrid
- Camera installation and mounting
- Assessing the camera scene and marking the FOV


## Site Survey
- Description of survey concepts (coordinate systemzs, UTM, local vs. global frame, RTK fix accuracy, PPP)
- Survey preparation
- Ground control selection and placement
- Survey setup
    - Hardware
    - Software
    - Process / training
- Survey execution
    - Camera location
    - Field of View
    - Quality Checkpoint
    - Control points
    - Discharge cross section
    - Level cross section
    - Water level
- Survey data processing
    - Adjusting for pole height
    - Calculating water level in the appropriate coordinate system
    - Converting the survey data to UTM and XYZ coords
    - Applying PPP corrections


## Software Configuration
- Configuring the PtBox
    - Orienting the image
    - Adding control points
    - Adding cross sections
    - Integrating with LiveORC server
    - Adding automated collection and upload




# Resources to use in assembling the manualj

- Images from trip: https://photos.google.com/share/AF1QipP2wTbrMXS88TQtg506-_Oe-fAGmaq86eMR27dwSG2iN5UEPjyEfqfDZ0vfZEZYyg?key=Tk1rVFJ6V1lWbk9XUk1mWFF6TGhaNW9zZGF2R2tR
- Survey process: (https://github.com/tom-jordan23/openrivercam/blob/main/procedures/SURVEY_PROCESS.md)
- Camera locator: [Calculating Camera Placement](https://docs.google.com/spreadsheets/d/1SKKfQRSXkeM2f6ueMxSa490PAB0ZW5w8ZF80bUu0O50/edit?gid=200643796#gid=200643796)
- Site Selection Notes for Sukabumi City: https://docs.google.com/spreadsheets/d/1SKKfQRSXkeM2f6ueMxSa490PAB0ZW5w8ZF80bUu0O50/edit?gid=0#gid=0
- LSPIV guide: (in this directory)