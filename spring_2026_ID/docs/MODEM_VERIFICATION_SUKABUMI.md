# LTE Modem Verification — Sukabumi Station

**Applies to:** Sukabumi site (orc-sukabumi)
**Modem:** Quectel EC25 LTE (USB ID `2c7c:0125`, firmware `EG25GGBR07A08M2G`)
**Carrier:** Verizon Wireless (US bench testing) / Telkomsel (field deployment)
**Last verified:** 2026-03-25

---

## Contents

- [Prerequisites](#prerequisites)
- [Step 1: Install ModemManager](#step-1-install-modemmanager)
- [Step 2: Confirm USB Detection](#step-2-confirm-usb-detection)
- [Step 3: Confirm Device Nodes](#step-3-confirm-device-nodes)
- [Step 4: Verify with ModemManager](#step-4-verify-with-modemmanager)
- [Step 5: Verify with AT Commands](#step-5-verify-with-at-commands-alternative)
- [Step 6: Interpret Results](#step-6-interpret-results)
- [Step 7: Verify APN Configuration](#step-7-verify-apn-configuration)
- [Bench Test Baseline](#bench-test-baseline-2026-03-25)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

---

## Prerequisites

- User in `dialout` group (default for `pi`)
- `python3` with `pyserial` installed (`pip install pyserial`) — for AT
  command diagnostics
- ModemManager + libqmi-utils — for managed data connections (see
  installation below)

---

## Step 1: Install ModemManager

```bash
sudo apt-get update
sudo apt-get install -y modemmanager
```

This also pulls in `libqmi-glib5`, `libqmi-proxy`, `libqmi-utils`,
`libmbim-glib4`, `libmbim-proxy`, and `libmbim-utils`.

**Important:** If the modem was already plugged in before ModemManager was
installed, the udev rules won't have been applied yet. Retrigger them:

```bash
sudo udevadm trigger
sudo udevadm settle
sudo systemctl restart ModemManager
sleep 5
mmcli -L
```

ModemManager starts automatically on boot via systemd (`ModemManager.service`).

---

## Step 2: Confirm USB Detection

```bash
lsusb | grep -i quectel
```

**Expected:**
```
Bus 001 Device 003: ID 2c7c:0125 Quectel Wireless Solutions Co., Ltd. EC25 LTE modem
```

If the modem does not appear, check the EXVIST Mini PCIe-USB carrier board
and the USB cable from the carrier to the Pi.

---

## Step 3: Confirm Device Nodes

```bash
ls /dev/ttyUSB* /dev/cdc-wdm*
```

**Expected:**
```
/dev/cdc-wdm0
/dev/ttyUSB0
/dev/ttyUSB1
/dev/ttyUSB2
/dev/ttyUSB3
```

The EC25 exposes four serial ports and one QMI control interface:

| Device | Interface | Driver | Purpose |
|---|---|---|---|
| `/dev/ttyUSB0` | if #0 | option | QCDM/DIAG (ignored by MM) |
| `/dev/ttyUSB1` | if #1 | option | NMEA GPS data |
| `/dev/ttyUSB2` | if #2 | option | AT command port (primary) |
| `/dev/ttyUSB3` | if #3 | option | AT command port (secondary) |
| `/dev/cdc-wdm0` | if #4 | qmi_wwan | QMI control (used by MM for data) |
| `wwan0` | — | qmi_wwan | Network interface for data connection |

---

## Step 4: Verify with ModemManager

### List modems

```bash
mmcli -L
```

**Expected:**
```
/org/freedesktop/ModemManager1/Modem/0 [QUALCOMM INCORPORATED] QUECTEL Mobile Broadband Module
```

The modem index (0, 1, 2, etc.) can change across restarts. Use `mmcli -L`
to find the current index before running `mmcli -m <index>`.

### Full modem status

```bash
mmcli -m 0
```

Key fields to check:

| Field | Expected | Notes |
|---|---|---|
| `state` | `registered` | Modem sees a tower and is registered |
| `access tech` | `lte` | Connected via LTE |
| `signal quality` | > 30% | Usable signal |
| `registration` | `home` or `roaming` | Network registration status |
| `operator name` | `Verizon` / `Telkomsel` | Carrier name |
| `equipment id` | 15-digit IMEI | Needed for POSTEL registration in Indonesia |

### Signal details

```bash
mmcli -m 0 --signal-setup
mmcli -m 0 --signal-get
```

---

## Step 5: Verify with AT Commands (Alternative)

AT commands work regardless of whether ModemManager is installed. If MM is
running, it may hold the AT port — either stop MM first
(`sudo systemctl stop ModemManager`) or use this approach for diagnostics
when MM is not available.

The modem AT port requires **115200 baud**:

```python
import serial, time

def at_cmd(ser, cmd):
    ser.write((cmd + '\r\n').encode())
    time.sleep(1)
    return ser.read(ser.in_waiting or 1).decode(errors='replace').strip()

s = serial.Serial('/dev/ttyUSB2', 115200, timeout=2)

# Basic connectivity
print(at_cmd(s, 'AT'))           # Should return "OK"

# SIM status
print(at_cmd(s, 'AT+CPIN?'))     # Should return "+CPIN: READY"

# Network registration (circuit-switched)
print(at_cmd(s, 'AT+CREG?'))     # +CREG: 0,1 = registered home

# Network registration (EPS/LTE)
print(at_cmd(s, 'AT+CEREG?'))    # +CEREG: 0,1 = registered home

# Signal quality
print(at_cmd(s, 'AT+CSQ'))       # +CSQ: <rssi>,<ber>

# Operator info
print(at_cmd(s, 'AT+COPS?'))     # Shows carrier name and access tech

# Network details (Quectel-specific)
print(at_cmd(s, 'AT+QNWINFO'))   # Band and channel info

# Detailed signal (Quectel-specific)
print(at_cmd(s, 'AT+QCSQ'))     # RSSI, RSRP, SINR, RSRQ

# APN configuration
print(at_cmd(s, 'AT+CGDCONT?'))  # PDP context / APN list

s.close()
```

**Note:** `socat` at 9600 baud does **not** work with this modem — use
pyserial at 115200.

---

## Step 6: Interpret Results

### Registration Status (+CREG / +CEREG)

| Second digit | Meaning |
|---|---|
| 0 | Not registered, not searching |
| 1 | Registered, home network |
| 2 | Not registered, searching |
| 3 | Registration denied |
| 5 | Registered, roaming |

Both `+CREG` and `+CEREG` should show `,1` (or `,5` if roaming).

### Signal Quality (+CSQ)

| CSQ value | dBm (approx) | Quality |
|---|---|---|
| 0–9 | < -93 | Marginal |
| 10–14 | -93 to -83 | OK |
| 15–19 | -83 to -73 | Good |
| 20–31 | -73 to -51 | Excellent |
| 99 | Unknown | No signal |

### Detailed Signal (+QCSQ)

Format: `+QCSQ: "LTE",<rssi>,<rsrp>,<sinr>,<rsrq>`

| Metric | Good | Fair | Poor |
|---|---|---|---|
| RSRP (dBm) | > -90 | -90 to -110 | < -110 |
| SINR (dB x 10) | > 100 (10 dB) | 0–100 | < 0 |
| RSRQ (dB) | > -10 | -10 to -15 | < -15 |

### Access Technology (+COPS fourth digit)

| Value | Technology |
|---|---|
| 0 | GSM |
| 2 | UTRAN (3G) |
| 7 | E-UTRAN (LTE) |

---

## Step 7: Verify APN Configuration

For **Verizon** (US bench test), APNs are auto-provisioned. Expected
contexts include `VZWINTERNET`, `VZWADMIN`, `VZWAPP`, etc.

For **Telkomsel** (field deployment in Indonesia), set the APN manually:

```python
at_cmd(s, 'AT+CGDCONT=1,"IP","internet"')
```

Or via ModemManager:

```bash
mmcli -m 0 --simple-connect="apn=internet"
```

---

## Bench Test Baseline (2026-03-25)

### AT Command Results

```
AT+CPIN?    → +CPIN: READY
AT+CREG?    → +CREG: 0,1          (registered, home)
AT+CEREG?   → +CEREG: 0,1         (registered, home)
AT+CSQ      → +CSQ: 18,99         (good signal, ~-77 dBm)
AT+COPS?    → +COPS: 0,0,"Verizon Wireless",7   (LTE)
AT+QNWINFO → +QNWINFO: "FDD LTE","311480","LTE BAND 13",5230
AT+QCSQ    → +QCSQ: "LTE",78,-106,123,-14
              RSRP: -106 dBm (fair)
              SINR: 12.3 dB (decent)
              RSRQ: -14 dB (fair)
AT+CGDCONT? → 6 Verizon APNs auto-provisioned
```

### ModemManager Results

```
state:          registered
access tech:    lte
signal quality: 55% (cached)
operator:       Verizon (311480)
registration:   home
bands:          eutran-4, eutran-13
carrier config: hVoLTE-Verizon
IMEI:           868998082171881
firmware:       EG25GGBR07A08M2G
```

**Verdict:** Modem registered on Verizon LTE Band 13 with usable signal.
SIM ready, APNs provisioned, ready for data connection.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| `lsusb` doesn't show modem | Reseat mPCIe card in EXVIST carrier; check USB cable |
| No `/dev/ttyUSB*` devices | `dmesg \| grep -i usb` — look for errors; try different USB port |
| `mmcli -L` shows no modems | Run `sudo udevadm trigger && sudo udevadm settle && sudo systemctl restart ModemManager` |
| `AT` returns no response | Confirm baud rate is 115200; try `/dev/ttyUSB3` as alternate AT port |
| AT port busy / no response (MM running) | MM holds the port; stop it first: `sudo systemctl stop ModemManager` |
| `+CPIN: SIM NOT INSERTED` | Reseat SIM in the mPCIe carrier's SIM slot |
| `+CREG: 0,0` (not searching) | Send `AT+CFUN=1` to enable radio; check antenna connections |
| `+CREG: 0,2` (searching) | Wait 30s; if persistent, check antenna or try `AT+COPS=0` |
| `+CREG: 0,3` (denied) | SIM may need activation or IMEI registration with carrier |
| `+CSQ: 99,99` | No signal — check both MIMO antenna leads are connected |

---

## Notes

- The modem index in `mmcli -m <N>` can change across restarts. Always
  check `mmcli -L` first.
- When ModemManager is running, it manages the AT ports. To use AT commands
  directly, either stop MM or use the secondary port (`/dev/ttyUSB3`).
- The `wwan0` network interface appears when the QMI driver loads but
  carries no traffic until a bearer/connection is established through MM.
- The IMEI (`868998082171881`) will need to be registered with POSTEL
  (Indonesian telecom authority) before the Telkomsel SIM will work
  in-country.
