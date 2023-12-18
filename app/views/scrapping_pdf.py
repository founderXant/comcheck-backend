import os

from app.constants import *
from app.models import PDFDocument
from app.serializer import ScrapePDFSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response

from comcheck.utils import PDFScraper
from comcheck.utils_2018 import PDFScraper_2018


class ScrapePDFViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapePDFSerializer
    queryset = PDFDocument.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):

        file = request.data.get('file')
        standard = request.data.get('standard')

        if file:
            pdf = PDFDocument.objects.create(file=file)
            file_path = pdf.file.path
            print(standard)

            output_filename = f'{PDF_SCRAPED_FILE}'
            pdfs_folder = 'media/pdfs'
            input_filename = os.path.basename(file_path)
            space_input_filename = os.path.join(pdfs_folder, input_filename)

            if standard == '2009':
                PDFScraper.main(space_input_filename, output_filename)
            elif standard == '2018':
                PDFScraper_2018.main(space_input_filename, output_filename)

            for filename in os.listdir(pdfs_folder):
                if filename != input_filename:
                    file_path = os.path.join(pdfs_folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.remove(file_path)

            return Response({'status': 'success', 'message': 'PDF scraped successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'failed', 'message': 'PDF file not found'}, status=status.HTTP_400_BAD_REQUEST)
