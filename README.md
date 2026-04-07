# Tiffin Service Backend System

##  Problem

Small tiffin and food service businesses often rely on manual processes like phone calls or WhatsApp for managing orders and payments. This leads to:

* No structured order tracking
* Difficulty in managing multiple customers
* Lack of online payment support
* High chances of human error

I started building this project to apply my Flask knowledge in a real-world scenario while also creating a practical solution that could benefit my friend’s startup.

---

## Approach

I designed a "backend-first system" using:

* Flask (Python) → REST API development
* PostgreSQL → Database for storing users, orders, and payments
* Modular Architecture → Separation of routes, services, and database logic
* Razorpay Integration (in progress) → For handling online payments

### Core Flow:

1. User registers and logs in
2. User creates an order
3. Backend stores order details in database
4. Payment flow is initiated (Razorpay)
5. Webhook confirms payment and updates order status

---

##  Iterations

This project was built incrementally:

* **Version 1:** Basic Flask setup and routing
* **Version 2:** User authentication (register/login APIs)
* **Version 3:** Order creation and database integration
* **Version 4:** API structuring and modularization
* **Current:** Integrating Razorpay payments and webhook handling

---

##  Key Design Choices

* Backend-controlled payments:
  Amount is always fetched from the database to prevent tampering.

* Webhook-based confirmation:
  Payment success is confirmed using Razorpay webhook instead of trusting frontend responses.

* Separation of concerns:
  Business logic is separated from routes to improve scalability and maintainability.

* Database-first validation:
  All critical operations (orders, payments) rely on database state rather than client input.

---

##  Current Status

*  User authentication implemented
*  Order system implemented
*  Razorpay order creation in progress
*  Currently working on webhook integration — faced issues understanding how Razorpay verifies payment securely

---

##  Daily Time Commitment

Worked consistently 2–3 hours daily, focusing on understanding backend concepts while building the project step-by-step.

---

##  Future Improvements

* Complete Razorpay payment + webhook flow
* Add order history for users
* Build frontend (React or Android)
* Add notifications (SMS/Email)
* Improve error handling and logging

---

##  Tech Stack

* Python (Flask)
* PostgreSQL
* REST APIs
* Razorpay (Payment Gateway - in progress)

---

##  Note

This project is actively being developed with a focus on learning real-world backend architecture and secure payment handling.
