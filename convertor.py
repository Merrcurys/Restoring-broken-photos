import asyncio
from tkinter import filedialog, Tk
from PIL import Image
import exifread
import io
import os

# Функция для обработки одного файла
async def process_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
        # Проверяем есть ли превью
        if 'JPEGThumbnail' in tags.keys():
            thumbnail_data = tags['JPEGThumbnail'] # Вытаскиваем не побитое превью
            thumbnail_img = Image.open(io.BytesIO(thumbnail_data))
            
            # Получаем базовое имя файла без расширения
            base_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(base_name)[0]
            
            # Используем абсолютный путь к корневой директории проекта для сохранения превью
            project_root = os.getcwd()  # Получаем путь к текущей рабочей директории
            thumbnail_dir = os.path.join(project_root, "thumbnails")
            thumbnail_path = os.path.join(thumbnail_dir, file_name_without_ext + ".jpg")
            
            # Создаем директорию для превью, если она еще не существует
            os.makedirs(thumbnail_dir, exist_ok=True)

            # Вытаскиваем старые метатеги
            image = Image.open(file_path)
            exif = image.info.get('exif')
            # Сохраняем превью
            if exif is None:
                thumbnail_img.save(thumbnail_path)
                print("Метатеги не были найдены у оригинальной фотографии.")
            else:
                thumbnail_img.save(thumbnail_path, exif=exif)
            
            print(f"Превью успешно сохранено по пути: {thumbnail_path}")
        else:
            print("Превью не найдено в изображении.")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Асинхронная функция для выбора и обработки нескольких файлов
async def extract_embedded_thumbnails():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Выберите изображения", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico")])
    
    if file_paths:
        await asyncio.gather(*(process_file(path) for path in file_paths))
    else:
        print("Файлы не выбраны.")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(extract_embedded_thumbnails())
