"""Text extraction from PDF and images with parallel processing"""
import os
from pathlib import Path
from typing import Tuple, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import PyPDF2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from app.config import settings

# Configure Tesseract path if specified
if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    print(f"Tesseract configured: {settings.TESSERACT_CMD}")


def extract_text_from_pdf(file_path: str) -> Tuple[str, int]:
    """
    Extract text from PDF file.
    First tries to extract text directly, then falls back to OCR for scanned PDFs.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (extracted_text, page_count)
    """
    page_count = 0
    extracted_text = ""
    
    try:
        # Try direct text extraction first
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n\n"
        
        # If we got meaningful text, return it
        if extracted_text.strip() and len(extracted_text.strip()) > 100:
            return extracted_text.strip(), page_count
        
        # Otherwise, use OCR
        print(f"PDF appears to be scanned. Using OCR for {file_path}")
        return extract_text_from_pdf_with_ocr(file_path)
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def _process_image_batch(batch_data: Tuple[int, Image.Image]) -> Tuple[int, str]:
    """
    Process a single image page with OCR (for parallel processing).
    
    Args:
        batch_data: Tuple of (page_number, image)
        
    Returns:
        Tuple of (page_number, extracted_text)
    """
    page_num, image = batch_data
    try:
        # Extract text from image using Tesseract
        text = pytesseract.image_to_string(
            image, 
            lang='eng',
            config='--psm 3 --oem 3'
        )
        print(f"✓ Processed page {page_num}")
        return page_num, text
    except Exception as e:
        print(f"✗ Error processing page {page_num}: {str(e)}")
        return page_num, f"[Error extracting text from page {page_num}]"


def extract_text_from_pdf_with_ocr(file_path: str) -> Tuple[str, int]:
    """
    Extract text from PDF using OCR with parallel processing.
    Uses ThreadPoolExecutor to process multiple pages simultaneously.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (extracted_text, page_count)
    """
    try:
        # Convert PDF to images with optimized settings
        poppler_kwargs = {'dpi': 200, 'fmt': 'jpeg', 'thread_count': 4}
        
        if settings.POPPLER_PATH:
            poppler_kwargs['poppler_path'] = settings.POPPLER_PATH
            print(f"Using Poppler path: {settings.POPPLER_PATH}")
        
        print(f"Converting PDF to images...")
        images = convert_from_path(file_path, **poppler_kwargs)
        page_count = len(images)
        print(f"✓ Converted {page_count} pages to images")
        
        # Process pages in parallel using ThreadPoolExecutor
        # Determine optimal number of workers (max 4 for CPU-bound OCR)
        max_workers = min(4, page_count)
        print(f"Processing {page_count} pages with {max_workers} parallel threads...")
        
        page_texts = {}
        
        # Create list of (page_number, image) tuples for parallel processing
        batch_data = [(i + 1, img) for i, img in enumerate(images)]
        
        # Use ThreadPoolExecutor for parallel OCR processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_page = {
                executor.submit(_process_image_batch, data): data[0] 
                for data in batch_data
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_page):
                page_num, text = future.result()
                page_texts[page_num] = text
        
        # Combine texts in correct page order
        extracted_text = ""
        for page_num in sorted(page_texts.keys()):
            extracted_text += f"--- Page {page_num} ---\n{page_texts[page_num]}\n\n"
        
        print(f"✓ Completed OCR for all {page_count} pages")
        return extracted_text.strip(), page_count
        
    except Exception as e:
        raise Exception(f"Error extracting text with OCR: {str(e)}")


def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from image file using OCR.
    Optimized for speed.
    
    Args:
        file_path: Path to image file
        
    Returns:
        Extracted text
    """
    try:
        image = Image.open(file_path)
        # Optimize image for OCR - resize if too large
        max_dimension = 3000
        if image.width > max_dimension or image.height > max_dimension:
            ratio = max_dimension / max(image.width, image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            print(f"Resized image to {new_size} for faster OCR")
        
        # Optimized Tesseract settings
        text = pytesseract.image_to_string(
            image, 
            lang='eng',
            config='--psm 3 --oem 3'
        )
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")


def extract_text(file_path: str, mime_type: str) -> Tuple[str, Optional[int]]:
    """
    Extract text from file based on type.
    
    Args:
        file_path: Path to file
        mime_type: MIME type of file
        
    Returns:
        Tuple of (extracted_text, page_count)
        page_count is None for images
    """
    if mime_type == "application/pdf":
        return extract_text_from_pdf(file_path)
    elif mime_type in ["image/png", "image/jpeg", "image/tiff"]:
        text = extract_text_from_image(file_path)
        return text, None
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")

