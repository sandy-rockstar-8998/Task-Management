# Deployment Guide

## Local Development

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```
   Access at: http://localhost:8000

---

## Deploy to Render.com

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Create Render Service
1. Go to [render.com](https://render.com)
2. Sign up and connect your GitHub account
3. Click **New +** → **Web Service**
4. Select your GitHub repository
5. Configure:
   - **Name**: TaskProject
   - **Environment**: Python 3
   - **Region**: Choose nearest
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn TaskProject.wsgi --log-file -`

### Step 3: Add Environment Variables
In Render dashboard, go to **Environment**:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Step 4: Deploy
Click **Deploy** button

---

## Deploy to Railway.app

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub**
3. Select your repository
4. Railway auto-detects Django

### Step 3: Add Environment Variables
In Railway dashboard:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHON_VERSION=3.12
```

### Step 4: Deploy
Railway auto-deploys on push to main branch

---

## Deploy to PythonAnywhere.com

1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to **Web** → **Add a new web app**
3. Choose **Manual configuration** with Python 3.12
4. Clone your repo and create virtual environment
5. Configure web app pointing to `TaskProject.wsgi:application`
6. Configure static/media files
7. Reload web app

---

## Production Checklist

- [ ] DEBUG = False
- [ ] Set SECRET_KEY environment variable
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for sensitive data
- [ ] Set up database (PostgreSQL recommended for production)
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Set up HTTPS/SSL
- [ ] Configure logging and monitoring

---

## Troubleshooting

**Static files not loading?**
```bash
python manage.py collectstatic --noinput
```

**Database errors?**
```bash
python manage.py migrate
```

**500 Error?**
Check logs in deployment dashboard for detailed error messages.
