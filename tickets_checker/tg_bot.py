import telebot

from os import environ
# from dotenv import load_dotenv


class TelegramBot:
    # load_dotenv()
    # token = environ.get("BOT_TOKEN")
    token = '6951917529:AAE1RnQuvJ6jR8hLiZyha0tf7VryKnSuxX4'
    chat_id = '-4160374340'

    bot = telebot.TeleBot(token)

    def notify_admin_folder_ready(self, folder, download_url):
        message = f'Папка {folder} доступна для скачивания по ссылке: {download_url}'
        self.bot.send_message(self.chat_id, message)

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)