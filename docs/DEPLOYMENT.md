# Deployment Guide for Render

This guide will help you deploy the Text Processing API to Render.

## Prerequisites

- A Render account (sign up at https://render.com)
- Your repository pushed to GitHub, GitLab, or Bitbucket
- Your API token ready

## Quick Deployment Steps

### Method 1: Using Render Dashboard (Recommended)

1. **Log in to Render** and go to your dashboard

2. **Click "New +"** and select **"Web Service"**

3. **Connect your repository:**
   - Select your Git provider (GitHub/GitLab/Bitbucket)
   - Choose the repository containing this project
   - Select the branch (usually `main` or `master`)

4. **Configure the service:**
   - **Name:** `text-processing-api` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** Choose the closest region to your users
   - **Branch:** `main` (or your default branch)
   - **Root Directory:** Leave empty (or `./` if needed)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables:**
   - Click on "Environment" tab
   - Add a new environment variable:
     - **Key:** `API_TOKEN`
     - **Value:** `pridrEspigUVoYlfefruyUPRobr$rEpIprucRUspirlxLYiTA5LRakepiy9qibic`
     - (Or your actual API token)

6. **Configure Health Check (Optional but Recommended):**
   - **Health Check Path:** `/health`

7. **Click "Create Web Service"**

8. **Wait for deployment** - Render will:
   - Install dependencies
   - Build your application
   - Start the service
   - Provide you with a URL (e.g., `https://text-processing-api.onrender.com`)

### Method 2: Using render.yaml (Infrastructure as Code)

If you prefer to use the `render.yaml` file:

1. **Push your code** with `render.yaml` to your repository

2. **Log in to Render** and go to your dashboard

3. **Click "New +"** and select **"Blueprint"**

4. **Connect your repository** and select the branch

5. **Render will automatically detect `render.yaml`** and configure the service

6. **Add the `API_TOKEN` environment variable** in the service settings

7. **Deploy!**

## Post-Deployment

### Verify Deployment

1. **Check the service status** in Render dashboard - should show "Live"

2. **Test the root endpoint:**
   ```bash
   curl https://your-service-name.onrender.com/
   ```

3. **Test the health endpoint:**
   ```bash
   curl https://your-service-name.onrender.com/health
   ```

4. **Access API documentation:**
   - Visit: `https://your-service-name.onrender.com/docs`
   - Or: `https://your-service-name.onrender.com/redoc`

### Test an Endpoint

```bash
curl -X POST "https://your-service-name.onrender.com/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test text to summarize."}'
```

## Environment Variables

### Required
- `API_TOKEN`: Your external API authentication token

### Automatic (Set by Render)
- `PORT`: Automatically set by Render - don't set this manually

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is correct
- Verify Python version compatibility
- Check build logs in Render dashboard

### Service Won't Start
- Verify the start command is correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Check that `main.py` exists in the root directory
- Review service logs in Render dashboard

### API Returns Errors
- Verify `API_TOKEN` environment variable is set correctly
- Check that the external API is accessible
- Review application logs for detailed error messages

### Service Goes to Sleep
- Free tier services on Render sleep after 15 minutes of inactivity
- Upgrade to a paid plan for always-on service
- Or use a service like UptimeRobot to ping your service periodically

## Updating Your Deployment

1. **Push changes** to your repository
2. **Render will automatically detect** the changes
3. **A new deployment will start** automatically
4. **Monitor the deployment** in the Render dashboard

## Custom Domain (Optional)

1. Go to your service settings in Render
2. Click on "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- **Logs:** Available in real-time in the Render dashboard
- **Metrics:** View CPU, memory, and request metrics
- **Alerts:** Set up alerts for service downtime

## Cost Considerations

- **Free Tier:** Services may sleep after inactivity
- **Starter Plan:** $7/month for always-on service
- **See Render pricing** for more details

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Render Support: support@render.com
