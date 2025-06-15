# Train Station Service

A RESTful API service for managing train stations, routes, trains, crews, journeys, orders, and tickets. Built with Django, Django REST Framework, PostgreSQL, and Docker. Provides endpoints for booking train journeys, managing schedules, and ticket ordering, with a modern API documentation interface (Swagger).

## Features

* CRUD operations for stations, routes, trains, train types, crews, journeys, orders, and tickets
* Nested creation of orders with tickets
* Filtering journeys by route, train, departure/arrival time and stations
* Permissions: Only admins can modify infrastructure (stations, routes, trains, etc.); authenticated users can view and filter available journeys, and can book and view their tickets
* JWT authentication
* Automatic database migrations
* Interactive API documentation at `/swagger/`
* Easy deployment via Docker Compose

## Technology Stack

* **Backend**: Python 3.12, Django, Django REST Framework
* **Database**: PostgreSQL 16 
* **API Docs**: drf-yasg (Swagger)
* **Containerization**: Docker, Docker Compose

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/lyaskov/TrainStation.git
cd TrainStation
```

### 2. Create `.env` file

Create a `.env` file in the root directory and add the following environment variables:

```env
DJANGO_SECRET_KEY="django-insecure-4#^xnph6ibzxxaqv@5ug3_gjl7$v@-^^@-hh!w)qex935av4#b"
DJANGO_DEBUG=True

POSTGRES_DB=train_station
POSTGRES_USER=train_station
POSTGRES_PASSWORD=train_station
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> **Note:** These values must match those in your docker-compose.yml and initial Postgres setup.

## Environment Variables

| Variable            | Description              |
| ------------------- |--------------------------|
| DJANGO\_SECRET\_KEY | Django secret key        |
| DJANGO\_DEBUG       | Enable debug mode        |
| POSTGRES\_DB        | PostgreSQL database name |
| POSTGRES\_USER      | PostgreSQL user          |
| POSTGRES\_PASSWORD  | PostgreSQL password      |
| POSTGRES\_HOST      | PostgreSQL host          |
| POSTGRES\_PORT      | PostgreSQL port          |

### 3. Build and Start the Application

```bash
docker-compose up --build
```

This will start both the Django app and the PostgreSQL database. The API will be available at [http://localhost:8000/](http://localhost:8000/).

### 4. Load Test Data (Optional)

After the containers are up and running, initial migrations will run automatically via the Docker Compose `command`. To load demo/test data (users, stations, etc.):

1. Open a shell into the web container:

   ```bash
   docker-compose exec web /bin/sh
   ```
2. Run:

   ```sh
   python manage.py loaddata initial_data.json
   ```

#### **Test Users in Demo Data:**

| Role  | Email                                     | Password   |
| ----- | ----------------------------------------- | ---------- |
| admin | [admin@admin.com](mailto:admin@admin.com) | 123456     |
| user  | [user1@user.com](mailto:user1@user.com)   | user123456 |

### 5. Open API Documentation (Swagger UI)

Go to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) in your browser for interactive API docs.

## API Authentication

* The API uses JWT authentication.
* Obtain access/refresh tokens using `/api/user/token/` (see Swagger UI for details).
* Include the access token in the `Authorization: Bearer <token>` header for all protected endpoints.

## Key Endpoints (see Swagger UI for full docs)

* `/api/stations/` — CRUD for stations *(admin only)*
* `/api/routes/` — CRUD for routes *(admin only)*
* `/api/trains/` — CRUD for trains *(admin only)*
* `/api/journeys/` — View, filter, create journeys
* `/api/orders/` — Create and view orders (with nested ticket creation)
* `/api/tickets/` — View your tickets

For details, request/response samples, and parameter descriptions, see Swagger docs at `/swagger/`.


## Troubleshooting

* **Port 5432 already in use**: Stop any local PostgreSQL server or change the external port in `docker-compose.yml`.
* **psycopg2 build errors**: Use `psycopg2-binary` in requirements.txt for easier installation in Docker.
* **Cannot connect to database**: Ensure env variables are set correctly and both containers are running.

## License

MIT (add your license here)

## Author & Support

* [lyaskov1@gmail.com](mailto:lyaskov1@gmail.com)
* Create an issue on GitHub for bug reports or suggestions.
