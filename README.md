# Kontakt — Contact Manager

A full-stack contact management web application built with **Python (Flask)**, **SQLAlchemy**, **SQLite**, and a responsive **HTML/CSS/JS** frontend.

---

## Features

- Add, edit, delete contacts with full validation
- Search contacts by name, email, or company (server-side)
- Filter by category: Work, Personal, Family, Favourites
- Sort A–Z or by most recently added
- Toggle favourite contacts
- Grid and list view
- Export all contacts to CSV
- Persistent storage with SQLite database
- REST API with proper error handling and HTTP status codes

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3.11, Flask 3.0            |
| Database | SQLite + Flask-SQLAlchemy         |
| Frontend | HTML5, CSS3, Vanilla JavaScript   |
| API      | RESTful JSON API (6 endpoints)    |

---

## Project Structure

```
contact-manager/
├── app.py                  # App factory, Flask setup
├── models.py               # SQLAlchemy Contact model
├── routes/
│   ├── __init__.py
│   └── contacts.py         # All API endpoints
├── utils/
│   ├── __init__.py
│   └── validators.py       # Input validation helpers
├── templates/
│   └── index.html          # Frontend GUI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/harshinidevinakka-del/contact-manager-python.git
cd contact-manager-python
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask server
```bash
python app.py
```

Server starts at: `http://localhost:5000`

### 5. Open the frontend
Open `templates/index.html` in your browser, or visit `http://localhost:5000` if you add a route to serve it.

---

## API Endpoints

| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| GET    | `/api/contacts`                   | List all contacts (supports `?q=`, `?category=`, `?sort=`) |
| POST   | `/api/contacts`                   | Create a new contact     |
| PUT    | `/api/contacts/<id>`              | Update a contact         |
| DELETE | `/api/contacts/<id>`              | Delete a contact         |
| PATCH  | `/api/contacts/<id>/favourite`    | Toggle favourite         |
| GET    | `/api/contacts/export`            | Download contacts as CSV |
| GET    | `/api/stats`                      | Get contact counts       |

### Example: Create a contact
```bash
curl -X POST http://localhost:5000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane@example.com",
    "phone": "+91 98765 43210",
    "category": "work",
    "company": "Acme Corp"
  }'
```

### Example: Search contacts
```bash
curl "http://localhost:5000/api/contacts?q=jane&sort=name"
```

---

## Contact Data Model

| Field        | Type    | Required | Notes                          |
|--------------|---------|----------|--------------------------------|
| firstName    | string  | Yes      | Auto-capitalized               |
| lastName     | string  | Yes      | Auto-capitalized               |
| email        | string  | Yes      | Must be unique, lowercased     |
| phone        | string  | No       | Accepts international formats  |
| company      | string  | No       |                                |
| address      | string  | No       |                                |
| category     | string  | No       | work / personal / family       |
| notes        | text    | No       |                                |
| is_favorite  | boolean | No       | Default: false                 |

---

## Author

**Harshinidevinakka** — [GitHub](https://github.com/harshinidevinakka-del)
