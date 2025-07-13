"""
Seed data for the database
"""

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.category import Category
from app.models.medicine import Medicine
from datetime import date, timedelta


def create_categories(db: Session):
    """Create initial categories"""
    categories_data = [
        {"name": "Pain Relief", "description": "Medicines for pain management and relief"},
        {"name": "Antibiotics", "description": "Prescription antibiotics for bacterial infections"},
        {"name": "Cold & Flu", "description": "Medicines for cold, flu, and respiratory symptoms"},
        {"name": "Digestive Health", "description": "Medicines for digestive and stomach issues"},
        {"name": "Vitamins & Supplements", "description": "Vitamins, minerals, and dietary supplements"},
        {"name": "Diabetes Care", "description": "Medicines and supplies for diabetes management"},
        {"name": "Heart & Blood Pressure", "description": "Cardiovascular medicines and blood pressure management"},
        {"name": "Skin Care", "description": "Topical medicines and skin care products"},
        {"name": "Eye Care", "description": "Eye drops and vision care medicines"},
        {"name": "Emergency Medicines", "description": "Critical and emergency medicines"},
    ]
    
    created_categories = {}
    for cat_data in categories_data:
        # Check if category already exists
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
            db.refresh(category)
            created_categories[cat_data["name"]] = category.id
            print(f"Created category: {cat_data['name']}")
        else:
            created_categories[cat_data["name"]] = existing.id
            print(f"Category already exists: {cat_data['name']}")
    
    return created_categories


def create_medicines(db: Session, categories: dict):
    """Create sample medicines"""
    medicines_data = [
        # Pain Relief
        {
            "name": "Paracetamol 500mg",
            "generic_name": "Paracetamol",
            "manufacturer": "Cipla Ltd",
            "category": "Pain Relief",
            "description": "Effective pain relief and fever reducer",
            "dosage_form": "Tablet",
            "strength": "500mg",
            "price": 25.50,
            "prescription_required": False,
            "stock_quantity": 100,
            "expiry_date": date.today() + timedelta(days=365),
            "batch_number": "PAR001",
            "side_effects": ["Nausea", "Stomach upset"],
            "contraindications": ["Liver disease", "Alcohol dependency"]
        },
        {
            "name": "Ibuprofen 400mg",
            "generic_name": "Ibuprofen",
            "manufacturer": "Sun Pharma",
            "category": "Pain Relief",
            "description": "Anti-inflammatory pain reliever",
            "dosage_form": "Tablet",
            "strength": "400mg",
            "price": 45.00,
            "prescription_required": False,
            "stock_quantity": 75,
            "expiry_date": date.today() + timedelta(days=300),
            "batch_number": "IBU001"
        },
        # Antibiotics
        {
            "name": "Amoxicillin 500mg",
            "generic_name": "Amoxicillin",
            "manufacturer": "Dr. Reddy's",
            "category": "Antibiotics",
            "description": "Broad-spectrum antibiotic",
            "dosage_form": "Capsule",
            "strength": "500mg",
            "price": 120.00,
            "prescription_required": True,
            "stock_quantity": 50,
            "expiry_date": date.today() + timedelta(days=400),
            "batch_number": "AMX001"
        },
        # Cold & Flu
        {
            "name": "Cetirizine 10mg",
            "generic_name": "Cetirizine",
            "manufacturer": "Lupin",
            "category": "Cold & Flu",
            "description": "Antihistamine for allergies and cold symptoms",
            "dosage_form": "Tablet",
            "strength": "10mg",
            "price": 35.00,
            "prescription_required": False,
            "stock_quantity": 80,
            "expiry_date": date.today() + timedelta(days=450),
            "batch_number": "CET001"
        },
        # Vitamins
        {
            "name": "Vitamin D3 1000 IU",
            "generic_name": "Cholecalciferol",
            "manufacturer": "Himalaya",
            "category": "Vitamins & Supplements",
            "description": "Vitamin D3 supplement for bone health",
            "dosage_form": "Tablet",
            "strength": "1000 IU",
            "price": 180.00,
            "prescription_required": False,
            "stock_quantity": 60,
            "expiry_date": date.today() + timedelta(days=500),
            "batch_number": "VD3001"
        },
        # Diabetes Care
        {
            "name": "Metformin 500mg",
            "generic_name": "Metformin",
            "manufacturer": "Glenmark",
            "category": "Diabetes Care",
            "description": "Type 2 diabetes medication",
            "dosage_form": "Tablet",
            "strength": "500mg",
            "price": 85.00,
            "prescription_required": True,
            "stock_quantity": 40,
            "expiry_date": date.today() + timedelta(days=350),
            "batch_number": "MET001"
        },
        # Emergency Medicines
        {
            "name": "Aspirin 75mg",
            "generic_name": "Acetylsalicylic Acid",
            "manufacturer": "Bayer",
            "category": "Emergency Medicines",
            "description": "Low-dose aspirin for heart protection",
            "dosage_form": "Tablet",
            "strength": "75mg",
            "price": 65.00,
            "prescription_required": False,
            "stock_quantity": 90,
            "expiry_date": date.today() + timedelta(days=600),
            "batch_number": "ASP001"
        }
    ]
    
    for med_data in medicines_data:
        # Check if medicine already exists
        existing = db.query(Medicine).filter(Medicine.name == med_data["name"]).first()
        if not existing:
            category_id = categories.get(med_data.pop("category"))
            medicine = Medicine(
                category_id=category_id,
                **med_data
            )
            db.add(medicine)
            db.commit()
            db.refresh(medicine)
            print(f"Created medicine: {medicine.name}")
        else:
            print(f"Medicine already exists: {med_data['name']}")


def seed_database():
    """Main function to seed the database"""
    db = SessionLocal()
    try:
        print("Starting database seeding...")
        
        # Create categories
        categories = create_categories(db)
        
        # Create medicines
        create_medicines(db, categories)
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
