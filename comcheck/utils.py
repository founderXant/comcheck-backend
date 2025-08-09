from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from random import randint

import json
import PyPDF2
import re

from app.constants import *

from django.conf import settings 
class PDFScraper:

    @staticmethod
    def read_space_input(filename):
        print(f'Starting to read: {filename}')

        f = open(filename, mode='rb')
        pdf = PyPDF2.PdfReader(f)

        page_texts = []
        page_count = 0
        while page_count < len(pdf.pages) - 1:
            print(f"Reading page no: {page_count + 1}")

            if page_count == 0:
                current_page = pdf.pages[page_count].extract_text()
                next_page = pdf.pages[page_count + 1].extract_text()
            else:
                current_page = next_page
                next_page = pdf.pages[page_count + 1].extract_text()

            if 'General Details' in current_page and 'General Details' in next_page:
                page_texts.append(current_page.splitlines())

                if page_count == len(pdf.pages) - 2:
                    page_texts.append(next_page.splitlines())

            elif 'General Details' in current_page and 'General Details' not in next_page:
                page_texts.append(current_page.splitlines() + next_page.splitlines())

            page_count += 1

        print(f'Completed reading {filename}')

        return page_texts



    @staticmethod
    def scrape_space_input(page_texts):
        all_info = []

        for text in page_texts:
            info = {
                'title': '',
                'building_choice_text': 'NONE',
                'building_choice_index': 'NONE',
                'floor_area': '',
                'walls_info': '',
                'roof': '',
                'floor': ''
            }

            start = 0
            end = 0
            no_walls = False

            for i in range(len(text) - 1):
                if 'General Details' in text[i + 1]:
                    building_desc = text[i].strip()
                    floor_area_text = text[i + 2]
                    floor_area = re.search(r'\d+', floor_area_text).group(0)
                    info['title'] = building_desc
                    info['floor_area'] = floor_area

            for i in range(len(text) - 2):
                if 'walls, windows, doors' in text[i].lower():
                    if 'exp' in text[i + 1].lower():
                        start = i + 2
                    else:
                        no_walls = True

                if text[i].startswith('3.1') or text[i].startswith('4'):
                    if start != 0:
                        end = i
                        break

            if not no_walls:
                table_lines = text[start:end]
                table_lines = list(map(lambda x: x.split()[1:], table_lines))
                converted_to_int = []
                for line in table_lines:
                    int_line = list(map(lambda x: int(float(x)), line))
                    converted_to_int.append(int_line)

                table_lines = converted_to_int



            else:
                table_lines = []

            info['walls_info'] = table_lines

            for i in range(len(text) - 1):
                if 'Roofs, Skylights' in text[i]:
                    if 'No Roof or Skylight data' not in text[i + 1]:
                        info['roof'] = text[i + 2].split()[1]
                        break

            for i in range(len(text) - 1):
                if '6. Floors:' in text[i] and 'No additional input required for this floor type' not in text[i + 2]:
                    floor_text = text[i + 2].strip()
                    try:
                        floor_value = re.search(r'\d+.\d+', floor_text).group(0)
                        info['floor'] = floor_value
                        break
                    except:
                        info['floor'] = ''

            # only add the building info if it has any of the values other wise if it doesn't has anything then skip it
            if info['walls_info'] or info['roof'] or info['floor']:
                all_info.append(info)

        return all_info



    @staticmethod
    def read_window_input(filename):
        print(f'Reading {filename}')
        f = open(filename, mode='rb')
        pdf = PyPDF2.PdfReader(f)
        text = pdf.pages[0].extract_text().splitlines()
        print(f'Completed reading {filename}')
        return text



    @staticmethod
    def scrape_window_input(text):

        windows = []

        for i in range(len(text)):
            if 'Height' in text[i]:
                height = float(re.search(r'\d+.\d+', text[i]).group(0))
                width = float(re.search(r'\d+.\d+', text[i + 1]).group(0))
                info = {
                    'height': height,
                    'width': width,
                    'area': height * width
                }
                windows.append(info)


        remaining = 2 - len(windows)

        while remaining > 0:
            info = {
                'height': 1,
                'width': 1,
                'area': 1
            }
            windows.append(info)
            remaining -= 1


        return windows



    @staticmethod
    def main(space_input_filename, output_filename):
        space_input_text = PDFScraper.read_space_input(space_input_filename)

        input_info = PDFScraper.scrape_space_input(space_input_text)


        with open(output_filename, mode='w') as f:
            json.dump(input_info, f, indent=4)

        print(f'Scraped information saved in: {output_filename}')



class XMLGenerator:
    def __init__(self):
        with open(f'{XML_ELEMENTS_INFO_FILE}', mode='r') as f:
            self.elements_info = json.load(f)

        self.building_list = self.elements_info['buildings_info']
        self.roof_list = self.elements_info['roofs_info']
        self.floor_list = self.elements_info['floors_info']
        self.wall_list = self.elements_info['walls_info']
        self.window_list = self.elements_info['windows_info']
        self.door_list = self.elements_info['doors_info']


    def get_building_xml(self, building_index, description, is_residential, floor_area) -> Element:

        building = self.building_list[building_index]
        building_name = building['name']
        power_density = building['power_density']
        internal_load = building['internal_load']
        residential = 'RESIDENTIAL' if is_residential else 'NON_RESIDENTIAL'
        building_key = randint(1000000, 9999999)

        building_xml = f'''
                    <activityUse>
                        <key>{building_key}</key>
                        <activityType>{building_name}</activityType>
                        <activityDescription><![CDATA[{description}]]></activityDescription>
                        <areaDescription><![CDATA[{description}]]></areaDescription>
                        <powerDensity>{power_density}</powerDensity>
                        <ceilingHeight>0</ceilingHeight>
                        <internalLoad>{internal_load}</internalLoad>
                        <listPosition>0</listPosition>
                        <constructionType>{residential}</constructionType>
                        <floorArea>{floor_area}</floorArea>
                        <interiorLightingSpace>
                            <description><![CDATA[{description}, {floor_area}]]>
                            </description>
                            <allowanceType>ALLOWANCE_NONE</allowanceType>
                            <allowanceFloorArea>0</allowanceFloorArea>
                            <rcrPerimeter>0</rcrPerimeter>
                            <rcrFloorToWorkplaneHeight>0</rcrFloorToWorkplaneHeight>
                            <rcrWorkplaneToLuminaireHeight>0</rcrWorkplaneToLuminaireHeight>
                        </interiorLightingSpace>
                    </activityUse>
                    '''

        return ET.fromstring(building_xml)


    def get_roof_xml(self, roof_index, building_key, gross_area, cavity_r_value, continuous_r_value) -> Element:
        roof_info = self.roof_list[roof_index]
        roof_name = roof_info['name']
        roof_description = roof_info['description']
        contains_continuous_r_value = roof_info['contains_continuous_r_value']
        contains_cavity_r_value = roof_info['contains_cavity_r_value']

        roof_xml = f'''
                    <roof>
                        <roofType>{roof_name}</roofType>
                        <roofInsulType>ROOF_INSUL_TYPE_UNSPECIFIED</roofInsulType>
                        <description>{roof_description}</description>
                        <assemblyType>Roof</assemblyType>
                        <bldgUseKey>{building_key}</bldgUseKey>
                        {'<cavityRvalue>' + str(cavity_r_value) + '</cavityRvalue>' if contains_cavity_r_value else ''}
                        {'<continuousRvalue>' + str(continuous_r_value) + '</continuousRvalue>' if contains_continuous_r_value else ''}
                        <allowanceType>ENV_ALLOWANCE_NONE</allowanceType>
                        <exemptionType>ENV_EXEMPTION_NONE</exemptionType>
                        <validAllowanceType>false</validAllowanceType>
                        <validExemptionType>false</validExemptionType>
                        <constructionType>NON_RESIDENTIAL</constructionType>
                        <adjacentSpaceType>ADJACENT_SPACE_EXTERIOR</adjacentSpaceType>
                        <grossArea>{gross_area}</grossArea>
                    </roof>
                '''
        return ET.fromstring(roof_xml)


    def get_floor_xml(self, floor_index, building_key, gross_area, cavity_r_value, continuous_r_value) -> Element:
        floor_info = self.floor_list[floor_index]
        floor_name = floor_info['name']
        floor_description = floor_info['description']
        contains_continuous_r_value = floor_info['contains_continuous_r_value']
        contains_cavity_r_value = floor_info['contains_cavity_r_value']

        floor_xml = f'''
                <floor>
                    <floorType>{floor_name}</floorType>

                    {'<depthOfInsulation>0.00</depthOfInsulation>'
                     '<insulationPosition>NO_INSULATION</insulationPosition>'
                     '<hasEdgeInsul>false</hasEdgeInsul>' if floor_index in [3, 4] else ''}

                    {'<floorExposedFrameType> FLOOR_EXPOSED_FRAME_TYPE_UNSPECIFIED </floorExposedFrameType>'
        if floor_index not in [3, 4] else ''}

                    <description>{floor_description}</description>
                    <assemblyType>Floor</assemblyType>
                    <bldgUseKey>{building_key}</bldgUseKey>

                    {'<cavityRvalue>' + str(cavity_r_value) + '</cavityRvalue>' if contains_cavity_r_value else ''}
                    {'<continuousRvalue>' + str(continuous_r_value) + '</continuousRvalue>' if contains_continuous_r_value else ''}

                    <allowanceType>ENV_ALLOWANCE_NONE</allowanceType>
                    <exemptionType>ENV_EXEMPTION_NONE</exemptionType>
                    <validAllowanceType>false</validAllowanceType>
                    <validExemptionType>false</validExemptionType>
                    <constructionType>NON_RESIDENTIAL</constructionType>
                    <adjacentSpaceType>ADJACENT_SPACE_EXTERIOR</adjacentSpaceType>
                    <grossArea>{gross_area}</grossArea>
                </floor>'''

        return ET.fromstring(floor_xml)


    def get_wall_xml(self, wall_index, building_key, gross_area, cavity_r_value, continuous_r_value) -> Element:
        wall_info = self.wall_list[wall_index]
        wall_name = wall_info['name']
        wall_description = wall_info['description']
        contains_continuous_r_value = wall_info['contains_continuous_r_value']
        contains_cavity_r_value = wall_info['contains_cavity_r_value']

        wall_xml = f'''
                <agWall>
                    <wallType>{wall_name}</wallType>
                    <nextToUncondSpace>false</nextToUncondSpace>
                    <description>{wall_description}</description>
                    <assemblyType><![CDATA[Ext. Wall]]></assemblyType>
                    <bldgUseKey>{building_key}</bldgUseKey>
                    {'<cavityRvalue>' + str(cavity_r_value) + '</cavityRvalue>' if contains_cavity_r_value else ''}
                    {'<continuousRvalue>' + str(continuous_r_value) + '</continuousRvalue>' if contains_continuous_r_value else ''}
                    <allowanceType>ENV_ALLOWANCE_NONE</allowanceType>
                    <exemptionType>ENV_EXEMPTION_NONE</exemptionType>
                    <validAllowanceType>false</validAllowanceType>
                    <validExemptionType>false</validExemptionType>
                    <constructionType>NON_RESIDENTIAL</constructionType>
                    <adjacentSpaceType>ADJACENT_SPACE_EXTERIOR</adjacentSpaceType>
                    <grossArea>{gross_area}</grossArea>
                    <windows></windows>
                    <doors></doors>
                </agWall>
            '''

        return ET.fromstring(wall_xml)


    def get_window_xml(self, window_index, building_key, gross_area) -> Element:
        window_info = self.window_list[window_index]
        window_name = window_info['name']
        window_description = window_info['description']
        window_u_factor = window_info['u_factor']

        window_xml = f'''
            <window>
                <windowOpenType>NON_OPERABLE_WINDOW</windowOpenType>
                <glazingType>SINGLE_PANE</glazingType>
                <glazingMaterialType>GLASS_GLAZING_MAT</glazingMaterialType>
                <frameType>{window_name}</frameType>
                <perfDataType>PERF_TYPE_DEFAULT</perfDataType>
                <solarType>CLEAR</solarType>
                <isSiteShading>false</isSiteShading>
                <feetAg>0.00</feetAg>
                <propShgc>0.800000</propShgc>
                <propProjectionFactor>0.00</propProjectionFactor>
                <listPosition>7</listPosition>
                <description>{window_description}</description>
                <assemblyType><![CDATA[Window]]></assemblyType>
                <bldgUseKey>{building_key}</bldgUseKey>
                <propUvalue>{window_u_factor}</propUvalue>
                <allowanceType>ENV_ALLOWANCE_NONE</allowanceType>
                <exemptionType>ENV_EXEMPTION_NONE</exemptionType>
                <validAllowanceType>false</validAllowanceType>
                <validExemptionType>false</validExemptionType>
                <constructionType>RESIDENTIAL</constructionType>
                <adjacentSpaceType>ADJACENT_SPACE_EXTERIOR</adjacentSpaceType>
                <grossArea>{gross_area}</grossArea>
            </window>
            '''

        return ET.fromstring(window_xml)


    def get_door_xml(self, door_index, building_key, gross_area, is_swinging) -> Element:
        door_info = self.door_list[door_index]
        door_name = door_info['name']
        door_description = door_info['description']

        door_xml = f'''
                    <door>
                        <doorType>{door_name}</doorType>
                        <doorOpenType>{'SWINGING_DOOR' if is_swinging else 'NON_SWINGING_DOOR'}</doorOpenType>
                        <description>{door_description}</description>
                        <assemblyType><![CDATA[Door]]></assemblyType>
                        <bldgUseKey>{building_key}</bldgUseKey>
                        <propUvalue>0.000000</propUvalue>
                        <allowanceType>ENV_ALLOWANCE_NONE</allowanceType>
                        <exemptionType>ENV_EXEMPTION_NONE</exemptionType>
                        <validAllowanceType>false</validAllowanceType>
                        <validExemptionType>false</validExemptionType>
                        <constructionType>RESIDENTIAL</constructionType>
                        <adjacentSpaceType>ADJACENT_SPACE_EXTERIOR</adjacentSpaceType>
                        <grossArea>{gross_area}</grossArea>
                    </door>'''

        return ET.fromstring(door_xml)