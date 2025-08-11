from django.db import models


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExcelSheets(models.Model):
    file = models.FileField(upload_to='excels/')
    uploaded_at = models.DateTimeField(auto_now_add=True)