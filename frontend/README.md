# MediQuick Frontend - Quick Commerce Medicine Delivery

A modern, accessible, and performant React frontend for the Quick Commerce Medicine Delivery application.

## 🚀 Features

### Core Features
- **Quick Medicine Search** - Real-time search with autocomplete and voice search
- **Prescription Upload** - Drag-and-drop prescription upload with OCR processing
- **Smart Cart Management** - Real-time cart updates with prescription validation
- **Order Tracking** - Live order status updates and delivery tracking
- **User Profile Management** - Medical profiles with allergy and condition tracking

### Accessibility Features (WCAG 2.1 AA Compliant)
- **Font Scaling** - 100%, 125%, 150% text size options
- **High Contrast Mode** - Enhanced color contrast for better visibility
- **Keyboard Navigation** - Full keyboard accessibility support
- **Screen Reader Support** - ARIA labels and semantic HTML
- **Voice Search** - Voice commands for medicine search
- **Large Touch Targets** - Minimum 44px clickable areas for elderly users

### Performance Features
- **Smooth Animations** - Three.js powered animations with 60fps target
- **Progressive Web App** - Offline support and installable
- **Code Splitting** - Optimized bundle loading
- **Image Optimization** - Lazy loading and responsive images
- **Caching Strategy** - Intelligent caching for better performance

## 🛠 Tech Stack

- **Framework**: Vite + React 18 + TypeScript
- **State Management**: Zustand
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion + Three.js
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios with interceptors
- **Routing**: React Router v6
- **PWA**: Service Worker + Web App Manifest

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # Basic UI components (Button, Input, etc.)
│   │   ├── forms/          # Form components
│   │   ├── animations/     # Three.js animation components
│   │   └── accessibility/  # Accessibility-focused components
│   ├── pages/              # Page components
│   ├── hooks/              # Custom React hooks
│   ├── stores/             # Zustand stores
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript type definitions
│   └── styles/             # Global styles and themes
├── public/                 # Static assets
└── docs/                   # Component documentation
```

## 🎨 Design System

### Color Palette
- **Primary**: Medical Blue (#2563EB)
- **Secondary**: Health Green (#059669)
- **Accent**: Emergency Red (#DC2626)
- **Neutral**: 8-step grayscale (#374151 to #F9FAFB)

### Typography
- **Font Family**: Inter (high readability)
- **Base Size**: 16px (accessibility compliant)
- **Scale**: Modular scale with 1.25 ratio
- **Line Height**: 1.6 for body text, 1.2 for headings

### Animation Principles
- **Duration**: 200-300ms for micro-interactions
- **Easing**: cubic-bezier(0.4, 0, 0.2, 1)
- **Performance**: GPU-accelerated transforms
- **Accessibility**: Respects prefers-reduced-motion

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shaonidutta/medicine-delivery-app.git
   cd medicine-delivery-app/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   ```
   http://localhost:5173
   ```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript checks
- `npm run test` - Run tests

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1

# App Configuration
VITE_APP_NAME=MediQuick
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_VOICE_SEARCH=true
VITE_ENABLE_PUSH_NOTIFICATIONS=true
VITE_ENABLE_THREE_JS_ANIMATIONS=true

# Third-party Services
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
VITE_FIREBASE_API_KEY=your_firebase_api_key

# Analytics
VITE_GOOGLE_ANALYTICS_ID=your_google_analytics_id
```

## 🎯 Key Components

### Authentication
- JWT token management with automatic refresh
- Protected routes with role-based access
- Secure token storage and rotation

### State Management
- **AuthStore**: User authentication and profile
- **CartStore**: Shopping cart management
- **UIStore**: UI state and accessibility settings

### API Integration
- Axios interceptors for authentication
- Error handling and retry logic
- Request/response transformation
- Real-time updates via WebSocket

### Accessibility Features
- Font size scaling (100%, 125%, 150%)
- High contrast mode toggle
- Keyboard navigation support
- Screen reader compatibility
- Voice search integration
- ARIA labels and semantic HTML

## 📱 Progressive Web App

### Features
- **Offline Support**: Basic functionality without internet
- **Installable**: Add to home screen capability
- **Push Notifications**: Order updates and reminders
- **Background Sync**: Sync data when connection restored

### Service Worker
- Caches critical resources
- Handles offline scenarios
- Background sync for orders
- Push notification handling

## 🧪 Testing Strategy

### Unit Tests
- Component testing with React Testing Library
- Hook testing with @testing-library/react-hooks
- Utility function testing

### Integration Tests
- API integration testing
- Store integration testing
- Route testing

### Accessibility Tests
- Screen reader compatibility
- Keyboard navigation
- Color contrast validation
- Font scaling verification

### Performance Tests
- Bundle size analysis
- Runtime performance monitoring
- Animation frame rate testing
- Memory leak detection

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

### Deploy to Netlify
```bash
npm run build
# Upload dist/ folder to Netlify
```

### Environment Setup
- Set environment variables in deployment platform
- Configure domain and SSL
- Set up monitoring and analytics

## 🔒 Security

### Client-Side Security
- XSS protection via React's built-in sanitization
- CSRF protection via SameSite cookies
- Secure token storage in httpOnly cookies
- Input validation with Zod schemas

### Data Protection
- No sensitive data in localStorage
- Encrypted medical data transmission
- GDPR compliance features
- User consent management

## 📊 Performance Optimization

### Bundle Optimization
- Code splitting by routes
- Tree shaking for unused code
- Dynamic imports for heavy components
- Vendor chunk separation

### Runtime Optimization
- React.memo for expensive components
- useMemo and useCallback for computations
- Virtual scrolling for large lists
- Image lazy loading

### Caching Strategy
- Service Worker caching
- HTTP cache headers
- CDN integration
- Browser cache optimization

## 🌐 Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Accessibility**: NVDA, JAWS, VoiceOver support

## 📈 Monitoring & Analytics

### Performance Monitoring
- Core Web Vitals tracking
- Real User Monitoring (RUM)
- Error tracking and reporting
- Bundle analysis

### User Analytics
- User journey tracking
- Conversion funnel analysis
- A/B testing framework
- Accessibility usage metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure accessibility compliance
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the docs/ folder
- **Issues**: Create an issue on GitHub
- **Email**: support@mediquick.com
- **Phone**: 1800-MEDIQUICK
