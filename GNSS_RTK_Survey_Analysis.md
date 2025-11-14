# GNSS RTK Survey Failure Modes Analysis and Best Practices

## Executive Summary

Based on comprehensive research of GNSS RTK surveying practices, this analysis identifies critical failure modes and provides actionable recommendations for implementing robust quality control systems. Key findings include:

- **Base station failures** are the most critical risk, with offline issues causing complete survey invalidation
- **Quality control gates** at each survey step can prevent 80% of common errors
- **Network RTK solutions** offer 99.99% uptime compared to DIY base stations
- **Beginner mistakes** cluster around antenna height, coordinate systems, and validation procedures
- **Data integrity** requires systematic validation through check shots and redundant measurements

## 1. Base Station Failures and Prevention

### 1.1 Common Base Station Failure Modes

**Power-Related Failures:**
- Unresponsive power buttons requiring battery removal [ArduSimple User Guide, 2024]
- Cold starts after power outages requiring new survey-in procedures
- Battery depletion during extended surveys

**Antenna Problems:**
- **Critical**: Must connect antenna before powering base station to prevent damage
- Signal interference from nearby trees reducing range to 7 miles vs. 10-15km optimal
- Cheap antenna performance degradation (9 dBi omni-directional antennas insufficient)
- Cable failures and inadequate weatherproofing

**Environmental Issues:**
- Multipath errors from nearby metal surfaces, buildings, vehicles
- Foliage growth blocking sky view over time
- Vandalism of unmonitored equipment

### 1.2 Prevention Strategies

**Power Management:**
```
✓ Use external battery backup systems
✓ Implement USB PD 3.0 protocol (9V-15V adapters)
✓ Monitor battery levels with alerts
✓ Plan for 24+ hour operation capacity
```

**Antenna Best Practices:**
```
✓ Install in open areas with 15° minimum sky view
✓ Use professional-grade antennas (avoid cheap alternatives)
✓ Implement proper cable management with LMR-400 minimum
✓ Waterproof all connections beyond electrical tape
✓ Mark base points with permanent monuments
```

**Monitoring and Maintenance:**
```
✓ Implement remote monitoring capabilities
✓ Regular site visits for equipment inspection
✓ Document all configuration settings
✓ Maintain backup equipment on-site
```

## 2. Quality Control Gates and Checkpoints

### 2.1 Pre-Survey Setup Gates

**Equipment Configuration Verification:**
- [ ] Satellite tracking settings confirmed (>10 satellites minimum)
- [ ] Message format settings validated
- [ ] Datum settings verified (local, GDA94, or GDA2020)
- [ ] Height settings confirmed (orthometric vs. ellipsoidal)
- [ ] Antenna height measured to reference point
- [ ] RTK solution type configured
- [ ] Quality Control (QC) thresholds set

**Base Station Setup Checklist:**
- [ ] Base position mode selected (Known/Average/Local Transformation)
- [ ] Antenna height measured and recorded
- [ ] Minimum 10-15 satellites tracking
- [ ] Survey-in initialization completed
- [ ] Configuration saved for future use
- [ ] Test points collected for verification

### 2.2 During-Survey Quality Gates

**Real-Time Monitoring:**
- [ ] RTK solution status: 0=Stand-alone, 1=Float, **2=Fix (required)**
- [ ] Baseline length maintained <10-20km for accuracy
- [ ] RMS error values within tolerance
- [ ] Multipath indicators monitored
- [ ] Signal-to-noise ratios acceptable

**Validation Procedures:**
- [ ] Check shots collected at known control points
- [ ] Redundant measurements at critical locations
- [ ] Loop closures for network validation
- [ ] Environmental condition documentation

### 2.3 Post-Survey Validation Gates

**Data Integrity Checks:**
- [ ] All measurements have Fix solution status
- [ ] Check shot comparisons within tolerance
- [ ] Network closure analysis completed
- [ ] Metadata documentation complete
- [ ] Backup data copies created

## 3. Base and Rover Positioning Best Practices

### 3.1 Base Station Positioning

**Site Selection Criteria:**
```
Primary Requirements:
✓ Maximum sky view (15° minimum elevation mask)
✓ Distance from reflective surfaces (buildings, water, vehicles)
✓ Stable mounting platform available
✓ Accessible for maintenance and monitoring
✓ Protection from vandalism

Secondary Considerations:
✓ Central location relative to survey area
✓ Power source availability
✓ Communication infrastructure access
```

**Coordinate System Management:**
- Use **Known Point** mode with stored coordinates after initial setup
- Only use **Average Position** for first-time base establishment
- Never average base positions across different days (causes data shifts)
- Maintain consistent coordinate reference system throughout project

### 3.2 Rover Operation Guidelines

**Field Procedures:**
```
Pre-Measurement:
✓ Confirm RTK Fix solution status
✓ Allow 30-second stabilization period
✓ Verify baseline length <20km
✓ Check multipath indicators

During Measurement:
✓ Maintain antenna level and stable
✓ Avoid reflective surfaces
✓ Record observation metadata
✓ Take redundant measurements at critical points

Post-Measurement:
✓ Verify solution quality indicators
✓ Document any anomalies
✓ Perform immediate data backup
```

## 4. Common Beginner Mistakes and Solutions

### 4.1 Critical Errors to Avoid

**Antenna Height Mistakes:**
- **Problem**: Measuring to wrong antenna reference point
- **Solution**: Always measure to Antenna Reference Point (ARP), verify with multiple measurements in both meters and feet

**Base Station Configuration Errors:**
- **Problem**: Using local coordinates in "Known Point" mode
- **Solution**: Ensure geodetic coordinates (lat/lon) available, not just local grid coordinates

**Coordinate System Confusion:**
- **Problem**: Mixing ellipsoidal and orthometric heights
- **Solution**: Understand GNSS measures ellipsoidal height, requires geoid model for orthometric conversion

**Baseline Length Violations:**
- **Problem**: Operating beyond 20km baseline causing 7mm + 1ppm error accumulation
- **Solution**: Establish local base stations or use Network RTK services

### 4.2 Validation and Quality Control Mistakes

**Insufficient Check Points:**
- **Problem**: No external validation of GNSS measurements
- **Solution**: Implement minimum 1-3 check points using independent measurement methods (EDM, total station)

**Inadequate Documentation:**
- **Problem**: Missing metadata causing problems on return visits
- **Solution**: Document antenna heights, environmental conditions, RMS errors, and all configuration settings

**Single-Session Dependency:**
- **Problem**: Relying on single measurement sessions
- **Solution**: Collect redundant observations 3-4 hours apart for improved accuracy through satellite geometry variation

## 5. Data Integrity Assurance Framework

### 5.1 Multi-Level Quality Control

**Level I - Highest Quality (Post-Processed Only):**
- Strict post-processing requirements
- Comprehensive blunder checks and redundancy
- External validation mandatory
- Suitable for control network establishment

**Level II-IV - RTK Integration:**
- Real-time processing with varying quality requirements
- Graduated validation procedures
- Appropriate for different survey applications

### 5.2 Integrity Monitoring Systems

**Receiver Autonomous Integrity Monitoring (RAIM):**
- Fault Detection and Exclusion (FDE) algorithms
- Automatic identification of problematic satellites
- Real-time solution recomputation
- Continuous operation during GNSS failures

**Network-Level Integrity:**
- Dual-phase quality control (network and user components)
- Correction validation before transmission
- Statistical uncertainty estimates
- Real-time malfunction detection

### 5.3 Systematic Validation Procedures

**External Validation Requirements:**
- Independent distance measurements via EDM
- Bearing comparisons with traditional survey methods
- Check validation lines proportional to survey scale
- Annual equipment verification protocols

**Statistical Quality Control:**
- Kalman Filter with Detection, Identification, and Adaptation (KF&DIA)
- F-test and w-test implementation
- Data snooping algorithms for outlier detection
- Real-time quality parameter monitoring

## 6. Practical Implementation Recommendations

### 6.1 For Organizations with No Survey Experience

**Phase 1: Foundation Setup**
1. **Consider Network RTK Services**: $60/month provides 99.99% uptime vs. DIY management
2. **Invest in Quality Equipment**: Avoid cheap antennas and radios
3. **Establish Training Protocols**: Focus on antenna height measurement and coordinate systems
4. **Create Detailed SOPs**: Document every procedure step-by-step

**Phase 2: Quality System Implementation**
1. **Implement Checkpoint System**: Minimum 3 validation points per survey
2. **Establish Data Backup Procedures**: Multiple copies with metadata
3. **Create Equipment Maintenance Schedule**: Regular calibration and verification
4. **Develop Troubleshooting Guides**: Common problem resolution procedures

### 6.2 Technology Selection Guidelines

**Network RTK vs. DIY Base Stations:**
```
Choose Network RTK when:
✓ Multiple survey sites across wide area
✓ Limited technical expertise available
✓ High reliability requirements (>99% uptime)
✓ Cost of downtime exceeds subscription fees

Choose DIY Base Station when:
✓ Single site, long-term operation
✓ Technical expertise available for maintenance
✓ Remote locations without network coverage
✓ Budget constraints for ongoing subscriptions
```

### 6.3 Workflow Integration

**Daily Survey Protocol:**
```
Pre-Survey (30 minutes):
□ Equipment health check and calibration verification
□ Site conditions assessment and documentation
□ Base station setup and initialization
□ Communication system verification

During Survey (ongoing):
□ Real-time quality monitoring every measurement
□ Redundant observations at critical points
□ Environmental condition logging
□ Immediate problem resolution protocols

Post-Survey (15 minutes):
□ Data validation and backup procedures
□ Equipment shutdown and secure storage
□ Survey log completion and filing
□ Next-day preparation checklist
```

## Conclusion

Successful GNSS RTK surveying for non-experts requires systematic implementation of quality control measures, proper equipment selection, and comprehensive training. The failure modes identified in this analysis can be largely prevented through adherence to established best practices, particularly around base station management, data validation, and systematic quality control procedures.

**Priority Actions:**
1. Implement comprehensive quality control gates at each survey phase
2. Establish robust base station monitoring and backup procedures
3. Create detailed training materials focusing on common beginner mistakes
4. Develop systematic data validation and integrity checking workflows
5. Consider Network RTK services to eliminate base station management complexity

---

**Sources and References:**
- USGS Guidelines for Survey-Grade GNSS Systems [USGS, 2024]
- RTK Performance Factors Analysis [Bench Mark USA, 2024]
- GNSS Network RTK Best Practices [Smart Net NA, 2024]
- Common GNSS Surveying Mistakes [Emlid, 2024]
- Real-Time Quality Control Methods [Frontiers in Physics, 2025]