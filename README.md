# Inventory Management System (Django)

A complete Inventory Management System built using Django. This project manages products, suppliers, purchases, sales, stock movements, POS billing, invoice generation, and payment integration (COD and eSewa).

---

# Features

## Product Management
- Create, update, and delete products
- Category-based organization
- Stock tracking system
- Low stock monitoring

## Supplier Management
- Add and manage suppliers
- Store supplier contact information

## Purchase Management
- Create purchase orders
- Add multiple items per purchase
- Automatically increase stock after confirmation

## Sales and POS System
- POS (Point of Sale) system for billing
- Cart-based product selection
- Increase and decrease product quantity
- Remove items from cart
- Checkout system

## Billing and Invoice System
- Automatic invoice generation after checkout
- Detailed item-wise billing
- Total calculation
- Printable invoice format

## Payment System
- Cash on Delivery (COD)
- eSewa payment gateway integration

## Dashboard
- Total products overview
- Stock value calculation
- Stock movement analytics
- Charts for categories and inventory trends

---

# Tech Stack

- Python 3.12+
- Django 6
- SQLite database
- HTML, CSS
- Bootstrap (UI styling)
- JavaScript (Chart.js for analytics)

---

# Installation Guide

## 1. Clone the repository

```bash
git clone https://github.com/your-username/inventory-management-system.git
cd inventory-management-system

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```
## Open application
http://127.0.0.1:8000/
