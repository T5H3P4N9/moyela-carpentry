# 🪚 Moyela Carpentry Website

A full-stack web application built with Flask for managing customer quote requests for a carpentry business. This project includes a public-facing website and an admin dashboard to manage incoming quotes.

---

## 🌐 Live Demo

👉 https://moyela-carpentry.onrender.com

---

## 📌 Features

### 👤 Public Users

* View homepage and about page
* Submit a quote request
* Select service type
* Provide contact details and project description

### 🔐 Admin Panel

* Secure login system (session-based)
* View all submitted quotes
* Update quote status (e.g., new, done)
* Delete quotes

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML, CSS (Jinja2 Templates)
* **Server:** Gunicorn
* **Deployment:** Render

---

## 📂 Project Structure

```
moyela-carpentry/
│
├── app.py
├── requirements.txt
├── instance/
│   └── database.db
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── quote.html
│   ├── login.html
│   └── admin.html
├── static/
│   └── (CSS, images, JS)
```

---

## ⚙️ Installation & Setup

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

## 🔑 Environment Variables

Create a `.env` file or set environment variables:

```
SECRET_KEY=your_secret_key_here
```

---

## 🚀 Deployment (Render)

* Build Command:

```
pip install -r requirements.txt
```

* Start Command:

```
gunicorn app:app
```

---

## ⚠️ Known Limitations

* Uses SQLite (data may reset on free hosting)
* Admin authentication is hardcoded (not secure for production)

---

## 🔮 Future Improvements

* 🔐 Secure authentication system (hashed passwords)
* 🐘 PostgreSQL database integration
* 📱 Mobile responsiveness improvements
* 🎨 UI/UX enhancements
* 📊 Admin dashboard analytics
* 🌍 SEO optimization

---

## 👨‍💻 Author

**Tshepang**
Aspiring Software Developer (Backend Focus)

---

## 📄 License

This project is for educational and portfolio purposes.
