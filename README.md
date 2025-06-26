# WOC - Flask API Backend

This is a clean, modular Flask API backend for the `woc` project, using MongoDB and JWT.

## 🔧 Features

- Flask with Blueprint-based API
- MongoDB integration via `flask-pymongo`
- JWT Authentication ready
- Clean separation: controllers, services, models
- Dockerized for easy deployment

## 📁 Project Structure

```
woc/
├── api/
│   ├── controllers/       # Route handlers
│   ├── services/          # Business logic
│   ├── models/            # MongoDB schemas
│   ├── auth/              # Decorators/auth utils
│   ├── utils/             # Helpers
│   ├── extensions.py      # Mongo, JWT, etc.
│   ├── config.py          # Configuration classes
│   └── routes.py          # Register all blueprints
├── main.py                # App entry point
├── .env                   # Environment variables
├── .flaskenv              # Flask environment config
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Multi-service (API + MongoDB)
└── README.md              # You're here!
```

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://your-repo-url.git
cd woc
```

### 2. Start with Docker

```bash
docker-compose up --build
```

Visit the API: [http://localhost:5000](http://localhost:5000)

### 3. API Example

```bash
curl -X POST http://localhost:5000/api/tenant/ -H "Content-Type: application/json" -d '{"user_id": "123", "first_name": "John", "last_name": "Doe"}'
```

---

## 🧪 Running Tests

Coming soon! Use `pytest` inside a virtualenv or container.

---

## 🔒 Environment Variables

`.env`

```env
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://mongo:27017/woc
```

---

## 📦 Dependencies

- Flask
- Flask-PyMongo
- Flask-JWT-Extended
- python-dotenv

---

## 🐳 Docker Notes

- Container: `woc_api` for Flask, `woc_mongo` for MongoDB
- Mongo is exposed at `localhost:27017`
