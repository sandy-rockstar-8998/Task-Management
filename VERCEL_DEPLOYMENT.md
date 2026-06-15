# Vercel Deployment Guide

## Prerequisites
- Vercel account (https://vercel.com)
- GitHub account with this repository pushed
- Vercel CLI installed (optional but recommended)

## Setup Steps

### 1. Set Environment Variables in Vercel

Go to your Vercel project settings and add these environment variables:

```
DEBUG = False
DJANGO_SETTINGS_MODULE = TaskProject.settings
SECRET_KEY = <generate-a-secure-key>
ALLOWED_HOSTS = .vercel.app,localhost
EMAIL_HOST_USER = <your-gmail>
EMAIL_HOST_PASSWORD = <your-app-specific-password>
```

To generate a secure SECRET_KEY, run:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### 3. Deploy with Vercel

**Option A: Using Vercel Dashboard**
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure project settings (framework: Other)
5. Add environment variables from Step 1
6. Click Deploy

**Option B: Using Vercel CLI**
```bash
npm install -g vercel
vercel
# Follow the prompts
```

## Troubleshooting

### If you get "ModuleNotFoundError: No module named 'django'"
- Verify requirements.txt exists and contains Django
- Check that all environment variables are set in Vercel dashboard
- Rebuild/redeploy the project

### If static files aren't loading
- Run `python manage.py collectstatic --noinput` locally to verify
- Check that STATICFILES_STORAGE is set to whitenoise
- Clear Vercel cache and redeploy

### Database Issues
- For SQLite: Database is stored in ephemeral filesystem, data will be lost on redeploy
- **Recommended**: Use PostgreSQL with a managed service
  - Update DATABASES in settings.py
  - Add DATABASE_URL to environment variables

## Important Notes

1. **DEBUG Mode**: Must be False in production
2. **Secret Key**: Change the SECRET_KEY to a secure random value
3. **Static Files**: Are served by WhiteNoise middleware
4. **Database**: SQLite works but data is ephemeral. Use PostgreSQL for production.
5. **Email**: Configure your Gmail app-specific password in environment variables

## Vercel Project Files Created

- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel build configuration
- `.env.example` - Example environment variables
- `build.sh` - Build script for static files and migrations
