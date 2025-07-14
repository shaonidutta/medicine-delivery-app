// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  errors?: string[];
}

// User Types
export interface User {
  id: string;
  email: string;
  phone: string;
  first_name: string;
  last_name: string;
  date_of_birth?: string;
  gender?: string;
  medical_conditions?: string[];
  allergies?: string[];
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  phone_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserRegistration {
  email: string;
  phone: string;
  password: string;
  first_name: string;
  last_name: string;
  date_of_birth?: string;
  gender?: string;
  medical_conditions?: string[];
  allergies?: string[];
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Medicine Types
export interface Medicine {
  id: string;
  name: string;
  generic_name?: string;
  manufacturer: string;
  category_id?: string;
  description?: string;
  dosage_form?: string;
  strength?: string;
  price: number;
  prescription_required: boolean;
  stock_quantity: number;
  min_stock_level: number;
  expiry_date?: string;
  batch_number?: string;
  storage_conditions?: string;
  side_effects?: string[];
  contraindications?: string[];
  active_ingredients?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface MedicineSearchParams {
  q?: string;
  category_id?: string;
  prescription_required?: boolean;
  min_price?: number;
  max_price?: number;
  in_stock?: boolean;
  manufacturer?: string;
  dosage_form?: string;
  sort_by?: string;
  sort_order?: string;
  page?: number;
  page_size?: number;
}

export interface MedicineSearchResponse {
  medicines: Medicine[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Category Types
export interface Category {
  id: string;
  name: string;
  description?: string;
  parent_category_id?: string;
  created_at: string;
  updated_at: string;
  subcategories?: Category[];
}

// Cart Types
export interface CartItem {
  id: string;
  cart_id: string;
  medicine_id: string;
  quantity: number;
  prescription_id?: string;
  notes?: string;
  unit_price: number;
  total_price: number;
  medicine?: Medicine;
  prescription?: Prescription;
  is_prescription_valid: boolean;
  created_at: string;
  updated_at: string;
}

export interface Cart {
  id: string;
  user_id: string;
  items: CartItem[];
  total_items: number;
  subtotal: number;
  tax_amount: number;
  delivery_fee: number;
  total_amount: number;
  has_prescription_items: boolean;
  prescription_validation_status: string;
  created_at: string;
  updated_at: string;
}

export interface AddToCartRequest {
  medicine_id: string;
  quantity: number;
  prescription_id?: string;
  notes?: string;
}

// Prescription Types
export interface Prescription {
  id: string;
  user_id: string;
  doctor_name: string;
  doctor_license?: string;
  patient_name: string;
  patient_age?: number;
  patient_gender?: string;
  diagnosis?: string;
  prescribed_medicines: any[];
  dosage_instructions?: string;
  prescription_date: string;
  valid_until?: string;
  notes?: string;
  image_url: string;
  status: 'pending' | 'processing' | 'verified' | 'rejected' | 'expired';
  verified_by?: string;
  verification_notes?: string;
  ocr_text?: string;
  created_at: string;
  updated_at: string;
}

// Order Types
export interface DeliveryAddress {
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  landmark?: string;
  contact_phone: string;
  contact_name: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  medicine_id: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  prescription_id?: string;
  medicine?: Medicine;
  prescription?: Prescription;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: string;
  user_id: string;
  order_number: string;
  status: 'pending' | 'confirmed' | 'processing' | 'packed' | 'shipped' | 'out_for_delivery' | 'delivered' | 'cancelled' | 'returned';
  payment_status: 'pending' | 'processing' | 'completed' | 'failed' | 'refunded';
  payment_method: 'cash_on_delivery' | 'credit_card' | 'debit_card' | 'upi' | 'net_banking' | 'wallet';
  delivery_address: DeliveryAddress;
  delivery_instructions?: string;
  items: OrderItem[];
  subtotal: number;
  tax_amount: number;
  delivery_fee: number;
  total_amount: number;
  tracking_number?: string;
  delivery_partner_id?: string;
  pharmacy_id?: string;
  estimated_delivery_time?: number;
  expected_delivery_date?: string;
  actual_delivery_date?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateOrderFromCart {
  delivery_address: DeliveryAddress;
  payment_method: string;
  delivery_instructions?: string;
  validate_prescriptions?: boolean;
}

// UI State Types
export interface FontScale {
  scale: 100 | 125 | 150;
  label: string;
}

export interface NotificationSettings {
  delivery_updates: boolean;
  medicine_reminders: boolean;
  order_status: boolean;
  prescription_expiry: boolean;
  marketing: boolean;
}

export interface AccessibilitySettings {
  font_scale: FontScale['scale'];
  high_contrast: boolean;
  reduced_motion: boolean;
  screen_reader: boolean;
}

// Search Types
export interface SearchSuggestion {
  id: string;
  name: string;
  type: 'medicine' | 'category' | 'brand';
  category?: string;
  prescription_required?: boolean;
}

export interface VoiceSearchResult {
  transcript: string;
  confidence: number;
  suggestions: SearchSuggestion[];
}

// Error Types
export interface ApiError {
  message: string;
  code?: string;
  field?: string;
  details?: Record<string, any>;
}

export interface FormError {
  field: string;
  message: string;
}

// Navigation Types
export interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}

// Animation Types
export interface AnimationConfig {
  duration: number;
  easing: string;
  delay?: number;
}

// Three.js Types
export interface ThreeJSScene {
  scene: any;
  camera: any;
  renderer: any;
  controls?: any;
}

export interface ParticleSystem {
  particles: any[];
  geometry: any;
  material: any;
  mesh: any;
}
