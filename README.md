# Simple Quote API

A RESTful API built with Django and Django REST framework for managing and retrieving quotes. This API supports CRUD operations, JWT authentication, filtering, and includes a feature to fetch a random quote.

## Features
- **CRUD Operations**: Create, Retrieve, Update, and Delete quotes.
- **Random Quote**: Fetch a random quote from the collection.
- **JWT Authentication**: Secure endpoints with JSON Web Tokens.
- **Filtering**: Filtering quotes by author or content.
- **Data Validation**: Ensures data integrity on Create and Update endpoints.

## Installation

### Prerequisites
- Python
- Django
- Django REST framework
- Django Filters
- Django Extensions
- Django Simple JWT
- SQLite (default database setup)

### Steps
#### Clone the repository:
```bash
git clone https://github.com/ddcsoftdev/simple-quote-api.git
cd quote-api
```
#### Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
#### Install dependencies:
```bash
pip install django djangorestframework django-filter django-extensions djangorestframework-simplejwt
```
#### Run migrations:
```bash
python manage.py migrate
```
#### Start the server:
```bash
python manage.py runserver
```

## API Endpoints

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|-------------------------|
| `/api/v1/quote/` | GET | List all quotes | No |
| `/api/v1/quote/` | POST | Create a new quote | Yes |
| `/api/v1/quote/<uuid>/` | GET | Retrieve a single quote | No |
| `/api/v1/quote/<uuid>/` | PUT | Fully update a quote | Yes |
| `/api/v1/quote/<uuid>/` | DELETE | Delete a quote | Yes |
| `/api/v1/quote/random/` | GET | Fetch a random quote | No |

### Authentication Endpoints
- **Login**: `POST /api/v1/login/` (Get JWT tokens)
- **Refresh Token**: `POST /api/v1/refresh/`

## Usage Examples

#### Get All Quotes
```bash
curl http://localhost:8000/api/v1/quote/
```
#### Get a Single Quote
```bash
curl http://localhost:8000/api/v1/quote/3fa85f64-5717-4562-b3fc-2c963f66afa6/
```
#### Create a Quote
```bash
curl -X POST http://localhost:8000/api/v1/quote/ \  
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    -H "Content-Type: application/json" \ 
    -d '{"author": "John Doe", "content": "Quote 1"}'
```
#### Update a Quote
```bash
curl -X PUT http://localhost:8000/api/v1/quote/3fa85f64-5717-4562-b3fc-2c963f66afa6/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"author": "Updated Author", "content": "Updated Quote"}'
```
#### Delete a Quote
```bash
curl -X DELETE http://localhost:8000/api/v1/quote/3fa85f64-5717-4562-b3fc-2c963f66afa6/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
#### Get a Random Quote
```bash
curl http://localhost:8000/api/v1/quote/random/
```

## Authentication
#### Obtain a JWT Token:
```bash
curl -X POST http://localhost:8000/api/v1/login/ \
  -d '{"username": "test_user", "password": "password1234"}'
```
#### Response:
```json
{
  "access": "YOUR_ACCESS_TOKEN",
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

## Data Structure
#### Quote Object
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "author": "John Doe",
  "content": "Sample quote text.",
  "created_at": "2023-09-15T12:34:56.789Z"
}
```

### Validation Rules
- `author`: Required (max 200 characters)
- `content`: Required
- `id` and `created_at`: Auto-generated (cannot be modified)

## Testing
Run the tests with:
```bash
python manage.py test
```

## Test Coverage
- CRUD operations
- Data integrity validation
- Authentication/Authorization checks
- Error handling (invalid IDs, missing fields)