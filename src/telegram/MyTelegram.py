import telegram
from src.consts.TelegramConst import telegramConst

class MyTelegram:

    def telegramSend(message):
        token = telegramConst('token')
        chatId = telegramConst('chatId')
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chatId, text=message)
        print('텔레그램에 메시지 전송 완료')

