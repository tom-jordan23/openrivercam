# LiveOpenRiverCam API access — guide for IPB University

Everything needed to read Sukabumi discharge and water-level data
programmatically. Written 2026-09-08 for LiveORC **v0.3.0**.

This directory is self-contained and is what gets sent to IPB. It contains no
credentials.

| | |
|---|---|
| **Base URL** | `https://openrivercam.endlessprojects.info` |
| **Institute id** | `1` |
| **Site of interest** | `4` — Sukabumi City |
| **Auth** | JWT bearer token, from email + password |
| **Access** | Read-only across the whole institute |
| **Sample script** | [`fetch_timeseries.py`](fetch_timeseries.py) |

---

## 1. Credentials

One service account is issued to IPB. It is a **machine credential**: it is
meant to live in a dashboard server's configuration and be read by software,
not typed by a person.

- The login is an **email address**, and it is the account's identity even
  though no mail is delivered to it. There is no password-reset flow.
- Store it wherever the dashboard's other secrets live. Not in a git
  repository, not in a notebook, not in a shared document.
- Name one person at IPB who is responsible for where it is stored, and tell
  us who that is.
- **If a second, differently-scoped consumer appears** — another dashboard,
  another group, a student project — ask for a second account rather than
  sharing this one. Issuing accounts is cheap; untangling one shared
  credential later is not.

The credentials themselves arrive separately, not through this document.

## 2. Authentication

```bash
curl -sS -X POST https://openrivercam.endlessprojects.info/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "<account>", "password": "<password>"}'
```

Returns:

```json
{"access": "eyJhbGci...", "refresh": "eyJhbGci..."}
```

Send the access token as `Authorization: Bearer <access>` on every subsequent
request.

- The **access token is valid for 6 hours**. Any job running longer than that
  must refresh mid-run.
- Renew with `POST /api/token/refresh/` and `{"refresh": "<refresh>"}`.
- **Refresh tokens rotate.** The refresh response contains a *new* refresh
  token and invalidates the one you sent. Always store what comes back — reusing
  a spent refresh token fails.
- Prefer refreshing over re-sending the password. The fewer places the password
  is read from, the better.

## 3. The one gotcha that wastes an afternoon

`GET /api/site/` returns an **empty list** — not an error — unless you pass the
institute id:

```bash
# returns []  — looks like an empty server
curl -H "Authorization: Bearer $TOKEN" .../api/site/

# returns the sites
curl -H "Authorization: Bearer $TOKEN" '.../api/site/?institute=1'
```

The institute id is **1**. The nested routes below (`/api/site/4/...`) do not
need it; only the top-level site list does.

## 4. What is there

The record grows as the station uploads, so treat these as a scale, not a
constant — site 4 held 2630 video records on 2026-08-25 and 2981 two weeks later.

| Site | Name | Time series rows | Videos | Notes |
|---|---|---|---|---|
| **4** | Sukabumi City | 2526 | 2981 | **The live station**, measured 2026-09-09. April 2026 onward. This is the data you want. |
| 2 | Test site | 1204 | 546 | Measured 2026-08-25. A prior device that failed in 2025. Its video files were deliberately removed from the server, so video records exist with no media behind them. Time series are real. |
| 3 | — | 0 | 0 | Empty. |

## 5. Time series — the endpoint that matters

```
GET /api/site/4/timeseries/
```

Each row is one measurement:

| Field | Meaning | Unit |
|---|---|---|
| `timestamp` | Date and time of the value | ISO 8601, **UTC** |
| `h` | Water level against the local datum | m |
| `q_05`, `q_25`, `q_50`, `q_75`, `q_95` | Discharge at 5/25/50/75/95% probability of non-exceedance. `q_50` is the median. | m³/s |
| `q_raw` | Discharge measured optically, before the probabilistic treatment | m³/s |
| `v_av` | Average surface velocity | m/s |
| `v_bulk` | Bulk velocity | m/s |
| `wetted_surface` | Wetted cross-sectional area at that level | m² |
| `wetted_perimeter` | Wetted perimeter at that level | m |
| `fraction_velocimetry` | Fraction of discharge resolved by velocimetry | – |
| `misc` | Free-form JSON from the processing chain | – |
| `video` | Id of the video this was derived from, if any | – |
| `site`, `creator`, `id` | Record keeping | – |

Any of these may be `null`. Water level in particular is present on some rows
and not others, so a dashboard should tolerate gaps rather than assume them.

**Timestamps are UTC.** Sukabumi local time is WIB, **UTC+7**. Convert on
display; do not store the converted value.

### Useful query parameters

| Parameter | Effect |
|---|---|
| `startDateTime=<ISO 8601>` | Lower bound on `timestamp`, inclusive |
| `endDateTime=<ISO 8601>` | Upper bound on `timestamp`, inclusive |
| `fields=timestamp,h,q_50` | Return only these columns |
| `format=csv` | Return CSV instead of JSON |

The two date filters are **camelCase**, unlike everything else in the API.

All four are confirmed against the running server with this account on
**2026-09-09**: the date bounds filter, `fields` trims, and `format=csv` switches
the renderer. CSV columns come back in **alphabetical order**
(`creator,fraction_velocimetry,h,id,misc,q_05,...`), not the order listed above,
so select columns by name rather than by position.

**The endpoint is not paginated.** The full matching set comes back in one
response — 2526 rows was 1.0 MB on 2026-09-09. That is convenient now and will
stop being convenient later,
so bound your queries by date and pull incrementally: keep the newest timestamp
you hold, pass it as `startDateTime` next time, and drop the duplicate first row.

### Worked example

```bash
TOKEN=$(curl -sS -X POST https://openrivercam.endlessprojects.info/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"email":"'"$LIVEORC_EMAIL"'","password":"'"$LIVEORC_PASSWORD"'"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access"])')

curl -sS -H "Authorization: Bearer $TOKEN" \
  'https://openrivercam.endlessprojects.info/api/site/4/timeseries/?startDateTime=2026-08-01&endDateTime=2026-09-01&fields=timestamp,h,q_50'
```

Or use the sample script, which handles the token, the institute id, the date
bounds and CSV output:

```bash
export LIVEORC_EMAIL='<account>'
read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD

./fetch_timeseries.py --list-sites
./fetch_timeseries.py --site 4 --start 2026-08-01 --out sukabumi.csv
```

It is standard-library Python 3.9+, so it needs no `pip install`. Read it as
documentation as much as tooling — it is short, and every awkward part of the
API is commented where it is handled.

## 6. The rest of the surface

| Endpoint | Gives you |
|---|---|
| `/api/site/?institute=1` | Site list: id, name, coordinates |
| `/api/site/4/timeseries/` | The measurements, as above |
| `/api/site/4/video/` | Video records: `timestamp`, `status`, `video_config`, `time_series`, and asset URLs |
| `/api/site/4/video/{id}/` | One video record |
| `/api/site/4/cameraconfig/` | Camera calibration |
| `/api/site/4/crosssection/` | Surveyed cross-section |
| `/api/site/4/videoconfig/` | Video processing configuration |
| `/api/version/` | Server version; needs no authentication |
| `/api/schema/` | Full OpenAPI 3.0.3 spec; **needs no authentication** |

The three configuration endpoints carry what makes the discharge numbers
reproducible. If you want to check how a value was derived, they are where to
look.

`/api/recipe/` and `/api/device/` return **empty lists** for this account. That
is upstream behaviour, not a permission problem — both endpoints filter on
institute and then discard the result. Recipe and device metadata are simply not
available over the API. Ask us if you need something from them.

## 7. Media, and why to leave it alone

Video and image bytes are reachable, at these routes only:

| Asset | Route |
|---|---|
| video | `/api/site/4/video/{id}/playback/` |
| analysis image | `/api/site/4/video/{id}/image/` |
| thumbnail | `/api/site/4/video/{id}/thumbnail/` |
| keyframe | no route exists — unreachable over the API |

The `file`, `keyframe`, `image` and `thumbnail` URLs in a video record point at
`/media/...` and **return 404** with or without a token. Media is behind
Django's storage API and was never on the web server's filesystem. Treat those
URLs as identifiers, not as links.

> **Do not bulk-download media.** Serving files through LiveORC is expensive per
> byte in a way that copying them is not, and the server is a small instance.
> On 2026-08-25 an internal job pulling video through these routes exhausted the
> host's CPU budget and took the whole service down for about 90 minutes after
> 773 files. Metadata and time series are cheap and you can pull them freely;
> media is not. Fetch individual clips when a person asks for one. If you need a
> bulk copy, ask us and we will export it server-side instead.

## 8. What this account cannot do

It is a member of institute 1, and it created none of the records. Under
LiveORC's permission model that means:

- **Read** everything belonging to the institute — all three sites.
- `PATCH` and `DELETE` return **403** on every record, always.

Two things to be aware of:

- It **can** create new records — this is a gap in LiveORC itself, not a
  permission we granted, and it applies to any authenticated account. Notably
  `POST /api/video/` uploads a file and can enqueue processing. Please do not
  post to the API. It cannot damage existing data, but it adds clutter and load
  to a production server. If your integration needs to write, tell us and we
  will work out the right shape for it.
- Access is bounded by **institute membership**, which is set by hand on our
  side. A `403` on a site you expected to read means membership, not a bug —
  tell us.

## 9. Service horizon

The server is funded through the current grant, which ends **31 December 2026**.
American Red Cross can carry the AWS host beyond that, and the working plan is
**to roughly 31 March 2027**. Where it lives after that is an open decision.

This is worth knowing before you build on it. A dashboard tied to this
hostname will need repointing when the server moves, so keep the base URL in
configuration rather than in code, and talk to Tom before committing to
anything with a longer horizon than the above.

## 10. When something does not work

| Symptom | Likely cause |
|---|---|
| `GET /api/site/` returns `[]` | Missing `?institute=1` |
| `401` on a request that worked earlier | Access token older than 6 hours; refresh it |
| `401` from `/api/token/refresh/` | Refresh token already spent — they rotate; store the new one each time |
| `403` on a nested site route | Not a member of that site's institute |
| `403` on `PATCH`/`DELETE` | Expected. The account is read-only |
| `404` on a `/media/...` URL | Expected. Use the `playback`/`image`/`thumbnail` routes |
| Empty `/api/recipe/` or `/api/device/` | Expected upstream behaviour |

Anything else, send us the request and the full response and we will look.
