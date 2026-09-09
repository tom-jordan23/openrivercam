# LiveOpenRiverCam API access — guide for IPB University

This guide describes how to read Sukabumi discharge and water-level data
programmatically. Written 2026-09-08 for LiveORC **v0.3.0**.

This directory contains everything required, and no credentials. Credentials
are supplied separately.

| | |
|---|---|
| **Base URL** | `https://openrivercam.endlessprojects.info` |
| **Institute id** | `1` |
| **Primary site** | `4` — Sukabumi City |
| **Auth** | JWT bearer token, from email + password |
| **Access** | Read-only across the whole institute |
| **Sample script** | [`fetch_timeseries.py`](fetch_timeseries.py) |

---

## 1. Credentials

One service account is issued to IPB. It is intended for use by software: the
credential should be stored in a dashboard server's configuration and read by
the application, rather than entered by a person.

- The login is an **email address**. It identifies the account, but no mail is
  delivered to it, and there is no password-reset function.
- Store the credential with the dashboard's other secrets. Please do not place
  it in a source repository, a notebook file, or a shared document.
- Please identify one person at IPB as responsible for where the credential is
  stored, and let us know who that is.
- **If another application later needs access** — a second dashboard, another
  research group, or a student project — please request a separate account
  rather than sharing this one. Additional accounts are straightforward for us
  to issue, whereas separating the activity of two applications sharing one
  credential is not possible afterwards.

The credentials are supplied separately and are not included in this document.

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
  token and invalidates the one submitted. Always store the token returned by
  each refresh; a previously used refresh token will be rejected.
- We recommend refreshing the token rather than re-sending the password, so
  that the password is read from as few places as possible.

## 3. Required parameter on the site list

`GET /api/site/` returns an **empty list** — not an error — unless you pass the
institute id:

```bash
# returns [] — an empty list, not an error
curl -H "Authorization: Bearer $TOKEN" .../api/site/

# returns the sites
curl -H "Authorization: Bearer $TOKEN" '.../api/site/?institute=1'
```

The institute id is **1**. The nested routes below (`/api/site/4/...`) do not
need it; only the top-level site list does.

## 4. Available data

These counts increase as the station uploads new data, so please treat them as
approximate. Site 4 held 2630 video records on 2026-08-25 and 2981 on
2026-09-09.

| Site | Name | Time series rows | Videos | Notes |
|---|---|---|---|---|
| **4** | Sukabumi City | 2526 | 2981 | **The active station**, measured 2026-09-09. Data from April 2026 onward. This is the primary dataset for the collaboration. |
| 2 | Test site | 1204 | 546 | Measured 2026-08-25. An earlier device that failed in 2025. Its video files were intentionally removed from the server, so video records exist without associated media files. The time series records remain valid. |
| 3 | — | 0 | 0 | Empty. |

## 5. Time series

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
| `site`, `creator`, `id` | Record identifiers | – |

Any of these fields may be `null`. Water level is present on some rows and
absent on others, so applications should handle missing values rather than
assume every field is populated.

**Timestamps are UTC.** Sukabumi local time is WIB, **UTC+7**. We recommend
converting to local time for display only, and storing the original UTC value.

### Query parameters

| Parameter | Effect |
|---|---|
| `startDateTime=<ISO 8601>` | Lower bound on `timestamp`, inclusive |
| `endDateTime=<ISO 8601>` | Upper bound on `timestamp`, inclusive |
| `fields=timestamp,h,q_50` | Return only these columns |
| `format=csv` | Return CSV instead of JSON |

Note that the two date filters use camelCase, unlike the other parameters in
the API.

All four parameters were confirmed against the server with this account on
**2026-09-09**. CSV columns are returned in **alphabetical order**
(`creator,fraction_velocimetry,h,id,misc,q_05,...`) rather than the order listed
above, so please select columns by name rather than by position.

**The endpoint is not paginated.** The complete matching set is returned in a
single response: 2526 rows was 1.0 MB on 2026-09-09. As the record grows, an
unbounded request will become progressively slower and larger.

We therefore recommend bounding queries by date and retrieving data
incrementally: store the most recent timestamp you have received, supply it as
`startDateTime` on the next request, and discard the duplicated first row (the
bounds are inclusive).

### Example request

```bash
TOKEN=$(curl -sS -X POST https://openrivercam.endlessprojects.info/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{"email":"'"$LIVEORC_EMAIL"'","password":"'"$LIVEORC_PASSWORD"'"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access"])')

curl -sS -H "Authorization: Bearer $TOKEN" \
  'https://openrivercam.endlessprojects.info/api/site/4/timeseries/?startDateTime=2026-08-01&endDateTime=2026-09-01&fields=timestamp,h,q_50'
```

Alternatively, use the sample script, which handles the token, the institute
id, the date bounds and CSV output:

```bash
export LIVEORC_EMAIL='<account>'
read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD

./fetch_timeseries.py --list-sites
./fetch_timeseries.py --site 4 --start 2026-08-01 --out sukabumi.csv
```

The script requires Python 3.9 or later and uses only the standard library, so
no packages need to be installed. It also serves as documentation: it is short,
and each behaviour described in this guide is commented at the point where the
script handles it.

A request that returns no new rows produces a CSV containing only the header
row, rather than an empty file, so that an incremental loader reads zero rows
instead of encountering a parse error.

`mock_liveorc.py`, included in this directory, serves the same response shapes
on `127.0.0.1:8731`. It was used to test the script before release, and allows
development without a credential or network access:

```bash
python3 mock_liveorc.py &
LIVEORC_BASE=http://127.0.0.1:8731 LIVEORC_EMAIL=any@example.local \
  LIVEORC_PASSWORD=any ./fetch_timeseries.py --site 4 --start 2026-08-08
```

## 6. Other endpoints

| Endpoint | Contents |
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

The three configuration endpoints contain the calibration information required
to reproduce the discharge values. Please refer to them if you need to verify
how a value was derived.

`/api/recipe/` and `/api/device/` return **empty lists** for this account. This
is the behaviour of LiveORC itself rather than a restriction on your permissions:
both endpoints filter by institute and then discard the result. Recipe and
device metadata are therefore not available over the API. Please contact us if
you need information from them.

## 7. Media

Video and image files are available only at the following routes:

| Asset | Route |
|---|---|
| video | `/api/site/4/video/{id}/playback/` |
| analysis image | `/api/site/4/video/{id}/image/` |
| thumbnail | `/api/site/4/video/{id}/thumbnail/` |
| keyframe | No route exists; not available over the API |

The `file`, `keyframe`, `image` and `thumbnail` URLs contained in a video record
point to `/media/...` and **return 404**, with or without a token. The media
files are held behind Django's storage layer and are not served from the web
server's filesystem. Please treat those URLs as identifiers rather than as
links.

> **Please do not bulk-download media.** Serving files through LiveORC uses
> considerably more server resources than transferring the same files by other
> means, and the server is a small instance. On 2026-08-25 an internal job that
> downloaded video through these routes exhausted the host's CPU allocation and
> caused a full service outage of approximately 90 minutes, after 773 files.
>
> Metadata and time series are inexpensive to retrieve and may be queried
> freely. Media files are not. Please request individual files as your users
> need them. If you require a bulk copy, please contact us and we will produce
> a server-side export instead.

## 8. Permissions of this account

The account is a member of institute 1 and is not the creator of any record.
Under LiveORC's permission model this means:

- **Read access** to all data belonging to the institute, across all three sites.
- `PATCH` and `DELETE` return **403** on every record.

Please note two further points:

- The account **is able to create** new records. This is a limitation of
  LiveORC itself rather than a permission we have granted, and it applies to
  any authenticated account. In particular, `POST /api/video/` uploads a file
  and may queue it for processing. Please do not send POST requests to the API.
  Doing so cannot damage existing data, but it creates unwanted records and
  additional load on a production server. If your integration requires write
  access, please tell us and we will agree a suitable approach.
- Access is determined by **institute membership**, which we configure manually.
  A `403` on a site you expected to be able to read indicates a membership
  setting rather than a fault in your code. Please tell us if this occurs.

## 9. Service horizon

The server is funded through the current grant, which ends **31 December 2026**.
American Red Cross is able to fund the AWS host beyond that date, and the
current plan is to continue **until approximately 31 March 2027**. Arrangements
after that date have not yet been decided.

Please take this into account before building on the API. A dashboard tied to
this hostname will need to be reconfigured when the server moves, so we
recommend keeping the base URL in configuration rather than in source code.
Please contact Tom before committing to any plan extending beyond the dates
above.

## 10. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `GET /api/site/` returns `[]` | Missing `?institute=1` |
| `401` on a request that previously succeeded | The access token is more than 6 hours old; refresh it |
| `401` from `/api/token/refresh/` | The refresh token has already been used. Tokens rotate; store the new one returned by each refresh |
| `403` on a nested site route | Not a member of that site's institute |
| `403` on `PATCH`/`DELETE` | Expected behaviour. The account is read-only |
| `404` on a `/media/...` URL | Expected behaviour. Use the `playback`, `image` or `thumbnail` routes |
| Empty `/api/recipe/` or `/api/device/` | Expected upstream behaviour |

For any other issue, please send us the request and the full response, and we
will investigate.
