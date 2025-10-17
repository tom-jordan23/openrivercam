# Live OpenRiverCam AWS Deployment Guide
## Complete Step-by-Step Instructions for Beginners

### 📋 Overview
This guide will walk you through deploying Live OpenRiverCam (LiveORC) on AWS. You'll set up a server that can receive video data from field stations and process it for river flow analysis.

**What you'll build:**
- EC2 instance running LiveORC with HTTPS
- S3 bucket for video storage (3-month retention)
- Secure API for field station uploads
- Web dashboard for monitoring

**Prerequisites:**
- AWS account with billing set up
- Domain name (or willingness to purchase one)
- Basic familiarity with terminal/command line

**Estimated time:** 2-3 hours  
**Monthly cost:** $80-85 depending on retention (can be reduced to $51-61 with reserved instances)

---

## 🚀 Phase 1: AWS Account Preparation

### Step 1.1: Log into AWS Console
1. Go to https://aws.amazon.com/console/
2. Sign in with your AWS account credentials
3. **Important:** Make sure you're in the **Asia Pacific (Singapore)** region
   - Look at the top-right corner of the console
   - If it doesn't say "Singapore", click the region dropdown and select "Asia Pacific (Singapore)"

### Step 1.2: Enable Billing Alerts
1. In the AWS Console, click your account name (top-right)
2. Select "Billing and Cost Management"
3. In the left sidebar, click "Billing preferences"
4. Check "Receive Billing Alerts"
5. Enter your email address
6. Click "Save preferences"

---

## 💾 Phase 2: Create S3 Storage Bucket

### Step 2.1: Create S3 Bucket
1. In AWS Console, search for "S3" and click on it
2. Click "Create bucket"
3. **Bucket name:** `openrivercam-video` (must be globally unique)
   - If this name is taken, try: `openrivercam-video-yourname` or `openrivercam-video-2024`
4. **Region:** Asia Pacific (Singapore) ap-southeast-1
5. **Bucket settings:**
   - Uncheck "Block all public access" (we'll configure security properly later)
   - Check the acknowledgment box
6. Leave other settings as default
7. Click "Create bucket"

### Step 2.2: Configure Bucket Lifecycle (Auto-delete old videos)
1. Click on your newly created bucket name
2. Go to the "Management" tab
3. Click "Create lifecycle rule"
4. **Rule name:** `Delete-After-90-Days`
5. **Choose a rule scope:** Apply to all objects in the bucket
6. Under "Lifecycle rule actions," check "Expire current versions of objects"
7. Set "Days after object creation:" to `90`
8. Click "Create rule"

### Step 2.3: Test Bucket Access
1. In your bucket, click "Upload"
2. Upload any small test file
3. Verify the file appears in the bucket
4. Delete the test file

---

## 🔐 Phase 3: Set Up IAM Policy and Role for EC2

### Step 3.1: Create Custom Policy First
1. In AWS Console, search for "IAM" and click on it
2. In the left sidebar, click "Policies"
3. Click "Create policy"
4. Click the "JSON" tab
5. Replace the existing content with:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::openrivercam-video",
        "arn:aws:s3:::openrivercam-video/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:*",
        "ssmmessages:*",
        "ec2messages:*"
      ],
      "Resource": "*"
    }
  ]
}
```
6. Click "Next"
7. **Policy name:** `LiveORC-S3-SSM-Policy`
8. **Description:** `Allows LiveORC EC2 instance to access S3 bucket and use Session Manager`
9. Click "Create policy"

### Step 3.2: Create IAM Role
1. In the left sidebar, click "Roles"
2. Click "Create role"
3. **Select trusted entity type:** AWS service
4. **Use case:** EC2
5. Click "Next"

### Step 3.3: Attach Policy to Role
1. In the search box, type "LiveORC-S3-SSM-Policy"
2. Check the box next to your policy
3. **Optional:** Also search for and add "CloudWatchAgentServerPolicy" for better monitoring
4. Click "Next"
5. **Role name:** `LiveORC-EC2-Role`
6. **Description:** `Role for LiveORC EC2 instance with S3 and SSM access`
7. Click "Create role"

---

## 🖥️ Phase 4: Launch EC2 Instance

### Step 4.1: Start Instance Creation
1. In AWS Console, search for "EC2" and click on it
2. Click "Launch instance"
3. **Name:** `LiveORC-Server`

### Step 4.2: Choose Amazon Machine Image (AMI)
1. Under "Application and OS Images"
2. Select "Ubuntu"
3. Choose "Ubuntu Server 22.04 LTS (HVM)"
4. Make sure "64-bit (x86)" is selected

### Step 4.3: Choose Instance Type
1. Under "Instance type"
2. Select "t3.large" (2 vCPU, 8 GB RAM)
   - Perfect for API server and data storage
   - Heavy processing happens on Raspberry Pi at field stations
   - Easy to upgrade to c6i.xlarge later if workload increases

### Step 4.4: Key Pair Configuration
1. Under "Key pair (login)"
2. Select **"Proceed without a key pair"**
   - We're using Session Manager, not SSH
   - More secure - no SSH keys to manage or lose!

### Step 4.5: Configure Network Settings
1. Click "Edit" next to "Network settings"
2. **Create security group:** Yes
3. **Security group name:** `LiveORC-Security-Group`
4. **Description:** `Security group for LiveORC server`
5. **Inbound security group rules:**
   - Rule 1: Type: HTTPS, Port: 443, Source: Anywhere (0.0.0.0/0)
   - Rule 2: Type: HTTP, Port: 80, Source: Anywhere (0.0.0.0/0) 
     - **Note:** HTTP only needed for SSL certificate validation, can be removed after setup
   - **NO SSH RULE** - We'll use Session Manager instead (more secure!)

### Step 4.6: Configure Storage
1. Under "Configure storage"
2. Change storage size to **50 GB**
3. **Storage type:** gp3
4. Leave other settings as default

### Step 4.7: Advanced Details
1. Expand "Advanced details"
2. **IAM instance profile:** Select `LiveORC-EC2-Role`
3. Scroll to "User data" and paste:
```bash
#!/bin/bash
# Update system
apt-get update -y
apt-get upgrade -y

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
apt-get install -y unzip
unzip awscliv2.zip
./aws/install
rm -rf awscliv2.zip aws/

# Install Session Manager Agent
curl "https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb" -o "amazon-ssm-agent.deb"
dpkg -i amazon-ssm-agent.deb
systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent
rm amazon-ssm-agent.deb

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu


# Install other dependencies
apt-get install -y s3fs git certbot

# Create initial directories
mkdir -p /opt/liveorc
mkdir -p /mnt/s3-storage
chown ubuntu:ubuntu /opt/liveorc
```

### Step 4.8: Launch Instance
1. Click "Launch instance"
2. Wait for the instance to start (about 2-3 minutes)
3. Note down the instance ID (starts with i-)

---

## 🌐 Phase 5: Set Up Domain (Optional)

### Step 5.1: Get Your EC2 Public IP
1. In EC2 console, select your LiveORC instance
2. Note the **Public IPv4 address** (e.g., 52.74.123.456)
3. **Note:** This IP may change if you stop/start the instance

### Step 5.2: Configure Domain (Optional - Choose one option)

**Option A: Use External Domain Provider**
1. Log into your domain provider (GoDaddy, Namecheap, etc.)
2. Find DNS management
3. Create an A record:
   - **Name:** liveorc
   - **Type:** A
   - **Value:** Your EC2 Public IP address
   - **TTL:** 300

**Option B: Use IP Address Directly**
1. Skip domain setup entirely
2. Access LiveORC using: `https://YOUR-EC2-PUBLIC-IP`
3. **Note:** You'll get SSL certificate warnings
4. Good for testing or internal use

---

## 🔧 Phase 6: Connect to EC2 and Install Software

### Step 6.1: Connect Using Session Manager (Recommended)
1. In EC2 console, select your instance
2. Click "Connect"
3. Choose "Session Manager" tab
4. Click "Connect"
5. You should now have a terminal session

**Note:** No SSH access is configured - Session Manager is more secure and works from anywhere!

### Step 6.2: Verify Installation
```bash
# Check that docker is installed
docker --version

# Check docker compose
docker compose --version

# Switch to ubuntu user if needed
sudo su - ubuntu
```

### Step 6.3: Configure S3 Access

**First, we need to get AWS access keys. Two options:**

#### Option A: Use EC2 Instance Profile (Recommended - No Keys Needed!)
```bash
# The EC2 role already has S3 permissions, so use IAM role credentials
sudo s3fs openrivercam-video /mnt/s3-storage \
    -o iam_role=auto \
    -o allow_other \
    -o use_cache=/tmp/s3fs \
    -o url=https://s3.ap-southeast-1.amazonaws.com

# If this works, skip to "Verify mount works" below
```

#### Option B: Create Access Keys (If Option A doesn't work)
**Skip to Step 6.4 below to create access keys first, then come back here**

After creating keys in Step 6.4, use them:
```bash
# Create credentials file with YOUR actual keys from Step 6.4
echo "YOUR_ACCESS_KEY_ID:YOUR_SECRET_ACCESS_KEY" > ~/.passwd-s3fs
chmod 600 ~/.passwd-s3fs

# Mount with credentials
sudo s3fs openrivercam-video /mnt/s3-storage \
    -o passwd_file=/home/ubuntu/.passwd-s3fs \
    -o allow_other \
    -o use_cache=/tmp/s3fs \
    -o url=https://s3.ap-southeast-1.amazonaws.com
```

#### Verify mount works:
```bash
# Check if mount succeeded
ls -la /mnt/s3-storage

# Create test file
echo "test" > /mnt/s3-storage/test.txt
ls -la /mnt/s3-storage/
rm /mnt/s3-storage/test.txt

# Add to fstab for persistence (choose the option that worked)
# For IAM role:
echo "openrivercam-video /mnt/s3-storage fuse.s3fs _netdev,allow_other,use_cache=/tmp/s3fs,iam_role=auto,url=https://s3.ap-southeast-1.amazonaws.com 0 0" | sudo tee -a /etc/fstab

# OR for access keys:
echo "openrivercam-video /mnt/s3-storage fuse.s3fs _netdev,allow_other,use_cache=/tmp/s3fs,passwd_file=/home/ubuntu/.passwd-s3fs,url=https://s3.ap-southeast-1.amazonaws.com 0 0" | sudo tee -a /etc/fstab
```

### Step 6.4: Create AWS Access Keys (Only if Option A didn't work)
1. In AWS Console, go to IAM
2. Click "Users" in left sidebar
3. Click "Create user"
4. **User name:** `liveorc-s3-user`
5. Click "Next"
6. **Attach policies:** Select "AmazonS3FullAccess"
7. Click "Create user"
8. Click on the new user
9. Go to "Security credentials" tab
10. Click "Create access key"
11. Choose "Application running on AWS compute service"
12. Click "Next" → "Create access key"
13. **Important:** Copy the Access Key ID and Secret Access Key

---

## 🛠️ Phase 7: Install and Configure LiveORC

### Step 7.1: Clone LiveORC Repository
```bash
# Change to installation directory
cd /opt

# Clone the repository
sudo git clone https://github.com/localdevices/LiveORC.git
sudo chown -R ubuntu:ubuntu LiveORC
cd LiveORC
```

### Step 7.2: Create Environment Configuration
```bash
# Create environment file
cat > .env << 'EOF'
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SecurePassword123!
POSTGRES_DB=liveorc

# Storage Configuration
STORAGE_PATH=/mnt/s3-storage
VIDEO_PATH=/mnt/s3-storage/videos
RESULTS_PATH=/mnt/s3-storage/results

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# API Keys (generate these)
API_KEY_SUKABUMI_01=your_generated_key_here
API_KEY_JAKARTA_01=another_generated_key_here

# Domain Configuration
DOMAIN_NAME=liveorc.yourdomain.com
EOF
```

### Step 7.3: Generate API Keys
```bash
# Generate secure API keys for each station
echo "Station 1 API Key:"
openssl rand -hex 32

echo "Station 2 API Key:"
openssl rand -hex 32

# Update the .env file with your generated keys
nano .env
```

### Step 7.4: Obtain SSL Certificate
```bash
# Stop any existing web services
sudo systemctl stop apache2 nginx 2>/dev/null || true

# Get SSL certificate (replace with your actual domain)
sudo certbot certonly --standalone \
    -d liveorc.yourdomain.com \
    --email your-email@example.com \
    --agree-tos \
    --non-interactive

# Verify certificate was created
sudo ls -la /etc/letsencrypt/live/liveorc.yourdomain.com/
```

### Step 7.5: Configure Nginx for HTTPS
```bash
# Create nginx configuration
cat > nginx.conf << 'EOF'
server {
    listen 443 ssl http2;
    server_name liveorc.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/liveorc.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/liveorc.yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    client_max_body_size 100M;  # Allow large video uploads
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts for large uploads
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

server {
    listen 80;
    server_name liveorc.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
EOF
```

### Step 7.6: Create Docker Compose Configuration
```bash
# Create or modify docker compose.yml
cat > docker compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgis/postgis:14-3.2
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  liveorc:
    image: localdevices/liveorc:latest
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - STORAGE_PATH=${STORAGE_PATH}
      - VIDEO_PATH=${VIDEO_PATH}
      - RESULTS_PATH=${RESULTS_PATH}
    volumes:
      - /mnt/s3-storage:/mnt/s3-storage
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    restart: unless-stopped

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
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF
```

### Step 7.7: Start LiveORC Services
```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Step 7.8: Set Up SSL Auto-Renewal
```bash
# Create renewal script
sudo tee /etc/cron.d/certbot-renew << 'EOF'
0 0,12 * * * root certbot renew --quiet && cd /opt/LiveORC && docker compose restart nginx
EOF

# Test the renewal process
sudo certbot renew --dry-run
```

---

## ✅ Phase 8: Verify Installation

### Step 8.1: Test Web Interface
1. Open your browser
2. Go to `https://liveorc.yourdomain.com`
3. You should see the LiveORC dashboard
4. Check that there are no SSL certificate warnings

### Step 8.1.5: Remove HTTP Access (Security Hardening)
Once HTTPS is working, remove the HTTP rule:

1. Go to **EC2** → **Security Groups**
2. Select `LiveORC-Security-Group`
3. Click **Inbound rules** tab
4. Find the HTTP (port 80) rule
5. Click **Delete** to remove it
6. **Result:** Only HTTPS traffic allowed

**Final Security State:**
- ✅ NO SSH port (never opened!)
- ✅ NO HTTP port (removed after setup)
- ✅ Only port 443 (HTTPS) exposed
- ✅ Access via Session Manager only

### Step 8.2: Test API Endpoint
```bash
# Test health endpoint
curl -k https://liveorc.yourdomain.com/health

# Test with API key
curl -k https://liveorc.yourdomain.com/api/v1/status \
  -H "Authorization: Bearer your_api_key_here"
```

### Step 8.3: Verify S3 Storage
```bash
# Create test folder structure
mkdir -p /mnt/s3-storage/test-site/videos/$(date +%Y/%m/%d)
echo "Test file" > /mnt/s3-storage/test-site/videos/$(date +%Y/%m/%d)/test.txt

# Check it appears in S3 bucket (via AWS Console)
# Clean up test file
rm /mnt/s3-storage/test-site/videos/$(date +%Y/%m/%d)/test.txt
```

### Step 8.4: Monitor System Resources
```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check Docker containers
docker stats

# Check system logs
journalctl -f
```

---

## 📱 Phase 9: Configure Field Station

### Step 9.1: Raspberry Pi Configuration
Create this configuration file on your Raspberry Pi:

```bash
# On Raspberry Pi: /home/pi/.openrivercam/config.yaml
station:
  name: sukabumi-01
  location: "Sukabumi City, Indonesia"
  
server:
  url: https://liveorc.yourdomain.com/upload
  api_key: your_generated_api_key_here
  verify_ssl: true
  timeout: 120
  retry_attempts: 3
  retry_delay: 300
  
video:
  duration: 60
  interval: 900  # 15 minutes
  resolution: [1920, 1080]
  codec: h264
  bitrate: 5000000
  
connectivity:
  check_interval: 60
  reconnect_delay: 300
```

### Step 9.2: Test Field Station Connection
```bash
# From Raspberry Pi, test connectivity
curl -k https://liveorc.yourdomain.com/health

# Test with API key
curl -k -X POST https://liveorc.yourdomain.com/upload \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"test": "connection"}'
```

---

## 🔍 Phase 10: Monitoring and Maintenance

### Step 10.1: Set Up CloudWatch Monitoring
1. In AWS Console, go to CloudWatch
2. Click "Dashboards" → "Create dashboard"
3. **Dashboard name:** `LiveORC-Monitoring`
4. Add widgets for:
   - EC2 CPU Utilization
   - EC2 Network In/Out
   - S3 Bucket Size
   - EC2 Status Checks

### Step 10.2: Create Billing Alerts
1. In CloudWatch, go to "Alarms"
2. Click "Create alarm"
3. Select "Billing" → "Total Estimated Charge"
4. Set threshold to $200 (or your preferred limit)
5. Create SNS topic for notifications
6. Add your email address

### Step 10.3: Regular Maintenance Tasks

**Daily Checks:**
```bash
# Check system status
docker compose ps
df -h  # Check disk space
free -h  # Check memory

# Check recent logs
docker compose logs --tail=50

# Check LiveORC dashboard
curl -k https://liveorc.yourdomain.com/health
```

**Weekly Maintenance:**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Check SSL certificate expiry
sudo certbot certificates

# Backup database
docker compose exec db pg_dump -U postgres liveorc > backup_$(date +%Y%m%d).sql

# Clean Docker images
docker system prune -f
```

**Monthly Tasks:**
```bash
# Review AWS costs
# Check S3 storage usage
aws s3 ls s3://openrivercam-video --recursive --human-readable --summarize

# Review CloudWatch metrics
# Check for security updates
```

---

## 🆘 Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Can't connect to LiveORC website"
**Solutions:**
1. Check security group allows HTTPS (443) from 0.0.0.0/0
2. Verify Elastic IP is associated with instance
3. Check DNS A record points to correct IP
4. Verify nginx container is running: `docker compose ps`

#### Issue: "SSL certificate errors"
**Solutions:**
```bash
# Check certificate status
sudo certbot certificates

# Regenerate certificate
sudo certbot certonly --standalone -d liveorc.yourdomain.com --force-renewal

# Restart nginx
docker compose restart nginx
```

#### Issue: "S3 mount not working"
**Solutions:**
```bash
# Check credentials
cat ~/.passwd-s3fs

# Remount S3
sudo umount /mnt/s3-storage
sudo s3fs openrivercam-video /mnt/s3-storage \
  -o passwd_file=/home/ubuntu/.passwd-s3fs \
  -o allow_other

# Check logs
tail -f /var/log/syslog | grep s3fs
```

#### Issue: "Videos not uploading from field station"
**Solutions:**
1. Check API key is correct
2. Verify network connectivity from field station
3. Check LiveORC logs: `docker compose logs liveorc`
4. Verify S3 permissions in IAM role

#### Issue: "High AWS costs"
**Solutions:**
1. Check S3 storage usage
2. Consider Reserved Instances for EC2
3. Verify lifecycle policies are working
4. Monitor data transfer costs

#### Issue: "Container won't start"
**Solutions:**
```bash
# Check logs
docker compose logs service_name

# Check system resources
df -h
free -h

# Restart specific service
docker compose restart service_name

# Full restart
docker compose down
docker compose up -d
```

---

## 📊 Performance Optimization

### Step 10.4: Optimize for Production

**Enable CloudWatch detailed monitoring:**
1. Go to EC2 console
2. Select your instance
3. Actions → Monitor and troubleshoot → Manage detailed monitoring
4. Enable detailed monitoring

**Set up automated backups:**
```bash
# Create backup script
sudo tee /usr/local/bin/backup-liveorc.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cd /opt/LiveORC

# Backup database
docker compose exec -T db pg_dump -U postgres liveorc | gzip > /tmp/liveorc_backup_${DATE}.sql.gz

# Upload to S3
aws s3 cp /tmp/liveorc_backup_${DATE}.sql.gz s3://openrivercam-video/backups/

# Clean local backup
rm /tmp/liveorc_backup_${DATE}.sql.gz

# Keep only last 7 days of backups in S3
aws s3 ls s3://openrivercam-video/backups/ --recursive | \
  while read -r line; do
    filename=$(echo $line | awk '{print $4}')
    if [[ "$filename" == *.sql.gz ]]; then
      file_date=$(echo $filename | grep -o '[0-9]\{8\}_[0-9]\{6\}')
      if [[ -n "$file_date" ]]; then
        days_old=$(( ($(date +%s) - $(date -d "${file_date:0:8} ${file_date:9:2}:${file_date:11:2}:${file_date:13:2}" +%s)) / 86400 ))
        if [[ $days_old -gt 7 ]]; then
          aws s3 rm "s3://openrivercam-video/$filename"
        fi
      fi
    fi
  done
EOF

chmod +x /usr/local/bin/backup-liveorc.sh

# Add to crontab for daily backups
echo "0 2 * * * root /usr/local/bin/backup-liveorc.sh" | sudo tee -a /etc/crontab
```

---

## 🎉 Congratulations!

You've successfully deployed Live OpenRiverCam on AWS! Your system is now ready to:

✅ Receive video uploads from field stations  
✅ Process river flow data  
✅ Store videos with automatic 3-month rotation  
✅ Provide secure HTTPS access  
✅ Monitor system health  

### Next Steps:
1. Configure your field stations to upload to your server
2. Set up monitoring alerts
3. Consider cost optimization with Reserved Instances
4. Plan for scaling if adding more field stations

### Support Resources:
- LiveORC Documentation: https://github.com/localdevices/LiveORC
- AWS Documentation: https://docs.aws.amazon.com/
- Community Forums: Check the LiveORC GitHub issues

**Remember to:**
- Monitor your AWS costs regularly
- Keep your system updated
- Back up your data
- Review security settings periodically

---

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review AWS CloudWatch logs** for error messages
3. **Check LiveORC logs** with `docker compose logs`
4. **Post issues** on the LiveORC GitHub repository
5. **AWS Support** can help with infrastructure issues

**Emergency contacts:**
- AWS Support: Use your AWS Console support center
- System logs: `journalctl -f` and `docker compose logs -f`

Good luck with your river monitoring project! 🌊📊