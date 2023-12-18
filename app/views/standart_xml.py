import json
import xml.etree.ElementTree as ET

from app.constants import *
from django.http import HttpResponse

from comcheck.utils import XMLGenerator
from comcheck.utils_2018 import XMLGenerator_2018


def xml_2009(STARTING_XML_2009_FILE, USER_INPUT_FILE, PDF_SCRAPED_FILE, XML_OUTPUT):
    namespace = {'ns': 'http://energycode.pnl.gov/ns/ComCheckBuildingSchema'}
    empty_file = STARTING_XML_2009_FILE
    tree = ET.parse(empty_file)
    root = tree.getroot()

    building_list = root.find(
        'ns:lighting/ns:activityUses', namespaces=namespace)
    floor_list = root.find('ns:envelope/ns:floors', namespaces=namespace)
    roof_list = root.find('ns:envelope/ns:roofs', namespaces=namespace)
    wall_list = root.find(
        'ns:envelope/ns:aboveGroundWalls', namespaces=namespace)

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
    print(user_input)
    print(window2_area)

    floor_r_values = user_input['r_values']['floor']
    roof_r_values = user_input['r_values']['roof']
    wall_r_values = user_input['r_values']['ext_wall']
    window_r_values = user_input['r_values']['window']

    xml_generator = XMLGenerator()
    for building_info in scraped_json:
        building_index = building_info['building_choice_index']-1
        building_description = building_info['title']
        building_floor_area = building_info['floor_area']
        building_wall_list = building_info['walls_info']
        floor_area = building_info['floor']
        roof_area = building_info['roof']

        building = xml_generator.get_building_xml(
            building_index, building_description, is_residential, building_floor_area)
        building_key = building.find('key').text

        if roof_area:
            roof = xml_generator.get_roof_xml(
                roof_index, building_key, roof_area, roof_r_values[0], roof_r_values[1])
            roof_list.append(roof)

        if floor_area not in ['', '0.0']:
            floor = xml_generator.get_floor_xml(
                floor_index, building_key, floor_area, floor_r_values[0], floor_r_values[1])
            floor_list.append(floor)

        for wall_info in building_wall_list:
            wall_area = wall_info[0]
            window1_quantity = wall_info[1]
            window2_quantity = wall_info[2]
            window1_area_quantity = window1_quantity * window1_area
            window2_area_quantity = window2_quantity * window2_area
            door_area = wall_info[3]

            if wall_area:
                wall = xml_generator.get_wall_xml(
                    wall_index, building_key, wall_area, wall_r_values[0], wall_r_values[1])
                window_list = wall.find('windows')
                door_list = wall.find('doors')

                if window1_area_quantity:
                    window = xml_generator.get_window_xml(
                        window1_index, building_key, window1_area_quantity)
                    window_list.append(window)

                if window2_area_quantity:
                    window = xml_generator.get_window_xml(
                        window2_index, building_key, window2_area_quantity)
                    window_list.append(window)

                if door_area:
                    door = xml_generator.get_door_xml(
                        door_index, building_key, door_area, is_swinging_door)
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
    tree.write(f'{XML_OUTPUT}', encoding='utf-8', xml_declaration=True)

    file_path = f'{XML_OUTPUT}'
    with open(file_path, 'rb') as xml_file:
        response = HttpResponse(
            xml_file.read(), content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename={XML_OUTPUT}'
    return response


def xml_2018(STARTING_XML_2018_FILE, USER_INPUT_FILE, PDF_SCRAPED_FILE, XML_OUTPUT):
    namespace = {'ns': 'http://energycode.pnl.gov/ns/ComCheckBuildingSchema'}
    empty_file = STARTING_XML_2018_FILE
    tree = ET.parse(empty_file)
    root = tree.getroot()

    building_list = root.find(
        'ns:lighting/ns:activityUses', namespaces=namespace)
    floor_list = root.find('ns:envelope/ns:floors', namespaces=namespace)
    roof_list = root.find('ns:envelope/ns:roofs', namespaces=namespace)
    wall_list = root.find(
        'ns:envelope/ns:aboveGroundWalls', namespaces=namespace)

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
    print(user_input)
    print(window2_area)

    floor_r_values = user_input['r_values']['floor']
    roof_r_values = user_input['r_values']['roof']
    wall_r_values = user_input['r_values']['ext_wall']
    window_r_values = user_input['r_values']['window']

    xml_generator = XMLGenerator()
    for building_info in scraped_json:
        building_index = building_info['building_choice_index']-1
        building_description = building_info['title']
        building_floor_area = building_info['floor_area']
        building_wall_list = building_info['walls_info']
        floor_area = building_info['floor']
        roof_area = building_info['roof']

        building = xml_generator.get_building_xml(
            building_index, building_description, is_residential, building_floor_area)
        building_key = building.find('key').text

        if roof_area:
            roof = xml_generator.get_roof_xml(
                roof_index, building_key, roof_area, roof_r_values[0], roof_r_values[1])
            roof_list.append(roof)

        for wall_info in building_wall_list:
            wall_orientation = wall_info[0]
            wall_area = wall_info[1]
            window1_quantity = wall_info[2]
            window2_quantity = wall_info[3]
            window1_area_quantity = window1_quantity * window1_area
            window2_area_quantity = window2_quantity * window2_area
            door_area = wall_info[4]

            if wall_area:
                wall = xml_generator.get_wall_xml(
                    wall_orientation, wall_index, building_key, wall_area, wall_r_values[0], wall_r_values[1])
                window_list = wall.find('windows')
                door_list = wall.find('doors')

                if window1_area_quantity:
                    window = xml_generator.get_window_xml(
                        window1_index, building_key, window1_area_quantity)
                    window_list.append(window)

                if window2_area_quantity:
                    window = xml_generator.get_window_xml(
                        window2_index, building_key, window2_area_quantity)
                    window_list.append(window)

                if door_area:
                    door = xml_generator.get_door_xml(
                        door_index, building_key, door_area, is_swinging_door)
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
    tree.write(f'{XML_OUTPUT}', encoding='utf-8', xml_declaration=True)

    file_path = f'{XML_OUTPUT}'
    with open(file_path, 'rb') as xml_file:
        response = HttpResponse(
            xml_file.read(), content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename={XML_OUTPUT}'
    return response


def xml_2020(STARTING_XML_2020_FILE, USER_INPUT_FILE, PDF_SCRAPED_FILE, XML_OUTPUT):
    namespace = {
        'ns': 'http://energycode.pnl.gov/ns/ComCheckBuildingSchema'}
    empty_file = STARTING_XML_2020_FILE
    tree = ET.parse(empty_file)
    root = tree.getroot()

    building_list = root.find(
        'ns:lighting/ns:activityUses', namespaces=namespace)
    floor_list = root.find('ns:envelope/ns:floors', namespaces=namespace)
    roof_list = root.find('ns:envelope/ns:roofs', namespaces=namespace)
    wall_list = root.find(
        'ns:envelope/ns:aboveGroundWalls', namespaces=namespace)

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

    floor_r_values = user_input['r_values']['floor']
    roof_r_values = user_input['r_values']['roof']
    wall_r_values = user_input['r_values']['ext_wall']
    window_r_values = user_input['r_values']['window']

    xml_generator = XMLGenerator()
    for building_info in scraped_json:
        building_index = building_info['building_choice_index']-1
        building_description = building_info['title']
        building_floor_area = building_info['floor_area']
        building_wall_list = building_info['walls_info']
        floor_area = building_info['floor']
        roof_area = building_info['roof']

        building = xml_generator.get_building_xml(
            building_index, building_description, is_residential, building_floor_area)
        building_key = building.find('key').text

        if roof_area:
            roof = xml_generator.get_roof_xml(
                roof_index, building_key, roof_area, roof_r_values[0], roof_r_values[1])
            roof_list.append(roof)

        if floor_area not in ['', '0.0']:
            floor = xml_generator.get_floor_xml(
                floor_index, building_key, floor_area, floor_r_values[0], floor_r_values[1])
            floor_list.append(floor)

        for wall_info in building_wall_list:
            wall_area = wall_info[0]
            window1_quantity = wall_info[1]
            window2_quantity = wall_info[2]
            window1_area_quantity = window1_quantity * window1_area
            window2_area_quantity = window2_quantity * window2_area
            door_area = wall_info[3]

            if wall_area:
                wall = xml_generator.get_wall_xml(
                    wall_index, building_key, wall_area, wall_r_values[0], wall_r_values[1])
                window_list = wall.find('windows')
                door_list = wall.find('doors')

                if window1_area_quantity:
                    window = xml_generator.get_window_xml(
                        window1_index, building_key, window1_area_quantity)
                    window_list.append(window)

                if window2_area_quantity:
                    window = xml_generator.get_window_xml(
                        window2_index, building_key, window2_area_quantity)
                    window_list.append(window)

                if door_area:
                    door = xml_generator.get_door_xml(
                        door_index, building_key, door_area, is_swinging_door)
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
    tree.write(f'{XML_OUTPUT}',
               encoding='utf-8', xml_declaration=True)

    file_path = os.path.join(XML_OUTPUT)

    with open(file_path, 'rb') as xml_file:
        response = HttpResponse(
            xml_file.read(), content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename={XML_OUTPUT}'
    return response
