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

## Notes

The included database points to an existing repair image path from the original project. The image file itself was not included in the uploaded files, so the package keeps the database reference but cannot restore that missing image.
