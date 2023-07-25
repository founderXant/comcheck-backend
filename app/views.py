from app.serializer import ScrapePDFSerializer, BuildingAreaSerializer,UserInputsSerializer
from app.models import PDFDocument
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status
from comcheck.utils import PDFScraper
from app.constants import *
import os
import json
import xml.etree.ElementTree as ET
from comcheck.utils import XMLGenerator
from rest_framework.views import APIView
from django.http import FileResponse
from django.http import HttpResponse




class ScrapePDFViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapePDFSerializer
    queryset = PDFDocument.objects.all()
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):

        file = request.data.get('file')
        if file:
            pdf = PDFDocument.objects.create(file=file)
            file_path = pdf.file.path
            print(file_path)
            
            output_filename =f'{PDF_SCRAPED_FILE}'
            pdfs_folder ='media/pdfs'
            input_filename = os.path.basename(file_path)  
            space_input_filename = os.path.join(pdfs_folder, input_filename)     
            PDFScraper.main(space_input_filename, output_filename)
            
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

def read_data(file):
    with open(file) as f:
        input_data = json.load(f)
        return input_data

def save_data(data,filename):
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
    
class GenerateXMLView(APIView):
    def get(self, request):
        
        namespace = {'ns': 'http://energycode.pnl.gov/ns/ComCheckBuildingSchema'}
        empty_file = STARTING_XML_FILE
        tree = ET.parse(empty_file)
        root = tree.getroot()
        
        building_list = root.find('ns:lighting/ns:activityUses', namespaces=namespace)
        floor_list = root.find('ns:envelope/ns:floors', namespaces=namespace)
        roof_list = root.find('ns:envelope/ns:roofs', namespaces=namespace)
        wall_list = root.find('ns:envelope/ns:aboveGroundWalls', namespaces=namespace)
        
        with open(f'{USER_INPUT_FILE}', mode='r') as f:
            user_input = json.load(f)

        with open(f'{PDF_SCRAPED_FILE}', mode='r') as f:
            scraped_json = json.load(f)
        
        
        is_residential = user_input['is_residential']
        
        floor_index = user_input['radio_btns']['floor']-1
        roof_index = user_input['radio_btns']['roof']-1
        wall_index = user_input['radio_btns']['ext_wall']-1
        window1_index = user_input['radio_btns']['window_col1']-1
        window2_index = user_input['radio_btns']['window_col2']-1
        door_index = user_input['radio_btns']['door']-1

        is_swinging_door = user_input['is_swinging_door']

        window1_area = user_input['window_area'][0]
        window2_area = user_input['window_area'][1]
        print (user_input)
        print (window2_area)

        floor_r_values = user_input['r-values']['floor']
        roof_r_values = user_input['r-values']['roof']
        wall_r_values = user_input['r-values']['ext_wall']
        window_r_values = user_input['r-values']['window']
        
        xml_generator = XMLGenerator()
        for building_info in scraped_json:
            building_index = building_info['building_choice_index']-1
            building_description = building_info['title']
            building_floor_area = building_info['floor_area']
            building_wall_list = building_info['walls_info']
            floor_area = building_info['floor']
            roof_area = building_info['roof']

            building = xml_generator.get_building_xml(building_index, building_description, is_residential, building_floor_area)
            building_key = building.find('key').text

            if roof_area:
                roof = xml_generator.get_roof_xml(roof_index, building_key, roof_area, roof_r_values[0], roof_r_values[1])
                roof_list.append(roof)

            if floor_area not in ['', '0.0']:
                floor = xml_generator.get_floor_xml(floor_index, building_key, floor_area, floor_r_values[0], floor_r_values[1])
                floor_list.append(floor)

            for wall_info in building_wall_list:
                wall_area = wall_info[0]
                window1_quantity = wall_info[1]
                window2_quantity = wall_info[2]
                window1_area_quantity = window1_quantity * window1_area
                window2_area_quantity = window2_quantity * window2_area
                door_area = wall_info[3]

                if wall_area:
                    wall = xml_generator.get_wall_xml(wall_index, building_key, wall_area, wall_r_values[0], wall_r_values[1])
                    window_list = wall.find('windows')
                    door_list = wall.find('doors')

                    if window1_area_quantity:
                        window = xml_generator.get_window_xml(window1_index, building_key, window1_area_quantity)
                        window_list.append(window)
                        
                    if window2_area_quantity:
                        window = xml_generator.get_window_xml(window2_index, building_key, window2_area_quantity)
                        window_list.append(window)

                    if door_area:
                        door = xml_generator.get_door_xml(door_index, building_key, door_area, is_swinging_door)
                        door_list.append(door)

                    wall_list.append(wall)

            building_list.append(building)
            
        # Remove the namespace prefix from the tag
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]

        # Add namespace declarations to the root element
        namespaces = {
            'xmlns': 'http://energycode.pnl.gov/ns/ComCheckBuildingSchema',
            'xmlns:xs': 'http://www.w3.org/2001/XMLSchema-instance'
        }

        for key, value in namespaces.items():
            root.set(key, value)

        # Save the modified XML to a new file while preserving namespaces
        tree.write(f'{XML_OUTPUT_FILE}', encoding='utf-8', xml_declaration=True)
        
        file_path = f'{XML_OUTPUT_FILE}'
        with open(file_path, 'rb') as xml_file:
            response = HttpResponse(xml_file.read(), content_type='application/xml')
            response['Content-Disposition'] = f'attachment; filename={XML_OUTPUT_FILE}'
        return response

        
        
            
        
       


    
    
        
        
 




    

   
       
    
            
    


        


