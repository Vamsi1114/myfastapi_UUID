from fastapi import APIRouter,Depends
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
import io
import os
from ..oauth2 import get_current_user
from app import models
from fastapi.responses import JSONResponse

router = APIRouter()

#print
@router.get("/pdf")
async def generate_pdf( user: models.User = Depends(get_current_user)):
    # profile = db.query(models.User).filter(models.User.user_id==user.id).first()
    # Create a byte stream to write the PDF to
    pdf_byte_stream = io.BytesIO()

    # Create the PDF file using ReportLab
    # pdf = SimpleDocTemplate("example.pdf")
    pdf = canvas.Canvas(pdf_byte_stream)
    pdf.drawString(100, 750, f"First_name : {user.first_name}")
    pdf.drawString(100, 730, f"Last_name : {user.last_name}")
    pdf.drawString(100, 700, f"Date_of_birth : {user.date_of_birth}")
    pdf.drawString(100, 670, f"Phone_number : {user.phone_number}")
    # pdf.drawText(f"First_name : {user.first_name}")
    pdf.save()

    # Reset the byte stream position to the beginning
    pdf_byte_stream.seek(0)
    # Save the PDF file to local system
    filename = "example.pdf"
    with open(filename, "wb") as f:
        f.write(pdf_byte_stream.getbuffer())

    # Get the absolute path of the PDF file
    file_path = os.path.abspath(filename)

    return JSONResponse({"filename": filename, "file_path": file_path})

    # Return the PDF file as a StreamingResponse
    # return StreamingResponse(pdf_byte_stream, media_type="application/pdf")