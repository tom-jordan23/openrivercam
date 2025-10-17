# Live OpenRiverCam AWS Deployment Guide
## Complete Step-by-Step Instructions for Beginners

### ⚠️ DEPLOYMENT STATUS NOTICE
**As of October 17, 2024:** The LiveORC server has been successfully deployed and is running with s3fs mounted storage. The following optional steps have NOT been completed:
- ❌ **Step 2.2**: S3 bucket lifecycle policy for automatic 90-day deletion
- ❌ **Step 7.5**: Systemd service for auto-start on reboot
- ❌ **Phase 9**: CloudWatch monitoring setup
- ❌ **Step 9.2**: Billing alerts configuration

The server is operational without these features, but they should be configured for production use.

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
3. **Important:** Make sure you're in the **US East (N. Virginia)** region
   - Look at the top-right corner of the console
   - If it doesn't say "N. Virginia", click the region dropdown and select "US East (N. Virginia)"

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
4. **Region:** US East (N. Virginia) us-east-1
5. **Bucket settings:**
   - Uncheck "Block all public access" (we'll configure security properly later)
   - Check the acknowledgment box
6. Leave other settings as default
7. Click "Create bucket"

### Step 2.2: Configure Bucket Lifecycle (Auto-delete old videos) *** NOT YET COMPLETED ***
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
apt-get install -y git s3fs

# Create S3 mount point
mkdir -p /mnt/s3-storage
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
# Check what user you're logged in as
whoami

# If it shows "ssm-user" or "root", switch to ubuntu user:
sudo su - ubuntu

# If it already shows "ubuntu", you're good!

# Verify docker is installed
docker --version

# Check docker compose (built into Docker now)
docker compose version

# Verify docker works without sudo (should not give permission error)
docker ps

# Verify AWS CLI is installed
aws --version

# Verify s3fs is installed
which s3fs
s3fs --version
```

### Step 6.3: Mount S3 Bucket with s3fs using IAM Role

Since the EC2 instance already has an IAM role with S3 access (from Step 3), we can mount S3 without creating additional credentials:

```bash
# Mount S3 bucket using IAM role authentication
sudo s3fs openrivercam-video /mnt/s3-storage \
  -o iam_role=auto \
  -o allow_other \
  -o use_cache=/tmp/s3fs \
  -o url=https://s3.us-east-1.amazonaws.com

# Verify mount worked
df -h | grep s3
ls -la /mnt/s3-storage/

# Test write access
echo "test" > /mnt/s3-storage/test.txt
cat /mnt/s3-storage/test.txt
rm /mnt/s3-storage/test.txt

# Add to fstab for persistence
echo "openrivercam-video /mnt/s3-storage fuse.s3fs _netdev,allow_other,use_cache=/tmp/s3fs,iam_role=auto,url=https://s3.us-east-1.amazonaws.com 0 0" | sudo tee -a /etc/fstab

# Test persistence
sudo mount -a
```

**Note:** The `iam_role=auto` option tells s3fs to use the EC2 instance's IAM role credentials automatically. No access keys needed!

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

### Step 7.2: Configure LiveORC for Mounted S3 Storage
```bash
# Create a startup script for LiveORC with mounted storage
cat > start-liveorc.sh << 'EOF'
#!/bin/bash
# LiveORC startup with mounted S3 storage

cd /opt/LiveORC

# Start LiveORC with mounted storage directory
./liveorc.sh start \
  --hostname YOUR_DOMAIN_OR_IP \
  --port 8000 \
  --storage-local \
  --storage-dir /mnt/s3-storage \
  --detached

echo "LiveORC started with mounted S3 storage at /mnt/s3-storage"
EOF

chmod +x start-liveorc.sh

echo "Edit start-liveorc.sh to replace YOUR_DOMAIN_OR_IP with your actual domain or IP"
```

### Step 7.3: Test LiveORC is Working
```bash
# Start LiveORC using the script
./start-liveorc.sh

# Check if services are running
docker ps

# View logs
docker logs liveorc_webapp
```

### Step 7.4: Configure SSL with LiveORC

LiveORC includes **automatic SSL certificate management** using Let's Encrypt. No manual certificate installation or renewal scripts are needed!

**How LiveORC manages SSL certificates:**
- ✅ **Automatic provisioning** via Let's Encrypt
- ✅ **Automatic renewal** every 90 days  
- ✅ **Domain validation** handled internally
- ✅ **No manual intervention** required

**Prerequisites for SSL:**
- Domain name pointed to your server's public IP
- Ports 80 (temporary) and 443 accessible for domain validation

```bash
# Stop LiveORC if running
./liveorc.sh stop

# Update the startup script to include SSL
cat > start-liveorc.sh << 'EOF'
#!/bin/bash
# LiveORC startup with mounted S3 storage and SSL

cd /opt/LiveORC

# Start LiveORC with SSL enabled (replace with your actual domain)
./liveorc.sh start \
  --hostname liveorc.yourdomain.com \
  --ssl \
  --port 8000 \
  --storage-local \
  --storage-dir /mnt/s3-storage \
  --detached

echo "LiveORC started with SSL and S3 storage"
EOF

# Start LiveORC with SSL
./start-liveorc.sh

# Check if LiveORC started successfully
docker ps

# Monitor SSL certificate provisioning (may take 2-3 minutes)
# First check if containers are running
docker ps

# View LiveORC webapp logs to see SSL setup progress
docker logs liveorc_webapp

# Check for any startup errors
docker logs liveorc_webapp | grep -i error

# Monitor SSL certificate provisioning specifically
docker logs liveorc_webapp | grep -i ssl
```

**Certificate Renewal:**
LiveORC automatically renews Let's Encrypt certificates before expiration. No manual steps needed!

**Troubleshooting SSL Setup:**
- Use `docker logs liveorc_webapp` to view actual LiveORC logs
- Check `docker ps` to verify containers are running
- SSL certificate provisioning can take 2-5 minutes for Let's Encrypt domain validation
- Ensure your domain's DNS A record points to this server's public IP
- Port 80 must be accessible for Let's Encrypt domain validation



### Step 7.5: Set Up Auto-Start Service *** NOT YET COMPLETED ***
```bash
# Create systemd service for auto-start on boot
sudo tee /etc/systemd/system/liveorc.service << 'EOF'
[Unit]
Description=LiveORC Server
After=network.target docker.service local-fs.target
Requires=docker.service
Wants=local-fs.target

[Service]
Type=forking
WorkingDirectory=/opt/LiveORC
Environment=HOME=/home/ubuntu
Environment=USER=ubuntu
Environment=AWS_DEFAULT_REGION=us-east-1
ExecStartPre=/bin/sleep 10
ExecStart=/opt/LiveORC/start-liveorc.sh
ExecStop=/opt/LiveORC/liveorc.sh stop
Restart=on-failure
RestartSec=30
User=ubuntu
Group=ubuntu

[Install]
WantedBy=multi-user.target
EOF

# First stop any manually running LiveORC instance
./liveorc.sh stop

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable liveorc.service
sudo systemctl start liveorc.service

# Check service status
sudo systemctl status liveorc.service

# Test auto-start with reboot
sudo reboot

# Wait 2-3 minutes, then reconnect via Session Manager

# After reconnecting, switch to ubuntu user
sudo su - ubuntu

# Verify LiveORC started automatically
sudo systemctl status liveorc.service
docker ps

# If the service failed, check logs for troubleshooting
sudo journalctl -u liveorc.service -f

# Common issues and solutions:
# 1. S3 mount not ready: Service waits for S3 mount before starting
# 2. Storage endpoint errors: Fixed by disabling MinIO environment variables
# 3. Permission issues: Service runs as ubuntu user with proper environment
```

**Understanding LiveORC Storage Backend Configuration:**

LiveORC supports multiple storage backend modes:
1. **MinIO mode** (default): Creates virtualized MinIO storage bucket at http://storage:9000/
2. **Local filesystem mode**: Uses `--storage-local` to write to local folders
3. **Cloud storage mode**: Uses `--storage-host`, `--storage-port`, etc. for external storage services

**Our Approach: S3FS Mounted Filesystem**

We use s3fs to mount the S3 bucket as a local filesystem:
- **s3fs** mounts the S3 bucket at `/mnt/s3-storage`
- **`--storage-local`** flag tells LiveORC to use filesystem mode
- **`--storage-dir /mnt/s3-storage`** specifies the mount point

This approach allows LiveORC to write directly to S3 through the filesystem interface.

### Step 7.6: Verify LiveORC is Running
```bash
# Check if LiveORC containers are running
docker ps

# View LiveORC logs
docker logs liveorc_webapp

# Check LiveORC status
docker ps

# Test health endpoint (replace with your domain/IP)
curl -k https://liveorc.yourdomain.com/health
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

## 🔍 Phase 9: Monitoring and Maintenance *** NOT YET COMPLETED ***

### Step 9.1: Set Up CloudWatch Monitoring *** NOT YET COMPLETED ***
1. In AWS Console, go to CloudWatch
2. Click "Dashboards" → "Create dashboard"
3. **Dashboard name:** `LiveORC-Monitoring`
4. Add widgets for:
   - EC2 CPU Utilization
   - EC2 Network In/Out
   - S3 Bucket Size
   - EC2 Status Checks

### Step 9.2: Create Billing Alerts *** NOT YET COMPLETED ***
1. In CloudWatch, go to "Alarms"
2. Click "Create alarm"
3. Select "Billing" → "Total Estimated Charge"
4. Set threshold to $200 (or your preferred limit)
5. Create SNS topic for notifications
6. Add your email address

### Step 9.3: Regular Maintenance Tasks

**Daily Checks:**
```bash
# Check system status
docker ps
df -h  # Check disk space
free -h  # Check memory

# Check recent logs
docker logs liveorc_webapp

# Check LiveORC dashboard
curl -k https://liveorc.yourdomain.com/health
```

**Weekly Maintenance:**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Check LiveORC status
docker ps

# Backup data (LiveORC handles database internally)
# S3 storage is already backed up automatically

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

