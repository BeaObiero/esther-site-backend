# Esther Waweru - Backend API

This is the official backend API for **Esther Waweru's website**, designed to handle user authentication, bookings, contact form submissions, document uploads, invoice generation, and admin portal features.

---

## 🚀 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite** (for development)
- **Pipenv** (virtual environment)
- **Uvicorn** (ASGI server)

---

## 📁 Folder Structure (Core)

```
app/
├── db/                # Database models and setup
├── routes/            # All API routes
├── utils/             # Reusable helpers (email, auth, etc.)
├── schemas.py         # Pydantic schemas (currently monolithic)
├── main.py            # App entrypoint
uploads/               # Uploaded documents (media files)
.env                   # Your environment secrets (SECRET_KEY, etc.)
```

---

## 📌 Setup Instructions

1. **Clone and install dependencies**
```bash
git clone <repo-url>
cd esther-site-backend
pipenv install
pipenv shell
```

2. **Run the development server**
```bash
uvicorn app.main:app --reload
```

3. **Create uploads folder** (to avoid file handling errors)
```bash
mkdir uploads
```

---


## ✅ Available API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET  /api/auth/me`

### Public
- `POST /api/contact`
- `POST /api/booking`

### Admin (Protected)
- `GET    /admin/users`
- `GET    /admin/documents`
- `POST   /admin/upload-document`
- `DELETE /admin/documents/{doc_id}`
- `GET    /admin/invoices/filter`
- `GET    /admin/report/invoices`

---

## 🧪 Testing 

Test files will be placed under:
```
tests/
├── test_auth.py
├── test_contact.py
├── test_booking.py
```

Run tests using:
```bash
pytest
```

---

## 📝 Author
**Esther Waweru**  
Contact: shi3.waweru@gmail.com


