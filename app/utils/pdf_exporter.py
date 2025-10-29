"""PDF export utility using ReportLab"""
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from typing import List, Dict
import html
import re


def sanitize_text_for_pdf(text: str) -> str:
    """
    Sanitize text for ReportLab PDF generation.
    Removes or escapes problematic characters and formatting.
    
    Args:
        text: Raw text that may contain markdown, HTML, special chars
        
    Returns:
        Sanitized text safe for ReportLab Paragraph
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove markdown bold/italic formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # *italic* -> italic
    text = re.sub(r'__(.+?)__', r'\1', text)  # __bold__ -> bold
    text = re.sub(r'_(.+?)_', r'\1', text)  # _italic_ -> italic
    
    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Convert markdown-style line breaks to spaces
    text = re.sub(r'\n\n+', ' ', text)  # Multiple newlines -> single space
    text = re.sub(r'\n', ' ', text)  # Single newlines -> space
    
    # Remove pipe table formatting
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'-{3,}', '', text)  # Remove table separator lines
    
    # Remove bullet points
    text = re.sub(r'[•\u2022\u2023\u25E6\u2043\u2219]', '', text)
    
    # Escape special HTML/XML characters
    text = html.escape(text)
    
    # Remove any remaining HTML tags
    text = re.sub(r'<(?!/?[bi]>)[^>]*>', '', text)  # Keep only <b>, </b>, <i>, </i>
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Trim
    text = text.strip()
    
    return text


def create_pdf_export(
    document_name: str,
    qa_history: List[Dict],
    output_path: str
) -> str:
    """
    Create a PDF export of document Q&A history.
    
    Args:
        document_name: Name of the document
        qa_history: List of Q&A dictionaries with 'question', 'answer', 'created_at'
        output_path: Path to save the PDF
        
    Returns:
        Path to created PDF file
    """
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#3498db',
        spaceAfter=12,
        spaceBefore=12
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor='#2c3e50',
        fontName='Helvetica-Bold',
        spaceAfter=8,
        leftIndent=20
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor='#34495e',
        spaceAfter=20,
        leftIndent=20,
        rightIndent=20
    )
    
    metadata_style = ParagraphStyle(
        'MetadataStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor='#7f8c8d',
        spaceAfter=6
    )
    
    # Title
    title = Paragraph("Document Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Document info - sanitize document name
    safe_doc_name = sanitize_text_for_pdf(document_name)
    doc_info = Paragraph(f"<b>Document:</b> {safe_doc_name}", metadata_style)
    elements.append(doc_info)
    
    generated_date = Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        metadata_style
    )
    elements.append(generated_date)
    
    qa_count = Paragraph(f"<b>Total Q&A:</b> {len(qa_history)}", metadata_style)
    elements.append(qa_count)
    
    elements.append(Spacer(1, 0.3 * inch))
    
    # Q&A Section
    qa_heading = Paragraph("Questions & Answers", heading_style)
    elements.append(qa_heading)
    elements.append(Spacer(1, 0.1 * inch))
    
    # Add each Q&A
    for idx, qa in enumerate(qa_history, 1):
        # Q&A number
        qa_number = Paragraph(f"<b>Q&A #{idx}</b>", metadata_style)
        elements.append(qa_number)
        
        # Question - sanitize text
        question_text = sanitize_text_for_pdf(qa.get('question', 'N/A'))
        question = Paragraph(f"<b>Q:</b> {question_text}", question_style)
        elements.append(question)
        
        # Answer - sanitize text
        answer_text = sanitize_text_for_pdf(qa.get('answer', 'N/A'))
        answer = Paragraph(f"<b>A:</b> {answer_text}", answer_style)
        elements.append(answer)
        
        # Timestamp
        if 'created_at' in qa:
            timestamp = datetime.fromisoformat(str(qa['created_at']).replace('Z', '+00:00'))
            timestamp_text = Paragraph(
                f"<i>Asked on {timestamp.strftime('%B %d, %Y at %I:%M %p')}</i>",
                metadata_style
            )
            elements.append(timestamp_text)
        
        elements.append(Spacer(1, 0.2 * inch))
    
    # Footer
    elements.append(Spacer(1, 0.3 * inch))
    footer = Paragraph(
        "<i>Generated by Finalytics - AI-Powered Financial Analytics Platform</i>",
        metadata_style
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    return output_path

