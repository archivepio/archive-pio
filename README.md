# Archive-PIO Backend

REST API backend for the **Archive-PIO** system — a digital request management platform for the Public Information Office of Gumaca, Quezon.

Built with **Django 4.2** + **Django REST Framework** + **PostgreSQL**.

---

## 📋 Features

- JWT-based authentication (login, register, token refresh)
- Role-based access control (citizen, staff, admin)
- Request submission and tracking system
- Staff approval workflow with email notifications
- Activity logging for all actions
- File/media upload management
- Event scheduling linked to requests
- Dashboard analytics (totals, trends, geolocation map data)
- **Swagger API documentation** at `/api/docs/`

---

## ⚙️ Setup Instructions

### 1. Clone and navigate

```bash
cd archive-pio
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Copy the example below and fill in your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=archive_pio_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 5. Create PostgreSQL database

```sql
CREATE DATABASE archive_pio_db;
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 8. Start development server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

| Method         | Endpoint                             | Description             | Access |
| -------------- | ------------------------------------ | ----------------------- | ------ |
| POST           | `/api/auth/register/`                | Register new user       | Public |
| POST           | `/api/auth/login/`                   | Login → get JWT tokens  | Public |
| POST           | `/api/auth/refresh/`                 | Refresh access token    | Public |
| GET/PUT        | `/api/auth/me/`                      | Get/update own profile  | Auth   |
| GET/POST       | `/api/requests/`                     | List / submit requests  | Auth   |
| GET/PUT/DELETE | `/api/requests/{id}/`                | Manage a request        | Auth   |
| GET/POST       | `/api/approvals/`                    | List / create approvals | Staff+ |
| GET/POST       | `/api/requesters/`                   | Manage requesters       | Auth   |
| GET/POST       | `/api/attachments/`                  | Upload attachments      | Auth   |
| GET/POST       | `/api/publications/`                 | Manage publications     | Auth   |
| GET/POST       | `/api/processing-logs/`              | Processing log entries  | Auth   |
| GET/POST       | `/api/events/`                       | Event management        | Auth   |
| GET/POST       | `/api/media/`                        | Media file uploads      | Auth   |
| GET            | `/api/notifications/`                | User notifications      | Auth   |
| PATCH          | `/api/notifications/{id}/mark_read/` | Mark notification read  | Auth   |
| PATCH          | `/api/notifications/mark_all_read/`  | Mark all read           | Auth   |
| GET            | `/api/notifications/unread_count/`   | Unread count            | Auth   |
| GET            | `/api/logs/`                         | Activity log            | Auth   |
| GET            | `/api/dashboard/stats/`              | Dashboard statistics    | Auth   |
| GET/POST       | `/api/users/`                        | User management         | Staff+ |
| GET/POST       | `/api/roles/`                        | Role management         | Staff+ |
| GET            | `/api/docs/`                         | Swagger UI              | Auth   |

---

## 🔐 Roles

| Role      | Permissions                                                       |
| --------- | ----------------------------------------------------------------- |
| `citizen` | Submit and view own requests, receive notifications               |
| `staff`   | All citizen permissions + approve/reject requests, manage content |
| `admin`   | Full access including user and role management                    |

---

## 📁 Project Structure

```
archive-pio/
├── config/         # Django settings, URLs, WSGI/ASGI
├── users/          # Custom user model, auth, roles, permissions
├── requests_app/   # Core request management
├── events/         # Event scheduling
├── media/          # File/media uploads
├── logs/           # Activity logging
├── notifications/  # In-app + email notifications
├── dashboard/      # Analytics & statistics API
├── requirements.txt
└── manage.py
```

---

## 🛠️ Tech Stack

- Python 3.x
- Django 4.2
- Django REST Framework
- SimpleJWT
- PostgreSQL + psycopg2
- drf-spectacular (Swagger docs)
- geopy (geocoding)
- Pillow, reportlab, openpyxl
"# archive-pio" 
"# archive-pio" 
