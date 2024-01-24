import os
import shlex  # Для получения параметров
import shutil


def show_message(text='Ошибка ввода!', color_code=35, noprint=False):
    '''Показ сообщений разным цветом
        Чёрный = 30, Красный = 31, Зелёный = 32, Жёлтый = 33, Синий = 34, Розовый = 35, Бирюзовый = 36, Белый(Серый) = 37
    '''
    if noprint:
        return f'\033[{color_code}m{text}\033[m'
    print(f'\033[{color_code}m{text}\033[m')


def get_part(path, type_data=3):
    '''Получить из указанного пути
    0 - путь без имени файла
    1 - только имя файла
    2 - только расширение с точкой
    3 - имя + расширение'''
    if type_data == 0:
        return os.path.dirname(path)
    elif type_data == 1:
        return os.path.splitext(os.path.basename(path))[0]
    elif type_data == 2:
        return os.path.splitext(os.path.basename(path))[1]
    elif type_data == 3:
        return f'{os.path.splitext(os.path.basename(path))[0]}{os.path.splitext(os.path.basename(path))[1]}'


def is_valid_name(file_name):
    '''Проверка на корректность имени файла'''
    pattern = '@!№;%$:?*\'\",'
    for x in pattern:
        if x in file_name:
            return False
    return True


def del_end_slash(line: str):
    '''Удалить концевой слэш '\' в строке, если он есть '''
    if not line:
        return line
    if line.strip()[-1] == '\\':
        return line[:-1]
    return line


def isexist(path):
    '''Проверить существование файла или каталога'''
    return os.path.exists(path)


def f_exit():
    '''Выход из программы'''
    exit()


def help():
    show_message(f'{" Справка по командам ":=^30}', 34)
    print(f'* Внимание! Если в параметрах есть пробелы, то возьмите их в кавычки')
    print(f'* Внимание! Если в параметрах не указать полный путь, то действие будет применено в каталоге по умоланию\n')
    for k, v in commands.items():
        print(f'* Команда {show_message(k, 34, noprint=True)}')
        print(f'  {v[1]}')
        print()


def defc():
    '''Получить текущий каталог'''
    kat = os.getcwd()
    return kat


def dir(path=None):
    '''Печать содержимого указанного каталога, по умолчанию текущего'''
    if not path:
        path = defc()
    path = f'{path}\\'  # Для корректного отображения: d: или d:\
    if not isexist(path):
        er_tit = 'Не найден каталог'
        show_message(f'{er_tit}: {path}')
        return er_tit
    lst_dir = os.listdir(path)
    show_message(f'Содержимое каталога: {path}', 34)
    for i, x in enumerate(lst_dir):
        print(f'{i + 1:>4}. {x}')
    return 'Каталог найден'

def cd(path):
    '''Изменить каталог по умолчанию'''
    if not isexist(path):
        er_tit = 'Не найден каталог'
        show_message(f'{er_tit}: {path}')
        return er_tit
    os.chdir(path)
    er_tit = 'Был изменен каталог по умолчанию'
    show_message(f'{er_tit}', 32)
    # print(defc())
    return er_tit


def f_create_file(path):
    '''Создать файл'''
    if not '\\' in path and not '/' in path:  # Если указан файл в текущем каталоге
        path = f'{defc()}\\{path}'
    if not isexist(get_part(path, 0)):
        er_tit = 'Не найден путь'
        show_message(f'{er_tit}: {get_part(path, 0)}')
        return er_tit
    if not is_valid_name(get_part(path)):
        er_tit = 'Не корректное имя'
        show_message(f'{er_tit}: {get_part(path)}')
        return er_tit
    # Создать файл
    try:
        with open(fr'{path}', 'w') as file:
            pass
    except Exception as e:
        show_message(f'Ошибка создания файла, {e.__class__} {e.__str__()}', 31)
    er_tit = 'Файл был удачно создан'
    show_message(f'{er_tit}: {path}', 32)
    return er_tit


def f_create_dir(path):
    '''Создать каталог'''
    if not '\\' in path and not '/' in path:  # Если указан каталог в текущем каталоге
        path = f'{defc()}\\{path}'
    if not isexist(get_part(path, 0)):
        er_tit = 'Не найден путь'
        show_message(f'{er_tit}: {get_part(path, 0)}')
        return er_tit
    if not is_valid_name(get_part(path)):
        er_tit = 'Не корректное имя'
        show_message(f'{er_tit}: {get_part(path)}')
        return er_tit
    # Создать файл
    try:
        os.mkdir(path)
    except Exception as e:
        show_message(f'Ошибка создания каталога, {e.__class__} {e.__str__()}', 31)
    er_tit = 'Каталог был удачно создан'
    show_message(f'{er_tit}: {path}', 32)
    return er_tit


def f_copy(a, b):
    '''Копировать файл или каталог'''
    # Проверка на существование
    if not isexist(a):
        a = f'{defc()}\\{a}'    # Добавить каталог по умолчанию перед именем
    if not isexist(a):
        er_tit = 'Не найден откуда копировать'
        show_message(f'{er_tit}: {a}')
        return er_tit
    if not isexist(get_part(b, 0)):
        er_tit = 'Не найден каталог куда копировать'
        show_message(f'{er_tit}: {b}')
        return er_tit
    if not is_valid_name(get_part(b)):
        er_tit = 'Не корректное имя куда копировать'
        show_message(f'{er_tit}: {get_part(b)}')
        return er_tit
    # Узнать файл или каталог
    if os.path.isfile(a):
        if os.path.isdir(b):  # Если куда копировать каталог
            b = f'{b}\\{get_part(a)}'  # Добавить имя файла
        if isexist(b):
            er_tit = 'Куда копировать уже существует'
            show_message(f'{er_tit}: {b}')
            return er_tit
        shutil.copy2(a, b)
        er_tit = 'Файл был удачно скопирован'
        show_message(er_tit, 32)
    else:
        if get_part(a) != get_part(b):
            b = f'{b}\\{get_part(a)}'
        if isexist(b):
            er_tit = 'Куда копировать уже существует'
            show_message(f'{er_tit}: {b}')
            return er_tit
        shutil.copytree(a, b)
        er_tit = 'Каталог был удачно скопирован'
        show_message(er_tit, 32)
    return er_tit

def f_move(a, b):
    '''Копировать файл или каталог'''
    # Проверка на существование
    if not isexist(a):
        a = f'{defc()}\\{a}'    # Добавить каталог по умолчанию перед именем
    if not isexist(a):
        er_tit = 'Не найден откуда переместить'
        show_message(f'{er_tit}: {a}')
        return er_tit
    if not isexist(get_part(b, 0)):
        er_tit = 'Не найден каталог куда переместить'
        show_message(f'{er_tit}: {b}')
        return er_tit
    if not is_valid_name(get_part(b)):
        er_tit = 'Не корректное имя куда копировать'
        show_message(f'{er_tit}: {get_part(b)}')
        return er_tit
    # Узнать файл или каталог
    if os.path.isfile(a):
        if os.path.isdir(b):  # Если куда копировать каталог
            b = f'{b}\\{get_part(a)}'  # Добавить имя файла
        if isexist(b):
            er_tit = 'Куда переместить уже существует'
            show_message(f'{er_tit}: {b}')
            return er_tit
        shutil.move(a, b)
        er_tit = 'Файл был удачно перемещен'
        show_message(er_tit, 32)
    else:
        if get_part(a) != get_part(b):
            b = f'{b}\\{get_part(a)}'
        if isexist(b):
            er_tit = 'Куда переместить уже существует'
            show_message(f'{er_tit}: {b}')
            return er_tit
        shutil.copytree(a, b)
        shutil.rmtree(a)
        er_tit = 'Каталог был удачно перемещен'
        show_message(er_tit, 32)
    return er_tit

def f_del(path):
    '''Удалить файл или каталог если он существует
    Если указан несушествующий файл или каталог, то ошибка не выдается
    '''
    if isexist(path):
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                show_message(f'Ошибка выполнения команды удаления, {e.__class__} {e.__str__()}', 31)
        else:
            try:
                shutil.rmtree(path)
            except Exception as e:
                show_message(f'Ошибка выполнения команды удаления, {e.__class__} {e.__str__()}', 31)
    er_tit = 'ОК'
    show_message(er_tit, 32)
    return er_tit


def main():
    while True:
        print(defc())
        s = del_end_slash(input(r' > ').strip()).replace('\\', '\\\\')
        try:
            lst = shlex.split(
                s)  # Можно вводить параметры с разными кавычками и без: сopy "c:\test 1.txt" 'd:\test1.txt'
        except:
            show_message('Неправильная команда')
            continue
        # print(lst)  # Для тестов
        if not lst:  # Если ничего не введено
            continue
        com_name = lst[0]  # Название команды, ключ в словаре commands
        if not com_name in commands or len(lst) > 3:
            show_message('Неправильная команда')
            print()
            continue

        fname = commands[com_name][0]  # Название функции по ключу в словаре
        command = f'{fname}()'  # Если вызов без параметров, if len(lst) == 1
        # Если вызов с параметрами
        # Удалить слэш \ в конце, если указан (обычно \ указывается для каталогов)
        if len(lst) > 1:
            par1 = del_end_slash(lst[1]).replace('\\', '\\\\')
            command = f'{fname}("{par1}")'
            if len(lst) == 3:
                par2 = del_end_slash(lst[2]).replace('\\', '\\\\')
                command = f'{fname}("{par1}", "{par2}")'  # Читаем сырве строки с двумя \\
        # Выполнить команду
        try:
            res = eval(command)
        except Exception as e:
            show_message(f'Ошибка выполнения команды: {command}, {e.__class__} {e.__str__()}', 31)

        print()

def set_tests():
    '''Тесты'''
    # Удалить каталог или файл. Если указан несуществующий файл или каталог, то ошибки не выдавать
    assert f_del(r'D:\test') == 'ОК'                    # Удалить каталог
    assert f_del(r'Y:\test\Проверка 1') == 'ОК'         # Не ругаемся на несуществующий каталог
    assert f_del(r'D:\test\Новый файл.txt') == 'ОК'     # Удалить файл
    assert f_del(r'D:\test\new.txt') == 'ОК'
    # Создать каталог
    assert f_create_dir(r'Y:\test') == 'Не найден путь'
    assert f_create_dir(r'D:\test') == 'Каталог был удачно создан'
    assert f_create_dir(r'D:\test\Каталог 1') == 'Каталог был удачно создан'
    assert f_create_dir(r'D:\test\Каталог 2') == 'Каталог был удачно создан'
    assert cd(r'D:\test') == 'Был изменен каталог по умолчанию'
    assert f_create_dir(r'Каталог 3') == 'Каталог был удачно создан'    # Создать без полного пути, в текущем каталоге
    # Создать файл
    assert  f_create_file(r'D:\test\Новый файл.txt') == 'Файл был удачно создан'
    assert  f_create_file(r'D:\test\new.txt') == 'Файл был удачно создан'
    # Показать содержимое каталога
    assert dir('qwer') ==  'Не найден каталог'
    assert dir(r'D:\test\Каталог 1') ==  'Каталог найден'
    assert dir(r'D:') ==  'Каталог найден'
    # Изменить каталог по умолчанию
    assert cd(r'Y:\test\Проверка 1') ==  'Не найден каталог'
    assert cd(r'D:\test') ==  'Был изменен каталог по умолчанию'
    # Копирование
    assert f_copy(r'new.txt', r'Y:\test\Каталог 1') == 'Не найден каталог куда копировать'
    # Т.к. не найден каталог test222, считаем что это имя файла без расширения
    assert f_copy(r'new.txt', r'D:\test\test222') == 'Файл был удачно скопирован'
    assert f_copy(r'new.txt', r'D:\test\Каталог 1') == 'Файл был удачно скопирован'
    assert f_copy(r'new.txt', r'D:\test\Каталог 1') == 'Куда копировать уже существует'
    assert f_copy(r'new.txt', r'D:\test\Файл без расширения') == 'Файл был удачно скопирован'
    assert f_copy(r'Каталог 1', r'D:\test\Каталог 2') == 'Каталог был удачно скопирован'
    assert f_copy(r'Каталог 1', r'D:\test\Каталог 2') == 'Куда копировать уже существует'
    # Перемещение
    assert f_move(r'new.txt', r'D:\test\Каталог 2') == 'Файл был удачно перемещен'
    assert f_move(r'Каталог 2', r'D:\test\Каталог 3') == 'Каталог был удачно перемещен'
    assert f_move(r'Каталог 2', r'D:\test\Каталог 3') == 'Не найден откуда переместить'
    assert f_move(r'Каталог 1', r'D:\test\Каталог 4\Каталог 5') == 'Не найден каталог куда переместить'
    # Создать каталог 'Каталог 4' внутрь которого перенести каталог 'Каталог 1'
    assert f_move(r'Каталог 1', r'D:\test\Каталог 4') == 'Каталог был удачно перемещен'
    assert f_move(r'd:\test\test222', r'D:\test\Каталог 4') == 'Файл был удачно перемещен'


if __name__ == '__main__':
    # Имя команды -> [Вызывающая функия, Описание функции]
    commands = {'exit': ['f_exit', 'Выход из программы'],
                'help': ['help', 'Справка по командам'],
                'dir': ['dir',
                        'dir        - показать содержимое каталога по умолчанию; \n  '
                        'dir c:\kat - показать содержимое указанного каталога'],
                'cd': ['cd',
                       'cd c:\kat           - сменить каталог по умолчанию; \n  '
                       'cd "c:\Новая папка" - сменить каталог по умолчанию'],
                'cfile': ['f_create_file',
                          'cfile d:\data 1.txt    - создать файл; \n  '
                          'cfile data 1.txt       - создать файл в каталоге по умолчанию; \n  '
                          'cfile "d:\data 1.txt"  - создать файл с пробелом в имени'],
                'cdir': ['f_create_dir',
                         'cdir d:\Folder     - создать каталог; \n  '
                         'cdir Folder        - создать каталог в каталоге по умолчанию; \n  '
                         'cdir "d:\Folder 2" - создать каталог с пробелом в имени'],
                'copy': ['f_copy',
                          'copy "Каталог 1" "D:\Test\Каталог 2"  - копировать каталог с пробелом в имени; \n  '
                          'copy new.txt "D:\Test\Каталог 2"      - копировать файл из каталога по умолчанию'],
                'move': ['f_move',
                         'move "Каталог 1" "D:\Test\Каталог 2"   - переместить каталог; \n  '
                         'move new.txt "D:\Test\Каталог 2"       - переместить файл из каталога по умолчанию'],
                'del': ['f_del',
                        'del c:\kat      - удалить каталог; \n  '
                        'del c:\doc.txt  - удалить файл; \n  '
                        'del doc.txt     - удалить файл в каталоге по умолчанию']
                }
    # set_tests()     # Тестирование кода
    main()
