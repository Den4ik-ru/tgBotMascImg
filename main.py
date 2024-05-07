import io
import telebot
from PIL import Image

bot = telebot.TeleBot("6895663582:AAFujN7gxg3l6a6nv_TvIyN83mop5VtoKjo")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправьте мне фотографию, которую нужно забрендировать.")

@bot.message_handler(content_types=['photo'])
def brand_photo(message):
    # Загрузка фотографии
    photo_file = bot.get_file(message.photo[-1].file_id)
    downloaded_photo = bot.download_file(photo_file.file_path)
    # Брендирование с помощью наложения логотипа
    image = Image.open(io.BytesIO(downloaded_photo))
    # Загрузка и изменение размера логотипа
    overlay = Image.open("logo.png").convert("RGBA")
    width, height = image.size
    if width == height:
        image = image
    elif width > height:
        left = (width - height) / 2
        top = 0
        right = left + height
        bottom = height
        image = image.crop((left, top, right, bottom))
    else:
        left = 0
        top = (height - width) / 2
        right = width
        bottom = top + width
        image = image.crop((left, top, right, bottom))
    width, height = image.size
    overlay = overlay.resize((width, int(height)))  # Установка высоты логотипа равной половине высоты изображения
    # Получение альфа-канала логотипа в качестве маски
    mask = overlay.split()[-1]
    # Накладываем логотип на изображение
    image.paste(overlay, (0, 0), mask=mask)
    # Сохранение забрендированной фотографии
    branded_photo_name = f"branded_{message.message_id}.jpg"
    image.save(branded_photo_name, "JPEG")
    # Отправка забрендированной фотографии
    bot.send_photo(message.chat.id, open(branded_photo_name, "rb"))

# Запуск бота
bot.polling()
