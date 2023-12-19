# files us2009 IECC,ed by the program
import os

folder = os.path.dirname(os.path.abspath(__file__))
json_folder = os.path.join(folder, 'json')
empty_xml_folder = os.path.join(folder, 'empty_xml')
output_xml_folder = os.path.join(folder, 'output_xml')

PDF_SCRAPED_FILE = os.path.join(json_folder, 'pdf_scraped.json')
USER_INPUT_FILE = os.path.join(json_folder, 'user_inputs.json')
XML_ELEMENTS_INFO_FILE = os.path.join(json_folder, 'elements_info.json')
XML_ELEMENTS_INFO_FILE_2018 = os.path.join(json_folder, 'elements_info_2018.json')
XML_OUTPUT = 'xml_output.cxl'


STARTING_XML_2009_FILE = os.path.join(empty_xml_folder, 'empty_2009.xml')
STARTING_XML_2020_FILE = os.path.join(empty_xml_folder, 'empty_2020.xml')
STARTING_XML_2018_FILE = os.path.join(empty_xml_folder, 'empty_2018.xml')
