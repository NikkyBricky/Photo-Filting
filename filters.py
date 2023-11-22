from PIL import Image, ImageFilter


# я не использовал наследование классов,
# т.к каждый класс выполняет совершенно разные функции и не имеет ничего общего с другими
class Blurring:
    @staticmethod  # это для PEP8
    def change_pic(image: Image.Image) -> Image.Image:
        def check_ans(n):
            while not (n.isdigit() and int(n) <= 1000000000):  # значения больше данного вызывают ошибку
                if n.isdigit() and int(n) > 1000000000:
                    print()
                    print('Слишком большое значение.')
                else:
                    print('Нет такого значения усиления размытия. Попробуй снова.')
                n = input('Введите корректное значения изменения размытия:\n')
            return int(n)

        def to_gauss(img, num_blur):

            blur_image = img.filter(ImageFilter.GaussianBlur(num_blur))
            blur_image.show()
            return blur_image

        def to_median(img):

            median = img.filter(ImageFilter.MedianFilter(9))
            median.show()
            return median

        def to_box(img, num_blur):

            box_blur = img.filter(ImageFilter.BoxBlur(num_blur))
            box_blur.show()
            return box_blur

        def filters_menu(img):  # меню для фильтров размытия изображения
            blurs = {'1': {'name': 'Размытие по Гауссу',
                           'meaning': 'Размытие, которое сглаживает неравномерные значения пикселей изображения,'
                                      ' обрезая самые высокие значения.',
                           'function': to_gauss},
                     '2': {'name': 'Медианное размытие',
                           'meaning': 'Один из способов размытия, '
                                      'в котором группы пикселей меняются на среднее значение пикселей.\n'
                                      ' Более высокие значения уменьшаются, более низкие – увеличиваются,'
                                      ' усредняя значения.',
                           'function': to_median},
                     '3': {'name': 'Размытие по рамке',
                           'meaning': 'Метод размытия изображения, который применяет концепцию замены значений пикселей'
                                      ' изображения средним значением соседних пикселей.',
                           'function': to_box}}
            print('Добро пожаловать в фильтр для размытия изображения! Вот, что он может:')
            for num_key in range(1, len(blurs.keys()) + 1):  # вывод меню фильтров
                print(f'{num_key} - {blurs[str(num_key)]['name']}')

            chosen_filter = input('Введите номер фильтра:\n')
            while chosen_filter not in blurs:
                print('Нет такого фильтра. Попробуй снова.')
                chosen_filter = input('Выберите номер фильтра:\n').lower()
            print(f'{blurs[chosen_filter]['name']}: \n', blurs[chosen_filter]['meaning'])  # вывод значения фильтра
            print()
            choice = input('Хотите применить фильтр к изображению (Да/Нет)?\n').lower()
            while choice not in ['да', 'нет', 'lf', 'ytn']:
                print('Нет такого ответа.')
                choice = input('Хотите применить фильтр к изображению (Да/Нет)?\n').lower()
            if choice in ['нет', 'ytn']:
                img = filters_menu(image)
                return img
            if chosen_filter == '2':
                img = blurs[chosen_filter]['function'](img)  # применение фильтра
            else:
                num_blur = input('На сколько сильное размытие вы хотите получить?\n(имеют смысл значения от 0 до 200, '
                                 'но вводить можно значения до 1000000000)\n')
                num_blur = check_ans(num_blur)
                img = blurs[chosen_filter]['function'](img, num_blur)
            return img
        image = filters_menu(image)
        return image


class Inverse:
    @staticmethod
    def change_pic(image: Image.Image) -> Image.Image:
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = image.getpixel((i, j))
                red = 255 - r
                green = 255 - g
                blue = 255 - b
                image.putpixel((i, j), (red, green, blue))
        image.show()
        return image


class Edges:
    @staticmethod
    def change_pic(image: Image.Image) -> Image.Image:
        img_gray = image.convert("L")
        ans = input('Фильтр к вашим услугам. Вот, что он может:\n'
                    '1 - показать контур объектов изображения\n'
                    '2 - показать сглаженный контур объектов изображения\n'
                    '3 - показать рельеф объектов изображения\n')
        while not (ans.isdigit() and int(ans) in range(1, 4)):
            print('Нет такого фильтра. Повторите попытку.')
            ans = input('Введите корректный номер фильтра:\n')
        if ans == '1':
            edges = img_gray.filter(ImageFilter.FIND_EDGES)
            edges.show()
            return edges
        if ans == '2':
            img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
            edges_smooth = img_gray_smooth.filter(ImageFilter.FIND_EDGES)
            edges_smooth.show()
            return edges_smooth
        if ans == '3':
            img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
            emboss = img_gray_smooth.filter(ImageFilter.EMBOSS)
            emboss.show()
            return emboss


class Noise:
    @staticmethod
    def change_pic(image: Image.Image) -> Image.Image:
        val = input('На сколько сильный шум вы хотите сделать (от 1 до 10)?\n')  # большие значения не имеют смысла
        while not (val.isdigit() and int(val) in range(1, 11)):
            print('Нет такого значения. Повторите попытку.')
            val = input('На сколько сильный шум вы хотите сделать (от 1 до 10)?\n')
        for i in range(int(val)):  # применение фильтра
            image = image.filter(ImageFilter.SHARPEN)
        image.show()
        return image


class Dirt:
    @staticmethod
    def change_pic(image: Image.Image) -> Image.Image:
        import random
        w, h = image.size
        ans = input('Вот, что может этот фильтр:\n'
                    '1 - "испачкать" изображение в рандомных местах\n'
                    '2 - "испачкать" изображение в рандомных местах и инверсировать цвет изображения\n')
        while not (ans.isdigit() and int(ans) in range(1, 3)):
            print('Нет такого номера функции фильтра. Повторите попытку.')
            ans = input('Введите корректное значение номера фильтра:\n')
        if ans == '1':
            for i in range(w):
                for j in range(h):
                    n = random.randint(0, 255)
                    r, g, b = image.getpixel((i, j))
                    red = max(0, r - n)
                    green = max(0, g - n)
                    blue = max(0, b - n)
                    image.putpixel((i, j), (red, green, blue))
        if ans == '2':
            for i in range(w):
                for j in range(h):
                    n = random.randint(0, 255)
                    r, g, b = image.getpixel((i, j))
                    red = max(0, n - r)
                    green = max(0, n - g)
                    blue = max(0, n - b)
                    image.putpixel((i, j), (red, green, blue))
        image.show()
        return image
