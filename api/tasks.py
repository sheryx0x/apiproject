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
        temp_pdf_path = os.path.join("C:\\temp", f"temp_user_{user_id}.pdf")
        c = canvas.Canvas(temp_pdf_path)

        pages = 50
        lines_per_page = 40
        start_y = 800
        line_height = 15

        for page in range(pages):
            for line in range(lines_per_page):
                y = start_y - (line * line_height)
                text = f"User {user_id} - Page {page + 1} Line {line + 1} " + \
                       "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                c.drawString(50, y, text)

                
                c.setStrokeColorRGB(0, 0, 0)
                c.line(40, y - 2, 550, y - 2)

            c.showPage()  

        c.save()
        print(f"✅ Temporary PDF created at {temp_pdf_path}")

        
        import shutil
        shutil.copy(temp_pdf_path, output_path)
        os.remove(temp_pdf_path)

        print(f"✅ Final PDF saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        raise
