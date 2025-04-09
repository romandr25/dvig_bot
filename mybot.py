import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

TOKEN = os.environ['TOKEN']
API_URL = os.environ['API_URL']
SECRET_KEY = os.environ['SECRET_KEY']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('Привет! Отправь текст анонса для базы данных.')

async def handle_text(update: Update, context):
    try:
        data = {
            'key': SECRET_KEY,
            'name': 'Новое событие',
            'descr': update.message.text,
            'date': '2025-01-01 19:00:00',
            'metro': '128',
            'cost': '0',
            'tags': '[]'
        }
        response = requests.post(API_URL, data=data)
        await update.message.reply_text(f"✅ Данные отправлены! Ответ: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()