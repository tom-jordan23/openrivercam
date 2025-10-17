# Live OpenRiverCam AWS Infrastructure Specifications
## Multi-Site Deployment Architecture

## 1. System Overview

LiveORC deployment on AWS for receiving, processing, and storing video data from field-deployed OpenRiverCam devices. The system captures 60-second HD videos every 15 minutes with configurable retention periods.

### Architecture Summary:
- **Deployment Model**: Single EC2 instance with S3 storage
- **Processing**: Edge processing at field stations, server handles API and storage
- **Database**: PostgreSQL with PostGIS on EC2 instance
- **Access**: HTTPS API with secure field station authentication
- **Management**: AWS Session Manager (no SSH exposure)

## 2. Infrastructure Components

### 2.1 EC2 Instance Specifications
- **Instance Type**: t3.large
- **vCPUs**: 2
- **Memory**: 8 GB RAM
- **Storage**: 50 GB EBS (gp3)
- **Operating System**: Ubuntu 22.04 LTS
- **Rationale**: Edge processing reduces server load; easily upgradeable to c6i.xlarge if needed

### 2.2 S3 Storage Configuration

#### Bucket Structure:
```
openrivercam-video/
├── [site-name]/
│   ├── videos/
│   │   └── YYYY/MM/DD/
│   │       └── [site]_video_YYYYMMDD_HHMMSS.mp4
│   ├── results/
│   │   └── YYYY/MM/DD/
│   │       └── [site]_result_YYYYMMDD_HHMMSS.json
│   └── config/
│       └── station_config.json
└── [additional-sites]/
    └── ...
```

#### Storage Requirements by Retention Period:
- **Video Format**: H.264 MP4 @ 5 Mbps
- **Single Video Size**: 60 seconds × 5 Mbps = 37.5 MB
- **Videos per Day**: 96 (every 15 minutes)
- **Daily Storage**: 96 × 37.5 MB = 3.6 GB
- **Monthly Storage**: 108 GB

**30-Day Retention:**
- Maximum Storage: 108 GB (videos) + 288 MB (results) = ~108 GB
- Use Case: Short-term monitoring, frequent analysis

**60-Day Retention:**
- Maximum Storage: 216 GB (videos) + 576 MB (results) = ~216 GB  
- Use Case: Seasonal analysis, event correlation

**90-Day Retention:**
- Maximum Storage: 324 GB (videos) + 864 MB (results) = ~325 GB
- Use Case: Long-term trends, research projects

### 2.3 Network Architecture
- **Region**: us-east-1 (N. Virginia)
- **Security Groups**: HTTPS (443) and temporary HTTP (80) for SSL certificate validation
- **Access Method**: AWS Session Manager (no SSH port exposure)
- **API Endpoint**: HTTPS with SSL/TLS encryption
- **Field Station Authentication**: API key-based authentication

### 2.4 Software Stack
- **Containerization**: Docker with Docker Compose
- **Web Server**: Nginx reverse proxy with SSL termination
- **Application**: LiveORC containers
- **Database**: PostgreSQL with PostGIS extension
- **SSL Certificates**: Let's Encrypt with automatic renewal

## 3. Cost Analysis

### 3.1 Monthly Cost Breakdown by Retention Period

#### 30-Day Retention:
```
EC2 t3.large:                $67.07
EBS 50GB (gp3):              $4.00
S3 Storage (108GB):          $2.48
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $79.55
Total Annual:                $954.60
```

#### 60-Day Retention:
```
EC2 t3.large:                $67.07
EBS 50GB (gp3):              $4.00
S3 Storage (216GB):          $4.97
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $82.04
Total Annual:                $984.48
```

#### 90-Day Retention:
```
EC2 t3.large:                $67.07
EBS 50GB (gp3):              $4.00
S3 Storage (325GB):          $7.48
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $84.55
Total Annual:                $1,014.60
```

### 3.2 Field Station Data Costs (External)
- **Videos per day**: 96 × 37.5MB = 3.6GB/day
- **Monthly cellular data usage**: ~108GB
- **Estimated carrier cost**: $50-100/month (varies by carrier and plan)

### 3.3 Cost Optimization Options

#### Reserved Instances (EC2 savings):
- **1-year Reserved**: Save 31% → $46.28/month (total: $51-61/month depending on retention)
- **3-year Reserved**: Save 52% → $32.19/month (total: $36-46/month depending on retention)
- **Spot Instance**: Save up to 70% → ~$20/month (less reliable)

#### Storage Optimization:
- **30-day retention**: Save $5/month vs 90-day
- **60-day retention**: Save $2.50/month vs 90-day
- **Choose retention based on actual monitoring needs**

#### Scaling Options:
- **t3.large → c6i.xlarge**: Easy upgrade if processing increases
- **Add more field stations**: Minimal server cost increase

## 4. Security Specifications

### 4.1 Network Security
- **Exposed Ports**: HTTPS (443) only after setup
- **SSH Access**: Disabled (Session Manager only)
- **Field Station Communication**: Encrypted HTTPS with API key authentication
- **SSL/TLS**: Let's Encrypt certificates with automatic renewal

### 4.2 IAM Configuration
- **EC2 Instance Role**: S3 full access to designated bucket, SSM access
- **Principle of Least Privilege**: Scoped permissions to required resources only
- **API Authentication**: Per-station API keys for field device access

### 4.3 Data Protection
- **Encryption in Transit**: TLS 1.2+ for all communications
- **Encryption at Rest**: S3 server-side encryption (AES-256)
- **Access Logging**: CloudWatch logs for audit trails

## 5. Scalability Considerations

### 5.1 Vertical Scaling
- **CPU/Memory**: Upgrade to c6i.xlarge (4→8 vCPU, 8→16GB RAM)
- **Storage**: Increase EBS volume size as needed
- **Database**: Add read replicas if query load increases

### 5.2 Horizontal Scaling
- **Multiple Field Stations**: Current architecture supports 100+ stations
- **Load Balancing**: Can add Application Load Balancer for high availability
- **Multi-Region**: Expandable to additional AWS regions

### 5.3 Performance Characteristics
- **Video Upload Handling**: ~96 uploads/day per station
- **API Response Time**: <500ms for typical requests
- **Storage Throughput**: S3 provides virtually unlimited throughput
- **Database Performance**: PostgreSQL handles typical query loads on t3.large

## 6. Monitoring and Alerting

### 6.1 CloudWatch Metrics
- **EC2 Metrics**: CPU, memory, disk usage, network I/O
- **Application Metrics**: Video upload counts, processing errors, API latency
- **Storage Metrics**: S3 bucket size, request counts
- **Database Metrics**: Connection counts, query performance

### 6.2 Automated Alerting
- **High Error Rate**: >5 processing errors in 5 minutes
- **Low Upload Rate**: <2 videos in 30 minutes (potential field station issue)
- **Storage Growth**: Unexpected increases in S3 usage
- **Instance Health**: EC2 status check failures

## 7. Backup and Recovery

### 7.1 Data Protection Strategy
- **S3 Data**: Inherently redundant across multiple AZs
- **Database**: Daily automated snapshots
- **Configuration**: Version-controlled Docker configurations
- **Recovery Time Objective (RTO)**: 2 hours
- **Recovery Point Objective (RPO)**: 15 minutes (last video upload)

### 7.2 Disaster Recovery
- **Data Recovery**: S3 data available across retention period
- **System Recovery**: Infrastructure as Code for rapid rebuilding
- **Cross-Region**: Optional replication to secondary region

## 8. Maintenance Requirements

### 8.1 Routine Maintenance
- **Security Updates**: Monthly OS and container updates
- **SSL Certificates**: Automated renewal via Let's Encrypt
- **Database Maintenance**: Weekly automated maintenance windows
- **Log Rotation**: Automated log cleanup and archival

### 8.2 Monitoring Tasks
- **Daily**: Review system health, upload statistics
- **Weekly**: Analyze performance trends, storage growth
- **Monthly**: Cost review, security audit, capacity planning
- **Quarterly**: Disaster recovery testing, performance optimization