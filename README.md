# marketPlace (Django) — Lab Submission Guide

A professional marketplace app built in Django implementing a full Product flow with a clean, modern UI and best practices (template inheritance, URL naming, admin integration).

- [ ] 

---

## 1) Connect the application to the database

Implemented in `marketPlace/settings.py`.
- Default: SQLite (no setup needed)

Verification:
- Run `python3 manage.py migrate` — succeeds without errors
- App runs: `python3 manage.py runserver` — home page loads

---

## 2) Create Product model with required fields

Defined in `products/models.py`:
- `name: CharField(200, db_index=True)`
- `price: DecimalField(10,2, db_index=True)`
- `description: TextField(db_index=True)`
- `image: ImageField(upload_to='products/', blank=True, null=True)`
- `in_stock: BooleanField(default=True)`
- `stock_quantity: PositiveIntegerField(default=0)`
- `created_at: DateTimeField(auto_now_add=True)`
- `updated_at: DateTimeField(auto_now=True)`
- `code: CharField(50, unique=True, db_index=True)` (auto-generated on save)

Verification:
- Open Admin → Products → Add Product shows all fields
- Create a product in Admin; record saves with a generated unique code

---

## 3) Connect application to DB (covered above) and 4) Run migrations

Commands:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
Expected: migrations apply for `products`, `auth`, `admin`, etc.

---

## 5) Add model to the admin panel

Configured in `products/admin.py` with a `ProductAdmin` (list display, filters, search, pagination).

Verification:
- Visit `http://127.0.0.1:8000/admin/`	
- Login and navigate to Products — list, search, filters work

---

## 6) Implement Product functionalities

Routes (namespaced under `products`):
- List: `GET /list/` → name: `products:product_list`
- Create: `GET|POST /create/` (login required) → name: `products:product_create`
- Show: `GET /<pk>/` → name: `products:product_detail`
- Delete: `GET /<pk>/delete/` → name: `products:product_delete`
- Bonus (Edit): `GET|POST /<pk>/edit/` → name: `products:product_update`

Templates (inherit from `templates/base.html`):
- `products/templates/products/home.html`
- `products/templates/products/product_list.html`
- `products/templates/products/product_detail.html`
- `products/templates/products/product_form.html`

Verification:
- Go to `/list/` — products render in a clean grid
- Click a product — see detail page
- Click Edit — update a product and get redirected to detail
- Click Add Product — submit form (login required) and see success message
- Delete via button — redirected back to list with success message

---

## 7) Beautiful (professional) design using template inheritance

- Global layout in `templates/base.html`
- Professional, marketplace-style theme in `static/styles.css`
- Font Awesome icons for a polished nav and actions
- All product pages extend `base.html` (template inheritance)
- URL naming used across templates: e.g. `href="{% url 'products:product_detail' product.pk %}"`

Verification:
- Inspect source — `{% extends 'base.html' %}` in product templates
- Nav links use named URLs with namespaces (`products:...`, `aboutus:...`)

---

## Data seeding (for demo/showcase)

Create sample products and images:
```bash
# 24 products
python3 manage.py seed_products --flush --count 24

# Generate placeholder images for products
python3 manage.py seed_product_images --overwrite
```

---

## How to run locally (quick start)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install Django Pillow

python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py runserver
```

Key URLs:
- Home: `http://127.0.0.1:8000/`
- List: `http://127.0.0.1:8000/list/`
- Create: `http://127.0.0.1:8000/create/` (login required)
- Admin: `http://127.0.0.1:8000/admin/`

---

## Project structure (high level)

```
marketPlace/
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
│   └── registration/login.html
├── static/styles.css
├── media/products/
└── marketPlace/settings.py
```

---

## Notes for the Instructor

- Database is SQLite by default; MySQL can be enabled via environment variables
- Auth URLs enabled; login template provided; create/edit/delete require login
- Media and static are configured for development; production would use proper storages/collectstatic
- URL naming and namespacing are consistently used throughout templates
