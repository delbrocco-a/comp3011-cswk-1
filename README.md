---

# COMP3011 - Personal Financing API

---


A REST API for personal finance management, built as part of the COMP3011 Web Services and Web Data module at the University of Leeds. The API allows users to track income and expenses, manage accounts, set budgets, and query spending analytics — essentially a lightweight backend for a personal accounting system supporting basic credit/debit operations across multiple accounts and categories.

## Production (prod branch) Deployment & Stack

> https://delbrocco.pythonanywhere.com/api/

- **Language -** Python (3.13)
- **Framework -** Django (5.2) [REST Framework] (3)
- **Database -** SQLite3
- **Authentication -** Token-based (DRF AuthToken)
- **Auto Docs -** drf-spectacular (OpenAPI 3)
- **Testing -** Django (TestCase) & DRF APIClient
- **CI/CD -** Done in Github Actions/Workflow
- **Deployment Architecture -** (handled by pythonanywhere)

> NB All versions listed are the version the initial API was written in, and for any version, users should refer to the dependencies in requirements.txt

## Pre-Setup

The API is structured around five core models — Accounts, Transactions, Categories, Budgets, and Users attempting to abide REST conventions closesly throughout. Accounts represent real-world financial accounts (like credit accounts eg checking, savings, cash, and debit accounts, eg food shopping, luxeries, holidays etc); transactions record individual income or expense operations against those aforementioned accounts, and categories allow users to organise spending into meaningful groups, and budget endpoints allow users to set spending limits per category. To provide a basic functionality to these models, outside of storing the data, analytics endpoints aggregate transaction data to provide monthly summaries, spending breakdowns, and multi-month trend analysis. All endpoints should require token-based authentication, meaning users only ever see and interact with their own data, however note that this project is in it's early stages, and thorough security analysis and checks haven't been carried out: THE PROJECT CONTRIBUTORS TAKE NO ACCOUNTABLILITY FOR THE SECURITY OF THIS API AS IT IS AN ACADEMIC EXERCISE, AND USERS SHOULD ADAPT IT TO THEIR OWN SECURITY NEEDS.

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

The analytics are all GET operations, with logic processing being completed by the server. Note that this is not multithreaded, and hence will not be able to reasonably compensate a load greater than a single user.

| Endpoint | Description |
|----------|-------------|
| `/api/analytics/summary/?month=YYYY-MM` | Income, expenses, and net savings |
| `/api/analytics/spending-by-category/?month=YYYY-MM` | Monthly spending per category |
| `/api/analytics/trends/?months=N` | Month-over-month income vs expense trend |
| `/api/analytics/budget-status/` | Budget usage and remaining amounts |

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

## Author & Support

For issues or questions, please open a GitHub issue on this repository.

Maintained by [delbrocco-a](https://github.com/delbrocco-a)
