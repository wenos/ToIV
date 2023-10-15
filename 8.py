import random
import time
import csv
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

CSV_FILE = 'data.csv'  # Имя CSV файла, куда будут сохраняться данные

def save_data_to_file_csv():
    # Создание записи с 4 показаниями датчиков, временем и номером чемодана (последние две цифры IP-адреса)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = HOST.split('.')[-1]
    record = {
        'power': JSON_DICT['power'],
        'motion': JSON_DICT['motion'],
        'temperature': JSON_DICT['temperature'],
        'sound': JSON_DICT['sound'],
        'date': timestamp,
        'suitcase_number': ip_address
    }

    # Открываем файл CSV для записи
    with open(CSV_FILE, 'a') as file:
        fieldnames = ['power', 'motion', 'temperature', 'sound', 'date', 'suitcase_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Если файл пустой, создаем заголовок
        if file.tell() == 0:
            writer.writeheader()

        # Записываем данные
        writer.writerow(record)

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
        time.sleep(0)
        # Сохраняем данные в файл
        save_data_to_file_json()
        save_data_to_file_csv()

        count += 1
        for value in SUB_TOPICS.values():
            JSON_DICT[value] = random.randint(1, 5)

        if count == 5:
            break

if __name__ == "__main__":
    main()
