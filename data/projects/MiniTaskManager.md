# Mini Task Manager

A modern, full-stack task management application built with Django REST Framework and React. This project demonstrates clean architecture principles, secure authentication, and responsive design patterns for managing personal tasks efficiently.

## 🎯 Project Overview

Mini Task Manager provides users with an intuitive interface to create, organize, and track their daily tasks. The application features user authentication, CRUD operations for tasks, due date management, and a responsive Material-UI interface that adapts to both light and dark themes.

### Key Features

- **User Authentication**: Secure token-based authentication system
- **Task Management**: Full CRUD operations with real-time updates
- **Due Date Tracking**: DateTime picker integration for scheduling
- **Responsive Design**: Mobile-first approach with Material-UI components
- **Theme Support**: Light and dark mode compatibility
- **Data Persistence**: SQLite database with Django ORM

## 🏗️ Architecture & Design

### Backend Architecture
The backend follows Django's MVT (Model-View-Template) pattern with REST API endpoints:

```
taskmanager/           # Django project configuration
├── settings.py        # Application settings and middleware
├── urls.py           # URL routing configuration
├── wsgi.py           # WSGI application entry point
└── asgi.py           # ASGI application entry point

tasks/                # Main application module
├── models.py         # Task and User data models
├── views.py          # API views and business logic
├── serializers.py    # Data serialization layer
├── urls.py           # App-specific URL patterns
└── tests.py          # Unit and integration tests
```

### Frontend Architecture
The frontend implements a feature-based structure with React and TypeScript:

```
src/
├── app/              # Application shell and routing
├── features/         # Feature-specific components
│   ├── auth/         # Authentication components
│   ├── tasks/        # Task management components
│   └── about/        # About page components
├── theme/            # Material-UI theme configuration
└── lib/              # Shared utilities and helpers
```

### Data Flow
1. **Authentication**: Token-based auth stored in sessionStorage
2. **API Communication**: RESTful endpoints with proper HTTP methods
3. **State Management**: React hooks with useReducer for complex forms
4. **Component Architecture**: Reusable components with TypeScript interfaces

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+** (for Django backend)
- **Node.js 16+** (for React frontend)
- **npm or yarn** (package manager)
- **Git** (version control)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mini-task-manager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Create environment configuration**:
   ```bash
   # Create .env file with:
   VITE_BACKEND_URL=http://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

The frontend application will be available at `http://localhost:5173`

### Running Both Services

For optimal development experience, run both services simultaneously:

```bash
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## 📁 Project Structure

### `/taskmanager` - Django Configuration
Contains the main Django project settings, URL configuration, and WSGI/ASGI setup. This directory handles application-wide configurations including database settings, middleware, and CORS policies.

### `/tasks` - Core Application Logic
Houses the main business logic including:
- **Models**: Task data structure and user relationships
- **Views**: API endpoints using Django REST Framework ViewSets
- **Serializers**: Data transformation between JSON and Python objects
- **Authentication**: Token-based user authentication system

### `/frontend` - React Application
Contains the complete frontend application with:
- **Component Architecture**: Reusable UI components with TypeScript
- **Routing**: Client-side navigation with React Router
- **Styling**: Material-UI theme system with custom components
- **State Management**: React hooks and reducers for application state

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/signin/` - User sign in

### Task Management Endpoints
- `GET /api/tasks/` - List user tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Retrieve specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task