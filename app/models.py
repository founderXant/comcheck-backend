from django.db import models

YEAR_STANDARD = (
    ('2009', '2009'),
    ('2018', '2018'),
    ('2020', '2020'),
)


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs/')
    standard = models.CharField(max_length=4, choices=YEAR_STANDARD)
    uploaded_at = models.DateTimeField(auto_now_add=True)
