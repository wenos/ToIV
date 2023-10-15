import json
import xml.etree.ElementTree as ET


def parse_json(file_path):

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    for record in json_data:
        power = record["power"]
        motion = record["motion"]
        temperature = record["temperature"]
        sound = record["sound"]
        date = record["date"]
        suitcase_number = record["suitcase_number"]

        print(f"Power: {power}")
        print(f"Motion: {motion}")
        print(f"Temperature: {temperature}")
        print(f"Sound: {sound}")
        print(f"Date: {date}")
        print(f"Suitcase Number: {suitcase_number}")


def parse_xml(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()

    for record in root.findall('record'):
        power = record.find('power').text
        motion = record.find('motion').text
        temperature = record.find('temperature').text
        sound = record.find('sound').text
        date = record.find('date').text
        suitcase_number = record.find('suitcase_number').text

        print(f"Power: {power}")
        print(f"Motion: {motion}")
        print(f"Temperature: {temperature}")
        print(f"Sound: {sound}")
        print(f"Date: {date}")
        print(f"Suitcase Number: {suitcase_number}")


parse_json("data.json")
parse_xml("data.xml")