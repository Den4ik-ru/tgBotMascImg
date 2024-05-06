import io
import telebot
from PIL import Image, ImageDraw, ImageFont

# Токен Telegram-бота
bot = telebot.TeleBot("key")
# Обработка команд
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

    # Добавление полупрозрачного изображения
    overlay = Image.open("logo.png").convert("RGBA")
    mask = Image.new("L", overlay.size, 128)
    image.paste(overlay, (image.width - overlay.width, image.height - overlay.height), mask=mask)
    # image.paste(overlay, (0, 0), mask=mask)

    # Сохранение забрендированной фотографии
    branded_photo_name = f"branded_{message.message_id}.jpg"
    image.save(branded_photo_name, "JPEG")

    # Отправка забрендированной фотографии
    bot.send_photo(message.chat.id, open(branded_photo_name, "rb"))

# Запуск бота
bot.polling()
