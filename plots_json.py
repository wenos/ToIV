from datetime import datetime
import matplotlib.pyplot as plt
import json


# Функция получения данных из json-файла
def get_data_from_json(filename):
    with open(filename, 'r') as file:
        file_data = json.load(file)
    return file_data


def create_plots(plots_data_lists):
    # Создание графиков для отрисовки данных
    fig, axs = plt.subplots(1, 3, figsize=(15,5)) # Получим окно с 1 колонкой и 2 столбцами графиков

    # fig - окно, в котором будут отрисовываться графики
    # axs содержит в себе список графиков для отрисовки на них значений

    # Задание набора точек для отрисовки
    # Первый аргумент - список значений по оси X, второй аргумент - по оси Y

    temp = {}
    for i in range(len(plots_data_lists['temperature'])):
        if plots_data_lists['temperature'][i] in temp:
            temp[plots_data_lists['temperature'][i]] += 1
        else:
            temp[plots_data_lists['temperature'][i]] = 1
    print(temp)


    axs[0].bar(temp.keys(), temp.values())
    axs[0].set_xlabel('Значения температуры')
    axs[0].set_ylabel('Частота записей')
    axs[0].set_title('Температура')
    print(plots_data_lists['date'])
    # Формирование гистограммы
    axs[1].plot(plots_data_lists['date'], plots_data_lists['motion'])
    axs[1].set_xlabel('Время')
    axs[1].set_title('Движение')

    labels = ['Категория A', 'Категория B', 'Категория C', 'Категория D']
    sizes = [30, 15, 25, 20]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # Опциональное "вырезание" секторов

    # Построение круговой диаграммы
    axs[2].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    axs[2].axis('equal')  # Это делает круговую диаграмму круглой

    # Добавление заголовка
    plt.title('Пример круговой диаграммы')
    return fig, axs


def main():
    plots_data_lists = {
        'motion': [],
        'sound': [],
        'date': [],
        'temperature': [],
        'power': []
    }

    json_data = get_data_from_json("data.json")

    # Заполнение списков с данными, с преобразованием типов
    for json_dict in json_data:
        plots_data_lists['motion'].append(int(json_dict.get('motion')))
        plots_data_lists['date'].append(datetime.fromisoformat(json_dict.get('date')))
        plots_data_lists['sound'].append(float(json_dict.get('sound')))
        plots_data_lists['power'].append(float(json_dict.get('power')))
        plots_data_lists['temperature'].append(float(json_dict.get('temperature')))

    fig, axs = create_plots(plots_data_lists)

    plt.show()


if __name__ == "__main__":
    main()
