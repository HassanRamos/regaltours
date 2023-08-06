import xml.etree.cElementTree as element
from xml.etree import ElementTree
import json
import xmltodict

def _convert_json_to_xml(data,root=None,is_start=True,start_node_name=None):
    if is_start and start_node_name == None:
        raise "error start node is needed"
    if is_start == True:
        root = element.Element("hot:"+start_node_name)

    for key in list(data.keys()):
        if type(data[key]).__name__ == "list":
            sub_root = element.SubElement(root,"hot:"+key)
            for list_item in data[key]:
                _convert_json_to_xml(data=list_item, root=sub_root, is_start=False)
        if type(data[key]).__name__ == "dict":
            sub_root = element.SubElement(root,"hot:"+key)
            _convert_json_to_xml(data=data[key], root=sub_root, is_start=False)
        else:
           element.SubElement(root, "hot:"+key).text = str(data[key])

    return root

def convert_json_to_xml(data,start_node_name):
    xml_string = ElementTree.tostring(_convert_json_to_xml(data,start_node_name=start_node_name), encoding='unicode')
    xml_string = xml_string.replace("</hot:"+start_node_name,"</hot:"+start_node_name.split(" ")[0])
    return xml_string

def convert_xml_to_json(xml_data):
        data_dict = xmltodict.parse(xml_data)
        return data_dict

