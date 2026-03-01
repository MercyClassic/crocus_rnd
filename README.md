# 🌸 CROCUS RND

## 📖 Description
CROCUS RND is an online flower shop with delivery in Rostov-on-Don.
The platform provides convenient features for both users and administrators:

- 🛒 **Cart** – add products to the cart
- 📝 **Order** – create and track orders
- ❤️ **Favourites** – save your favorite products
- 💳 **Payments** – integration with Yookassa API
- 🤖 **Telegram Bot** – admin panel and notifications

[Visit the website](https://crocus-rnd.ru/)

---

## 🛠 Project Stack

| Component              | Technology / Framework |
|------------------------|------------------------|
| **Backend**            | Python 3.11, DRF (API) |
| **Frontend**           | React                  |
| **Streaming (notify)** | Fast Stream            |
| **Telegram Bot**       | Aiogram3               |
| **Database**           | PostgreSQL             |
| **Cache**              | Redis                  |
| **Broker**             | RabbitMQ               |
| **Containerization**   | Docker                 |
| **Web Server**         | Nginx                  |
| **Monitoring**         | Sentry                 |

---

## 🔗 Architecture Overview
- **API**: REST API using Django REST Framework (DRF) for frontend communication
- **DB**: PostgreSQL stores users, orders, and product data
- **Cache**: Redis for faster access to frequently used data
- **Queue**: RabbitMQ for background tasks and notifications
- **Payments**: Yookassa for secure online payments
- **Telegram Bot**: Admin panel and order notifications

---

## ⚙️ License
- **BSD 3-Clause License**
- © 2023–present MercyClassic
