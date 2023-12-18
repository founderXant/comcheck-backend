from app.constants import *
from app.models import PDFDocument
from app.views.standart_xml import xml_2009, xml_2018, xml_2020
from django.http import HttpResponse
from rest_framework.views import APIView


class GenerateXMLView(APIView):
    def get(self, request):
        last_pdf = PDFDocument.objects.last()
        print(last_pdf)

        if last_pdf:
            if last_pdf.standard == '2009':
                response = xml_2009(STARTING_XML_2009_FILE, USER_INPUT_FILE,
                                    PDF_SCRAPED_FILE, XML_OUTPUT)
                return response

            elif last_pdf.standard == '2018':
                response = xml_2018(STARTING_XML_2018_FILE, USER_INPUT_FILE,
                                    PDF_SCRAPED_FILE, XML_OUTPUT)
                return response

            elif last_pdf.standard == '2020':
                response = xml_2020(STARTING_XML_2020_FILE, USER_INPUT_FILE,
                                    PDF_SCRAPED_FILE, XML_OUTPUT)
                return response

            else:
                return HttpResponse('Error')
