from celery import shared_task
import time
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

os.makedirs("C:\\temp", exist_ok=True)

@shared_task
def generate_pdf_task(user_id):
    print(f"Running PDF task for user {user_id}")
    try:
        output_path = os.path.join("C:\\temp", f"generated_pdf_user_{user_id}.pdf")
        
        # Generate basic PDF with reportlab
        temp_pdf_path = os.path.join("C:\\temp", f"temp_user_{user_id}.pdf")
        c = canvas.Canvas(temp_pdf_path)
        
        for i in range(5):  # Simulating 5 lines
            c.drawString(100, 800 - (i * 20), f"Line {i+1}")
            print(f"Added line {i+1}")
            time.sleep(1)

        c.save()
        print(f"✅ Temporary PDF created at {temp_pdf_path}")

        # Optional: Load with PyPDF2 and save (for future manipulation)
        reader = PdfReader(temp_pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        print(f"✅ Final PDF saved to {output_path}")
        os.remove(temp_pdf_path)  # Clean up temp file

        return output_path

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        raise
