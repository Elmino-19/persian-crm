# Django CRM

This is a CRM application built with Django.

## High-level description

This project is a Customer Relationship Management (CRM) system designed to help businesses manage their interactions with current and potential customers. It provides tools for managing contacts, tracking sales, and handling customer service inquiries.

## Classes and Methods

### `webcrm/settings.py`

This file contains the Django settings for the project. Key settings include:

*   `DEBUG`: Set to `True` for development to enable detailed error pages and automatic static file serving.
*   `DATABASES`: Configured to use PostgreSQL.
*   `STATIC_URL`: The URL to use when referring to static files.
*   `STATIC_ROOT`: The directory where `collectstatic` will collect static files for deployment.

### `webcrm/urls.py`

This file defines the URL patterns for the project. It includes patterns for the admin interface, as well as for the various apps within the project. In development, it is configured to serve static files.

### `manage.py`

This is a command-line utility that lets you interact with this Django project in various ways. The most common use is to run the development server, but it can also be used to run management commands like `collectstatic`.

## Installation and Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/django-crm.git
    cd django-crm
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install uv
    uv pip install -r requirements.txt
    ```

3.  **Configure the database:**

    Open `webcrm/settings.py` and configure the `DATABASES` setting with your database credentials.

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Collect static files:**
    ```bash
    python manage.py collectstatic
    ```

6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000`.
