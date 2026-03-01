# BookHive - Library Management System API

A production-ready RESTful API for library management built with Django and Django REST Framework. BookHive provides complete functionality for managing books, users, and borrowing transactions with proper authentication and authorization.

## Live Demo

**Base URL:** `https://bookhive.pythonanywhere.com`

## Features

### Book Management
- Complete CRUD operations for books
- ISBN validation with format checking (10/13 digit support)
- Automatic availability tracking
- Search and filter by title, author, or ISBN

### User Authentication
- JWT-based authentication
- User registration and login
- Role-based permissions (Admin vs Member)
- Profile management

### Borrow/Return System
- Checkout books with availability validation
- Return processing with automatic copy count updates
- Prevention of duplicate checkouts
- Complete transaction history tracking
- Atomic database operations for data integrity

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Django 5.2 |
| API Framework | Django REST Framework 3.16 |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | SQLite (development) / PostgreSQL (production) |
| Deployment | PythonAnywhere |
| Environment | python-decouple for configuration |

## API Endpoints

### Authentication

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/register/` | Create new user account | Public |
| POST | `/api/login/` | Obtain JWT tokens | Public |
| POST | `/api/logout/` | Blacklist refresh token | Authenticated |
| GET/PUT | `/api/profile/` | View/update profile | Authenticated |

### Books

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/api/books/` | List all books | Public |
| GET | `/api/books/{id}/` | Retrieve single book | Public |
| POST | `/api/books/` | Create new book | Admin |
| PUT | `/api/books/{id}/` | Full update | Admin |
| PATCH | `/api/books/{id}/` | Partial update | Admin |
| DELETE | `/api/books/{id}/` | Delete book | Admin |
| POST | `/api/books/{id}/checkout/` | Borrow book | Authenticated |
| POST | `/api/books/{id}/return/` | Return book | Authenticated |

### Transactions

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/transactions/` | List all transactions | Admin |
| GET | `/api/transactions/my_transactions/` | User's borrowing history | Authenticated |
| GET | `/api/transactions/{id}/` | Transaction details | Owner/Admin |

### User Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/users/` | List all users | Admin |
| GET | `/api/users/{id}/` | User details | Admin |
| GET | `/api/users/{id}/history/` | User's borrow history | Admin/Self |

## Database Schema

```python
# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

# Transaction Model
class Transaction(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Checked Out'
        RETURNED = 'RETURNED', 'Returned'
        OVERDUE = 'OVERDUE', 'Overdue'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
```

## 🔧 Installation

### Prerequisites
- Python 3.10+
- pip package manager
- virtualenv (recommended)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/Molecule-Cloud/BookHive.git
cd BookHive
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the application**
- API Root: `http://127.0.0.1:8000/api/books/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## Testing with curl

### Register a new user
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"UserPassword123","password2":"UserPassword123"}'
```

### Login to obtain token
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"UserPassword123"}'
```

### Access protected endpoint
```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer <your-access-token>"
```

### Checkout a book
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/checkout/ \
  -H "Authorization: Bearer <your-access-token>"
```

## Project Structure

```
BookHive/
├── bookhive/               # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/                  # Books app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── users/                  # Custom user app
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── transactions/           # Borrow/return app
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── api/                    # API routing
│   └── urls.py
├── manage.py
├── requirements.txt
└── .env
```

## Deployment on PythonAnywhere

1. **Create account** at pythonanywhere.com
2. **Open Bash console** and clone repository
3. **Create virtual environment** and install dependencies
4. **Configure web app** with manual configuration
5. **Update WSGI file** with project path
6. **Set ALLOWED_HOSTS** to your domain
7. **Run migrations** and **collectstatic**
8. **Reload web app**

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 400 Bad Request | Check `ALLOWED_HOSTS` in settings.py |
| 401 Unauthorized | Include valid JWT token in `Authorization` header |
| 403 Forbidden | User lacks required permissions |
| 404 Not Found | Verify URL and object ID |
| 500 Server Error | Check server logs for details |

## License

This project is licensed under the MIT License.

## Author

**Your Name**
- GitHub: [@yourusername](https://github.com/Molecule-Cloud)
- LinkedIn: [Your Profile](https://linkedin.com/in/benjaminappiah1223)

## Acknowledgments

- Django REST Framework documentation
- PythonAnywhere for hosting
- Contributors and testers

---

**Built with Django REST Framework** • **Deployed on PythonAnywhere** • **© 2024 BookHive**
