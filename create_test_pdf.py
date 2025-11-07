from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, content)
    c.save()

if __name__ == "__main__":
    create_test_pdf("test.pdf", "This is a test PDF for the summarizer.")
