# Live OpenRiverCam AWS Deployment Specifications (Simplified)
## Multi-Site Deployment

## 1. Overview

Simple deployment of LiveORC on a single EC2 instance with S3 storage for video files. The system captures 60-second HD videos every 15 minutes with a 3-month retention policy.

### Requirements:
- **Video**: 60 seconds HD (1920x1080) every 15 minutes
- **Storage**: 3-month rotation (~325 GB steady state)
- **Architecture**: Single EC2 instance running LiveORC Docker containers
- **Database**: PostgreSQL with PostGIS on the same instance

## 2. EC2 Instance Specification

### Recommended Instance:
- **Type**: t3.large
- **vCPUs**: 2
- **Memory**: 8 GB RAM
- **Storage**: 100 GB EBS (gp3)
- **Cost**: $67.07/month (on-demand)
- **Rationale**: Edge processing reduces server load; easily upgradeable

### Operating System:
- Ubuntu 22.04 LTS
- Docker CE with Docker Compose

## 3. S3 Storage Configuration

### Bucket Setup:
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

### S3 Mount using s3fs-fuse:
```bash
# Install s3fs
sudo apt-get install s3fs

# Configure credentials
echo ACCESS_KEY:SECRET_KEY > ~/.passwd-s3fs
chmod 600 ~/.passwd-s3fs

# Mount S3 bucket
sudo mkdir -p /mnt/s3-storage
sudo s3fs openrivercam-video /mnt/s3-storage \
    -o passwd_file=~/.passwd-s3fs \
    -o allow_other \
    -o use_cache=/tmp/s3fs \
    -o url=https://s3.ap-southeast-1.amazonaws.com

# Add to fstab for persistence
echo "openrivercam-video /mnt/s3-storage fuse.s3fs _netdev,allow_other,use_cache=/tmp/s3fs,url=https://s3.ap-southeast-1.amazonaws.com 0 0" | sudo tee -a /etc/fstab
```

### S3 Lifecycle Rule (3-Month Deletion):
```json
{
  "Rules": [{
    "ID": "Delete-After-90-Days",
    "Status": "Enabled",
    "Prefix": "videos/",
    "Expiration": {
      "Days": 90
    }
  }]
}
```

## 4. LiveORC Installation

### Step 1: Install Dependencies
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Clone and Configure LiveORC
```bash
# Clone repository
cd /opt
sudo git clone https://github.com/localdevices/LiveORC.git
cd LiveORC

# Create environment file
cat > .env << EOF
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=liveorc

# Storage
STORAGE_PATH=/mnt/s3-storage
VIDEO_PATH=/mnt/s3-storage/videos
RESULTS_PATH=/mnt/s3-storage/results

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
EOF
```

### Step 3: Configure HTTPS with Let's Encrypt
```bash
# Install Certbot
sudo apt-get install certbot

# Get SSL certificate (replace with your domain)
sudo certbot certonly --standalone \
    -d liveorc.yourdomain.com \
    --email your-email@example.com \
    --agree-tos

# Create nginx configuration
cat > nginx.conf << 'EOF'
server {
    listen 443 ssl;
    server_name liveorc.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/liveorc.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/liveorc.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}

server {
    listen 80;
    server_name liveorc.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
EOF
```

### Step 4: Update Docker Compose for HTTPS
```yaml
# Add to docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - liveorc
```

### Step 5: Start LiveORC with HTTPS
```bash
# Start all services
sudo docker-compose up -d

# Check status
sudo docker-compose ps

# Set up auto-renewal for SSL
echo "0 0,12 * * * root certbot renew --quiet && docker-compose restart nginx" | sudo tee -a /etc/crontab
```

## 5. Security Configuration

### Security Group Rules:
```
Inbound:
- SSH (22): See SSH access options below
- HTTPS (443): 0.0.0.0/0 (for LiveORC API)
- HTTP (80): 0.0.0.0/0 (for Let's Encrypt only)

Outbound:
- All traffic allowed
```

### SSH Access Options for Dynamic IPs:

**Option 1: AWS Systems Manager Session Manager (Recommended)**
```bash
# No inbound SSH port needed!
# Install SSM agent (included in Ubuntu AMI)
# Access via AWS Console or CLI:
aws ssm start-session --target i-instanceid
```

**Option 2: EC2 Instance Connect**
```bash
# Temporary SSH access (60 seconds)
# AWS automatically updates security group
aws ec2-instance-connect send-ssh-public-key \
    --instance-id i-instanceid \
    --ssh-public-key file://~/.ssh/id_rsa.pub
```

**Option 3: Tailscale VPN**
```bash
# Install on EC2
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Access via Tailscale IP (100.x.x.x)
ssh ubuntu@your-instance.tail-scale.ts.net
```

**Option 4: Dynamic DNS + Security Group Update**
```bash
# Update security group with current IP
MY_IP=$(curl -s checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxx \
    --protocol tcp --port 22 \
    --cidr $MY_IP/32
```

### IAM Role for EC2:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::openrivercam-video",
        "arn:aws:s3:::openrivercam-video/*"
      ]
    }
  ]
}
```

## 6. Field Station Configuration

Configure the Raspberry Pi with cellular connectivity:

```yaml
# /home/pi/.openrivercam/config.yaml
station:
  name: sukabumi-01  # Unique identifier for this station
  location: "Sukabumi City, Indonesia"
  
server:
  url: https://liveorc.yourdomain.com/upload
  api_key: your_secure_api_key_here
  verify_ssl: true
  timeout: 120  # 2 minutes for cellular uploads
  retry_attempts: 3
  retry_delay: 300  # 5 minutes between retries
  
video:
  duration: 60
  interval: 900  # 15 minutes
  resolution: [1920, 1080]
  codec: h264
  bitrate: 5000000
  
# Cellular connection monitoring
connectivity:
  check_interval: 60  # Check every minute
  reconnect_delay: 300  # Wait 5 minutes before reconnect
```

### API Key Configuration in LiveORC:
```bash
# Generate secure API keys for each station
openssl rand -hex 32  # For station 1
openssl rand -hex 32  # For station 2, etc.

# Add to LiveORC configuration (supports multiple keys)
cat >> /opt/LiveORC/.env << EOF
# Station API Keys
API_KEY_SUKABUMI_01=generated_key_here
API_KEY_JAKARTA_01=generated_key_here
API_KEY_BANDUNG_01=generated_key_here
EOF
```

## 7. Monitoring Setup

### Basic CloudWatch Monitoring:
- CPU Utilization
- Disk Usage (EBS)
- Network In/Out
- StatusCheckFailed

### Application Logs:
```bash
# View LiveORC logs
sudo docker-compose logs -f

# Save logs to file
sudo docker-compose logs > /var/log/liveorc.log
```

## 8. Cost Breakdown

### Monthly Costs by Retention Period:

#### 30-Day Retention:
```
EC2 t3.large:                $67.07
EBS 100GB (gp3):             $8.00
S3 Storage (108GB):          $2.48
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $83.55
Total Annual:                $1,002.60
```

#### 60-Day Retention:
```
EC2 t3.large:                $67.07
EBS 100GB (gp3):             $8.00
S3 Storage (216GB):          $4.97
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $86.04
Total Annual:                $1,032.48
```

#### 90-Day Retention:
```
EC2 t3.large:                $67.07
EBS 100GB (gp3):             $8.00
S3 Storage (325GB):          $7.48
S3 Requests:                 $1.00
Data Transfer (est):         $5.00
CloudWatch Basic:            Free
--------------------------------
Total Monthly:               $88.55
Total Annual:                $1,062.60
```

Field Station Cellular Data:
- 96 videos/day × 37.5MB = 3.6GB/day
- Monthly data usage: ~108GB
- Estimated data cost: $50-100/month (varies by carrier)
```

### Cost Optimization Options:

#### Reserved Instances (EC2 savings):
- **1-year Reserved**: Save 31% → $46.28/month (total: $55-65/month depending on retention)
- **3-year Reserved**: Save 52% → $32.19/month (total: $40-50/month depending on retention)
- **Spot Instance**: Save up to 70% → ~$20/month (less reliable)

#### Storage Optimization:
- **30-day retention**: Save $5/month vs 90-day
- **60-day retention**: Save $2.50/month vs 90-day
- **Choose retention based on actual monitoring needs**

#### Scaling Options:
- **t3.large → c6i.xlarge**: Easy upgrade if processing increases
- **Add more field stations**: Minimal server cost increase

## 9. Maintenance Tasks

### Daily:
- Check LiveORC dashboard
- Verify video uploads from field station
- Monitor disk space

### Weekly:
- Review CloudWatch metrics
- Check Docker container health
- Backup database

### Monthly:
- Apply security updates
- Review S3 storage usage
- Check cost reports

## 10. Deployment Checklist

### AWS Console Setup:
- [ ] Create S3 bucket: `openrivercam-video`
- [ ] Enable lifecycle rule for 90-day deletion
- [ ] Launch EC2 instance (t3.large, Ubuntu 22.04)
- [ ] Allocate 100GB EBS volume
- [ ] Create and attach IAM role with S3 permissions
- [ ] Configure Security Group (HTTPS 443 & HTTP 80 open to 0.0.0.0/0)
- [ ] Allocate Elastic IP (required for domain setup)
- [ ] Register domain name or use Route 53
- [ ] Configure DNS A record to point to Elastic IP

### EC2 Instance Setup:
- [ ] Configure SSH access (SSM, EC2 Connect, or VPN)
- [ ] Install Docker and Docker Compose
- [ ] Install and configure s3fs
- [ ] Mount S3 bucket
- [ ] Clone LiveORC repository
- [ ] Configure environment variables
- [ ] Install Certbot and obtain SSL certificate
- [ ] Configure nginx for HTTPS
- [ ] Start LiveORC containers with HTTPS
- [ ] Test HTTPS video upload endpoint

### Field Station Setup:
- [ ] Configure server URL in Raspberry Pi
- [ ] Test connectivity to EC2 instance
- [ ] Verify first video upload
- [ ] Check LiveORC dashboard

## 11. Troubleshooting

### Common Issues:

**S3 mount not working:**
```bash
# Check s3fs logs
tail -f /var/log/syslog | grep s3fs

# Remount
sudo umount /mnt/s3-storage
sudo s3fs openrivercam-video /mnt/s3-storage -o passwd_file=~/.passwd-s3fs,allow_other
```

**Docker containers not starting:**
```bash
# Check logs
sudo docker-compose logs

# Restart containers
sudo docker-compose down
sudo docker-compose up -d
```

**Videos not uploading from cellular field station:**
```bash
# Check LiveORC API logs for authentication errors
sudo docker logs liveorc_web_1 | grep "auth"

# Test API endpoint with key over HTTPS
curl -X GET https://liveorc.yourdomain.com/health \
  -H "Authorization: Bearer your_api_key_here"

# Monitor cellular data usage
# On Raspberry Pi:
sudo ifconfig wwan0  # or appropriate interface

# Check upload queue on field station
ls -la /home/pi/.openrivercam/upload_queue/
```

## 12. Next Steps

Once the basic system is running:
1. Enable AWS CloudWatch detailed monitoring
2. Implement automated database backups
3. Add SNS alerts for system failures
4. Consider autoscaling for multiple stations
5. Implement S3 storage tiering for cost savings
6. Set up AWS WAF for additional API protection