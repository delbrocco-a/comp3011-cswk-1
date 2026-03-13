---

# COMP3011 - Personal Financing API

---

REST based API implementing basic credit/debit accounting, and income/expense operations.

## Production (prod branch) Deployment & Stack
https://delbrocco.pythonanywhere.com/api/

- **Framework:** Django 5.2 (REST Framework)
- **Database:** SQLite
- **Authentication:** Token-based (DRF AuthToken)
- **Testing:** Django TestCase + GitHub Actions CI

## Set-up 

- 1. Clone the repository
```bash
git clone https://github.com/yourusername/comp3011-cswk-1.git
cd comp3011-cswk-1
```

- 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

- 3. Dependencies
```bash
pip install -r requirements.txt
```

- 4. Migrate
```bash
python manage.py migrate
```

- 5. Init superuser (optional)
```bash
python manage.py createsuperuser
```

- 6. Deploy
```bash
python manage.py runserver
```

## API Endpoints

There are four principle data models, each linked to an individual user:

| Model | Description |
| ------| ------------|
| Account | A financial account, holding balance of credit/debits |
| Transaction | A representation of a credit to a debit between two accounts |
| Category | Akin to "labels"; categorisation of transactions |
| Budget | Spending tacker for a given category (with limits) |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive token |
| POST | `/api/auth/logout/` | Logout and invalidate token |

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/` | List all accounts |
| POST | `/api/accounts/` | Create an account |
| PUT | `/api/accounts/{id}/` | Update an account |
| DELETE | `/api/accounts/{id}/` | Delete an account |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List all transactions |
| POST | `/api/transactions/` | Create a transaction |
| PUT | `/api/transactions/{id}/` | Update a transaction |
| DELETE | `/api/transactions/{id}/` | Delete a transaction |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create a category |
| PUT | `/api/categories/{id}/` | Update a category |
| DELETE | `/api/categories/{id}/` | Delete a category |

### Budgets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/budgets/` | List all budgets |
| POST | `/api/budgets/` | Create a budget |
| PUT | `/api/budgets/{id}/` | Update a budget |
| DELETE | `/api/budgets/{id}/` | Delete a budget |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/summary/?month=YYYY-MM` | Income, expenses, and net savings |
| GET | `/api/analytics/spending-by-category/` | Lifetime spending per category |
| GET | `/api/analytics/spending-by-category/?month=YYYY-MM` | Monthly spending per category |
| GET | `/api/analytics/trends/?months=N` | Month-over-month income vs expense trend |
| GET | `/api/analytics/budget-status/` | Budget usage and remaining amounts |

## Authentication

All endpoints except `/api/auth/register/` and `/api/auth/login/` require a token in the request header:
```
Authorization: Token <your_token>
```

## Testing

Run the test suite locally:
```bash
python manage.py test
```

Tests are also run automatically on every push via GitHub Actions.

## API Documentation

Full API documentation is available in `docs`