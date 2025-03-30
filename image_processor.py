from PIL import Image, ImageEnhance, ImageFilter
import pytesseract # type: ignore
import cv2
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_image(input_path):
    """Professional-grade image processing pipeline"""
    try:
        base_name = os.path.basename(input_path)
        processed_name = f"processed_{base_name}"
        output_path = os.path.join(os.path.dirname(input_path), processed_name)
        
        with Image.open(input_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            img.thumbnail((1200, 1200))
            
            cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2LAB)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cv_img[:,:,0] = clahe.apply(cv_img[:,:,0])
            img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_LAB2RGB))
            
            img = img.filter(ImageFilter.SHARPEN)
            
            img.save(output_path, quality=95)
            return processed_name
            
    except Exception as e:
        print(f"Image processing error: {str(e)}")
        return None

def extract_text(image_path):
    """Advanced OCR with preprocessing"""
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        text = pytesseract.image_to_string(
            denoised,
            config='--oem 3 --psm 6 -c preserve_interword_spaces=1'
        )
        return text.strip()
    except Exception as e:
        print(f"OCR error: {str(e)}")
        return ""