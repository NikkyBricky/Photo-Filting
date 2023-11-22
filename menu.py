# Бунин Николай, 21 группа
from PIL import Image
from filters import Blurring, Inverse, Edges, Noise, Dirt
pic = None


def filtered_img():
    global pic
    pic = pic


# проверка введенного пути. Сделано без os, т.к она проверяет лишь наличие файла, а не его содержимое.
def to_path():
    while True:
        path = input('Введите путь к файлу с изображением:\n')
        # комментарий ниже нужен, чтобы PEP8 не выдавал weak point
        #  noinspection PyBroadException
        try:
            Image.open(path)
        except Exception:
            print('Путь к файлу с изображением введён неверено. Повторите попытку.')
        else:
            global pic
            pic = Image.open(path).convert('RGB')
            break


# функция для меню фильтров
def menu():
    print('Добро пожаловать в меню фильтров для изображений!')
    global pic
    filters = {'1': {'name': 'Blur Filter',
                     'meaning': 'Позволяет сделать различные виды размытия изображения.',
                     'class': Blurring},
               '2': {'name': 'Inverse Filter',
                     'meaning': 'Меняет значение цветов для каждого пикселя на обратное.',
                     'class': Inverse()},
               '3': {'name': 'Edges Filter',
                     'meaning': 'Выделяет границы объектов изображения и выводит их в ч/б формате.',
                     'class': Edges},
               '4': {'name': 'Noise Filter',
                     'meaning': 'Создает "шум" на изображении с интенсивностью в зависимости от выбора пользователя.',
                     'class': Noise},
               '5': {'name': 'Dirt Filter',
                     'meaning': '"Пачкает" изображение, создавая в рандомных местах черные пиксели, '
                                'если изображение светлое.\n'
                                ' Также делает изображение более темным, если оно темное.',
                     'class': Dirt},
               '6': {'name': 'Возврат к выбору пути файла'},
               '0': {'name': 'Выход'}}
    for num_key in range(0, len(filters.keys())):  # вывод меню фильтров
        print(f'{num_key} - {filters[str(num_key)]['name']}')
    chosen_filter = input('Выберите номер фильтра (или 0 для выхода):\n').lower()
    while chosen_filter not in filters:
        print('Нет такого фильтра. Попробуй снова.')
        chosen_filter = input('Выберите номер фильтра (или 0 для выхода):\n').lower()
    if chosen_filter == '0':
        print('Удачи!')
        quit()
    if chosen_filter == '6':  # изменение пути файла
        to_path()
        menu()
    print(f'{filters[chosen_filter]['name']}: \n', filters[chosen_filter]['meaning'])   # вывод значения фильтра
    print()
    choice = input('Хотите применить фильтр к изображению (Да/Нет)?\n').lower()
    while choice not in ['да', 'нет', 'lf', 'ytn']:
        print('Нет такого ответа.')
        choice = input('Хотите применить фильтр к изображению (Да/Нет)?\n').lower()
    if choice in ['нет', 'ytn']:
        menu()
    pic = filters[chosen_filter]['class'].change_pic(pic)  # применение фильтра
    while True:  # проверка ввода пути файла
        saving = input('Куда сохранить? (0 - если не хотите сохранять)\n')
        if saving == '0':
            break
        #  noinspection PyBroadException
        try:
            pic.save(saving)
        except Exception:
            print('Что-то пошло не так. Повторите попытку.')
        else:
            pic.save(saving)
            break
    ask = input('Еще? (Да/Нет) или (1 - если не хотите менять изоображение\n'
                '                   2 - если хотите применить фильтр '
                'к только что отфильтрованному изображению)\n').lower()
    if ask == '1':
        menu()
    if ask == '2':
        filtered_img()
        menu()
    while ask not in ['да', 'нет', 'lf', 'ytn']:
        print('Нет такого ответа.')
        ask = input('Еще?\n').lower()
    if ask == 'да' or ask == 'lf':
        to_path()
        menu()
    else:
        exit('Удачи!')


# начало программы. путь и меню разделены для того, чтобы пользователь возвращался конкретно в меню фильтров,
# а не в начало  программы, если он не захотел применять фильтр.
to_path()
menu()
