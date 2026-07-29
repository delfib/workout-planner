# Workout Planner 💪

**Workout Planner** is a full-stack web application that allows users to create, organize, and manage their personalized workout routines. Users can build weekly workout schedules, create reusable exercises, and keep track of their workouts through a simple and intuitive interface.

## Features

- User authentication with secure account registration and login.
- Create, search, filter, and delete custom exercises organized by categories.
- Build personalized workouts by assigning exercises with custom descriptions.
- Organize workouts by days of the week through a weekly planner view.
- Assign existing workouts to different days or create new ones directly from the planner.
- Edit workout details, add or remove exercises, and manage workout assignments.

---

## Tech Stack

### Frontend
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev/)
- [React Router](https://reactrouter.com/)

### Backend
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)


### Database
- [PostgreSQL](https://www.postgresql.org/)
- [Neon](https://neon.tech/) (cloud-hosted PostgreSQL database)  

---
## Backend Setup

#### Navigate to the backend directory:

```bash
cd backend
```

#### Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

#### Install the required dependencies:
```bash
pip install -r requirements.txt
```
#### Configure environment variables:
Create a `.env` file with the required database and authentication settings.

#### Run the Backend server:
```bash
flask run
```

---

## Frontend Setup

#### Navigate to the frontend directory:
```bash
cd frontend
```

#### Install the required dependencies:
```bash
npm install
```

#### Start the development server:
```bash
npm run dev
```