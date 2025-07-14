# 🏥 MediQuick - Quick Commerce Medicine Delivery Application

A comprehensive, accessible, and high-performance medicine delivery platform built with modern technologies for quick and reliable healthcare solutions.

## 🎯 Project Overview

**MediQuick** is a full-stack quick commerce medicine delivery application that enables users to order medicines online with 30-minute delivery. The platform features prescription upload with OCR processing, real-time order tracking, and accessibility-first design optimized for elderly users.

### ✨ Key Features

- **🔍 Smart Medicine Search**: Real-time search with autocomplete and voice search
- **📋 Prescription Management**: Upload and verify prescriptions with OCR technology  
- **🛒 Intelligent Cart**: Real-time cart updates with prescription validation
- **📱 Real-time Tracking**: Live order status updates and delivery tracking
- **♿ Accessibility First**: WCAG 2.1 AA compliant with elderly-friendly features
- **🔒 Secure Payments**: Multiple payment options with secure transactions
- **⚡ Quick Delivery**: 30-minute delivery with emergency 15-minute option
- **👨‍⚕️ Admin Dashboard**: Comprehensive management tools for pharmacies

## 🏗️ Architecture & Technology Stack

### 🔧 Backend (90%+ PRD Compliance)
- **Framework**: FastAPI (Python 3.11+) - High-performance async API
- **Database**: SQLite with SQLAlchemy ORM + Alembic migrations
- **Authentication**: JWT tokens with bcrypt password hashing
- **File Processing**: OCR for prescription text extraction
- **API Documentation**: Automatic OpenAPI/Swagger documentation

### 🎨 Frontend (Complete Implementation)
- **Framework**: Vite + React 18 + TypeScript
- **State Management**: Zustand for global state
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion + Three.js for smooth interactions
- **Forms**: React Hook Form with Zod validation

## 📊 Implementation Status

| Component | Status | Compliance |
|-----------|--------|------------|
| **Backend API** | ✅ Complete | 90%+ PRD |
| **Frontend UI** | ✅ Complete | 95%+ PRD |
| **Authentication** | ✅ Complete | 100% |
| **Medicine Catalog** | ✅ Complete | 100% |
| **Cart Management** | ✅ Complete | 100% |
| **Order Processing** | ✅ Complete | 100% |
| **Prescription Upload** | ✅ Complete | 95% |
| **Accessibility** | ✅ Complete | WCAG 2.1 AA |

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)

### 🔧 Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🎨 Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 🌐 Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
medicine-delivery-app/
├── 🔧 backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   ├── core/              # Core configuration and security
│   │   ├── database/          # Database configuration
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic services
│   │   └── main.py            # FastAPI application entry point
│   ├── alembic/               # Database migrations
│   └── requirements.txt       # Python dependencies
├── 🎨 frontend/               # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── stores/           # Zustand state management
│   │   ├── services/         # API services
│   │   └── types/            # TypeScript definitions
│   └── package.json          # Node.js dependencies
└── docs/                     # Project documentation
```

## 🔌 Key API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Medicine Catalog
- `GET /api/v1/medicines/search` - Search medicines
- `GET /api/v1/categories/` - Get categories
- `GET /api/v1/medicines/{id}` - Medicine details

### Cart & Orders
- `GET /api/v1/cart/` - Get user cart
- `POST /api/v1/cart/items` - Add to cart
- `POST /api/v1/orders/from-cart` - Create order
- `GET /api/v1/orders/{id}/tracking` - Track order

## ♿ Accessibility Features (WCAG 2.1 AA)

- **📱 Font Scaling**: 100%, 125%, 150% options
- **🔆 High Contrast**: Enhanced visibility mode
- **⌨️ Keyboard Navigation**: Full keyboard support
- **🔊 Screen Reader**: ARIA labels and semantic HTML
- **🎤 Voice Search**: Voice commands for search
- **👆 Large Touch Targets**: 44px minimum for elderly users

## 🚀 Deployment

### Backend (Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy with automatic builds

### Frontend (Vercel)
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Deploy with automatic builds

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration

## ⚡ Performance Optimization

- Database query optimization
- Caching strategies ready
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Progressive Web App (PWA)

## 🧪 Testing

### Backend
```bash
cd backend
python test_api.py  # Comprehensive API testing
pytest tests/ -v    # Unit tests
```

### Frontend
```bash
cd frontend
npm test           # Component tests
npm run type-check # TypeScript validation
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **📧 Email**: support@mediquick.com
- **📞 Phone**: 1800-MEDIQUICK
- **🐛 Issues**: [GitHub Issues](https://github.com/shaonidutta/medicine-delivery-app/issues)
- **📚 Documentation**: Check the `docs/` folder

---

<div align="center">

**🏥 MediQuick - Delivering Health, Delivering Hope 🏥**

*Built with ❤️ for accessible healthcare delivery*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![WCAG 2.1 AA](https://img.shields.io/badge/accessibility-WCAG%202.1%20AA-green.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

</div>
