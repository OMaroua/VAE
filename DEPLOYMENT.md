# Deployment Guide

This guide explains how to make your VAE denoising interface accessible beyond localhost.

## Option 1: Local Network Access (Simplest)

The application is already configured to accept connections from your local network.

### Steps:

1. **Find your computer's IP address:**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Or use
   hostname -I
   
   # Windows
   ipconfig
   ```

2. **Start the application:**
   ```bash
   python3 app.py
   ```

3. **Access from other devices on the same network:**
   - From your computer: `http://localhost:5000`
   - From other devices: `http://YOUR_IP_ADDRESS:5000`
   - Example: `http://192.168.1.100:5000`

### Firewall Configuration:

**macOS:**
- System Settings → Network → Firewall
- Allow incoming connections for Python

**Linux:**
```bash
sudo ufw allow 5000/tcp
```

**Windows:**
- Windows Defender Firewall → Allow an app
- Allow Python through firewall

---

## Option 2: Public Access with ngrok (Quick & Easy)

ngrok creates a secure tunnel to your local server, making it publicly accessible.

### Steps:

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/download
   ```

2. **Start your Flask app:**
   ```bash
   python3 app.py
   ```

3. **In a new terminal, start ngrok:**
   ```bash
   ngrok http 5000
   ```

4. **Access your app:**
   - ngrok will provide a public URL like: `https://abc123.ngrok.io`
   - Share this URL with anyone
   - The URL changes each time you restart ngrok (unless you have a paid account)

**Note:** Free ngrok URLs are temporary. For permanent URLs, consider ngrok's paid plans.

---

## Option 3: Cloud Deployment (Production)

### 3.1 Deploy to Heroku

1. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

2. **Create required files:**

   `Procfile`:
   ```
   web: gunicorn app:app
   ```

   `runtime.txt`:
   ```
   python-3.9.18
   ```

3. **Update requirements.txt** (add gunicorn):
   ```
   Flask==3.0.0
   tensorflow>=2.13.0
   Pillow>=10.0.0
   numpy>=1.24.0
   werkzeug>=3.0.0
   gunicorn>=21.2.0
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### 3.2 Deploy to AWS EC2

1. **Launch an EC2 instance** (Ubuntu recommended)

2. **SSH into the instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

4. **Clone and set up your application:**
   ```bash
   git clone your-repo
   cd VAE
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt gunicorn
   ```

5. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

6. **Set up Nginx as reverse proxy** (optional but recommended)

### 3.3 Deploy to Google Cloud Platform

1. **Create a Cloud Run service:**
   ```bash
   gcloud run deploy vae-denoising \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. **Or use App Engine** with `app.yaml` configuration

### 3.4 Deploy to Azure

1. **Use Azure App Service:**
   ```bash
   az webapp up --name your-app-name --resource-group your-resource-group
   ```

---

## Option 4: Production Setup with Gunicorn

For production use on your own server:

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Create a startup script** `start.sh`:
   ```bash
   #!/bin/bash
   source venv/bin/activate
   gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
   ```

3. **Make it executable:**
   ```bash
   chmod +x start.sh
   ```

4. **Run:**
   ```bash
   ./start.sh
   ```

5. **Set up as a systemd service** (for auto-start on boot):

   Create `/etc/systemd/system/vae-denoising.service`:
   ```ini
   [Unit]
   Description=VAE Denoising Web Interface
   After=network.target

   [Service]
   User=your-username
   WorkingDirectory=/path/to/VAE
   Environment="PATH=/path/to/VAE/venv/bin"
   ExecStart=/path/to/VAE/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable vae-denoising
   sudo systemctl start vae-denoising
   ```

---

## Security Considerations

When deploying publicly:

1. **Disable debug mode** in production:
   ```python
   app.run(debug=False, host='0.0.0.0', port=port)
   ```

2. **Add authentication** (if needed):
   ```bash
   pip install flask-httpauth
   ```

3. **Use HTTPS** (required for production):
   - Use a reverse proxy (Nginx) with SSL certificates
   - Or use cloud platforms that provide HTTPS automatically

4. **Set up rate limiting:**
   ```bash
   pip install flask-limiter
   ```

5. **Configure CORS** if needed:
   ```bash
   pip install flask-cors
   ```

---

## Quick Reference

| Method | Best For | Difficulty | Cost |
|--------|----------|------------|------|
| Local Network | Testing on same network | Easy | Free |
| ngrok | Quick public demo | Easy | Free (temporary) |
| Heroku | Simple cloud deployment | Medium | Free tier available |
| AWS/GCP/Azure | Production, scalable | Hard | Pay-as-you-go |
| Own Server | Full control | Medium | Server costs |

---

## Troubleshooting

**Can't access from other devices:**
- Check firewall settings
- Ensure both devices are on the same network
- Verify the IP address is correct
- Try disabling VPN if active

**Port already in use:**
- Change the port in `app.py`
- Or kill the process using the port:
  ```bash
  # Find process
  lsof -i :5000
  # Kill it
  kill -9 <PID>
  ```

**Model loading issues on cloud:**
- Ensure model file is included in deployment
- Check file paths are relative, not absolute
- Verify TensorFlow/Keras versions match

