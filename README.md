# 🍽️ FoodFiesta — Food Ordering & Restaurant Management System

A full-stack food ordering web application built with **Python and Django**, designed to simplify the food ordering experience for customers while providing restaurant and order management capabilities for administrators.

FoodFiesta brings restaurant discovery, menu browsing, cart management, order placement, and payment integration together in one web application.

---

## 📌 Table of Contents

* [Overview](#-overview)
* [Key Features](#-key-features)
* [Technology Stack](#-technology-stack)
* [Application Modules](#-application-modules)
* [Project Structure](#-project-structure)
* [Getting Started](#-getting-started)
* [Environment Configuration](#-environment-configuration)
* [Running the Application](#-running-the-application)
* [Payment Integration](#-payment-integration)
* [Security](#-security)
* [Future Enhancements](#-future-enhancements)
* [Author](#-author)

---

## 📖 Overview

FoodFiesta is a Django-based food delivery application that connects customers with restaurants through a simple and intuitive interface.

The application supports customer account access, restaurant and menu management, cart operations, order processing, and Razorpay test-mode payment integration. It also includes a Smart Leftover feature.

The project demonstrates the development of a web application using Django, database models, server-rendered templates, frontend styling, and third-party payment integration.

## ✨ Key Features

### 👤 Customer Module

* Customer registration and login
* Browse available restaurants
* Explore restaurant menus and food items
* Add food items to the cart
* Place food orders
* View orders and order details
* Proceed through the payment workflow

### 🛠️ Administration Module

* Access the administration interface
* Add and manage restaurants
* Update restaurant information
* Manage food menus and menu items
* View and manage customer orders

### 💳 Payment Integration

* Razorpay payment gateway integration
* Test-mode payment workflow for development
* Environment-based configuration for API credentials

### ♻️ Smart Leftover

* Dedicated Smart Leftover feature
* Separate interface integrated into the FoodFiesta application

### 🎨 User Interface

* Food-themed website design
* Dedicated pages for customers and administrators
* Reusable navigation component
* Styled templates and responsive layout elements

---

## 🧰 Technology Stack

| Category                  | Technologies            |
| ------------------------- | ----------------------- |
| Backend                   | Python, Django          |
| Frontend                  | HTML5, CSS3, JavaScript |
| Database                  | SQLite                  |
| Payment Gateway           | Razorpay (Test Mode)    |
| Environment Configuration | python-dotenv           |
| Version Control           | Git, GitHub             |

---

## 🧩 Application Modules

| Module                  | Description                                     |
| ----------------------- | ----------------------------------------------- |
| Customer Authentication | Customer registration and login                 |
| Restaurant Management   | Create, view, and update restaurant information |
| Menu Management         | Manage restaurant menu items                    |
| Cart & Orders           | Cart operations and order processing            |
| Payment                 | Razorpay test-mode payment integration          |
| Smart Leftover          | Dedicated leftover-related feature              |

---

## 📂 Project Structure

```text
FoodFiesta/
│
├── delivery/
│   ├── migrations/
│   ├── static/
│   │   └── delivery/
│   │       └── style.css
│   ├── templates/
│   │   └── delivery/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── foodfiesta/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .gitignore
├── manage.py
└── README.md
```

---

## 🚀 Getting Started

Follow these steps to run FoodFiesta locally.

### Prerequisites

Install the following:

* Python
* pip
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/Sindhuanand233672/FoodFiesta.git
cd FoodFiesta
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate the Virtual Environment

**Windows — Command Prompt:**

```cmd
myenv\Scripts\activate
```

### 4. Install Dependencies

If the repository contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If it does not exist yet, create it from your working environment before publishing the README:

```bash
pip freeze > requirements.txt
```

Then add and commit the file to GitHub.

### 5. Configure Environment Variables

Create a `.env` file in the project root, in the same directory as `manage.py`.

Add the following configuration:

```env
DJANGO_SECRET_KEY=your_local_django_secret_key
DEBUG=True
RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
```

Replace the placeholder values with your own local development credentials.

**Never commit `.env` or expose secret keys in public repositories.**

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create an Administrator Account

Create your own local Django administrator account:

```bash
python manage.py createsuperuser
```

Follow the prompts to set the username, email address, and password.

### 8. Start the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

**http://127.0.0.1:8000/**

---

## 🔐 Environment Configuration

FoodFiesta loads sensitive configuration from environment variables.

| Variable              | Purpose                               |
| --------------------- | ------------------------------------- |
| `DJANGO_SECRET_KEY`   | Django application secret             |
| `DEBUG`               | Enables or disables Django debug mode |
| `RAZORPAY_KEY_ID`     | Razorpay API key ID                   |
| `RAZORPAY_KEY_SECRET` | Razorpay API secret                   |

For production deployment, use a secure secret key, disable debug mode, configure allowed hosts, and store credentials in the hosting provider's environment settings.

---

## 💳 Payment Integration

FoodFiesta integrates with Razorpay for its payment workflow.

The project is configured for **Razorpay Test Mode**. Use test credentials and test transactions during development.

Live payments require a properly configured Razorpay account and production credentials. Never publish API secrets or use test credentials for live transactions.

---

## 🛡️ Security

* Secret keys and API credentials should be stored in environment variables.
* The `.env` file must remain excluded from version control.
* Do not publish real customer data or active account passwords.
* Use unique, strong passwords for administrator accounts.
* Disable Django debug mode in production.
* Configure production security settings before deployment.

---

## 🔮 Future Enhancements

Potential improvements include:

* Live deployment with a production database
* Order status notifications
* Improved search and filtering
* Enhanced customer profile management
* Automated testing
* Improved mobile responsiveness
* Production-ready payment configuration

---

## 👩‍💻 Author

**Sindhu A**
B.E. — Artificial Intelligence and Machine Learning

GitHub: [Sindhuanand233672](https://github.com/Sindhuanand233672)

Project: [FoodFiesta Repository](https://github.com/Sindhuanand233672/FoodFiesta)

---

*FoodFiesta — Bringing restaurants and customers together, one order at a time.*
