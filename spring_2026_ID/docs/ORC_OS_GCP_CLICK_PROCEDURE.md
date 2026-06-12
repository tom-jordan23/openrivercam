# ORC-OS GCP Click & Video-Config Procedure

A reusable, **coord-free** walkthrough for building a camera/video configuration
in the ORC-OS dashboard: clicking ground control points (GCPs), fitting the
camera pose, drawing the area-of-interest bounding box, and assigning
cross-sections.

Verified against the ORC-OS dashboard source (the per-video "Video Configuration"
view). Your **site-specific values** — GCP world coordinates, `z_0`/`h_ref`, which
transect is the water-level one, the calibration video filename — live in your
private survey handoff, **not here**. This document is the *method*; the *numbers*
stay private.

> Related: `VIDEO_CONFIG_SETUP.md` (higher-level deployment flow + survey prep),
> `survey/ORC_OS_DOCKER.md` (running ORC-OS locally in Docker for fitment).

---

## The model: video-first

In ORC-OS the camera config is **part of a per-video "Video Configuration"**. You
open a video first; everything (GCPs/pose, cross-sections, recipe) is built on
that page, and the video supplies the frame you click against. Frame width/height
come from the video automatically — there is no manual frame-size step.

1. Open the dashboard → **Videos** page.
2. Open your calibration video. This opens the **Video Configuration** page.
3. If the video already has a config and you want a clean start, click the
   **🗑 Delete video configuration** icon (top-right of "Manage configuration")
   and confirm. If this video is the config's reference video, that removes it +
   its dependencies and the page auto-creates a fresh empty config.

**Page layout:**
- **Left — "Image view":** *Camera view* (click GCP pixels + draw the bbox here)
  and *Top view*; a *Side view* sits bottom-right.
- **Right — "Manage configuration":** tabs run left→right in working order —
  **Name + details → Camera pose → Cross sections → Processing**. Later tabs stay
  **locked until prerequisites are met** (Camera pose needs a name; Cross sections
  needs a successful fit). Top-right: **💾 Save**, **▶ Run**, **🗑 Delete**.

---

## 1. "Name + details" tab

Give the config a traceable name. This unlocks the Camera pose tab.

---

## 2. "Camera pose" tab — GCPs + fit

Holds the **Control points** table (`Select | Row | Col | X | Y | Z | Delete`) and
the fit button.

**a. Load world coordinates.** Use the **"CSV or GeoJSON with x, y, z"** file
picker to load your GCP file (a CSV with an `x,y,z` header, or GeoJSON), and set
the **"Coordinate reference system"** field to your survey CRS. This fills X/Y/Z
for all points at once — no hand-typing of coordinates. (Alternatively, add points
one at a time with **"Click to add GCP"** and enter X/Y/Z per row.)

**b. Click the pixels.** For each row: hit **Select**, then click that marker on
the **Camera view** to set its **Row/Col**. Zoom/pan to place faint markers
precisely.

**c. Validate (= the fit).** Click **Validate**. It enables only once **≥6** points
have all of row/col/x/y/z. It reports **"average error: X m"** (the UI warns above
**0.10 m**). Set your own acceptance target (e.g. ≤ 0.05 m for a certified fit).

**d. Drop-and-refit.** If the error is high, **Delete** the worst point and
re-**Validate**. Keep all four image quadrants covered so the pose stays
well-constrained.

**Recommended click order** (coord-free strategy): seat the reliable, well-spread
anchors first; then the frame-edge / high-and-low points that constrain lens
distortion; then near-bank fill; then faint markers (zoom in); finally any
verify-only or hard-to-locate markers — keep those only if you can identify them
confidently.

> ⚠️ Editing/adding/deleting a GCP **resets the fit** (clears focal/distortion/
> pose) **and any bbox + cross-section links**. Finish the clicks and get a clean
> Validate *before* moving on — returning to this tab later means redoing the bbox
> and re-selecting cross-sections.

---

## 3. "Cross sections" tab — water level, bbox, transects

Unlocks **only after a successful Validate/fit**. Order inside it:

1. **Set water levels.** `z_0` = the water-surface elevation in the GCP coordinate
   system at calibration time. `h_ref` auto-defaults to `z_0` — leave it equal
   unless you process several videos against a separately-measured local gauge.
2. **Draw the bounding box** (the AOI on the water surface where PIV estimates
   velocities). The **"Draw bounding box"** button enables once `z_0` + pose are
   set. See "Choosing the bounding box" below.
3. **Upload + assign cross-sections.** **"Upload new"** → upload each transect as
   **GeoJSON** (not CSV — CSV loses the CRS). Then set the two dropdowns:
   **"Select discharge cross section"** (the one discharge is integrated over) and
   **"Select optical water level cross section"** (the transect on the structure/
   bank used to read water level optically). Confirm visually that each projects
   onto the frame where you expect (Camera/Top view).

### Choosing the bounding box

The AOI is the rectangle on the **water surface** that gets orthorectified and
where velocities are estimated. The discharge cross-section **must sit inside it**.

**Mechanic — 3 clicks** (the on-screen prompt says it too: *"First click left bank,
then right bank, then expand up and downstream"*):

1. **Left bank** — click the left waterline edge.
2. **Right bank** — click the right waterline edge. These first two clicks set the
   **width and orientation**: the box's cross-stream axis runs along this line, so
   its long axis ends up **streamwise**. Make the line roughly perpendicular to the
   flow.
3. **Expand up/downstream** — a third click sets the along-flow length; the box
   finalizes.

Because the box is defined in real-world space at the `z_0` surface, it renders as
a **trapezoid** on the camera image (perspective) — that's correct.

**Placement rules:**
- **Contain both transects** (discharge + optical-WL), with margin. Draw the bbox
  *after* assigning the cross-sections so you can see where they land.
- **Span the full potential flow width**, not just the current low-water stream —
  include bank/wall areas that inundate at high flow, so one config works across
  stages.
- **≥ ~2 m up and downstream** of the discharge transect to give PIV a run of
  surface to track features across — but don't overextend: a longer box at fixed
  recipe resolution = more grid cells (more memory/time) and the far end loses
  pixel resolution to perspective.
- **Stay on traceable water.** Exclude sky, vegetation, dry bank, deep shadow,
  glare, and static structures — non-water area adds noise and wastes resolution.

**Verify** in **Top view**: a clean rectangle covering the reach with both
transects inside. If it's skewed, tiny, or misses a transect, click **"Draw
bounding box"** again and redo the 3 clicks. (Re-drawing is cheap — but per the
caveat above, going back to the Camera pose tab to touch a GCP wipes the bbox.)

---

## 4. "Processing" tab, then Save + Run

1. **Processing tab:** review/adjust the recipe (frame range, resolution,
   interrogation window, etc.).
2. **Save:** click **💾 Save** to persist the whole video config. Edits also stream
   live as you work.
3. **Run:** the **▶ Run** icon enables once the config is ready to run (fitted +
   pose + bbox). Click it to process the video.

> **Historical "clobber" caveat.** An older, *standalone* CameraConfig dashboard
> form could rewrite the whole config blob on save and revert `h_ref` to 0. The
> current integrated video-config UI streams field-level edits and saves the whole
> config together, so it doesn't bite the same way. Still: after saving, confirm
> the processing log reports the water level was set (e.g. `Water level set to
> <z_0> m.`) rather than `Running without water level…`, which means `h_ref`
> didn't persist.

---

## Verify the result

- Processing log shows the water level was applied (not "running without water
  level").
- The resulting time-series row has a **non-zero discharge** (a config with
  placeholder/low-quality pixel clicks can yield q=0 — an input-quality artifact,
  not a config error).
- The velocity-field plot (`plot_quiver.jpg` in the video's output dir) looks
  physically sane.
