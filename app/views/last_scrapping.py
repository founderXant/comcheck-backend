from app.models import PDFDocument
from app.serializer import ScrapePDFSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


class LastFileViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapePDFSerializer
    queryset = PDFDocument.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        last_file = PDFDocument.objects.last()
        if last_file:
            response = {
                'status': 'success',
                'message': 'Last file found',
                'last_file': last_file.file.name,
                'standard': last_file.standard
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failed', 'message': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)
