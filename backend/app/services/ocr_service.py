"""
OCR service for extracting text from prescription images
"""

import re
from typing import Dict, List, Any, Optional
from datetime import date, datetime


class OCRService:
    """Service for OCR processing of prescription images"""
    
    def __init__(self):
        # Common medicine patterns for extraction
        self.medicine_patterns = [
            r'(?i)(paracetamol|acetaminophen)\s*(\d+\s*mg)?',
            r'(?i)(ibuprofen)\s*(\d+\s*mg)?',
            r'(?i)(amoxicillin)\s*(\d+\s*mg)?',
            r'(?i)(metformin)\s*(\d+\s*mg)?',
            r'(?i)(aspirin)\s*(\d+\s*mg)?',
            r'(?i)(cetirizine)\s*(\d+\s*mg)?',
            r'(?i)(vitamin\s*d3?)\s*(\d+\s*iu)?',
        ]
        
        # Doctor name patterns
        self.doctor_patterns = [
            r'(?i)dr\.?\s+([a-z\s]+)',
            r'(?i)doctor\s+([a-z\s]+)',
            r'(?i)physician\s+([a-z\s]+)',
        ]
        
        # Date patterns
        self.date_patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',
            r'(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{4})',
        ]
    
    def extract_text_from_image(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from prescription image using OCR
        
        This is a mock implementation. In a real application, you would use:
        - Google Cloud Vision API
        - AWS Textract
        - Azure Computer Vision
        - Tesseract OCR
        
        Args:
            image_path: Path to the prescription image
            
        Returns:
            dict: OCR results with extracted text and structured data
        """
        # Mock OCR result - in real implementation, this would process the actual image
        mock_prescription_text = """
        Dr. Sarah Johnson, MD
        Medical License: ML12345
        
        Patient: John Doe
        Age: 35
        Date: 13/07/2025
        
        Prescription:
        1. Paracetamol 500mg - Take 1 tablet every 6 hours as needed for pain
        2. Ibuprofen 400mg - Take 1 tablet twice daily with food
        3. Vitamin D3 1000 IU - Take 1 tablet daily
        
        Diagnosis: Mild fever and body ache
        
        Valid for 30 days from date of issue.
        
        Dr. Sarah Johnson
        Signature
        """
        
        # Extract structured information
        extracted_data = self._extract_structured_data(mock_prescription_text)
        
        return {
            "text": mock_prescription_text.strip(),
            "confidence": 0.95,  # Mock confidence score
            "extracted_medicines": extracted_data["medicines"],
            "doctor_name": extracted_data["doctor_name"],
            "patient_name": extracted_data["patient_name"],
            "prescription_date": extracted_data["prescription_date"],
            "diagnosis": extracted_data["diagnosis"]
        }
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from OCR text
        
        Args:
            text: Raw OCR text
            
        Returns:
            dict: Structured data extracted from text
        """
        result = {
            "medicines": [],
            "doctor_name": None,
            "patient_name": None,
            "prescription_date": None,
            "diagnosis": None
        }
        
        # Extract doctor name
        for pattern in self.doctor_patterns:
            match = re.search(pattern, text)
            if match:
                result["doctor_name"] = match.group(1).strip()
                break
        
        # Extract patient name
        patient_match = re.search(r'(?i)patient:?\s+([a-z\s]+)', text)
        if patient_match:
            result["patient_name"] = patient_match.group(1).strip()
        
        # Extract prescription date
        for pattern in self.date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if len(match.groups()) == 3:
                        day, month, year = match.groups()
                        if len(year) == 4:  # YYYY format
                            result["prescription_date"] = date(int(year), int(month), int(day))
                        else:  # Assume DD/MM/YYYY or MM/DD/YYYY
                            result["prescription_date"] = date(int(year), int(month), int(day))
                        break
                except (ValueError, TypeError):
                    continue
        
        # Extract diagnosis
        diagnosis_match = re.search(r'(?i)diagnosis:?\s+([^\n]+)', text)
        if diagnosis_match:
            result["diagnosis"] = diagnosis_match.group(1).strip()
        
        # Extract medicines
        result["medicines"] = self._extract_medicines(text)
        
        return result
    
    def _extract_medicines(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract medicine information from text
        
        Args:
            text: OCR text
            
        Returns:
            list: List of extracted medicines with dosage and instructions
        """
        medicines = []
        
        # Split text into lines and look for numbered items
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for numbered medicine entries
            numbered_match = re.match(r'^\d+\.?\s+(.+)', line)
            if numbered_match:
                medicine_line = numbered_match.group(1)
                medicine_info = self._parse_medicine_line(medicine_line)
                if medicine_info:
                    medicines.append(medicine_info)
            
            # Also check for medicine patterns in any line
            for pattern in self.medicine_patterns:
                match = re.search(pattern, line)
                if match:
                    medicine_name = match.group(1)
                    dosage = match.group(2) if len(match.groups()) > 1 else None
                    
                    # Extract instructions from the rest of the line
                    instructions = line.replace(match.group(0), '').strip(' -')
                    
                    medicine_info = {
                        "name": medicine_name,
                        "dosage": dosage.strip() if dosage else None,
                        "instructions": instructions if instructions else None,
                        "frequency": self._extract_frequency(line),
                        "duration": self._extract_duration(line)
                    }
                    
                    # Avoid duplicates
                    if not any(m["name"].lower() == medicine_name.lower() for m in medicines):
                        medicines.append(medicine_info)
        
        return medicines
    
    def _parse_medicine_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single medicine line to extract structured information
        
        Args:
            line: Medicine line text
            
        Returns:
            dict: Medicine information or None if not parseable
        """
        # Look for medicine name and dosage pattern
        medicine_match = re.match(r'([a-z\s]+?)\s*(\d+\s*(?:mg|iu|ml|g))\s*[-–]?\s*(.*)', line, re.IGNORECASE)
        
        if medicine_match:
            name = medicine_match.group(1).strip()
            dosage = medicine_match.group(2).strip()
            instructions = medicine_match.group(3).strip()
            
            return {
                "name": name,
                "dosage": dosage,
                "instructions": instructions,
                "frequency": self._extract_frequency(instructions),
                "duration": self._extract_duration(instructions)
            }
        
        return None
    
    def _extract_frequency(self, text: str) -> Optional[str]:
        """Extract dosage frequency from text"""
        frequency_patterns = [
            r'(?i)(once|twice|thrice|\d+\s*times?)\s*(?:a\s*)?(?:day|daily)',
            r'(?i)every\s*(\d+)\s*hours?',
            r'(?i)(morning|evening|night|bedtime)',
            r'(?i)(before|after)\s*meals?'
        ]
        
        for pattern in frequency_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_duration(self, text: str) -> Optional[str]:
        """Extract treatment duration from text"""
        duration_patterns = [
            r'(?i)for\s*(\d+)\s*(days?|weeks?|months?)',
            r'(?i)(\d+)\s*(days?|weeks?|months?)',
            r'(?i)(until\s*symptoms\s*improve)',
            r'(?i)(as\s*needed)'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None


# Global instance
ocr_service = OCRService()


def extract_text_from_image(image_path: str) -> Dict[str, Any]:
    """
    Extract text from image using the global OCR service
    
    Args:
        image_path: Path to the image
        
    Returns:
        dict: OCR results
    """
    return ocr_service.extract_text_from_image(image_path)
