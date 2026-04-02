import io
from typing import Tuple
import pdfplumber
from docx import Document
from fastapi import UploadFile, HTTPException
from logging_config import get_logger

logger = get_logger(__name__)

class DocumentParserService:
    """Service for parsing PDF and DOCX files with a page limit."""
    
    MAX_PAGES = 50

    def parse_pdf(self, file_content: bytes) -> Tuple[str, int]:
        """Extract text from a PDF file using pdfplumber."""
        logger.info("Parsing PDF file...")
        text_content = []
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                page_count = len(pdf.pages)
                if page_count > self.MAX_PAGES:
                    logger.warning(f"PDF too long: {page_count} pages. Limit is {self.MAX_PAGES}.")
                    raise HTTPException(
                        status_code=413,
                        detail=f"PDF exceeds the {self.MAX_PAGES} page limit (found {page_count})."
                    )
                
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_content.append(extracted_text)
            
            return "\n".join(text_content), page_count
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")

    def parse_docx(self, file_content: bytes) -> Tuple[str, int]:
        """Extract text from a DOCX file using python-docx."""
        logger.info("Parsing DOCX file...")
        try:
            doc = Document(io.BytesIO(file_content))
            # Heuristic: ~3000 chars per page, or use section count if available.
            # Using paragraph count as a proxy for complexity.
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            text = "\n".join(full_text)
            # Rough estimate of pages for DOCX
            estimated_pages = max(1, len(text) // 3000)
            
            return text, estimated_pages
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to parse DOCX: {str(e)}")

    async def parse_file(self, file: UploadFile) -> Tuple[str, int]:
        """Generic file parser dispatcher."""
        content = await file.read()
        filename = file.filename.lower() if file.filename else ""
        
        if filename.endswith(".pdf"):
            return self.parse_pdf(content)
        elif filename.endswith(".docx"):
            return self.parse_docx(content)
        else:
            logger.warning(f"Unsupported file type: {filename}")
            raise HTTPException(
                status_code=415,
                detail="Unsupported file type. Only PDF and DOCX are supported."
            )
