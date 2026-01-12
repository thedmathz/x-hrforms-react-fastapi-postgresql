# HR Forms

HR Forms is a web-based Human Resource application designed to digitize employee filing and approval workflows such as **Leave** and **Travel Requests**.  
It enables employees, recommenders, and approvers to manage applications efficiently through a secure, role-based system.

---

## 🚀 Features

### Core Modules
- **Dashboard** – Overview of application statistics and status
- **My Applications** – Employee filing and tracking of leave and travel requests
- **For Approvals** – Recommender and approver review & decision module
- **Offices** – Office management
- **Positions** – Position management
- **Users** – User account management
- **User Types / Roles** – Role-based access control
- **Authentication** – Token-based authentication (Access & Refresh tokens)

---

## 🔐 Security & Access Control
- Role-Based Access Control (RBAC) managed by **Admin**
- Encrypted IDs in URL parameters
- JWT Authentication
  - Access Token
  - Refresh Token
- Secure API endpoints
- Async backend processing using FastAPI

---

## 📊 Additional Capabilities
- Excel export of application records
- PDF printing of employee application lists
- Centralized approval workflow
- Async API for improved performance

---

## 🛠️ Tech Stack

### Frontend
- React
- JavaScript / TypeScript
- Axios
- Modern UI components

### Backend
- FastAPI (Async)
- Python
- JWT Authentication

### Database
- PostgreSQL

---

## 🗄️ Database Design
The system uses a relational PostgreSQL database to manage users, applications, approvals, and organizational structure.

> 📌 **Database Schema**
> <img width="1249" height="1217" alt="Database Schema" src="https://github.com/user-attachments/assets/a3a7b48f-50e8-4fe4-9c64-7a3000dd2640" />


