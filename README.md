# MjrPrj — Computer Asset & Credential Management REST API

A Django REST Framework–based backend service that provides APIs for tracking and managing computer hardware/software inventory across Unix/macOS and Windows endpoints, as well as authenticating user credentials. Designed for deployment on Heroku using Gunicorn and SQLite/WhiteNoise.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Data Models](#data-models)
   - [OS_UNIX](#os_unix-model)
   - [OS_Windows](#os_windows-model)
   - [CRED_VERIFY](#cred_verify-model)
5. [API Endpoints](#api-endpoints)
   - [Unix / macOS Endpoints](#unix--macos-endpoints-os_unix)
   - [Windows Endpoints](#windows-endpoints-os_windows)
   - [Credential Verification Endpoints](#credential-verification-endpoints-cred_verify)
6. [Request & Response Examples](#request--response-examples)
7. [Prerequisites](#prerequisites)
8. [Local Development Setup](#local-development-setup)
9. [Running the Application Locally](#running-the-application-locally)
10. [Database Migrations](#database-migrations)
11. [Configuration & Settings](#configuration--settings)
12. [Deploying to Heroku](#deploying-to-heroku)
13. [Dependencies](#dependencies)
14. [Project Conventions](#project-conventions)
15. [Security Considerations](#security-considerations)

---

## Project Overview

**MjrPrj** (Major Project) is a REST API built with Django 3.2 and Django REST Framework. It serves as a centralized backend for:

- **Unix/macOS Computer Inventory (`os_unix`)** — Stores and retrieves detailed hardware and software metadata about macOS/Unix machines in a managed environment. Each record tracks the machine's identity (serial number, hardware UUID, provisioning UDID, hostname, IP address, MAC address), its operating system version, build version, and a complete list of installed software along with counts of authenticated vs. unauthenticated software packages.

- **Windows Computer Inventory (`os_windows`)** — Mirrors the same inventory concept for Windows endpoints. Records include computer name, Windows product key, hostname, IP address, MAC address, and software inventory with authentication metrics.

- **Credential Verification (`cred_verify`)** — Manages user login credentials. Stores user profiles with names, email addresses, numeric user IDs, hashed passwords, and role-based access types (Admin, Teacher, or Student).

The API is designed to be consumed by client-side agents (e.g., scripts running on managed machines) or administrative dashboards that need programmatic access to endpoint inventory data.

---

## Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.9.16 |
| Web Framework | Django | 3.2.19 |
| REST API Framework | Django REST Framework | 3.14.0 |
| WSGI Server | Gunicorn | 20.1.0 |
| ASGI Support | asgiref | 3.6.0 |
| Database | SQLite (default) | — |
| Static Files | WhiteNoise | 6.4.0 |
| Cloud Storage | boto3 / botocore (AWS S3) | 1.26.126 / 1.29.126 |
| Multi-select Fields | django-multiselectfield | 0.1.12 |
| Code Style | autopep8, pycodestyle | 2.0.2 / 2.10.0 |
| Deployment Platform | Heroku | — |

---

## Project Structure

```
MjrPrj/
├── manage.py                     # Django management utility entry point
├── Procfile                      # Heroku process definition (Gunicorn)
├── runtime.txt                   # Heroku Python runtime specification
├── requirements.txt              # Python package dependencies
├── db.sqlite3                    # SQLite database file (development)
│
├── mjrprj_api/                   # Core Django project package
│   ├── __init__.py
│   ├── settings.py               # Project-wide Django settings
│   ├── urls.py                   # Root URL configuration (routes to apps)
│   ├── wsgi.py                   # WSGI entry point for deployment
│   └── asgi.py                   # ASGI entry point (async support)
│
├── os_unix/                      # App: Unix/macOS computer inventory
│   ├── __init__.py
│   ├── admin.py                  # Django admin registration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # OS_UNIX database model
│   ├── serializers.py            # DRF serializer for OS_UNIX
│   ├── views.py                  # API view functions
│   ├── urls.py                   # URL patterns for os_unix endpoints
│   ├── tests.py                  # Unit tests
│   └── migrations/               # Database migration files
│
├── os_windows/                   # App: Windows computer inventory
│   ├── __init__.py
│   ├── admin.py                  # Django admin registration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # OS_Windows database model
│   ├── serializers.py            # DRF serializer for OS_Windows
│   ├── views.py                  # API view functions
│   ├── urls.py                   # URL patterns for os_windows endpoints
│   ├── tests.py                  # Unit tests
│   └── migrations/               # Database migration files
│
└── cred_verify/                  # App: User credential management
    ├── __init__.py
    ├── admin.py                  # Django admin registration
    ├── apps.py                   # App configuration
    ├── models.py                 # CRED_VERIFY database model
    ├── serializers.py            # DRF serializer for CRED_VERIFY
    ├── views.py                  # API view functions
    ├── urls.py                   # URL patterns for cred_verify endpoints
    ├── tests.py                  # Unit tests
    └── migrations/               # Database migration files
```

---

## Data Models

### OS_UNIX Model

Defined in `os_unix/models.py`. Represents a single Unix/macOS managed endpoint.

| Field | Type | Description |
|---|---|---|
| `computer_id` | AutoField (PK) | Auto-incremented primary key uniquely identifying the computer record |
| `username` | IntegerField | Numeric identifier of the user associated with this machine |
| `computer_name` | CharField(100) | Human-readable name assigned to the computer (e.g., MacBook-Pro-John) |
| `os_version` | CharField(100) | Full macOS/Unix operating system version string (e.g., `macOS 13.3.1`) |
| `serial_number` | CharField(30) | Hardware serial number printed on the machine |
| `build_version` | CharField(100) | Specific OS build identifier (e.g., `22E261`) |
| `hardware_uuid` | CharField(100) | Unique hardware UUID assigned to the logic board |
| `provisioning_udid` | CharField(100) | Unique Device Identifier used for MDM provisioning |
| `hostname` | CharField(100) | Network hostname of the machine (e.g., `johnsmbp.local`) |
| `ip_address` | GenericIPAddressField | Current IPv4 or IPv6 address of the machine |
| `mac_address` | CharField(100) | MAC address of the primary network interface |
| `softwares_installed` | TextField | Serialized list or newline-delimited string of all installed software packages |
| `software_count` | IntegerField | Total number of installed software packages |
| `authentic_software_count` | IntegerField | Number of software packages that passed authenticity checks |
| `unauthentic_software_count` | IntegerField | Number of software packages that failed authenticity checks |

---

### OS_Windows Model

Defined in `os_windows/models.py`. Represents a single Windows managed endpoint.

| Field | Type | Description |
|---|---|---|
| `computer_id` | AutoField (PK) | Auto-incremented primary key uniquely identifying the computer record |
| `username` | IntegerField | Numeric identifier of the user associated with this machine |
| `computer_name` | CharField(100) | Human-readable name assigned to the computer (e.g., DESKTOP-ABC123) |
| `product_key` | CharField(30) | Windows product activation key (e.g., `XXXXX-XXXXX-XXXXX-XXXXX-XXXXX`) |
| `hostname` | CharField(100) | Network hostname of the machine |
| `ip_address` | GenericIPAddressField | Current IPv4 or IPv6 address of the machine |
| `mac_address` | CharField(100) | MAC address of the primary network interface |
| `softwares_installed` | TextField | Serialized list or newline-delimited string of all installed software packages |
| `software_count` | IntegerField | Total number of installed software packages |
| `authentic_software_count` | IntegerField | Number of software packages that passed authenticity checks |
| `unauthentic_software_count` | IntegerField | Number of software packages that failed authenticity checks |

---

### CRED_VERIFY Model

Defined in `cred_verify/models.py`. Stores login credentials and role information for users of the system.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField (PK) | Auto-incremented primary key (Django default) |
| `name` | CharField(100) | Full name of the user |
| `email` | EmailField | User's email address (validated email format) |
| `username` | IntegerField | Numeric identifier for the user |
| `password` | CharField(100) | User's password (**currently stored as plain text** — see [Security Considerations](#security-considerations)) |
| `type_login` | CharField(1) | Role of the user: `A` = Admin, `T` = Teacher, `S` = Student |

---

## API Endpoints

All responses are returned as JSON. The base URL in production is your deployed Heroku app URL (e.g., `https://your-app.herokuapp.com`). For local development it is `http://127.0.0.1:8000`.

### Unix / macOS Endpoints (`os_unix`)

#### `GET /os_unix/`

Retrieve a list of all Unix/macOS computer records stored in the database.

- **Method:** `GET`
- **URL:** `/os_unix/`
- **Query Parameters:**
  - `name` *(optional)*: Filter records by name (case-insensitive substring match).
- **Response:** `200 OK` — JSON array of OS_UNIX objects.

---

#### `POST /os_unix/`

Create a new Unix/macOS computer record.

- **Method:** `POST`
- **URL:** `/os_unix/`
- **Request Body:** JSON object with all required OS_UNIX fields (see [OS_UNIX Model](#os_unix-model)).
- **Response:**
  - `201 Created` — JSON object of the newly created record.
  - `400 Bad Request` — JSON object describing validation errors.

---

#### `DELETE /os_unix/`

Delete **all** Unix/macOS computer records from the database.

- **Method:** `DELETE`
- **URL:** `/os_unix/`
- **Response:** `204 No Content` — JSON message confirming how many records were deleted.

> ⚠️ **Warning:** This operation is destructive and irreversible. It deletes every record in the `os_unix` table.

---

#### `GET /os_unix/<username>/`

Retrieve all Unix/macOS computer records associated with a specific username (numeric user ID).

- **Method:** `GET`
- **URL:** `/os_unix/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) to filter by.
- **Response:** `200 OK` — JSON array of matching OS_UNIX objects.

---

#### `DELETE /os_unix/<username>/`

Delete all Unix/macOS computer records associated with a specific username.

- **Method:** `DELETE`
- **URL:** `/os_unix/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) whose records should be deleted.
- **Response:** `204 No Content` — JSON message confirming deletion.

---

#### `PUT /os_unix/<computer_name>/update/`

Update an existing Unix/macOS computer record identified by its `computer_name`.

- **Method:** `PUT`
- **URL:** `/os_unix/<str:name>/update/`
- **URL Parameters:**
  - `name`: The `computer_name` of the record to update.
- **Request Body:** Full JSON object with all OS_UNIX fields (full replacement update).
- **Response:**
  - `200 OK` — JSON object of the updated record.
  - `400 Bad Request` — JSON object describing validation errors.
  - `404 Not Found` — JSON message if no record with that `computer_name` exists.

---

### Windows Endpoints (`os_windows`)

#### `GET /os_windows/`

Retrieve a list of all Windows computer records stored in the database.

- **Method:** `GET`
- **URL:** `/os_windows/`
- **Query Parameters:**
  - `name` *(optional)*: Filter records by name (case-insensitive substring match).
- **Response:** `200 OK` — JSON array of OS_Windows objects.

---

#### `POST /os_windows/`

Create a new Windows computer record.

- **Method:** `POST`
- **URL:** `/os_windows/`
- **Request Body:** JSON object with all required OS_Windows fields (see [OS_Windows Model](#os_windows-model)).
- **Response:**
  - `201 Created` — JSON object of the newly created record.
  - `400 Bad Request` — JSON object describing validation errors.

---

#### `DELETE /os_windows/`

Delete **all** Windows computer records from the database.

- **Method:** `DELETE`
- **URL:** `/os_windows/`
- **Response:** `204 No Content` — JSON message confirming how many records were deleted.

> ⚠️ **Warning:** This operation is destructive and irreversible. It deletes every record in the `os_windows` table.

---

#### `GET /os_windows/<username>/`

Retrieve all Windows computer records associated with a specific username (numeric user ID).

- **Method:** `GET`
- **URL:** `/os_windows/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) to filter by.
- **Response:** `200 OK` — JSON array of matching OS_Windows objects.

---

#### `DELETE /os_windows/<username>/`

Delete all Windows computer records associated with a specific username.

- **Method:** `DELETE`
- **URL:** `/os_windows/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) whose records should be deleted.
- **Response:** `204 No Content` — JSON message confirming deletion.

---

#### `PUT /os_windows/<computer_name>/update/`

Update an existing Windows computer record identified by its `computer_name`.

- **Method:** `PUT`
- **URL:** `/os_windows/<str:name>/update/`
- **URL Parameters:**
  - `name`: The `computer_name` of the record to update.
- **Request Body:** Full JSON object with all OS_Windows fields (full replacement update).
- **Response:**
  - `200 OK` — JSON object of the updated record.
  - `400 Bad Request` — JSON object describing validation errors.
  - `404 Not Found` — JSON message if no record with that `computer_name` exists.

---

### Credential Verification Endpoints (`cred_verify`)

#### `GET /cred_verify/`

Retrieve a list of all credential/user records stored in the database.

- **Method:** `GET`
- **URL:** `/cred_verify/`
- **Query Parameters:**
  - `name` *(optional)*: Filter records by name (case-insensitive substring match).
- **Response:** `200 OK` — JSON array of CRED_VERIFY objects.

---

#### `POST /cred_verify/`

Create a new credential/user record.

- **Method:** `POST`
- **URL:** `/cred_verify/`
- **Request Body:** JSON object with all required CRED_VERIFY fields (see [CRED_VERIFY Model](#cred_verify-model)).
- **Response:**
  - `201 Created` — JSON object of the newly created record.
  - `400 Bad Request` — JSON object describing validation errors.

---

#### `DELETE /cred_verify/`

Delete **all** credential/user records from the database.

- **Method:** `DELETE`
- **URL:** `/cred_verify/`
- **Response:** `204 No Content` — JSON message confirming how many records were deleted.

> ⚠️ **Warning:** This operation is destructive and irreversible. It deletes every record in the `cred_verify` table.

---

#### `GET /cred_verify/<username>/`

Retrieve all credential records associated with a specific username (numeric user ID).

- **Method:** `GET`
- **URL:** `/cred_verify/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) to filter by.
- **Response:** `200 OK` — JSON array of matching CRED_VERIFY objects.

---

#### `DELETE /cred_verify/<username>/`

Delete all credential records associated with a specific username.

- **Method:** `DELETE`
- **URL:** `/cred_verify/<str:name>/`
- **URL Parameters:**
  - `name`: The numeric username (user ID) whose records should be deleted.
- **Response:** `204 No Content` — JSON message confirming deletion.

---

## Request & Response Examples

### Create a Unix/macOS Computer Record

**Request:**
```http
POST /os_unix/
Content-Type: application/json

{
    "username": 1001,
    "computer_name": "MacBook-Pro-Alice",
    "os_version": "macOS 13.3.1",
    "serial_number": "C02XG1JYJGH5",
    "build_version": "22E261",
    "hardware_uuid": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
    "provisioning_udid": "00008103-001A2B3C4D5E001E",
    "hostname": "alices-mbp.local",
    "ip_address": "192.168.1.42",
    "mac_address": "a4:83:e7:1b:2c:3d",
    "softwares_installed": "Python 3.9\nNode.js 18\nVSCode 1.78\nChrome 113",
    "software_count": 4,
    "authentic_software_count": 4,
    "unauthentic_software_count": 0
}
```

**Response (`201 Created`):**
```json
{
    "computer_id": 1,
    "username": 1001,
    "computer_name": "MacBook-Pro-Alice",
    "os_version": "macOS 13.3.1",
    "serial_number": "C02XG1JYJGH5",
    "build_version": "22E261",
    "hardware_uuid": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
    "provisioning_udid": "00008103-001A2B3C4D5E001E",
    "hostname": "alices-mbp.local",
    "ip_address": "192.168.1.42",
    "mac_address": "a4:83:e7:1b:2c:3d",
    "softwares_installed": "Python 3.9\nNode.js 18\nVSCode 1.78\nChrome 113",
    "software_count": 4,
    "authentic_software_count": 4,
    "unauthentic_software_count": 0
}
```

---

### Create a Windows Computer Record

**Request:**
```http
POST /os_windows/
Content-Type: application/json

{
    "username": 1002,
    "computer_name": "DESKTOP-BOB123",
    "product_key": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
    "hostname": "DESKTOP-BOB123",
    "ip_address": "192.168.1.55",
    "mac_address": "b8:27:eb:4a:5c:6d",
    "softwares_installed": "Office 365\nChrome 113\nVLC 3.0\nPython 3.10",
    "software_count": 4,
    "authentic_software_count": 3,
    "unauthentic_software_count": 1
}
```

**Response (`201 Created`):**
```json
{
    "computer_id": 1,
    "username": 1002,
    "computer_name": "DESKTOP-BOB123",
    "product_key": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
    "hostname": "DESKTOP-BOB123",
    "ip_address": "192.168.1.55",
    "mac_address": "b8:27:eb:4a:5c:6d",
    "softwares_installed": "Office 365\nChrome 113\nVLC 3.0\nPython 3.10",
    "software_count": 4,
    "authentic_software_count": 3,
    "unauthentic_software_count": 1
}
```

---

### Create a Credential Record

> ⚠️ **Security Warning:** The current implementation stores the `password` field as plain text. Before using this in any real environment, passwords must be hashed. See [Security Considerations](#security-considerations).

**Request:**
```http
POST /cred_verify/
Content-Type: application/json

{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "username": 1001,
    "password": "securepassword123",
    "type_login": "T"
}
```

**Response (`201 Created`):**
```json
{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "username": 1001,
    "password": "securepassword123",
    "type_login": "T"
}
```

---

### Get All Unix Records

**Request:**
```http
GET /os_unix/
```

**Response (`200 OK`):**
```json
[
    {
        "computer_id": 1,
        "username": 1001,
        "computer_name": "MacBook-Pro-Alice",
        "os_version": "macOS 13.3.1",
        ...
    }
]
```

---

### Update a Unix Record by Computer Name

**Request:**
```http
PUT /os_unix/MacBook-Pro-Alice/update/
Content-Type: application/json

{
    "username": 1001,
    "computer_name": "MacBook-Pro-Alice",
    "os_version": "macOS 13.4.0",
    "serial_number": "C02XG1JYJGH5",
    ...
}
```

**Response (`200 OK`):** Updated record object.

---

### Delete Records by Username

**Request:**
```http
DELETE /os_unix/1001/
```

**Response (`204 No Content`):**
```json
{
    "message": "Alert was deleted successfully!"
}
```

---

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- **Python 3.9.16** — The exact version specified in `runtime.txt`. It is strongly recommended to use [pyenv](https://github.com/pyenv/pyenv) to manage Python versions.
- **pip** — Python package installer (typically bundled with Python).
- **virtualenv** or **venv** — For creating isolated Python environments.
- **Git** — For cloning the repository.
- *(Optional)* **Heroku CLI** — Required only if you intend to deploy to or manage a Heroku app.

---

## Local Development Setup

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/akulka404/MjrPrj.git
cd MjrPrj
```

### 2. Create and Activate a Virtual Environment

It is best practice to use a virtual environment to isolate project dependencies from your system Python installation.

**On macOS / Linux:**
```bash
python3.9 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
py -3.9 -m venv venv
venv\Scripts\activate.bat
```

**On Windows (PowerShell):**
```powershell
py -3.9 -m venv venv
venv\Scripts\Activate.ps1
```

You should now see `(venv)` prepended to your terminal prompt, indicating the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This installs Django, Django REST Framework, Gunicorn, WhiteNoise, boto3, and all other required packages listed in `requirements.txt`.

---

## Running the Application Locally

### 1. Apply Database Migrations

Before starting the server for the first time, you must apply all database migrations to create the required database tables:

```bash
python manage.py migrate
```

This command creates (or updates) the `db.sqlite3` SQLite database file in the project root with all necessary tables for `os_unix`, `os_windows`, `cred_verify`, and Django's built-in apps (auth, sessions, admin, etc.).

### 2. (Optional) Create a Django Superuser

To access the Django admin interface at `/admin/`, create a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter a username, email address, and password.

### 3. Start the Development Server

```bash
python manage.py runserver
```

By default, Django starts the development server at `http://127.0.0.1:8000/`. You can now send HTTP requests to the API endpoints described in the [API Endpoints](#api-endpoints) section.

To bind to a different port or IP address:

```bash
python manage.py runserver 0.0.0.0:8080
```

### 4. Verify the Server is Running

Open a browser or use `curl` to test a basic endpoint:

```bash
curl http://127.0.0.1:8000/os_unix/
```

An empty JSON array `[]` indicates the server is running correctly and the database is empty.

---

## Database Migrations

When making changes to any of the models (`OS_UNIX`, `OS_Windows`, `CRED_VERIFY`), you must generate and apply new migration files.

### Create New Migrations

After modifying a model, run:

```bash
python manage.py makemigrations
```

Django will detect your changes and generate a new migration file inside the app's `migrations/` directory.

### Apply Migrations

```bash
python manage.py migrate
```

### Check Migration Status

To see which migrations have been applied and which are pending:

```bash
python manage.py showmigrations
```

### Reset the Database (Development Only)

If you need a clean database during development, simply delete `db.sqlite3` and re-run `migrate`:

```bash
rm db.sqlite3
python manage.py migrate
```

---

## Configuration & Settings

All project configuration is contained in `mjrprj_api/settings.py`. Key settings are described below:

### `SECRET_KEY`

A long, random string used by Django to provide cryptographic signing. The key in `settings.py` is the default generated key and **must be replaced** with a securely generated value before deploying to any non-development environment.

Generate a new secret key using Python:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

In production, store this value in an environment variable and read it in `settings.py`:

```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-only-for-dev')
```

### `DEBUG`

Currently set to `False`. During local development, you may wish to set this to `True` to see detailed error pages and enable the DRF browsable API. **Never set `DEBUG = True` in production.**

### `ALLOWED_HOSTS`

Currently set to `['*']`, which allows all hostnames. In production, restrict this to your specific domain(s):

```python
ALLOWED_HOSTS = ['your-app.herokuapp.com', 'yourdomain.com']
```

### `DATABASES`

Configured to use SQLite by default:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For production on Heroku, you would typically use PostgreSQL via the `dj-database-url` package:

```python
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
```

### `STATIC_ROOT` and `STATIC_URL`

WhiteNoise is configured to serve static files. The static root is set to `staticfiles/` in the project root. Before deploying, collect static files:

```bash
python manage.py collectstatic
```

### `INSTALLED_APPS`

The three custom applications are registered here alongside Django's built-in apps:

```python
INSTALLED_APPS = [
    ...
    'os_unix',
    'os_windows',
    'cred_verify',
    'rest_framework',
]
```

### Time Zone

The application uses UTC (`TIME_ZONE = 'UTC'`) with timezone support enabled (`USE_TZ = True`).

---

## Deploying to Heroku

This project is configured for Heroku deployment out of the box with a `Procfile` and `runtime.txt`.

### 1. Install the Heroku CLI

Follow the official [Heroku CLI installation guide](https://devcenter.heroku.com/articles/heroku-cli).

### 2. Log In to Heroku

```bash
heroku login
```

### 3. Create a New Heroku App

```bash
heroku create your-app-name
```

### 4. Set Environment Variables

At minimum, set a secure `SECRET_KEY` on Heroku:

```bash
heroku config:set DJANGO_SECRET_KEY="your-securely-generated-secret-key"
```

### 5. Deploy the Application

```bash
git push heroku main
```

### 6. Run Database Migrations on Heroku

```bash
heroku run python manage.py migrate
```

### 7. (Optional) Create a Superuser on Heroku

```bash
heroku run python manage.py createsuperuser
```

### 8. Open the Application

```bash
heroku open
```

### `Procfile` Details

The `Procfile` instructs Heroku to start the application using Gunicorn:

```
web: gunicorn mjrprj_api.wsgi --log-file -
```

- `web` — Declares a web dyno process type.
- `gunicorn mjrprj_api.wsgi` — Starts Gunicorn using the WSGI application defined in `mjrprj_api/wsgi.py`.
- `--log-file -` — Directs Gunicorn logs to stdout, which Heroku captures in its log stream.

### `runtime.txt` Details

Specifies the exact Python runtime for Heroku:

```
python-3.9.16
```

Heroku will use this file to provision the correct Python version for your dyno.

---

## Dependencies

All dependencies are pinned to specific versions in `requirements.txt` to ensure reproducible builds.

| Package | Version | Purpose |
|---|---|---|
| `Django` | 3.2.19 | Core web framework |
| `djangorestframework` | 3.14.0 | REST API framework built on top of Django |
| `gunicorn` | 20.1.0 | Production WSGI HTTP server for deployment |
| `asgiref` | 3.6.0 | ASGI framework (required by Django for async support) |
| `whitenoise` | 6.4.0 | Serves static files directly from Django without a separate CDN |
| `boto3` | 1.26.126 | AWS SDK for Python — enables S3 file storage integration |
| `botocore` | 1.29.126 | Low-level AWS service client (dependency of boto3) |
| `django-multiselectfield` | 0.1.12 | Adds multi-select field support to Django models |
| `s3transfer` | 0.6.0 | S3 transfer manager (dependency of boto3) |
| `jmespath` | 1.0.1 | JSON query language (dependency of boto3) |
| `python-dateutil` | 2.8.2 | Extended date/time parsing utilities |
| `pytz` | 2023.3 | World timezone definitions for Python |
| `six` | 1.16.0 | Python 2/3 compatibility library |
| `sqlparse` | 0.4.4 | SQL parser used internally by Django |
| `typing_extensions` | 4.5.0 | Backport of newer Python typing features |
| `urllib3` | 1.26.15 | HTTP client library (used by boto3/botocore) |
| `autopep8` | 2.0.2 | Automatically formats Python code to PEP 8 style |
| `pycodestyle` | 2.10.0 | Python style checker (PEP 8 compliance) |
| `tomli` | 2.0.1 | TOML file parser (used by pycodestyle and other tools) |

---

## Project Conventions

- **View naming:** Although the view functions are named `criminal_data` and `criminal_name`, they are general-purpose CRUD handlers for computer inventory and credential records, respectively. This naming reflects the project's origins in a security/asset monitoring context.
- **URL patterns:** The project uses Django's `url()` (regex-based) for collection endpoints (e.g., `/os_unix/`) and `path()` for detail endpoints (e.g., `/os_unix/<name>/`).
- **Serializers:** Each app uses a `ModelSerializer` that exposes all fields of the corresponding model. No nested serializers or hyperlinked relationships are used.
- **HTTP Methods:**
  - Collection endpoints (`/os_unix/`, `/os_windows/`, `/cred_verify/`) support `GET`, `POST`, and `DELETE`.
  - Detail-by-username endpoints (`/<app>/<username>/`) support `GET` and `DELETE`.
  - Update endpoints (`/<app>/<computer_name>/update/`) support `PUT` only (full replacement, no `PATCH`).
- **Response format:** All responses use `JsonResponse` with `safe=False` for list responses (to allow top-level JSON arrays). No pagination is currently implemented.
- **Authentication:** No authentication or permission classes are applied to the API endpoints. All endpoints are publicly accessible. See [Security Considerations](#security-considerations).
- **Admin interface:** All three apps are registered with the Django admin site and accessible at `/admin/` after creating a superuser.

---

## Security Considerations

> ⚠️ **This section describes known security gaps in the current codebase that must be addressed before deploying to any production or shared environment.**

### 1. Plain-Text Password Storage

The `CRED_VERIFY` model stores the `password` field as a plain-text `CharField`. This is a critical security vulnerability — if the database is compromised, all user passwords are immediately exposed.

**Recommended fix:** Use Django's built-in password hashing utilities or the built-in `User` model:

```python
from django.contrib.auth.hashers import make_password, check_password

# Hash before saving:
hashed = make_password("user_plaintext_password")

# Verify during login:
is_valid = check_password("user_plaintext_password", hashed)
```

Alternatively, replace the `CRED_VERIFY` model with Django's built-in `AbstractUser` or `AbstractBaseUser` which handles secure password storage automatically.

### 2. No API Authentication or Authorization

All API endpoints are fully open — any client that can reach the server can read, write, or delete all records without any credentials. This exposes sensitive computer inventory and credential data to unauthorized access.

**Recommended fix:** Add DRF authentication and permission classes in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Or apply permissions per-view using the `@permission_classes` decorator.

### 3. Open `ALLOWED_HOSTS`

`ALLOWED_HOSTS = ['*']` in `settings.py` allows the application to respond to requests with any HTTP `Host` header. This can expose the application to HTTP Host header injection attacks.

**Recommended fix:** Restrict `ALLOWED_HOSTS` to only the domains your application is actually served from:

```python
ALLOWED_HOSTS = ['your-app.herokuapp.com', 'yourdomain.com']
```

### 4. Hardcoded `SECRET_KEY`

The `SECRET_KEY` in `settings.py` is the auto-generated default value committed to source control. Anyone with access to the repository can use this key to forge session cookies and CSRF tokens.

**Recommended fix:** Replace the hardcoded key with an environment variable:

```python
import os
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

Then set the variable in your deployment environment (e.g., `heroku config:set DJANGO_SECRET_KEY=...`).

### 5. Unauthenticated Bulk Delete Endpoints

The `DELETE /os_unix/`, `DELETE /os_windows/`, and `DELETE /cred_verify/` endpoints delete **all records** in their respective tables with no confirmation, pagination, or access control. A single unauthenticated HTTP request can wipe the entire database.

**Recommended fix:** Protect these endpoints with admin-only permissions and consider requiring explicit confirmation parameters.
