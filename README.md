#  Moyela Carpentry Website – Quote Management System

A full-stack Flask web application for managing carpentry quote requests, admin dashboard analytics, and email notifications. Built for a real business workflow with authentication, database storage, and data visualization.

---

##  Live Demo

 https://moyela-carpentry.onrender.com

---

##  Features

    Public website (Home, About, Quote page)
    Quote submission form (clients request quotes)
    Admin login system (secure session auth)
    Admin dashboard with analytics:
        Total leads counter
        Quotes per day chart
        Most requested services chart
    Email notifications for new quotes (SMTP Gmail)
    Admin controls:
        Mark quote as done
        Delete quotes
    PostgreSQL / SQLite support (Render-ready deployment)
    Production deployment ready (Render / any cloud platform)

---

##  Tech Stack

Backend: Flask (Python)
Database: SQLAlchemy (SQLite / PostgreSQL)
Frontend: HTML, CSS, JavaScript
Charts: Chart.js
Auth: Flask sessions + Werkzeug security
Email: SMTP (Gmail App Password)

---

##  Project Structure

```
project/
│
├── app.py
├── instance/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── quote.html
│   ├── login.html
│   └── admin.html
│
├── static/
│   └── styles.css
│
└── README.md
```

---

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/moyela-carpentry.git
cd moyela-carpentry
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

##  Environment Variables

Create a `.env` file or set on Render:

```
SECRET_KEY=your_secret_key

DATABASE_URL=your_postgres_url

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

EMAIL_USER=yourgmail@gmail.com
EMAIL_PASS=your_google_app_password
EMAIL_RECEIVER=yourgmail@gmail.com
```

---

##  Deployment (Render)

 Build Command:

```
pip install -r requirements.txt
```

 Start Command:

```
gunicorn app:app
```

---

##  Admin Dashboard

/login

  ## Admin features:

    View all quotes
    Track leads
    View charts (Chart.js)
    Manage quote status

---

## Email System

When a client submits a quote:

Email is sent automatically to admin
Uses Gmail SMTP
Requires Google App Password

---

## Deployment (Render)
Push project to GitHub
Create Render Web Service
## Add environment variables:
    DATABASE_URL
    SECRET_KEY
    EMAIL_USER
    EMAIL_PASS
Deploy


## 👨‍💻 Author

**Tshepang**
Aspiring Software Developer (Backend Focus)

---

## 📄 License

This project is for educational and portfolio purposes.
