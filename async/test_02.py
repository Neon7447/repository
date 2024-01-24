import shutil

source_path = 'путь_к_исходному_файлу/имя_исходного_файла'  # Укажите путь и имя исходного файла
destination_path = 'путь_к_целевому_каталогу/имя_целевого_файла'  # Укажите путь и имя для целевого файла

try:
    shutil.move(source_path, destination_path)
    print("Файл успешно перемещен.")
except FileNotFoundError:
    print("Файл не найден.")
except PermissionError:
    print("Не удалось переместить файл из-за отсутствия разрешений.")
except Exception as e:
    print("Произошла ошибка при перемещении файла:", str(e))