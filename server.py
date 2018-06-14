from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import File, ReplyKeyboardMarkup
from requests import get, post
import math
import api
import json
import os
from skimage import io
from telegram.ext.dispatcher import run_async

@run_async
def handle_text(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Пришли мне фото, и я скажу, на какого футболиста сборной РФ ты похож.")


@run_async
def handle_photo(bot, update):
    try:
        new_file = bot.getFile(update.message['photo'][1]['file_id'])
        new_file.download(os.path.join('archive', 'img{0}_1.png'.format(str(update.message.chat_id))))
        img = io.imread(os.path.join('archive', 'img{0}_1.png'.format(str(update.message.chat_id))))
        img = img[:, :, :3].copy()
        char = api.detect(img)[0]

        bot.sendMessage(chat_id=update.message.chat_id, text='Футболист - {0}\nСборная - {1}\nТочность - {2}'.format(char['name'].split('.')[0], char['country'], char['mn']))
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open(os.path.join(os.path.join('teams', char['country']), '_'.join(char['name'].split(" "))), 'rb'))
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id=update.message.chat_id, text="Произошла ошибка. Убедитесь, что на фотографии лицо видно четко.")


@run_async
def handle_command(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Пришли мне фото, и я скажу, на какого футболиста сборной РФ ты похож.")



#def main():
api.load_data()
updater = Updater(token='575308485:AAHO2daTi9bwAcfZu2_mqcoM0I7unud0uXw')
text_handler = MessageHandler(Filters.text, handle_text)
command_handler = MessageHandler(Filters.command, handle_command)
photo_handle = MessageHandler(Filters.photo, handle_photo)
updater.dispatcher.add_handler(text_handler)
updater.dispatcher.add_handler(photo_handle)
updater.dispatcher.add_handler(command_handler)
updater.start_polling()


# if __name__ == '__main__':
#     main()