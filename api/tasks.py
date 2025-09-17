from celery import shared_task
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from silk.profiling.profiler import silk_profile
from datetime import datetime


os.makedirs("C:\\temp", exist_ok=True)

@shared_task
def generate_pdf_task(user_id, queue_type='default'):
    """
    Generate PDF for user. Different styling for high and low priority.
    Each run produces a unique file (no overwrites).
    """
    with silk_profile(name=f"PDF Task {queue_type} - User {user_id}"):

        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"C:\\temp\\generated_pdf_user_{user_id}_{queue_type}_{timestamp}.pdf"

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.fontSize = 12
        normal_style.leading = 14

        # --- High Priority Styling ---
        if queue_type == 'high_priority':
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.red)
            c.drawCentredString(width / 2, height - 2*cm, f"🔥 High Priority Report for User {user_id}")

            text = ("This is a HIGH PRIORITY report.\n"
                    "Includes full detailed data for user analysis.\n"
                    "Everything is thoroughly documented.")
            p = Paragraph(text.replace("\n", "<br />"), normal_style)
            p.wrapOn(c, width - 4*cm, height - 6*cm)
            p.drawOn(c, 2*cm, height - 5*cm)

            data = [
                ["Metric", "Value"],
                ["Tasks Completed", 25],
                ["Pending Tasks", 2],
                ["Score", "95%"]
            ]
            table = Table(data, colWidths=[8*cm, 5*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.red),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            table.wrapOn(c, width, height)
            table.drawOn(c, 2*cm, height - 12*cm)

        # --- Low Priority Styling ---
        elif queue_type == 'low_priority':
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(width / 2, height - 2*cm, f"ℹ️ Low Priority Report for User {user_id}")

            text = ("This is a low priority report.\n"
                    "Contains summary data only.\n"
                    "Quick overview for monitoring purposes.")
            p = Paragraph(text.replace("\n", "<br />"), normal_style)
            p.wrapOn(c, width - 4*cm, height - 6*cm)
            p.drawOn(c, 2*cm, height - 5*cm)

            data = [
                ["Metric", "Value"],
                ["Tasks Completed", 10],
                ["Pending Tasks", 5],
            ]
            table = Table(data, colWidths=[8*cm, 5*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.blue),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            table.wrapOn(c, width, height)
            table.drawOn(c, 2*cm, height - 10*cm)

        
        else:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.black)
            c.drawCentredString(width / 2, height - 2*cm, f"Default Report for User {user_id}")
            c.drawString(2*cm, height - 4*cm, "This is a basic report without priority styling.")

        
        c.showPage()
        c.save()
        return filename



def send_high_priority_pdf_task(user_id):
    return generate_pdf_task.apply_async(
        args=[user_id, 'high_priority'],
        queue='high_priority',
        routing_key='task.high'
    )

def send_low_priority_pdf_task(user_id):
    return generate_pdf_task.apply_async(
        args=[user_id, 'low_priority'],
        queue='low_priority',
        routing_key='task.low'
    )

def send_default_priority_pdf_task(user_id):
    return generate_pdf_task.apply_async(
        args=[user_id, 'default'],
        queue='default',
        routing_key='task.default'
    )
