# MarkMate 👨🏻‍🏫

MarkMate is an AI-powered educational platform that revolutionizes assignment grading through intelligent automation. It combines modern web technologies with advanced language models to provide instructors with efficient, consistent, and detailed grading capabilities.

## 🌟 Features

- **AI-Powered Grading**: Automated assignment evaluation using GPT-4 with customizable rubrics
- **Multi-Role Support**: Comprehensive role management for students, instructors, and administrators
- **Course Management**: Complete course creation, enrollment, and administration system
- **Assignment Workflow**: Full lifecycle management from assignment creation to submission grading
- **Intelligent Document Processing**: PDF parsing and content analysis for assignments and submissions
- **Dark Mode Support**: Modern, responsive UI with theme switching capabilities
- **Real-time Updates**: Dynamic interface updates and progress tracking

## 🏗️ Architecture

MarkMate follows a microservices architecture with three main components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │◄──►│   Backend       │◄──►│   LLM Service   │
│   (React)       │    │   (Django)      │    │   (Flask)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

- **Frontend**: React application with modern UI components and routing
- **Backend**: Django REST API with PostgreSQL database
- **LLM Service**: Flask microservice integrating OpenAI GPT-4 for grading

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MarkMate
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Setup LLM Service**
   ```bash
   cd llm
   pip install -r requirements.txt
   # Add your OpenAI API key to .env file
   python main.py
   ```

### Environment Variables

Create `.env` files in the `llm` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📱 Usage

1. **Access the application** at `http://localhost:5173`
2. **Create an account** as an instructor or student
3. **Create courses** and assignments with custom rubrics
4. **Submit assignments** for automated grading
5. **Review grades** and detailed feedback

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern UI library with hooks
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and development server

### Backend
- **Django 5.1**: Python web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Token Authentication**: Secure API access

### LLM Service
- **Flask**: Lightweight Python web framework
- **LangChain**: LLM application framework
- **OpenAI GPT-4**: Advanced language model
- **PyPDF**: PDF document processing

## 📁 Project Structure

```
MarkMate/
├── backend/          # Django REST API server
├── frontend/         # React web application
├── llm/             # Flask LLM microservice
└── README.md        # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please contact the development team or create an issue in the repository.

---

**MarkMate** - Transforming education through intelligent automation 🚀