import json

from app.constants import *
from app.serializer import UserInputsSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


def read_data(file):
    with open(file) as f:
        input_data = json.load(f)
        return input_data


def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


FILENAME = f'{PDF_SCRAPED_FILE}'
input_data = read_data(FILENAME)


class UserInputsViewSet (viewsets.ModelViewSet):
    serializer_class = UserInputsSerializer
    queryset = ''
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data

        data["options_floors"] = "Options for floors, A, B, C"
        data["options_roof"] = "Options for roof, A, B, C"
        data["options_ext_wall"] = "Options for external walls, A, B, C"
        data["options_window"] = "Options for windows, A, B, C"
        data["options_doors"] = "Options for doors, A, B, C"

        save_data(data, USER_INPUT_FILE)
        return Response({'status': 'success', 'message': '  User inputs saved successfully'}, status=status.HTTP_201_CREATED)
