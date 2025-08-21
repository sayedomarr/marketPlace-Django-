#  Marketplace using django

A Django marketplace that implements full CRUD for Products and Categories with authentication, clean URL naming, template inheritance, media handling, and a modern, neutral UI.

## Contents
- Overview
- Tech Stack
- Features
- Screenshots (placeholders to add images)
- Project Structure
- Database Configuration (SQLite default, MySQL optional)
- Setup & Run (step-by-step)
- Data Seeding (optional)
- URL Map
- Admin Usage
- Lab 3 Checklist (verification steps)
- Notes & Production Tips
- Push to GitHub

---

## Overview
This app demonstrates a marketplace with two core entities: Products and Categories. Each Product can belong to a Category. The UI follows a professional marketplace style (light theme, blue accents). CRUD is implemented using Django generic views and ModelForms, with login protection on write operations.

## Tech Stack
- Django 5
- SQLite (default) or MySQL (optional)
- Pillow (image handling)
- HTML/CSS 

## Features
- Products
  - Create, List, Detail (Show), Update, Delete
  - Image upload, price, stock status, unique code, timestamps
  - Link to Category and show category on product detail
- Categories
  - Create, List, Detail, Update, Delete (CRUD)
  - Category detail shows all products in that category
  - Create/Edit/Delete require login
- Authentication
  - Login/Logout (Django auth)
  - Signup page for new users (`/accounts/signup/`)
- Templates & URLs
  - Template inheritance via `templates/base.html`
  - Consistent URL naming and namespacing (`products:...`, `categories:...`)
- Styling
  - Professional, marketplace-friendly design (`static/styles.css`)

---

## Screenshots (placeholders)
Create a folder `docs/screenshots/` and add images, then update these links.

- Home (/)
  
- ![image-20250821174657297](../.config/Typora/typora-user-images/image-20250821174657297.png)
  
- Products List (/list/)  
  ![image-20250821174729825](../.config/Typora/typora-user-images/image-20250821174729825.png)

- Product Detail (/<<id>>/)  
  ![image-20250821174822830](../.config/Typora/typora-user-images/image-20250821174822830.png)

- Product Create (/create/)  
  ![image-20250821174842085](../.config/Typora/typora-user-images/image-20250821174842085.png)

- Categories List (/categories/)  
  ![image-20250821174856008](../.config/Typora/typora-user-images/image-20250821174856008.png)

- Category Detail (/categories/<<id>>/)  
  ![image-20250821174918834](../.config/Typora/typora-user-images/image-20250821174918834.png)
  - Category Create (/categories/create/)  
    ![image-20250821174938189](../.config/Typora/typora-user-images/image-20250821174938189.png)
  
- Login (/accounts/login/)  
  ![image-20250821175001512](../.config/Typora/typora-user-images/image-20250821175001512.png)

- Signup (/accounts/signup/)  
  ![image-20250821175017674](../.config/Typora/typora-user-images/image-20250821175017674.png)

- Admin (/admin/)  
  ![image-20250821175041205](../.config/Typora/typora-user-images/image-20250821175041205.png)

---

## Project Structure (high level)
```
marketPlace/
├── categories/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/categories/
│       ├── category_confirm_delete.html
│       ├── category_detail.html
│       ├── category_form.html
│       └── category_list.html
├── products/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/products/
│       ├── home.html
│       ├── product_detail.html
│       ├── product_form.html
│       └── product_list.html
├── templates/
│   ├── base.html
│   └── registration/
│       ├── login.html
│       └── signup.html
├── static/styles.css
├── media/ (runtime; user-uploaded images)
├── marketPlace/
│   ├── settings.py
│   ├── urls.py
│   └── views.py (signup)
└── manage.py
```

---

## Database Configuration (SQLite default, MySQL optional)
Default is SQLite. MySQL can be enabled via environment variables.

- SQLite (default): no configuration needed
- MySQL (optional):
```bash
export USE_MYSQL=1
export MYSQL_DB=marketplace
export MYSQL_USER=marketplace_user
export MYSQL_PASSWORD=marketplace123
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
```

Verify the active DB:
```bash
python3 manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default'])"
```

---

## Setup & Run (step-by-step)
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv && source .venv/bin/activate

# 2) Install dependencies
pip install -U pip
pip install Django Pillow

# 3) Apply migrations
python3 manage.py migrate

# 4) Create a superuser
python3 manage.py createsuperuser

# 5) Run the dev server
python3 manage.py runserver
```

Key URLs:
- Home: `http://127.0.0.1:8000/`
- Products list: `http://127.0.0.1:8000/list/`
- Product create: `http://127.0.0.1:8000/create/` (login required)
- Categories list: `http://127.0.0.1:8000/categories/`
- Category create: `http://127.0.0.1:8000/categories/create/` (login required)
  - Admin: `http://127.0.0.1:8000/admin/`

- Login: `http://127.0.0.1:8000/accounts/login/`
- Signup: `http://127.0.0.1:8000/accounts/signup/`

---

## Data Seeding (optional)
Populate the DB for demos and screenshots.
```bash
# Seed categories (names + descriptions)
python3 manage.py seed_categories --flush --count 8

# Generate placeholder images for categories
python3 manage.py seed_category_images --overwrite

# Create sample products
python3 manage.py seed_products --flush --count 24

# Generate placeholder images for products
python3 manage.py seed_product_images --overwrite

# Link products to categories randomly
python3 manage.py link_products_to_categories
```

---

## URL Map
- Products (namespace `products`)
  - List: `/list/` → `products:product_list`
  - Detail: `/<int:pk>/` → `products:product_detail`
  - Create: `/create/` → `products:product_create` (login required)
  - Update: `/<int:pk>/edit/` → `products:product_update` (login required)
  - Delete: `/<int:pk>/delete/` → `products:product_delete` (login required)
- Categories (namespace `categories`)
  - List: `/categories/` → `categories:category_list`
  - Detail: `/categories/<int:pk>/` → `categories:category_detail`
  - Create: `/categories/create/` → `categories:category_create` (login required)
  - Update: `/categories/<int:pk>/edit/` → `categories:category_update` (login required)
  - Delete: `/categories/<int:pk>/delete/` → `categories:category_delete` (login required)
- Auth
  - Login: `/accounts/login/`
  - Logout: `/accounts/logout/` (POST)
  - Signup: `/accounts/signup/`

---

## Admin Usage
- Visit `/admin/`, login with superuser
- Manage Products and Categories
- Verify list filters, search, inline editing (where enabled), and read-only timestamps

