# CureConnect – Integrated Hospital Management System

CureConnect is a full-stack Integrated Hospital Management System designed to streamline hospital operations and improve patient care. It integrates critical healthcare functions like appointment booking, blood bank management, bed availability, doctor ratings, patient history, and ambulance services into a single, user-friendly platform.

## 🚀 Features
- Patient Appointment Booking – Patients can schedule, reschedule, and cancel appointments online.
- Blood Bank Management – Track donations, manage stock, and ensure real-time availability.
- Bed Availability Monitoring – View and update real-time bed occupancy across wards (ICU, General, Private).
- Doctor Rating System – Patients provide feedback, improving accountability and service quality.
- Patient History Management – Secure digital repository of patient records for better diagnosis and continuity of care.
- Ambulance Dispatch System – Ride-sharing style ambulance requests with GPS tracking and optimized response time.

## 🛠️ Tech Stack
- Frontend: HTML, CSS, JavaScript (with responsive design)
- Backend: Flask (Python)
- Database: MySQL 
- APIs: RESTful APIs for communication between modules
- Hosting: Cloud-ready (AWS / Azure)

## 📂 Project Structure
```
CureConnect/
  │── backend/          # Flask backend with APIs
  │── frontend/         # HTML, CSS, JS frontend
  │── database/         # SQL schema and migration files
  │── docs/             # Documentation and UML diagrams
  │── README.md         # Project overview
```

## ⚙️ Installation & Setup

### Clone the repository:
```
git clone https://github.com/Somcr1510/CureConnect.git
cd CureConnect
```

### Create a virtual environment & install dependencies:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup database (MySQL):
```
CREATE DATABASE cureconnect;
```

### Run migrations & start the backend:
```
flask db upgrade
flask run
```

### Open the app in browser:
```
http://127.0.0.1:5000
```

## 📊 System Architecture
### Three-tier architecture:
- Presentation Layer: User-friendly web interface (patients, doctors, admins)

- Application Layer: Business logic & APIs

- Database Layer: Secure medical records, appointments, inventory

## 📸 Screenshots

- ### Appointment Booking Interface

- ### Bed Availability Dashboard

- ### Blood Bank & Donation System

- ### Ambulance Request System


## 🔒 Security & Compliance
- Role-based access control (Admin, Doctor, Patient)
- Encrypted data storage 
- Regular database backups
