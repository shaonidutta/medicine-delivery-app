# Quick Commerce Medicine Delivery Application - Product Requirements Document (PRD)

## 1. Executive Summary

### 1.1 Product Overview
A comprehensive quick commerce medicine delivery platform that enables users to order medicines with 10-30 minute delivery promise, featuring prescription handling, real-time inventory tracking, and optimized user experience for medical needs.

### 1.2 Key Features
- User authentication with medical profile management
- Medicine catalog with search and categorization
- Prescription upload and verification system
- Shopping cart with prescription validation
- Real-time order tracking and delivery
- Emergency medicine delivery
- Location-based pharmacy integration

## 2. Frontend Components Specifications

### 2.1 Authentication Components

#### 2.1.1 Registration Component (`RegisterForm`)
**Purpose**: User registration with medical profile creation
**Functionality**:
- Multi-step form with personal details, medical information, and delivery address
- Phone number verification integration
- Form validation with medical-specific fields
- Accessibility features for elderly users

**User Interactions**:
- Form input with real-time validation
- Phone OTP verification flow
- Medical profile setup (allergies, chronic conditions)
- Address autocomplete with geolocation

**Visual Design**:
- Clean, medical-themed UI with trust indicators
- Large, readable fonts for accessibility
- Progress indicator for multi-step process
- Smooth transitions between steps

**State Management**:
- Form data persistence across steps
- Validation error states
- Loading states for API calls
- Phone verification status

**Props/Data Requirements**:
```typescript
interface RegisterFormProps {
  onSuccess: (user: User) => void;
  onError: (error: string) => void;
  initialData?: Partial<UserRegistration>;
}
```

#### 2.1.2 Login Component (`LoginForm`)
**Purpose**: User authentication
**Functionality**:
- Email/phone and password login
- Remember me functionality
- Password reset flow
- Social login options

**Responsive Design**: Mobile-first with tablet and desktop optimizations

### 2.2 Medicine Catalog Components

#### 2.2.1 Medicine Search Component (`MedicineSearch`)
**Purpose**: Advanced medicine search with filters
**Functionality**:
- Real-time search with autocomplete
- Category filtering
- Price range filtering
- Prescription requirement filtering
- Sort by relevance, price, availability

**User Interactions**:
- Debounced search input
- Filter toggles with visual feedback
- Search suggestions dropdown
- Clear filters functionality

**State Management**:
- Search query state
- Filter selections
- Search results with pagination
- Loading and error states

#### 2.2.2 Medicine Card Component (`MedicineCard`)
**Purpose**: Display individual medicine information
**Functionality**:
- Medicine details (name, price, manufacturer)
- Stock availability indicator
- Prescription requirement badge
- Add to cart functionality
- Alternative medicines suggestion

**Visual Design**:
- Card layout with subtle shadows
- Color-coded availability status
- Prescription requirement visual indicator
- Hover effects with smooth animations

### 2.3 Prescription Management Components

#### 2.3.1 Prescription Upload Component (`PrescriptionUpload`)
**Purpose**: Upload and manage prescription images
**Functionality**:
- Drag-and-drop image upload
- Camera capture for mobile
- Image preview and editing
- OCR text extraction preview
- Multiple prescription management

**Technical Requirements**:
- Image compression and optimization
- File type validation
- Progress indicators
- Error handling for upload failures

### 2.4 Shopping Cart Components

#### 2.4.1 Cart Component (`ShoppingCart`)
**Purpose**: Manage selected medicines and quantities
**Functionality**:
- Item quantity adjustment
- Prescription validation display
- Price calculation with taxes
- Delivery time estimation
- Emergency delivery option

**State Management**:
- Cart items with real-time updates
- Prescription validation status
- Price calculations
- Delivery options

### 2.5 Order Management Components

#### 2.5.1 Order Tracking Component (`OrderTracker`)
**Purpose**: Real-time order status and delivery tracking
**Functionality**:
- Live order status updates
- Delivery partner information
- Estimated delivery time
- Interactive map with delivery route
- Push notification integration

**Visual Design**:
- Timeline-based status display
- Interactive map component
- Real-time updates with smooth animations
- Emergency contact options

## 3. Backend Components Specifications

### 3.1 Authentication Service

#### 3.1.1 User Management Module
**API Endpoints**:
- `POST /auth/register` - User registration
- `POST /auth/login` - Authentication
- `GET /auth/me` - Profile retrieval
- `PUT /auth/profile` - Profile updates
- `POST /auth/verify-phone` - Phone verification

**Database Schema**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    medical_conditions TEXT[],
    allergies TEXT[],
    emergency_contact JSONB,
    delivery_addresses JSONB[],
    phone_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Business Logic**:
- Password hashing with bcrypt (passlib)
- JWT token generation and validation with python-jose
- Phone number verification via SMS
- Medical profile validation with Pydantic
- Address geocoding and validation

**Authentication Requirements**:
- JWT-based authentication with FastAPI security
- Role-based access control (user, pharmacy_admin, pharmacist, delivery_partner)
- Session management with Redis
- Password complexity requirements with Pydantic validators

**FastAPI Implementation Details**:
```python
# Dependencies for authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

security = HTTPBearer()

async def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    # JWT token validation logic
    pass

async def require_role(required_role: str):
    # Role-based access control decorator
    pass
```

### 3.2 Medicine Catalog Service

#### 3.2.1 Medicine Management Module
**API Endpoints**:
- `GET /medicines` - Medicine listing with pagination
- `POST /medicines` - Add medicine (admin only)
- `PUT /medicines/{id}` - Update medicine
- `DELETE /medicines/{id}` - Remove medicine
- `GET /medicines/search` - Advanced search
- `GET /medicines/{id}/alternatives` - Alternative medicines
- `PATCH /medicines/{id}/stock` - Stock updates

**Database Schema**:
```sql
-- Categories table for medicine categorization
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    parent_category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Medicines table with complete specifications
CREATE TABLE medicines (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255),
    manufacturer VARCHAR(255) NOT NULL,
    category_id UUID REFERENCES categories(id),
    description TEXT,
    dosage_form VARCHAR(100),
    strength VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    prescription_required BOOLEAN DEFAULT FALSE,
    stock_quantity INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 10,
    expiry_date DATE,
    batch_number VARCHAR(100),
    storage_conditions TEXT,
    side_effects TEXT[],
    contraindications TEXT[],
    active_ingredients JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_medicines_category ON medicines(category_id);
CREATE INDEX idx_medicines_name ON medicines(name);
CREATE INDEX idx_medicines_prescription_required ON medicines(prescription_required);
CREATE INDEX idx_medicines_stock ON medicines(stock_quantity);
CREATE INDEX idx_categories_parent ON categories(parent_category_id);
```

#### 3.2.2 Category Management Module
**API Endpoints**:
- `GET /categories` - Get all medicine categories
- `POST /categories` - Create new category (pharmacy admin)
- `PUT /categories/{id}` - Update category (pharmacy admin)
- `DELETE /categories/{id}` - Delete category (pharmacy admin)

**Business Logic**:
- Hierarchical category structure support
- Category-based medicine filtering
- Admin-only category management
- Cascade delete protection for categories with medicines

**FastAPI Models and Schemas**:
```python
# Pydantic models for request/response
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_category_id: Optional[str] = None

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    parent_category_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MedicineCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    generic_name: Optional[str] = None
    manufacturer: str = Field(..., min_length=1, max_length=255)
    category_id: Optional[str] = None
    description: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    price: float = Field(..., gt=0)
    prescription_required: bool = False
    stock_quantity: int = Field(default=0, ge=0)
    min_stock_level: int = Field(default=10, ge=0)
```

### 3.3 Prescription Service

#### 3.3.1 Prescription Processing Module
**API Endpoints**:
- `POST /prescriptions/upload` - Upload prescription
- `GET /prescriptions` - User prescriptions
- `GET /prescriptions/{id}` - Get specific prescription details
- `PUT /prescriptions/{id}/verify` - Pharmacist verification
- `GET /prescriptions/{id}/medicines` - Extract medicines

**Database Schema**:
```sql
-- Prescriptions table for prescription management
CREATE TABLE prescriptions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, verified, rejected
    doctor_name VARCHAR(255),
    doctor_license VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    extracted_medicines JSONB,
    verification_notes TEXT,
    verified_by UUID REFERENCES users(id), -- pharmacist who verified
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_prescriptions_user ON prescriptions(user_id);
CREATE INDEX idx_prescriptions_status ON prescriptions(status);
CREATE INDEX idx_prescriptions_verified_by ON prescriptions(verified_by);
```

**Business Logic**:
- Image processing and OCR
- Medicine extraction from prescription
- Pharmacist verification workflow
- Prescription validity checking
- Digital signature verification

### 3.4 Shopping Cart Service

#### 3.4.1 Cart Management Module
**API Endpoints**:
- `GET /cart` - Get user's cart with prescription validation
- `POST /cart/items` - Add medicine to cart
- `PUT /cart/items/{id}` - Update cart item quantity
- `DELETE /cart/items/{id}` - Remove medicine from cart
- `DELETE /cart` - Clear entire cart
- `POST /cart/validate-prescriptions` - Validate prescription medicines in cart

**Database Schema**:
```sql
-- Shopping cart table
CREATE TABLE carts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Cart items table
CREATE TABLE cart_items (
    id UUID PRIMARY KEY,
    cart_id UUID REFERENCES carts(id) ON DELETE CASCADE,
    medicine_id UUID REFERENCES medicines(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    prescription_id UUID REFERENCES prescriptions(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(cart_id, medicine_id)
);

-- Indexes for performance
CREATE INDEX idx_carts_user ON carts(user_id);
CREATE INDEX idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX idx_cart_items_medicine ON cart_items(medicine_id);
```

### 3.5 Order Management Service

#### 3.5.1 Order Processing Module
**API Endpoints**:
- `POST /orders` - Create order from cart with delivery details
- `GET /orders` - Get user's orders with delivery status
- `GET /orders/{id}` - Get specific order details
- `PATCH /orders/{id}/status` - Update order status (pharmacy/delivery partner)
- `GET /orders/{id}/track` - Real-time order tracking
- `POST /orders/{id}/delivery-proof` - Upload delivery confirmation

**Database Schema**:
```sql
-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    total_amount DECIMAL(10,2) NOT NULL,
    delivery_address JSONB NOT NULL,
    delivery_partner_id UUID REFERENCES delivery_partners(id),
    pharmacy_id UUID REFERENCES pharmacies(id),
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    emergency_order BOOLEAN DEFAULT FALSE,
    delivery_proof_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    medicine_id UUID REFERENCES medicines(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    prescription_id UUID REFERENCES prescriptions(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_delivery_partner ON orders(delivery_partner_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### 3.6 Delivery Service

#### 3.6.1 Delivery Optimization Module
**API Endpoints**:
- `GET /delivery/estimate` - Get delivery time estimate
- `GET /delivery/partners` - Get available delivery partners
- `POST /delivery/emergency` - Create emergency medicine delivery request
- `GET /nearby-pharmacies` - Find nearby pharmacies with stock

**Database Schema**:
```sql
-- Delivery partners table
CREATE TABLE delivery_partners (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    vehicle_type VARCHAR(50), -- bike, scooter, car
    license_number VARCHAR(100),
    current_location POINT,
    is_available BOOLEAN DEFAULT TRUE,
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_deliveries INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Pharmacies table
CREATE TABLE pharmacies (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    location POINT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    license_number VARCHAR(100) NOT NULL,
    operating_hours JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Pharmacy medicine inventory
CREATE TABLE pharmacy_medicines (
    id UUID PRIMARY KEY,
    pharmacy_id UUID REFERENCES pharmacies(id),
    medicine_id UUID REFERENCES medicines(id),
    stock_quantity INTEGER DEFAULT 0,
    price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE(pharmacy_id, medicine_id)
);

-- Indexes for performance
CREATE INDEX idx_delivery_partners_location ON delivery_partners USING GIST(current_location);
CREATE INDEX idx_delivery_partners_available ON delivery_partners(is_available);
CREATE INDEX idx_pharmacies_location ON pharmacies USING GIST(location);
CREATE INDEX idx_pharmacy_medicines_pharmacy ON pharmacy_medicines(pharmacy_id);
CREATE INDEX idx_pharmacy_medicines_medicine ON pharmacy_medicines(medicine_id);
```

**Business Logic**:
- Route optimization algorithms
- Real-time partner tracking
- Dynamic delivery time calculation
- Emergency prioritization system
- Inventory-based pharmacy selection

## 4. System Architecture

### 4.1 High-Level Architecture
```
Frontend (React/Next.js) ↔ API Gateway ↔ Microservices
                                        ↓
                                   Database Layer
                                        ↓
                              External Services
```

### 4.2 Microservices Architecture
- **Authentication Service**: User management and security
- **Catalog Service**: Medicine and category management
- **Prescription Service**: Image processing and verification
- **Order Service**: Order processing and management
- **Delivery Service**: Logistics and tracking
- **Notification Service**: Push notifications and alerts
- **Payment Service**: Transaction processing

### 4.3 Data Flow
1. User authentication and profile management
2. Medicine search and catalog browsing
3. Prescription upload and verification
4. Cart management with validation
5. Order creation and processing
6. Real-time delivery tracking
7. Order completion and feedback

## 5. Technical Requirements

### 5.1 Frontend Technology Stack
- **Framework**: Vite with React 18 and TypeScript
- **UI Library**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom medical theme
- **State Management**: Zustand for global state
- **Forms**: React Hook Form with Zod validation
- **HTTP Client**: Axios with interceptors
- **Real-time**: WebSocket client for real-time updates
- **Maps**: Google Maps API
- **Animations**: Three.js for 3D animations and Framer Motion
- **Build Tool**: Vite for fast development and building

### 5.2 Backend Technology Stack
- **Framework**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for session and data caching
- **Authentication**: JWT with refresh tokens using python-jose
- **File Storage**: AWS S3 for prescription images
- **Real-time**: WebSockets with FastAPI WebSocket support
- **Background Tasks**: Celery with Redis broker
- **Validation**: Pydantic for request/response validation
- **Migration**: Alembic for database migrations
- **Testing**: pytest with pytest-asyncio
- **API Documentation**: Automatic OpenAPI/Swagger with FastAPI

### 5.3 Infrastructure Requirements
- **Hosting**: AWS/Vercel for frontend, AWS ECS for backend
- **Database**: AWS RDS PostgreSQL
- **Cache**: AWS ElastiCache Redis
- **CDN**: CloudFront for static assets
- **Monitoring**: AWS CloudWatch
- **CI/CD**: GitHub Actions

### 5.4 Performance Requirements
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 500ms
- **Delivery Promise**: 10-30 minutes
- **Uptime**: 99.9%
- **Concurrent Users**: 10,000+

### 5.5 Security Requirements
- **Data Encryption**: TLS 1.3 for data in transit
- **Authentication**: Multi-factor authentication
- **Authorization**: Role-based access control
- **Data Privacy**: HIPAA compliance for medical data
- **Input Validation**: Server-side validation for all inputs
- **Rate Limiting**: API rate limiting and DDoS protection

## 6. Implementation Guidelines

### 6.1 Development Phases
1. **Phase 1**: Authentication and user management
2. **Phase 2**: Medicine catalog and search
3. **Phase 3**: Prescription handling
4. **Phase 4**: Cart and order management
5. **Phase 5**: Delivery tracking and optimization
6. **Phase 6**: Testing and deployment

### 6.2 Quality Assurance
- Unit testing with Jest and React Testing Library
- Integration testing for API endpoints
- End-to-end testing with Playwright
- Performance testing with Lighthouse
- Security testing and vulnerability assessment

### 6.3 Accessibility Requirements
- WCAG 2.1 AA compliance
- Screen reader compatibility
- Keyboard navigation support
- High contrast mode
- Large font options for elderly users

This PRD provides comprehensive specifications for building a quick commerce medicine delivery application with all required features and technical considerations.
