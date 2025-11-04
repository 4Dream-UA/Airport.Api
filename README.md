# ✈️ Airport API

Airport API is a backend REST system for managing flights, airplanes, routes, crews, and tickets.  
The project is built with **Django REST Framework** and provides a full airline operation cycle —  
from route creation to user ticket booking.

---

## ⚙️ Technologies

- Python 3.12  
- Django 5.x  
- Django REST Framework  
- PostgreSQL  
- JWT
- Swagger
- Docker

---

## 📦 Installation and Launch

### 1️⃣ Clone the repository

```bash
git clone https://github.com/4Dream-UA/Airport.Api.git
````

### 2️⃣ Run in Docker

```bash
docker-compose up --build
```

After startup, the API will be available at:

```
http://localhost:8000/
```

---

### 3️⃣ Create superuser
```bash
docker-compose exec app createsuperuser
```

## 🔐 Authentication

To access most endpoints, you need to obtain a token:

* `POST /api/token/` — obtain JWT token
* `POST /api/token/refresh/` — refresh the token

---

## 🧭 Main Endpoints

| Section              | Description                      | URL Prefix       |
| -------------------- | -------------------------------- | ---------------- |
| 👤 **User**      | User registration and management | `/api/user/`     |
| 🎫 **Tickets**   | User tickets and orders          | `/api/tickets/`  |
| 🛫 **Airlines**  | Airplanes, types, airline routes | `/api/airlines/` |
| 🌍 **Air Zone**  | Flights, airports, routes        | `/api/air_zone/` |
| 🔑 **JWT Auth**      | Access tokens                    | `/api/token/`    |
| 📘 **Documentation** | OpenAPI/Swagger documentation    | `/api/docs/`     |

---

## 🧩 Project Structure

```
airport_api/
│
├── air_zone/        # Route, airport and supported countries
├── airlines/        # Airplane, type, and crew models
├── tickets/         # Ticket and order
├── user/            # User registration
│
├── airport_service/     # Django configuration files
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

---

## 🧠 Core Logic

* Users can **view flights** and **create orders** with tickets.
* When a ticket is created, an **Order** is automatically generated and linked to the current user.
* Airplanes use **ImageField** for image uploads.
* Routes are **automatically created** if not found.
* Each ticket is unique within a flight (`UniqueConstraint(row, seat, flight)`).

---

## 🧾 Request Examples

### 🔹 Get all flights

```
GET /api/air_zone/flights/
```

### 🔹 Create a ticket

```
POST /api/tickets/
{
  "row": 3,
  "seat": 5,
  "flight": 7
}
```

### 🔹 View user orders

```
GET /api/tickets/orders/
```

---

## 📚 API Documentation

Swagger documentation is available at:

```
http://localhost:8000/api/docs/
```
