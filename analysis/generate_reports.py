from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, content)
    c.save()
