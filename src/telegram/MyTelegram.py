import telegram
from src.consts.TelegramConst import telegramConst

# 나의 텔레그램
class MyTelegram:
    # 내 텔레그램 봇에 메신저 보내기
    def telegramSend(message):
        token = telegramConst('token')
        chatId = telegramConst('chatId')
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chatId, text=message)
        print('텔레그램에 메시지 전송 완료')

