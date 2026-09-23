# OpenRiverCam Whitepaper — Tom Jordan Voice Guide

**Source:** [Tom Jordan writing repository](https://github.com/tom-jordan23/writing)
**Primary guides consulted:** `tojo_style.md`, `STYLE_INDEX.md`, `STYLE_PROMPT_CONDENSED.md`, `STYLE_Humanitarian_Executive.md`, `STYLE_Humanitarian_Technical.md`, and `STYLE_Academic_University_Business.md`
**Application:** Technical implementation and lessons-learned whitepaper primarily for humanitarian IT; program leaders, university partners, and government scientists are secondary readers

This guide adapts Tom's established voice to this paper. It is a drafting and editing reference, not an evidence source.

## 1. Voice in one paragraph

Write as an experienced practitioner explaining a difficult but navigable problem to capable peers. Begin with the humanitarian purpose, establish a clear framework, and then move from principle to concrete field evidence. Be candid about failures without dramatizing them. Use exact examples, costs, dates, and measurements where the evidence supports them. Treat technology as a tool that serves people and institutions. Give local partners, practitioners, and communities agency; the author is a participant and learner, not the hero.

## 2. Audience blend

The primary register is humanitarian technical. Assume an IT practitioner who understands infrastructure, networking, remote support, and service operations but needs hydrology and survey concepts explained. Use concrete architecture, interfaces, failure mechanisms, and support requirements. Technical depth should help the reader evaluate or operate the service; configuration recipes belong in linked documentation.

The paper needs three aspects of Tom's voice:

### Humanitarian executive

Use for the opening, partnership argument, institutional model, and conclusion.

- Begin with the humanitarian decision or capability, not the device.
- Keep affected communities and operational purpose visible.
- Acknowledge resource constraints, protection, sustainability, and local ownership.
- Frame partnership as shared authority and capability, not outside experts transferring knowledge to passive recipients.
- State risks and tradeoffs directly, then give a practical path forward.

### Humanitarian technical

Use for system explanation, deployment evidence, failures, and recommendations.

- Explain how the system works in plain language before introducing technical terminology.
- Use measured values, versions, time windows, and cost scopes.
- Explain failure mechanisms, not merely symptoms.
- Design for unreliable power, connectivity, staffing, supply chains, and long-term maintenance.
- Favor open, repairable, locally supportable technology, while acknowledging when integration creates new dependencies.

### Academic and shared-governance

Use for university/government collaboration and the proposed next phase.

- Use consultative rather than directive language.
- Respect distinct institutional mandates and expertise.
- Present alternatives and tradeoffs rather than a predetermined product decision.
- Make explicit which questions belong to hydrologists, humanitarian decision-makers, community partners, and technology teams.
- Treat peer review, validation, and disagreement as strengths.

## 3. Signature argument pattern

Tom's strongest recurring structure is:

1. **Problem:** Name the practical or institutional problem in human terms.
2. **Framework:** Show how to think about it; define responsibilities, stages, or decision criteria.
3. **Specific approach:** Explain what the team attempted.
4. **Evidence:** Give concrete deployment results, including failures.
5. **Tradeoff:** State what the approach gains and what it costs or requires.
6. **Guidance:** Offer a path that another capable team can adapt.

For this whitepaper, that becomes:

> Humanitarian organizations need better local river information. A camera can generate observations, but observations become useful only through a data-to-action system. The Indonesia project tested one part of that system. Its strongest evidence includes both a functioning station and the failures that exposed hidden dependencies. Those lessons point toward a partnership model in which National Societies, universities, government agencies, communities, and technology developers own different parts of the work.

## 4. Tone

### Use

- Calm confidence
- Practitioner-to-practitioner respect
- Intellectual humility
- Direct acknowledgment of complexity
- Warmth toward the people who did the work
- Optimism grounded in a next step
- Precise language about uncertainty

### Avoid

- Product marketing or technological triumphalism
- “Revolutionary,” “game-changing,” “seamless,” or “simple”
- Treating failure as embarrassment or assigning blame
- Presenting outside expertise as rescue
- Abstract claims about “communities” without naming their role
- False precision or unsupported impact statistics
- Academic distance that removes the people and decisions from the story

### Preferred stance

> This is hard. The failure is understandable. The evidence tells us what to change. Capable partners can navigate the next step together.

## 5. Sentence and paragraph habits

- Prefer active voice and name the actor: “IPB re-surveyed the site,” not “the site was re-surveyed.”
- Keep one principal idea per sentence when translation matters.
- Use paragraphs of roughly three to five sentences.
- Move from principle to example to implication.
- Use em dashes sparingly to define or contrast, not as a substitute for sentence structure.
- Define technical terms on first use.
- Use short sentences for important limits: “That is not discharge accuracy.”
- Use parallel construction for responsibilities and recommendations.
- Use “we” for project-team decisions and learning, not to absorb partner achievements.
- Prefer “can,” “may,” “often,” and “in this deployment” when evidence is contextual.

## 6. Evidence language

Tom's voice is credible when it is specific and transparent about evidence strength.

### Measured

> In a 200-capture sample, every rejected optical water-level result occurred during daylight. None occurred at night.

### Documented but not independently verified

> The operating record attributes the 4.8-day communications outage to an unfunded prepaid SIM. The boot history confirms that the station continued to wake during the outage; it does not independently confirm the account balance.

### Interpretation

> The time-of-day pattern is consistent with specular reflection from the water surface. Direct image-based confirmation remains pending.

### Recommendation

> A future operational station should include an independent water-level reference. This recommendation follows from the measured failure; it does not depend on proving the optical cause.

### Future potential

> High-frequency river observations could support anticipatory action when partners also establish validated thresholds, decision authority, communication channels, and community response plans.

## 7. How to write about failure

Failure analysis is a central feature of Tom's voice and of this project. Use a four-part pattern:

1. What happened.
2. How the team established it.
3. Why it mattered to the larger system.
4. What should change next time.

Keep people out of the causal chain unless human action is itself the relevant, documented system issue. Prefer:

> The first survey method failed twice under the site's conditions. Repeating it with the same equipment and process reproduced the same noise. IPB changed the method and recovered the project with a total-station survey. The lesson is not that RTK is inherently unsuitable; it is that an independent field check must fail before the team leaves, and a failed method should not be repeated unchanged.

Avoid:

> The team conducted a bad survey and IPB fixed it.

## 8. How to write about partnership

Partnership language should identify real contributions and authority.

### Prefer

- “IPB changed the survey method and produced the geometry used by the deployed configuration.”
- “PMI and SIBAT brought local relationships, site presence, and community connection.”
- “BHLK contributed standards knowledge and an independent measurement opportunity.”
- “The next phase should begin with hydrologic questions developed with the institutions responsible for understanding and managing the basin.”

### Avoid

- “We trained local partners.”
- “Beneficiaries accepted the technology.”
- “Local capacity was built” without saying who did what and what capability remained.
- “Stakeholder engagement” when the actual relationship can be named.

Ask throughout:

- Who defined the problem?
- Who made the decision?
- Whose knowledge changed the design?
- Who maintains the system after the grant?
- Who can access and interpret the data?
- Who bears risk if the system is wrong or unavailable?

## 9. Translation-friendly humanitarian writing

The paper is intended for Indonesian translation. Clarity is operational, not cosmetic.

- Avoid idioms such as “low-hanging fruit,” “move the needle,” “deep dive,” “red flag,” “silver bullet,” and “boots on the ground.”
- Avoid phrasal verbs when a direct verb is clearer: use “expand,” “review,” “investigate,” and “begin.”
- Keep pronoun references unambiguous.
- Do not stack several qualifications inside one sentence.
- Use consistent terminology for National Society, station, water level, discharge, calibration, validation, and early warning.
- Expand acronyms on first use in each major standalone section.
- Put critical caveats in the main text, not only in footnotes.
- Have Teguh review meaning, institutional terminology, and cultural context rather than relying only on machine translation.

## 10. Anti-oppressive and locally led framing

- Treat Indonesian institutions and communities as knowledge holders and decision-makers.
- Do not equate international credentials with superior expertise.
- Attribute IPB, PMI, SIBAT, BHLK, and other Indonesian contributions specifically.
- Do not use “capacity building” as a one-directional claim; identify mutual learning and the capability or authority being developed.
- Distinguish community participation from community consent and governance.
- Examine who can access data and warnings, who may be excluded, and who carries maintenance or surveillance risk.
- Avoid language of pity, rescue, or passive beneficiaries.

## 11. Cost, maintenance, and sustainability

Tom's voice evaluates the whole system, not the purchase price.

Whenever stating a cost:

1. Define what is included.
2. List material exclusions.
3. Separate actual expenditure from estimates.
4. Identify recurring costs and institutional owners.
5. Address maintenance, replacement, power, connectivity, hosting, training, staff time, and end-of-life.

Preferred form:

> The Sukabumi electronics and enclosure bill totaled approximately USD 1,340. That figure excludes the existing solar panel and battery, survey, shipping, customs, travel, staff time, connectivity, hosting, maintenance, and replacement. It is a materials figure, not the cost of an operational monitoring service.

## 12. Open-source language

Open source should be framed as agency and inspectability, not as a guarantee of sustainability.

- Explain what is open and who maintains it.
- Credit upstream authors clearly.
- Acknowledge support, skills, version compatibility, hosting, and security maintenance.
- Do not claim the whole repository is formally open-licensed until TODO-202 is resolved.
- Connect openness to local adaptation and knowledge sharing without assuming every partner has equal time or technical resources to use it.

## 13. Opening and closing patterns

### Recommended opening pattern

Open with the shared problem, not a dramatic anecdote or a list of specifications:

> Flood and drought decisions depend on understanding how rivers behave. In many places, the local observations needed to build that understanding are sparse, difficult to maintain, or dangerous to collect during the events that matter most. Camera-based monitoring offers another way to observe a river. Our work in Indonesia showed both the promise of that approach and the partnerships required to make its data useful.

### Recommended closing pattern

Return to capable people and a practical next step:

> OpenRiverCam gave us a way to test the technology. The deployment gave PMI, IPB, BHLK, community volunteers, and the American Red Cross a reason to work across institutional boundaries. The next phase should begin with the river questions these partners need to answer together. The station may change. The relationships and shared capability are what can endure.

## 14. Whitepaper-specific editing checklist

### Mission and people

- [ ] Does each technical section explain the humanitarian or scientific decision it serves?
- [ ] Are Indonesian partner contributions named specifically?
- [ ] Do communities have agency rather than appearing only as recipients?
- [ ] Is technology consistently subordinate to the mission?

### Evidence and humility

- [ ] Is every number sourced and scoped?
- [ ] Are measured results separated from interpretations and future potential?
- [ ] Are failure causes labeled according to confidence?
- [ ] Does the paper state plainly that no humanitarian decision has yet used Sukabumi data?
- [ ] Is calibration fit kept separate from discharge accuracy?

### Style

- [ ] Does the argument follow problem → framework → approach → evidence → tradeoff → guidance?
- [ ] Are paragraphs short enough to remain readable?
- [ ] Are technical terms defined once in plain language?
- [ ] Have marketing language and generic enthusiasm been removed?
- [ ] Are recommendations practical and adaptable rather than universal directives?

### Translation and inclusion

- [ ] Are idioms and culture-specific metaphors removed?
- [ ] Are acronyms expanded and terminology consistent?
- [ ] Can each sentence be translated without resolving ambiguous pronouns?
- [ ] Are protection, access, and exclusion risks acknowledged?
- [ ] Has Teguh reviewed Indonesian meaning and institutional context?

## 15. Factual warning about the writing repository

The writing repository is authoritative for voice, not for OpenRiverCam project facts. Some audience guides contain stale or incorrect project biographical examples, including an October 2025 Indonesia date and a Delft University partnership. The current OpenRiverCam repository establishes an April 2026 deployment and names PMI, IPB, BHLK, and American Red Cross as partners. Use the source-note hierarchy for facts.
