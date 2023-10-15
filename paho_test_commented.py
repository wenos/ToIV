import random
import time

import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
import json
from datetime import datetime


# Параметры подключения к MQTT-брокеру
HOST = "192.168.1.23" # IP чемодана
PORT = 1883 # Стандартный порт подключения для Mosquitto
KEEPALIVE = 60 # Время ожидания доставки сообщения, если при отправке оно будет прeвышено, брокер будет считаться недоступным

# Словарь с топиками и собираемыми из них параметрами
SUB_TOPICS = {
    '/devices/wb-map12e_23/controls/Ch 1 P L2': 'power',
    '/devices/wb-msw-v3_21/controls/Current Motion': 'motion',
    '/devices/wb-ms_11/controls/Temperature': 'temperature',
    '/devices/wb-msw-v3_21/controls/Sound Level': 'sound'
}

JSON_LIST = []
XML_LIST = []
# Создание словаря для хранения данных JSON
JSON_DICT = {}
for value in SUB_TOPICS.values():
    JSON_DICT[value] = 0


def on_connect(client, userdata, flags, rc):
    """ Функция, вызываемая при подключении к брокеру

    Arguments:
    client - Экземпляр класса Client, управляющий подключением к брокеру
    userdata - Приватные данные пользователя, передаваемые при подключениии
    flags - Флаги ответа, возвращаемые брокером
    rc - Результат подключения, если 0, всё хорошо, в противном случае идем в документацию
    """
    print("Connected with result code " + str(rc))

    # Подключение ко всем заданным выше топикам
    for topic in SUB_TOPICS.keys():
        client.subscribe(topic)


def on_message(client, userdata, msg):
    """ Функция, вызываемая при получении сообщения от брокера по одному из отслеживаемых топиков

    Arguments:
    client - Экземпляр класса Client, управляющий подключением к брокеру
    userdata - Приватные данные пользователя, передаваемые при подключениии
    msg - Сообщение, приходящее от брокера, со всей информацией
    """
    payload = msg.payload.decode() # Основное значение, приходящее в сообщение, например, показатель температуры
    topic = msg.topic # Топик, из которого пришло сообщение, поскольку функция обрабатывает сообщения из всех топиков

    param_name = SUB_TOPICS[topic]
    JSON_DICT[param_name] = payload
    JSON_DICT['time'] = str(datetime.now())

    JSON_LIST.append(JSON_DICT.copy())

    print(topic + " " + payload)

    # Запись данных в файл
    with open('data.json', 'w') as file:
        json_string = json.dumps(JSON_LIST) # Формирование строки JSON из словаря
        file.write(json_string)


def save_data_to_file_json():
    # Создание записи с 4 показаниями датчиков, временем и номером чемодана (последние две цифры IP-адреса)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = HOST.split('.')[-1]
    record = {
        'power': JSON_DICT['power'],
        'motion': JSON_DICT['motion'],
        'temperature': JSON_DICT['temperature'],
        'sound': JSON_DICT['sound'],
        'date': date,
        'suitcase_number': ip_address
    }

    JSON_LIST.append(record)

    # Запись данных в файл
    with open('data.json', 'w') as file:
        json_string = json.dumps(JSON_LIST)  # Формирование строки JSON из списка записей
        print(json_string)
        file.write(json_string)



def save_data_to_file_xml():
    datet = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = HOST.split('.')[-1]
    # Создаем корневой элемент
    root = ET.Element("data")

    # Создаем подэлементы для каждой записи
    record = ET.SubElement(root, "record")
    power = ET.SubElement(record, "power")
    power.text = str(JSON_DICT['power'])
    motion = ET.SubElement(record, "motion")
    motion.text = str(JSON_DICT['motion'])
    temperature = ET.SubElement(record, "temperature")
    temperature.text = str(JSON_DICT['temperature'])
    sound = ET.SubElement(record, "sound")
    sound.text = str(JSON_DICT['sound'])
    date = ET.SubElement(record, "date")
    date.text = datet
    suitcase_number = ET.SubElement(record, "suitcase_number")
    suitcase_number.text = ip_address

    tree = ET.ElementTree(root)

    with open('data.xml', 'wb') as file:
        tree.write(file, encoding="utf-8")


def main():
    # Создание и настройка экземпляра класса Client для подключения в Mosquitto
    # client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(HOST, PORT, KEEPALIVE)
    #
    # client.loop_forever() # Бесконечный внутренний цикл клиента в ожидании сообщений
    count = 0
    while True:
        time.sleep(5)
        # Сохраняем данные в файл
        save_data_to_file_json()
        save_data_to_file_xml()
        count += 1
        for value in SUB_TOPICS.values():
            JSON_DICT[value] = random.randint(1, 5)
        if count == 5:
            break
if __name__ == "__main__":
    main()
