import json

from app.constants import *
from app.serializer import BuildingAreaSerializer
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


class BuildingAreaViewSet(viewsets.GenericViewSet):
    serializer_class = BuildingAreaSerializer
    queryset = []

    def get_input_data(self):
        FILENAME = f'{PDF_SCRAPED_FILE}'
        return read_data(FILENAME)

    def write_data(self, data):
        with open(FILENAME, 'w') as json_file:
            json.dump(data, json_file)

    def list(self, request, *args, **kwargs):
        input_data = self.get_input_data()

        output_data = []
        for item in input_data:
            output_data.append({
                'title': item['title'],
                'choice': item['building_choice_index']
            })
        self.queryset = output_data
        return Response(output_data, status=status.HTTP_200_OK)

    def update_choice(self, request, *args, **kwargs):

        updated_data = request.data
        if not isinstance(updated_data, list) or not all(isinstance(item, dict) for item in updated_data):
            return Response({'error': 'Invalid data format. Expected a list of dictionaries.'},
                            status=status.HTTP_400_BAD_REQUEST)

        input_data = self.get_input_data()

        for item in updated_data:
            title = item.get('title')
            choice = item.get('choice')
            if title is None or choice is None:
                return Response({'error': 'Invalid data. "title" and "choice" are required.'},
                                status=status.HTTP_400_BAD_REQUEST)
            for item in input_data:
                if item['title'] == title:
                    item['building_choice_index'] = choice
        self.queryset = input_data
        save_data(input_data, FILENAME)

        return Response({'status': 'success', 'message': 'Building choice updated successfully'}, status=status.HTTP_200_OK)
