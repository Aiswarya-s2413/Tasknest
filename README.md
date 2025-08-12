# TaskNest 🗂️

A modern, full-stack task management application built with Django REST Framework and vanilla JavaScript. TaskNest helps you organize, schedule, and track your tasks with an intuitive interface and powerful features.

## ✨ Features

### 🔐 Authentication & Security
- **Dual Login Options**: Password-based and OTP-based authentication
- **JWT Token Authentication**: Secure API access with refresh tokens
- **User Registration**: Complete signup flow with email verification
- **Cookie-based Session Management**: Seamless user experience

### 📋 Task Management
- **CRUD Operations**: Create, read, update, and delete tasks
- **Priority Levels**: Organize tasks by Low, Medium, and High priority
- **Due Dates & Scheduling**: Set deadlines and schedule tasks
- **Task Status Tracking**: Mark tasks as complete/incomplete
- **Overdue Detection**: Automatic identification of overdue tasks

### 📅 Dashboard & Calendar
- **Interactive Calendar**: Visual task scheduling and overview
- **Task Overview**: Quick glance at your task statistics
- **Responsive Design**: Works seamlessly across devices

### 🎨 User Interface
- **Modern Design**: Clean and intuitive interface
- **Smooth Animations**: Fade-in effects and transitions
- **Mobile Responsive**: Optimized for all screen sizes
- **Dark/Light Theme Support**: Comfortable viewing experience

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.4 with Django REST Framework
- **Database**: MongoDB with MongoEngine ODM
- **Authentication**: JWT with SimpleJWT
- **Email**: SMTP integration for OTP delivery
- **CORS**: Configured for cross-origin requests

### Frontend
- **Languages**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with modern design patterns
- **API Communication**: Fetch API for backend integration
- **Deployment**: Vercel-ready configuration

### Key Dependencies
```
Django==5.2.4
djangorestframework==3.16.0
mongoengine==0.29.1
djangorestframework_simplejwt==5.5.1
django-cors-headers==4.7.0
pymongo==4.13.2
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Node.js (for frontend development)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskNest
   ```

2. **Set up virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

5. **Database Setup**
   Update MongoDB connection in `core/settings.py`:
   ```python
   connect(
       db='your-database-name',
       username='your-username',
       password='your-password',
       host='your-mongodb-connection-string'
   )
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Update API endpoints**
   Modify the API base URL in JavaScript files to match your backend URL.

3. **Serve the frontend**
   - For development: Use a local server (Live Server extension in VS Code)
   - For production: Deploy to Vercel or any static hosting service

## 📁 Project Structure

```
TaskNest/
├── backend/
│   ├── core/                 # Django project settings
│   │   ├── settings.py       # Main configuration
│   │   ├── urls.py          # URL routing
│   │   └── wsgi.py          # WSGI configuration
│   ├── tasks/               # Main application
│   │   ├── models/          # Data models
│   │   │   ├── auth.py      # User authentication model
│   │   │   └── task.py      # Task model
│   │   ├── views/           # API views
│   │   ├── serializers/     # Data serializers
│   │   ├── urls/            # App URL patterns
│   │   └── authentication.py # Custom JWT authentication
│   ├── requirements.txt     # Python dependencies
│   └── manage.py           # Django management script
├── frontend/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   ├── login.js        # Login functionality
│   │   ├── signup.js       # Registration functionality
│   │   ├── dashboard.js    # Dashboard logic
│   │   ├── tasks.js        # Task management
│   │   └── calendar.js     # Calendar functionality
│   ├── index.html          # Login page
│   ├── signup.html         # Registration page
│   ├── dashboard.html      # Main dashboard
│   ├── tasks.html          # Task management page
│   └── vercel.json         # Vercel deployment config
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Password login
- `POST /api/auth/request-otp/` - Request OTP
- `POST /api/auth/verify-otp/` - Verify OTP login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `PATCH /api/tasks/{id}/complete/` - Mark task as complete
- `PATCH /api/tasks/{id}/incomplete/` - Mark task as incomplete

## 🎯 Key Features Explained

### Task Model
```python
class Task(Document):
    user = ReferenceField(User, required=True)
    title = StringField(required=True, max_length=200)
    description = StringField()
    due_date = DateTimeField()
    priority = StringField(choices=['low', 'medium', 'high'])
    is_completed = BooleanField(default=False)
    scheduled_time = DateTimeField()
    # ... additional fields
```

### Authentication Flow
1. **Password Login**: Traditional email/password authentication
2. **OTP Login**: Email-based one-time password system
3. **JWT Tokens**: Secure API access with automatic refresh
4. **Cookie Management**: Seamless session handling

### Task Management
- **Priority System**: Three-level priority classification
- **Due Date Tracking**: Automatic overdue detection
- **Status Management**: Complete/incomplete state tracking
- **User Association**: Tasks linked to authenticated users

## 🚀 Deployment

### Backend (Django)
- Deploy to platforms like Heroku, DigitalOcean, or AWS
- Configure environment variables for production
- Set up MongoDB Atlas for database hosting
- Configure email service for OTP functionality

### Frontend
- Deploy to Vercel, Netlify, or GitHub Pages
- Update API endpoints to production URLs
- Configure CORS settings in Django for production domain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues & Roadmap

### Current Limitations
- Email configuration required for OTP functionality
- MongoDB Atlas dependency for database

### Future Enhancements
- [ ] Task categories and tags
- [ ] Team collaboration features
- [ ] Mobile app development
- [ ] Advanced reporting and analytics
- [ ] Integration with calendar applications
- [ ] Notification system
- [ ] Task templates
- [ ] Bulk operations


**TaskNest** - Organize your tasks, organize your life! 🚀