# Workout Planner 

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
- [Pytest](https://docs.pytest.org/)


### Database
- [PostgreSQL](https://www.postgresql.org/)
- [Neon](https://neon.tech/) (cloud-hosted PostgreSQL database)  

---
## Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Configure environment variables:
Create a `.env` file inside the `backend` directory containing the required database and authentication settings:

```
DATABASE_URL=your_neon_database_url
JWT_SECRET_KEY=your_secret_key
```

5. Run the Backend server:
```bash
flask run
```

---

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install the required dependencies:
```bash
npm install
```

3. Configure environment variables:
Create a `.env` file inside the `frontend` directory:

```
VITE_API_URL=http://localhost:5000/api
```

4. Start the development server:
```bash
npm run dev
```

## Deployment

The application is deployed using:

- Frontend: Vercel
- Backend: Render
- Database: Neon PostgreSQL

Live Demo: 
https://workout-planner-lilac.vercel.app