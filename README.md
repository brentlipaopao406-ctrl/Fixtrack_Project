# FixTrack - Complete Repair Management System

A Django-based repair and maintenance management system designed for school and community repair requests.

## Included features

### Repair requests
- Submit a repair request
- Category, location, problem, priority, status, and optional image
- View all requests
- Search requests
- Sort by priority
- View ticket details
- Delete requests (staff only)

### Technician management
- Add technician
- Edit technician
- Activate/deactivate technician
- Delete technician
- Store specialization, phone, and email
- Assign technicians to repair requests

### Repair history
- Automatic history entry when a status changes
- Automatic history entry when a technician is assigned
- Old status and new status
- User who made the change
- Technician involved
- Notes
- Timestamp

### Category management
- Add, edit, activate/deactivate, and delete categories
- Dashboard request form loads active categories dynamically

### Dashboard
- Total requests
- Pending
- In progress
- Completed
- Cancelled
- Recent repair requests
- Polished responsive design

## Existing data

`db.sqlite3` is your supplied database. It contains the existing Django users and your existing repair request data.
`db_original_backup.sqlite3` is an unchanged backup of that database.

## First run

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Deploy to Vercel

Vercel's filesystem is temporary, so repair photos must be stored outside the
function. This project uses Cloudinary for persistent images and PostgreSQL for
application data when running on Vercel.

1. Create a Cloudinary account and a PostgreSQL database (for example, using
   Neon or Supabase).
2. Import this repository into Vercel and add these project environment
   variables for Production (and Preview if needed):
   - `SECRET_KEY`: a new, private Django secret key.
   - `DATABASE_URL`: the PostgreSQL connection URL from your database provider.
   - `CLOUDINARY_URL`: the Cloudinary URL from your Cloudinary dashboard.
   - `ALLOWED_HOSTS`: `.vercel.app` and any custom domain, comma-separated.
   - `CSRF_TRUSTED_ORIGINS`: `https://*.vercel.app` and any custom domain as a
     full `https://` origin, comma-separated.
3. Import the repository into Vercel and deploy. Vercel detects Django from
   `manage.py`, uses `repair_system/wsgi.py` as the application entry point,
   and collects files from `STATIC_ROOT` for its CDN.
4. Apply database migrations against the production database before using the
   app:

   ```powershell
   $env:DATABASE_URL = "your-production-postgres-url"
   python manage.py migrate
   ```

   Create an administrator with `python manage.py createsuperuser` using the
   same `DATABASE_URL`.

The existing local SQLite database is not deployed automatically. The deployed
app starts with a fresh PostgreSQL database; migrate or import any data you
want to keep. Image uploads are stored in Cloudinary and remain available
across Vercel deployments.

## Notes

The included database points to an existing repair image path from the original project. The image file itself was not included in the uploaded files, so the package keeps the database reference but cannot restore that missing image.
