# RC-Box Design Specification Diagrams

Companion diagrams for DESIGN_SPECS.md. Render Mermaid diagrams using a compatible viewer (GitHub, VS Code with Mermaid extension, mermaid.live, etc.)

---

## System Architecture Overview

High-level view of all RC-Box components and their relationships.

```mermaid
flowchart TB
    subgraph External["External Systems"]
        SUN["☀️ Solar Panel<br/>50-200W"]
        CLOUD["☁️ Cloud/ORC Server"]
        SENSOR["📊 Commercial Sensors<br/>(Modbus RTU)"]
    end

    subgraph Power["Power System"]
        MPPT["MPPT Charge<br/>Controller"]
        BATT["LiFePO4 Battery<br/>20-100Ah"]
        FUSE1["20A Fuse"]
        TB12V["12V Terminal<br/>Block"]
        DCDC["DC-DC Buck<br/>Converter"]
        FUSE2["5A Polyfuse"]
    end

    subgraph Compute["Compute System"]
        WITTY["Witty Pi 4<br/>(RTC/Power Mgmt)"]
        PI["Raspberry Pi 5"]
        SSD["512GB+ SSD"]
        MODEM["4G Cellular<br/>Modem"]
    end

    subgraph Cameras["Camera System"]
        CAM1["📷 Camera 1<br/>IP67/IP68 Sealed"]
        CAM2["📷 Camera 2<br/>IP67/IP68 Sealed"]
    end

    subgraph IRSystem["IR Spotlight System"]
        USBRELAY["5V USB Relay"]
        PHOTORELAY["Photoresistor<br/>Relay Module"]
        IR["💡 IR Spotlight<br/>20-30W 850nm"]
    end

    subgraph Sensors["Sensor Interface"]
        RS485["USB-RS485<br/>Adapter"]
        TERMBLK["Terminal Block<br/>A+ B- GND 12V"]
    end

    subgraph Security["Anti-Theft System"]
        TAMPER["Tamper Switch<br/>(N.C.)"]
        VIBRATION["Vibration Sensor"]
        ALARM["Alarm Controller"]
        SIREN["🔊 120dB Siren"]
    end

    %% Power flow
    SUN --> MPPT
    MPPT --> BATT
    BATT --> FUSE1
    FUSE1 --> TB12V
    TB12V --> DCDC
    DCDC --> FUSE2
    FUSE2 --> WITTY
    WITTY --> PI

    %% Compute connections
    PI --> SSD
    PI --> MODEM
    MODEM --> CLOUD

    %% Camera connections
    PI -->|USB| CAM1
    PI -->|USB| CAM2

    %% IR system
    PI -->|USB 5V| USBRELAY
    TB12V --> PHOTORELAY
    USBRELAY -->|Enable| PHOTORELAY
    PHOTORELAY --> IR

    %% Sensor interface
    PI -->|USB| RS485
    RS485 --> TERMBLK
    TB12V -->|12V| TERMBLK
    TERMBLK --> SENSOR

    %% Security
    TB12V --> ALARM
    TAMPER --> ALARM
    VIBRATION --> ALARM
    ALARM --> SIREN
```

---

## Power System Detail

Detailed view of power flow from solar panel to all loads.

```mermaid
flowchart LR
    subgraph Solar["Solar Input"]
        PANEL["Solar Panel<br/>50-200W<br/>18V nominal"]
        MC4P["MC4+"]
        MC4N["MC4-"]
    end

    subgraph Protection["Input Protection"]
        SURGE1["DC Surge<br/>Protector"]
    end

    subgraph Charging["Charge System"]
        MPPT["MPPT Controller<br/>10-30A"]
        BATT["LiFePO4<br/>12V 20-100Ah"]
    end

    subgraph Distribution["Power Distribution"]
        FUSE_MAIN["Fuse 20A"]
        TB["Terminal Block<br/>12V Distribution"]
    end

    subgraph Loads["12V Loads"]
        IR["IR Spotlight<br/>20-30W"]
        SENSOR_PWR["Sensor Power<br/>1-3W"]
        ALARM_PWR["Alarm System<br/>0.1W standby"]
    end

    subgraph FiveVolt["5V System"]
        DCDC["DC-DC Buck<br/>12V → 5V<br/>5A capable"]
        POLYFUSE["5A Polyfuse"]
        PI_PWR["To Pi 5<br/>via GPIO"]
    end

    PANEL --> MC4P & MC4N
    MC4P & MC4N --> SURGE1
    SURGE1 --> MPPT
    MPPT <--> BATT
    BATT --> FUSE_MAIN
    FUSE_MAIN --> TB

    TB --> IR
    TB --> SENSOR_PWR
    TB --> ALARM_PWR
    TB --> DCDC
    DCDC --> POLYFUSE
    POLYFUSE --> PI_PWR
```

---

## IR Spotlight Control Logic

Two-stage control using commodity relay modules.

```mermaid
flowchart TB
    subgraph Inputs["Control Inputs"]
        PI_USB["Pi USB Port<br/>(5V when awake)"]
        DAYLIGHT["Ambient Light<br/>(photoresistor)"]
    end

    subgraph Stage1["Stage 1: Pi Power State"]
        RELAY1["5V USB Relay<br/>(N.O. contacts)"]
        STATE1{"Pi Awake?"}
    end

    subgraph Stage2["Stage 2: Light Level"]
        PHOTO["Photoresistor<br/>Relay Module"]
        STATE2{"Dark Outside?"}
    end

    subgraph Output["Output"]
        IR["IR Spotlight<br/>20-30W"]
    end

    subgraph Truth["Logic Truth Table"]
        TABLE["| Pi | Light | IR |<br/>|OFF| Day  | OFF|<br/>|OFF|Night | OFF|<br/>| ON| Day  | OFF|<br/>| ON|Night | ON |"]
    end

    PI_USB --> RELAY1
    RELAY1 --> STATE1
    STATE1 -->|Yes| PHOTO
    STATE1 -->|No| OFF1["IR OFF"]

    DAYLIGHT --> PHOTO
    PHOTO --> STATE2
    STATE2 -->|Yes| IR
    STATE2 -->|No| OFF2["IR OFF"]
```

---

## Configuration A: Two-Box System

Physical layout showing separate compute and power enclosures.

```mermaid
flowchart TB
    subgraph External["External Components"]
        SOLAR["Solar Panel<br/>Pole/Roof Mount"]
        ANT["Cellular Antenna<br/>External"]
        CAM1["Camera 1<br/>Adjustable Mount"]
        CAM2["Camera 2<br/>Adjustable Mount"]
        IR["IR Spotlight"]
        GROUND["Ground Rod"]
    end

    subgraph PowerBox["Power Enclosure (Box 2)<br/>IP67 ~300x250x150mm"]
        direction TB
        MPPT2["MPPT Controller"]
        BATT2["LiFePO4 Battery"]
        TB2["Terminal Blocks"]
        FUSES2["Fuses"]
        VENT2["GORE Vent"]
    end

    subgraph ComputeBox["Compute Enclosure (Box 1)<br/>IP67 ~200x150x100mm"]
        direction TB
        PI2["Raspberry Pi 5"]
        WITTY2["Witty Pi 4"]
        MODEM2["4G Modem"]
        SSD2["SSD Storage"]
        VENT1["GORE Vent"]
    end

    %% Connections
    SOLAR -->|"MC4 cables<br/>M20 glands"| PowerBox
    PowerBox -->|"12V DC cable<br/>M20 gland"| ComputeBox
    ComputeBox -->|"USB cables<br/>M16 glands"| CAM1 & CAM2
    ComputeBox -->|"SMA bulkhead<br/>M12"| ANT
    PowerBox -->|"12V power<br/>M16 gland"| IR
    PowerBox -->|"Ground wire<br/>M16 gland"| GROUND
```

---

## Configuration B: Combined Single-Box System

All components in one enclosure.

```mermaid
flowchart TB
    subgraph External["External Components"]
        SOLAR2["Solar Panel"]
        ANT2["Cellular Antenna"]
        CAM3["Camera 1"]
        CAM4["Camera 2"]
        IR2["IR Spotlight"]
        GROUND2["Ground Rod"]
        SENSOR2["Modbus Sensors"]
    end

    subgraph CombinedBox["Combined Enclosure<br/>IP67 ~400x300x200mm"]
        subgraph PowerSection["Power Section"]
            MPPT3["MPPT Controller"]
            BATT3["LiFePO4 Battery"]
            TB3["12V Terminal Block"]
        end

        subgraph ComputeSection["Compute Section"]
            PI3["Raspberry Pi 5"]
            WITTY3["Witty Pi 4"]
            MODEM3["4G Modem"]
            SSD3["SSD"]
            RS485_3["USB-RS485"]
        end

        VENT3["GORE Vent"]
        DIVIDER["Optional Thermal<br/>Divider"]
    end

    SOLAR2 -->|"M20 glands"| CombinedBox
    CombinedBox -->|"M16 USB glands"| CAM3 & CAM4
    CombinedBox -->|"M12 SMA"| ANT2
    CombinedBox -->|"M16 gland"| IR2
    CombinedBox -->|"M16 gland"| GROUND2
    CombinedBox -->|"M16 gland"| SENSOR2
```

---

## Sensor Integration

Connection of commercial Modbus sensors.

```mermaid
flowchart LR
    subgraph RCBox["RC-Box"]
        PI4["Raspberry Pi 5"]
        USB["USB Port"]
        RS485["USB-RS485<br/>Adapter"]
        TB4["Terminal Block<br/>A+ B- GND 12V"]
        PWR["12V from<br/>Battery"]
    end

    subgraph Bus["RS485 Bus<br/>(up to 1200m)"]
        WIRE["4-wire Shielded<br/>Cable"]
    end

    subgraph Sensors["Commercial Sensors"]
        RAIN["Rain Gauge<br/>Addr: 1"]
        WEATHER["Weather Station<br/>Addr: 2"]
        LEVEL["Water Level<br/>Addr: 3"]
    end

    PI4 --> USB
    USB --> RS485
    RS485 --> TB4
    PWR --> TB4
    TB4 --> WIRE
    WIRE --> RAIN & WEATHER & LEVEL
```

---

## Anti-Theft System

Security sensor chain with fail-secure design.

```mermaid
flowchart TB
    subgraph Power["Power"]
        BATT4["12V Battery"]
        FUSE4["2A Fuse"]
    end

    subgraph Sensors["Sensors (N.C. Chain)"]
        TAMPER2["Tamper Switch<br/>Lid Opening"]
        VIB["Vibration Sensor<br/>Cutting/Prying"]
        TILT["Tilt Sensor<br/>Pole Removal"]
    end

    subgraph Controller["Alarm Controller"]
        CTRL["Latching Relay<br/>or Smart Module"]
        RESET["Key Switch<br/>(Reset)"]
    end

    subgraph Alert["Alert Devices"]
        SIREN2["120dB Siren"]
        STROBE["Strobe Light"]
    end

    subgraph Logic["Fail-Secure Logic"]
        NOTE["All sensors N.C.<br/>Wired in series<br/>↓<br/>Cut wire = ALARM<br/>Open sensor = ALARM<br/>Only closed chain = OK"]
    end

    BATT4 --> FUSE4
    FUSE4 --> CTRL
    TAMPER2 --> VIB
    VIB --> TILT
    TILT --> CTRL
    CTRL --> SIREN2 & STROBE
    RESET --> CTRL
```

---

## Data Flow

How data moves through the system.

```mermaid
flowchart LR
    subgraph Capture["Data Capture"]
        CAM5["Cameras<br/>(Video)"]
        SENS["Sensors<br/>(Time Series)"]
    end

    subgraph Local["Local Processing"]
        PI5["Raspberry Pi 5"]
        SSD4["Local SSD<br/>512GB+"]
    end

    subgraph Schedule["Power Schedule"]
        WAKE["Wake 2-3 min"]
        RECORD["Record Video"]
        LOG["Log Sensors"]
        UPLOAD["Upload Data"]
        SLEEP["Sleep 12-13 min"]
    end

    subgraph Remote["Remote Systems"]
        CELL["4G Cellular"]
        ORC["ORC Cloud<br/>Server"]
    end

    CAM5 --> PI5
    SENS --> PI5
    PI5 --> SSD4
    PI5 --> CELL
    CELL --> ORC

    WAKE --> RECORD --> LOG --> UPLOAD --> SLEEP
    SLEEP -->|"Repeat"| WAKE
```

---

## Enclosure Sealing Detail

Cable gland and environmental protection.

```mermaid
flowchart TB
    subgraph Enclosure["IP67 Enclosure"]
        subgraph Top["Top Surface"]
            VENT5["GORE Vent<br/>M12<br/>Pressure Equalization"]
        end

        subgraph Walls["Wall Penetrations"]
            G1["M20 Gland<br/>Solar MC4+"]
            G2["M20 Gland<br/>Solar MC4-"]
            G3["M16 Gland<br/>USB Camera 1"]
            G4["M16 Gland<br/>USB Camera 2"]
            G5["M12 SMA<br/>Cellular Antenna"]
            G6["M16 Gland<br/>Ground Wire"]
            G7["M16 Blank<br/>Spare"]
        end

        subgraph Sealing["Sealing Requirements"]
            REQ["All glands: IP68<br/>Thread sealant: Silicone<br/>Max gap: 0.5mm<br/>Gasket: Inspect before closing"]
        end
    end

    subgraph Protection["Environmental Protection"]
        ANT_PROOF["Ant-Proof<br/>(no gaps >0.5mm)"]
        DUST["Dust-Tight<br/>(IP6x)"]
        WATER["Waterproof<br/>(IPx7 - 1m/30min)"]
    end
```

---

## Deployment Topology

Typical installation showing physical arrangement.

```mermaid
flowchart TB
    subgraph Site["River Monitoring Site"]
        subgraph Pole["Mounting Pole<br/>3-6 inch diameter"]
            ENCLOSURE["RC-Box Enclosure<br/>(1.5-2m height)"]
            PANEL_MOUNT["Solar Panel<br/>(above enclosure)"]
        end

        subgraph CameraArm["Camera Mounting"]
            ARM1["Adjustable Arm 1"]
            ARM2["Adjustable Arm 2"]
            C1["Camera 1<br/>Upstream View"]
            C2["Camera 2<br/>Downstream View"]
        end

        subgraph Lighting["IR Illumination"]
            IR_MOUNT["IR Spotlight<br/>Covers full width"]
        end

        subgraph Ground["Ground Level"]
            GROD["Ground Rod<br/>8ft copper"]
            RIVER["River<br/>(up to 30m wide)"]
        end

        subgraph Optional["Optional Sensors"]
            RAIN_GAUGE["Rain Gauge<br/>(1m above ground)"]
            WX["Weather Station"]
        end
    end

    PANEL_MOUNT --> ENCLOSURE
    ENCLOSURE --> ARM1 & ARM2
    ARM1 --> C1
    ARM2 --> C2
    ENCLOSURE --> IR_MOUNT
    ENCLOSURE --> GROD
    C1 & C2 -.->|"View"| RIVER
    IR_MOUNT -.->|"Illuminates"| RIVER
```
