# Apartment Visitor & Delivery Security System

A full-stack web application that digitizes visitor management and delivery tracking for residential apartments. The system enables residents to create visitor passes, security guards to verify visitors using QR codes and OTPs, and track deliveries securely.

## Features

### Resident
- Secure login using JWT authentication
- Create visitor passes
- Generate QR code for visitors
- View visitor history
- Receive delivery notifications
- Track deliveries

### Security Guard
- Secure login
- Verify visitors using QR Code or OTP
- Check-in and Check-out visitors
- Register incoming deliveries
- Update delivery status
- View active visitors

### Admin
- Manage apartments
- Manage residents
- View all visitors
- View all deliveries
- Monitor emergency alerts

---

## Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Axios
- React Router
- React Hot Toast
- Lucide React

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pydantic

### Database
- PostgreSQL

### DevOps
- Docker
- Docker Compose

---

## Project Structure

```
apartment_visitor/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## System Modules

### Authentication
- Resident Login
- Security Guard Login
- Admin Login
- JWT Token Authentication

### Visitor Management
- Create Visitor Pass
- QR Code Generation
- OTP Verification
- Visitor Check-In
- Visitor Check-Out
- Visitor History

### Delivery Management
- Register Delivery
- Update Delivery Status
- Delivery Tracking
- Resident Notifications

### Apartment Management
- Apartment Details
- Resident Profiles

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/apartment-visitor-security-system.git
cd apartment-visitor-security-system
```

---

## Using Docker

Start the application:

```bash
docker compose up --build
```

Frontend

```
http://localhost:5173
```

Backend

```
http://localhost:8000
```

Swagger API

```
http://localhost:8000/docs
```

---

## Database

PostgreSQL is used for storing:

- Users
- Residents
- Apartments
- Visitors
- Visitor Logs
- Deliveries
- Security Guards

---

## API Endpoints

### Authentication

```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Visitors

```
POST /api/visitors/
GET  /api/visitors/
POST /api/visitors/check-in
POST /api/visitors/{id}/check-out
```

### Deliveries

```
POST /api/deliveries/
GET  /api/deliveries/
PATCH /api/deliveries/{id}
```

### Apartments

```
GET /api/apartments/
POST /api/apartments/
```

---

## Future Enhancements

- Face Recognition
- SMS OTP Integration
- Email Notifications
- Visitor Photo Upload
- Resident Mobile App
- AI-based Visitor Analytics

---

## Screenshots

Add screenshots of:

- Login Page
- Resident Dashboard
- Security Dashboard
- Create Visitor Pass
- Delivery Management
- QR Code Generation

---

## Author

**Ratchana M**

Integrated M.Tech Computer Science and Engineering

SSN College of Engineering

---

## License

This project is developed for educational and learning purposes.
