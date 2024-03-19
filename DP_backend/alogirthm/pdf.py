from reportlab.pdfgen import canvas


def generate_pdf_file(user):
    from io import BytesIO
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Create pdf documents
    p.drawString(100,750,"Eye Disease Report")
    
    y = 700
    p.drawString(100,y,f"Name: {user.username}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
    