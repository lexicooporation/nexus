# <img src="https://img.shields.io/badge/-Nexus-0A2540?style=flat-square&logo=target&logoColor=white" alt="Nexus"> Nexus

> **Work smarter, together.** A full-stack SaaS team management platform built with Django — featuring subscription billing, email authentication, and a clean responsive marketing site.

---

## 📸 Overview

Nexus is a production-ready Django SaaS boilerplate that handles everything from user sign-up to payment processing. It ships with a polished marketing frontend, a powerful admin dashboard, and a complete Paystack billing flow — so you can focus on your product, not the plumbing.

---

## ✨ Features

- 🔐 **Custom Email Authentication** — users log in with email, not username; Django admin still uses username fallback
- 💳 **Paystack Billing** — full subscription flow: checkout → payment → webhook callback → subscription record
- 📊 **Jazzmin Admin Dashboard** — custom-branded Django admin with sidebar icons, colour themes, and modal forms
- 📧 **SendGrid Email** — transactional email via SendGrid backend
- 🛡️ **Rate-Limited Contact Form** — IP-based rate limiting with Django cache (3 submissions/hour)
- 🔧 **Maintenance Mode** — toggle site maintenance on/off without a deploy; superusers bypass it
- ⚡ **WhiteNoise Static Files** — compressed static file serving, no extra web server needed
- 🎨 **Responsive Marketing Site** — Home, Pricing, About, Contact, Legal pages built with Bootstrap 5
- 🗄️ **PostgreSQL** — production-grade database, fully env-variable driven

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x, Python 3.12 |
| Database | PostgreSQL |
| Payments | Paystack |
| Email | SendGrid |
| Frontend | Bootstrap 5, Bootstrap Icons, Sora/Inter fonts |
| Admin | Jazzmin |
| Static Files | WhiteNoise |
| Environment | python-dotenv |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- A [Paystack](https://paystack.com) account
- A [SendGrid](https://sendgrid.com) account

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nexus.git
cd nexus
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key

# Database
DB_NAME=nexusdb
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost

# Paystack
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxx
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxx

# SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
DEFAULT_FROM_EMAIL=you@example.com

# Optional
DEBUG=True
```

### 5. Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — the site is live.  
Admin panel: `http://127.0.0.1:8000/admin/`

---

## 💳 Payment Flow

```
User clicks "Get Started" on a plan
        ↓
/pricing/checkout/<plan_id>/        — shows plan summary
        ↓
/pricing/initiate/<plan_id>/        — calls Paystack API, redirects user
        ↓
Paystack hosted payment page
        ↓
/pricing/callback/                  — verifies transaction, saves Subscription
        ↓
/payment/success/  or  /payment/failed/
```

Amounts are stored in **Naira**. Paystack receives amounts in kobo (× 100) and the callback converts back.

---

## 📁 Project Structure

```
nexus/
├── nexus/                  # Project config (settings, urls, wsgi)
├── nexusApp/               # Main application
│   ├── models.py           # Testimonial, PricingPlan, FAQ, TeamMember, Subscription
│   ├── views.py            # Home, Pricing, About, Contact, Auth views
│   ├── payment_views.py    # Checkout, initiate, callback views
│   ├── backends.py         # Custom email auth backend
│   ├── forms.py            # Contact, SignUp, EmailLogin forms
│   └── admin.py            # Jazzmin admin config
├── templates/              # Django HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads (gitignored)
└── staticfiles/            # Collected static files (gitignored)
```

---

## ⚙️ Configuration Notes

**Switching to Redis cache (production)**

Uncomment the Redis block in `settings.py` and install `django-redis`:

```bash
pip install django-redis
```

**Maintenance mode**

Toggle in `settings.py` or via the admin:

```python
MAINTENANCE_MODE = True   # Takes the site offline for non-superusers
```

---

## 🌍 Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py collectstatic`
- [ ] Switch `CACHES` to Redis
- [ ] Use a process manager (Gunicorn + Nginx recommended)
- [ ] Set all secret keys as environment variables — never hardcode them

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Built by **lexiworld** · [Twitter](https://x.com/lexyystore02) · [LinkedIn](https://linkedin.com/in/nwankwo-ifeanyi-5014a8227)
