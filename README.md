# SSCatFacts

## Overview

A simple app that allows users to discover random cat facts, manage their favorite ones, and explore the most popular facts.

---

## Features

### Public

* Browse random cat facts retrieved from an external API.
* View the most popular cat facts based on the number of favorites.

### Authenticated

* Register a new account.
* Log in using JWT authentication.
* Add or remove favorite cat facts.
* View your personal list of favorite facts.

---

## Built With

### Backend

* Python 3.12
* Django
* Django REST Framework
* Simple JWT
* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Vanilla JavaScript

### Development Tools

* Black
* Flake8
* ESLint
* Prettier
* HTMLHint

---

## Project Structure

```yaml
sscatfacts/
├── backend/
│   ├── catfacts/
│   ├── users/
│   └── config/
├── frontend/
│   ├── css/
│   ├── js/
│   └── *.html
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CrisTheObserver/sscatfacts
cd sscatfacts
```

---

### 2. Backend

Create and activate a virtual environment:

#### macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
cd backend
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/api/
```

---

### 3. Frontend

From the `frontend` directory:

```bash
python -m http.server 5000
```

Open your browser at:

```
http://127.0.0.1:5000
```

> **Note**
>
> The frontend currently uses a hardcoded API base URL (`http://127.0.0.1:8000/api`). In a production environment, this value should be provided through environment-specific configuration.

### 4. Development Tools (Optional)
The following dependencies are only required to run the project's code quality tools. They are **not required** to run the application.

Install the Python development dependencies:

```bash
pip install -r requirements-dev.txt
```

Install the frontend development dependencies:

```bash
npm install
```

---

## Environment Variables

The backend supports the following environment variable:

| Variable          | Default                      |
| ----------------- | ---------------------------- |
| `CATFACT_API_URL` | `https://catfact.ninja/fact` |

---

## API Endpoints

### Authentication

| Method | Endpoint              | Authentication |
| ------ | --------------------- | -------------- |
| POST   | `/api/auth/register/` | No             |
| POST   | `/api/auth/login/`    | No             |
| POST   | `/api/auth/refresh/`  | No             |

### Cat Facts

| Method | Endpoint                       | Authentication |
| ------ | ------------------------------ | -------------- |
| GET    | `/api/catfacts/random/`        | No             |
| GET    | `/api/catfacts/popular/`       | No             |
| POST   | `/api/catfacts/{id}/favorite/` | Yes            |
| GET    | `/api/catfacts/favorites/`     | Yes            |

---

## Running Tests

Backend tests can be executed with:

```bash
python manage.py test
```

---

## Code Quality

### Backend

```bash
black backend/
flake8 backend/
```

### Frontend

```bash
npx eslint "frontend/**/*.js"
npx prettier . --check
npx htmlhint "frontend/*.html"
```

---

## TO DO:

* Docker setup for easier deployment
* Environment-based config for the API URL (currently hardcoded for simplicity)
* Auto-refresh JWT tokens
* Setting up a CI pipeline to automatically run tests and linters.
* Providing visual feedback on the frontend.
* Adding pagination for large result sets.
