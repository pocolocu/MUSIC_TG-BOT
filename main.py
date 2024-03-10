import os
import telebot
from pytube import YouTube
from pytube import Search
from telebot import types

# Токен бота
TOKEN = '7161955117:AAGcVD4j1Z3aJrIEhs5IMWE782fS6SVA-Fg'
bot = telebot.TeleBot(TOKEN)

def search_youtube(query):
    try:
        # Используем pytube для поиска видео
        search = Search(query)
        # Возвращаем первое видео из результатов поиска
        return search.results[0]
    except Exception as e:
        print(e)
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может скачивать и конвертировать музыку из YouTube. Просто отправь мне название песни.")

@bot.message_handler(func=lambda message: message.text.startswith('@'))
def handle_music_request(message):
    try:
        # Парсим запрос на название песни
        song_name = message.text.split(' ', 1)[1]
        # Используем pytube для поиска видео
        video = search_youtube(song_name)

        if video:
            audio = video.streams.filter(only_audio=True).first()
            audio_file = audio.download(output_path=".")
            base, ext = os.path.splitext(audio_file)
            new_file = base + '.mp3'
            os.rename(audio_file, new_file)

            with open(new_file, 'rb') as f:
                bot.send_audio(message.chat.id, f)
            # Удаляем файл после отправки
            os.remove(new_file)
        else:
            bot.reply_to(message, "Произошла ошибка при поиске музыки.")

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке вашего запроса.")
        print(e)

if __name__ == '__main__':
    bot.polling()