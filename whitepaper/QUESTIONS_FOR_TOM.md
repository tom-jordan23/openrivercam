# OpenRiverCam Humanitarian Whitepaper — Questions for Tom

Answer each question by placing as much text as you need inside its `Tom` comment block. You may leave questions unanswered, write `TBD`, or point to another document. The comments will not appear when this file is rendered as Markdown.

## 1. Purpose and audience

### 1.1 What is the single most important outcome you want from this whitepaper?

Examples might include securing funding for another pilot, recruiting implementation partners, influencing humanitarian monitoring practice, documenting lessons, or establishing OpenRiverCam's credibility.

<!-- Tom:
I want to highlight the capabilities that new tech like openrivercam can deliver, and the new partnerships that national societies will need to build with their university and government partners in order to effectively deploy, support and operate these new technology platforms. Additionally, I would like to address scientific data generation, sharing, interpretation, analysis and action across these partners with a focus on building preparedness and capability for anticipatory action.
-->

### 1.2 Who is the primary reader?

Please name the kind of person, their organization, and their likely level of technical knowledge. Add secondary audiences if needed.

<!-- Tom:
Humanitarians, Red Cross societies, academics and government scientists
-->

### 1.3 What should the primary reader think, feel, or do after reading it?

<!-- Tom:
Advanced tech has great potential for humanitarian applications, but implementation will require partnerships with university, government and local commities that we need to actively develo.
-->

### 1.4 How would you characterize the paper?

Is it principally a field case study, a humanitarian position paper, a lessons-learned report, a pilot proposal, or some combination?

<!-- Tom:
Lessons learned report.
-->

### 1.5 Where do you expect the paper to be published or distributed?

Include any conferences, organizational websites, donor meetings, mailing lists, or private circulation you have in mind.

<!-- Tom:
The paper will probably be circulated in the humanitarian community, among Red Cross societies, etc. It may complement a presentation that Hessel will be doing at the WMO in Amsterdam in OCtober.
-->

## 2. Central argument

### 2.1 In your own words, what is the paper's main argument?

Do not worry about polished language. What do you believe the Indonesia work demonstrates?

<!-- Tom:
This approach has a lot of potential, but is very complex for a national society to implement on their own. Seek partnerships with university and government partners.
-->

### 2.2 What claims do you most want the paper to make?

List both technical and humanitarian claims, even if some will require more evidence.

<!-- Tom:
1. OpenRiverCam is an effective tool for anticipatory action, raising an understanding of river behavior based on data analysis. This effort demonstrated the capability of the technology, and future projects should build on it by being more intentional about the hydrology questions we're trying to answer.
2. National Societies should seek to build partnerships with the hydrology experts in their university and government circles, as there are natural partnerships beyond OpenRiverCam that benefit all parties and the public.
-->

### 2.3 What should the paper explicitly avoid claiming?

<!-- Tom:
This technology has not yet reached consumer level. A fair amount of technical expertise is required in electronics, survey, etc.
-->

### 2.4 What makes this work distinctive compared with conventional gauges, water-level sensors, satellite products, or other camera systems?

<!-- Tom:
Contactless monitoring - ability to monitor flows that might be dangerous to work in or install equipment in
Low station cost - ~$1k usd ea for the stations we built, with the possibility to refine and adapt
Deployable off-grid - can work with multiple power and connectivity strategies
Extremely low maintenance - Hessel reports visiting sites only a few times a year to clear vegetation.
Temporal resolution - can recognize rapid onset events such as flood waves, etc.
Multimodal response - The station design includes additional relays that could trigger sirens, SMS messages, etc.
Open source and extensible, with excellent support from the author
-->

### 2.5 Where is OpenRiverCam not the right solution?

Describe unsuitable sites, operational contexts, organizational conditions, or use cases.

<!-- Tom:
Site characteristics are very important. The repo has lots of information about what makes a good vs. bad site.
-->

## 3. Humanitarian problem and use

### 3.1 What humanitarian problem originally motivated this project?

What information was missing, for whom, and what decisions could that information improve?

<!-- Tom:
Better understanding of river behavoir and how to use river stage and flow data to better predict and detect developing flood events, gauge their likely scale and guide decision-making.
-->

### 3.2 Which humanitarian use case should lead the paper?

Examples include flood preparedness, anticipatory action, operational situational awareness, WASH or water-resource management, climate adaptation, or strengthening national monitoring networks.

<!-- Tom:
anticipatory action on flood and drought preparedness. Operational awareness and response planning. Possible recovery and climate adaptions. A major theme should be partnering with university and government on climate adaptation strategies. We need to work together to address these challenges.
-->

### 3.3 How do you imagine OpenRiverCam data leading to a humanitarian action?

Describe the chain from measurement to interpretation, decision, communication, and action. Identify what parts OpenRiverCam provides and what must be supplied by partners.

<!-- Tom:
I would imagine that OpenRiverCam might be something run by university or government partners in conjunction with national societies. National societies should work to be engaged with data analysis, interpretation, planning and response. National societies with strong technolgy skills may operate independently, but the real power is in collaboration with partners. We should highlight how BMKG showed interest in using this for developing a future drought model and for enhancing their risk-based forecasting model.
-->

### 3.4 Were any real humanitarian decisions made using data from the Sukabumi station?

If so, who made them, what data did they use, and what changed? If not, say so plainly.

<!-- Tom:
Not at this time. This has been primarily a project to explore how to deploy and support the tech, and to understand what can be done with the data generated.
-->

### 3.5 Have community members, PMI personnel, or government users given feedback about the system?

Include favorable, critical, and informal feedback. Note whether quotations may be published and attributed.

<!-- Tom:
Hold this as an open question
-->

## 4. Project origin and history

### 4.1 How did you personally become involved with OpenRiverCam?

<!-- Tom:
Let's leave this section for Dan
-->

### 4.2 How did the Indonesia project originate?

Who first identified the need, who initiated the partnership, and how did the original concept change?

<!-- Tom:
Let's leave this section for Dan
-->

### 4.3 What were the project's original objectives and success criteria?

Which were achieved, partially achieved, changed, or not achieved?

<!-- Tom:
Let's leave this section for Dan
-->

### 4.4 What was the original plan for Sukabumi and Jakarta?

Why were two configurations built, and what was each intended to demonstrate?

<!-- Tom:
We wanted Jakarta to be an always-on / commercial power demonstration station that we could use to show visitors to the PMI headquarters, and also to test hardware / software configurations and to generate data that could be widely shared as an example.
-->

### 4.5 Which dates and milestones are essential to the story?

<!-- Tom:
These should be largely available in the documentation corpus in our github repo.
-->

## 5. Technical explanation

### 5.1 How would you explain OpenRiverCam to a humanitarian program manager in one paragraph?

<!-- Tom:
OpenRiverCam uses Computer Vision and Edge Computing to calculate river stage (height) and discharge volume based solely on camera observations and a very accurate initial survey of the river's morphology (shape). This allows for low cost, off-grid deployment in remote areas as well as flexible deployment options for urban areas. OpenRiverCam can be deployed with a high temporal resolution, allowing for detection of rapid onset events like flood waves.
-->

### 5.2 What components of the system should the paper describe?

Consider the camera, compute hardware, power, connectivity, water-level measurement, survey, processing software, server, dashboard, and operator workflow.

<!-- Tom:
This is well documented in the repo.
-->

### 5.3 Which parts come from upstream OpenRiverCam, ORC, ORC-OS, pyorc, or LocalDevices, and which parts were developed by this project?

Please describe the boundary carefully so credit and ownership are accurate.

<!-- Tom:
This is well documented in the repo.
-->

### 5.4 What does the station measure directly, and what does it calculate or infer?

<!-- Tom:
This is well documented in the repo.
-->

### 5.5 What technical conditions must be present for a valid measurement?

Include site geometry, visible tracers, lighting, survey quality, water level, calibration, and any other important dependencies.

<!-- Tom:
This is well documented in the repo.
-->

### 5.6 What accuracy or uncertainty statements can we responsibly make?

Separate camera-fit RMSE, water-level accuracy, surface-velocity accuracy, and final discharge accuracy. Note what has and has not been independently validated.

<!-- Tom:
This is well documented in the repo.
-->

### 5.7 Which design principles matter most?

For example: commodity parts, no soldering, common tools, component replacement, open software, local repair, remote diagnostics, or bilingual documentation.

<!-- Tom:
This is well documented in the repo.
-->

## 6. Indonesia field evidence

### 6.1 What do you consider the strongest verified accomplishments from Sukabumi?

<!-- Tom:
We demonstrated the technology can work in really difficult environments, and that a national society can build the partnerships needed to apply this and other advanced technologies in partnership with university and government agencies.
-->

### 6.2 What does the 0.037 m calibration RMSE establish—and what does it not establish?

<!-- Tom:
This is well documented in the repo.
-->

### 6.3 What data has the Sukabumi station collected to date?

Include the time period, number of captures or measurements, completeness, flow conditions represented, and known gaps if available.

<!-- Tom:
This is well documented in the repo.
-->

### 6.4 What do we know about station availability and data-delivery reliability?

Please distinguish station uptime, successful capture, valid processing, successful upload, and availability to an end user.

<!-- Tom:
This is well documented in the repo.
-->

### 6.5 Has discharge been compared with an independent reference method?

Describe any comparisons, their limitations, and any future validation planned.

<!-- Tom:
This is well documented in the repo, and is ongoing.
-->

### 6.6 What should readers understand about Jakarta?

What was learned from building it, why was it not deployed, and what future role could it serve?

<!-- Tom:
This is well documented in the repo.
-->

## 7. Failures and lessons

### 7.1 Which three failures or surprises are most important to feature?

For each, explain what happened, why it mattered, how it was discovered, and what should change next time.

<!-- Tom:
This is well documented in the repo.
-->

### 7.2 What happened with the two RTK surveys?

Explain the failure in accessible language, why the repeated result initially appeared credible, how IPB resolved it, and what procedural lesson follows.

<!-- Tom:
This is well documented in the repo.
-->

### 7.3 What should we say about daylight optical water-level failures?

Distinguish measured evidence from the current causal hypothesis and describe the recommended independent water-level reference.

<!-- Tom:
This is well documented in the repo.
-->

### 7.4 What should we say about power, duty cycling, connectivity, synchronization, and server failures?

Which issues were design problems, software defects, operational ownership problems, or ordinary field constraints?

<!-- Tom:
This is well documented in the repo.
-->

### 7.5 What did the site-permission failure teach you?

<!-- Tom:
This is well documented in the repo.
-->

### 7.6 Which parts of the current design would you retain, and which would you replace before another operational deployment?

<!-- Tom:
This is well documented in the repo.
-->

## 8. Costs and sustainability

### 8.1 How should we describe the approximately USD 1,340 Sukabumi materials cost?

Identify exclusions such as the existing solar panel and battery, shipping, customs, survey, travel, labor, connectivity, hosting, spares, and maintenance.

<!-- Tom:
This is well documented in the repo. Dan should cover the administrative aspects in his section.
-->

### 8.2 What would a realistic installed cost or three-to-five-year total cost of ownership include?

Provide known figures where possible and mark unknowns.

<!-- Tom:
This is well documented in the repo.
-->

### 8.3 Who currently pays for and manages connectivity, server hosting, repairs, consumables, and ongoing technical support?

<!-- Tom:
This is all grant funded through the end of this calendar year. Beyond that is up to PMI to determine.
-->

### 8.4 What institutional arrangement would make a future deployment sustainable?

Who should own deployment, technical maintenance, hydrologic validation, data, decision-making, and funding?

<!-- Tom:
This is well documented in the repo.
-->

### 8.5 What does “local ownership” mean in practical terms for this project?

<!-- Tom:
This is well documented in the repo.
-->

## 9. Partners and people

### 9.1 What role did each partner actually play?

Please cover PMI, American Red Cross, IPB, BHLK, LocalDevices, and any others that should be credited.

<!-- Tom:
This is well documented in the repo.
-->

### 9.2 Which partner contributions or individuals must be acknowledged?

Include correct names, titles, organizations, and preferred wording if known.

<!-- Tom:
This is well documented in the repo. If there's data missing, call it out and i'll get it.
-->

### 9.3 Which statements about partners require their review or approval?

<!-- Tom:
all of them. we will circulate a draft prior to publishing.
-->

### 9.4 May the paper use partner logos, field photographs, site names, and quotations?

Identify known permissions and anything that still needs clearance.

<!-- Tom:
yes, after circulation.
-->

### 9.5 Are there any sensitive relationships, failures, or institutional details that should be anonymized or handled carefully?

<!-- Tom:
no
-->

## 10. Protection, ethics, and data responsibility

### 10.1 What can the cameras capture besides the river?

Could imagery include identifiable people, homes, routes, livelihoods, private property, or sensitive infrastructure?

<!-- Tom:
yes, we will cover that when we gain approval.
-->

### 10.2 What privacy or data-governance controls currently exist?

Consider field-of-view restrictions, masking, audio, access, retention, server location, sharing, deletion, security, and incident response.

<!-- Tom:
This is well documented in the repo.
-->

### 10.3 Were communities or nearby property owners consulted about the camera installation?

Describe the process and any gaps.

<!-- Tom:
yes, we had excellent community support from PMI through their SIBAT network of community volunteers.
-->

### 10.4 What safeguards should be mandatory in future humanitarian deployments?

<!-- Tom:
This is well documented in the repo.
-->

### 10.5 Could the imagery or river data create risks if misused?

Consider surveillance, policing, migration control, security, land or water disputes, and unequal access to warnings or resources.

<!-- Tom:
This is well documented in the repo.
-->

## 11. Proposed next pilot

### 11.1 What should the next phase of work be?

Describe the number and type of sites, location if known, duration, partners, and intended operational use.

<!-- Tom:
Next phase should focus on the hydrology aspects - let IPB help determine the most important hydrology questions to answer in the next phase.
-->

### 11.2 What questions must the next pilot answer?

<!-- Tom:
Next questions should be hydrology focused - what basins to monitor, what rivers to try to model for rain / flood / drought behavior.
-->

### 11.3 What evidence would justify scaling beyond the pilot?

Consider measurement validity, availability, latency, maintenance burden, operator usability, cost, decision use, community acceptance, and humanitarian outcomes.

<!-- Tom:
This is well documented in the repo.
-->

### 11.4 What should be treated as a go/no-go gate before field deployment?

<!-- Tom:
This is well documented in the repo.
-->

### 11.5 What partners, expertise, funding, or permissions are needed next?

<!-- Tom:
This is well documented in the repo.
-->

### 11.6 What is the concrete invitation or call to action at the end of the whitepaper?

<!-- Tom:
Do not be afraid to adopt new technology, but know that there's a maturity curve so expect that it will take time and require expertise.
-->

## 12. Author roles and review

### 12.1 What is Dan's role and subject-matter expertise?

Which sections or questions should he own?

<!-- Tom:
Dan is manager of the American Red Cross International Services Data Tech and Innovation group. He was instrumental in identifying this grant opportunity, securing funding and getting the grant moving. He's been the senior humanitarian advisor helping the project find its direction.
-->

### 12.2 What is Teguh's role and subject-matter expertise?

Which sections or questions should he own?

<!-- Tom:
Teguh is the senior program manager for the Indonesian delegation of the American Red Cross, based in Jakarta. Teguh is the point of liaison with the PMI and managed much of the in-country activity.
-->

### 12.3 Who should serve as final editor and make decisions when authors disagree?

<!-- Tom:
I will handle this.
-->

### 12.4 Who should conduct technical, humanitarian, ethics/privacy, and Indonesian-context reviews?

<!-- Tom:
I will review the technical. Dan will provide the senior humanitarian review. Teguh will ensure the indonesian context is proper.
-->

### 12.5 Who must approve the final paper before publication?

<!-- Tom:
Dan, Teguh and Tom
-->

## 13. Format, style, and logistics

### 13.1 Do the cover and references count toward the 8–10 page limit?

<!-- Tom:
No
-->

### 13.2 Is there a target publication date or external deadline?

<!-- Tom:
Let's shoot for 11/1
-->

### 13.3 Should the tone be institutional, academic, donor-facing, personal and reflective, or another style?

Please name example publications whose tone or design you admire, if any.

<!-- Tom:
Let's say humanitarian academic. I would really like to emphasize the networking and interagency aspects of this project.
-->

### 13.4 Does the paper need versions in Bahasa Indonesia or any other language?

If so, who will perform and review the translation?

<!-- Tom:
Teguh will facilitate translation / review in indonesian.
-->

### 13.5 Which photographs, diagrams, maps, tables, or charts do you most want included?

<!-- Tom:
System diagram, some of the data products we used to analyze the survey data, and some of the ORC data products (timeseries, graphs, etc). And of course photos of the site and the AR view that ORC provides.
-->

### 13.6 Are there branding, attribution, accessibility, citation-style, or template requirements?

<!-- Tom:
Follow American Red Cross standards / templates for comms.
-->

## 14. Anything the outline misses

### 14.1 What story, result, concern, or opinion have these questions failed to capture?

<!-- Tom:
The amazing teamwork and community spirit of the PMI, particularly the Sukabumi team and their SIBAT volunteers. What an amazing group!
-->

### 14.2 If readers remember only one sentence from the paper, what should it be?

<!-- Tom:
The technology is interesting, but it's the partnerships that will pay off over the long term. And those partnerships will be critical for helping national societies, universities and government face problems like climate adaption together as a single team.
-->
