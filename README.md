# User Verification REST API

A simple Python REST API that verifies user existence by checking usernames from API headers against a local SQLite database.

## Features

- ✅ User verification via API header
- ✅ Local SQLite database
- ✅ Pre-populated with sample users (including "toms")
- ✅ Returns 200 for existing users, 404 for non-existing users
- ✅ Additional endpoints to list and add users

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the API

1. Start the server:
```bash
python app.py
```

2. The API will start on `http://127.0.0.1:5000`

The database will be automatically initialized with sample users: `toms`, `alice`, `bob`, `charlie`

## API Endpoints

### 1. Verify User (Main Endpoint)
**Endpoint:** `GET /api/verify` or `POST /api/verify`

**Headers Required:**
- `X-Username: <username>` or `Username: <username>`

**Responses:**
- `200 OK` - User exists in database
- `404 Not Found` - User does not exist
- `400 Bad Request` - Username header missing

**Example using curl:**
```bash
# User exists (returns 200)
curl -H "X-Username: toms" http://127.0.0.1:5000/api/verify

# User doesn't exist (returns 404)
curl -H "X-Username: john" http://127.0.0.1:5000/api/verify
```

**Example using PowerShell:**
```powershell
# User exists (returns 200)
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/verify" -Headers @{"X-Username"="toms"}

# User doesn't exist (returns 404)
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/verify" -Headers @{"X-Username"="john"}
```

**Example using Python:**
```python
import requests

# User exists (returns 200)
response = requests.get('http://127.0.0.1:5000/api/verify', 
                       headers={'X-Username': 'toms'})
print(response.status_code)  # 200
print(response.json())

# User doesn't exist (returns 404)
response = requests.get('http://127.0.0.1:5000/api/verify', 
                       headers={'X-Username': 'john'})
print(response.status_code)  # 404
```

### 2. List All Users
**Endpoint:** `GET /api/users`

**Response:** `200 OK` with list of all users

**Example:**
```bash
curl http://127.0.0.1:5000/api/users
```

### 3. Add New User
**Endpoint:** `POST /api/users`

**Body:** JSON with username
```json
{
  "username": "newuser"
}
```

**Responses:**
- `201 Created` - User added successfully
- `400 Bad Request` - Username missing
- `409 Conflict` - User already exists

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"newuser\"}" http://127.0.0.1:5000/api/users
```

### 4. Home/Help
**Endpoint:** `GET /`

**Response:** API information and available endpoints

## Database

- **Type:** SQLite (file-based, no separate server needed)
- **File:** `users.db` (created automatically)
- **Table:** `users` with columns: `id`, `username`, `created_at`

### Manual Database Initialization

If you need to reset or manually initialize the database:
```bash
python init_db.py
```

## Testing the API

Once the server is running, test it using any of these methods:

1. **Web Browser:** Visit `http://127.0.0.1:5000/` to see API info

2. **PowerShell:**
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/verify" -Headers @{"X-Username"="toms"}
   ```

3. **Postman:** 
   - Create a GET request to `http://127.0.0.1:5000/api/verify`
   - Add header: `X-Username` with value `toms`

## Project Structure

```
restapi/
├── app.py              # Main Flask application
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── users.db           # SQLite database (created automatically)
```

## Status Codes

- `200 OK` - User found in database
- `201 Created` - User successfully added
- `400 Bad Request` - Missing required header or body parameter
- `404 Not Found` - User not found in database
- `409 Conflict` - User already exists (when adding)

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.
