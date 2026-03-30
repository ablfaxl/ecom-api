# 🚀 SonicStore API - Modern E-commerce Backend

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15+-A30000?style=for-the-badge&logo=django&logoColor=white)](https://django-rest-framework.org)

A scalable, high-performance E-commerce API built with a **User-Centric Architecture**. This project handles everything from dynamic product management to complex cart logic and secure order fulfillment, ensuring a seamless experience for both developers and end-users.

---

## ✨ Key Features

* **🛒 User-Centric Cart System:** No more manual UUID management on the frontend. The server automatically associates a persistent cart with the authenticated user via the `/carts/me/` endpoint.
* **🔐 Advanced Authentication:** Fully implemented JWT (JSON Web Token) auth using **Djoser** and **SimpleJWT** for secure sign-ups and logins.
* **📦 Inventory Logic & Guardrails:** Real-time inventory checks during checkout. The system prevents over-ordering and automatically updates stock levels upon successful payment.
* **🛡 Atomic Transactions:** Utilizes `transaction.atomic` to ensure data integrity during the order process—if one step fails, all changes are rolled back.
* **🌱 Rapid Seeding:** Built-in `seed_db` management command to populate the database with realistic products in milliseconds.

---

## 🛠 Tech Stack

* **Backend:** Django, Django REST Framework (DRF)
* **Auth:** SimpleJWT (JWT), Djoser
* **Database:** SQLite (Production-ready for PostgreSQL)
* **Architecture:** RESTful API with Nested Routers
* **Frontend Demo:** Vanilla JavaScript, Tailwind CSS 

---

## 🚀 Quick Start

### 1. Installation & Environment
Clone the repository and activate your virtual environment:
```bash
git clone [https://github.com/your-username/ecom-api.git](https://github.com/your-username/ecom-api.git)
cd ecom-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Setup Database
Apply migrations to build the schema:
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```


### 3. Seed Data & Admin
Create a superuser and populate the store with products:

```bash
python manage.py seed_db
python manage.py createsuperuser
```

### 4. Run Server

```bash
4. Run Server
```

| Feature        | Method   | Endpoint                   | Auth Required |
|----------------|----------|----------------------------|---------------| 
| Product List   | GET      | `/api/v1/products/`        | No            |
| Manage My Cart | GET/POST | `/api/v1/carts/me/`        | Yes           |
| Place Order    | POST     | `/api/v1/orders/`          | Yes           |
| Get JWT Token  | POST     | `/api/v1/auth/jwt/create/` | No            |

### 👨‍💻 Author
Abolfazl Taghavi Frontend & Backend Engineer Passionate about building clean, modular code and high-performance web applications.

---
