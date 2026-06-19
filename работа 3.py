import telebot
import time
import threading
bot = telebot.TeleBot(token='токен')
dailywater = 2000
userdrank = {}
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 'Привет, это бот для сохранения водного баланса!\n\n'
                 'Бот будет напоминать пить воду\n'
                 'чтобы настроить время напоминания, например каждый час, используй: /setreminder 1\n'
                 'также ты должен отвечать сколько воды выпил\n'
                 'Например если выпил 300мл пишешь так: /drank 300\n'
                 'чтобы увидеть сколько еще нужно выпить в течении дня, напиши: /status\n'
                 'Если хочешь увидеть это сообщение снова, напиши: /start или /help')
def reminder_timer(chat_id, seconds):
    time.sleep(seconds)
    bot.send_message(chat_id, 'Пора пить воду!')
@bot.message_handler(commands=['setreminder'])
def setreminder(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, 'Пример: /setreminder 1')
        return
    try:
        reminder = float(parts[1].strip().replace(',', '.'))
        seconds = reminder * 3600
        threading.Thread(target=reminder_timer, args=(message.chat.id, seconds), daemon=True).start()
        bot.reply_to(message, f'Напоминание установлено на через {reminder} ч.')
    except ValueError:
        bot.reply_to(message, 'Введите правильно пожалуйста')
@bot.message_handler(commands=['drank'])
def drank(message):
    chat_id = message.chat.id
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, 'Пример: /drank 300')
        return
    try:
        drink = int(parts[1])
        if drink <= 0:
            bot.reply_to(message, 'Количество мл должно быть выше нуля')
            return
        if chat_id not in userdrank:
            userdrank[chat_id] = 0
        userdrank[chat_id] += drink
        current_drank = userdrank[chat_id]
        bot.reply_to(message, f"Успешно записано {drink} мл.\nВсего выпито: {current_drank} из {dailywater} мл.")
        if current_drank >= dailywater:
            bot.send_message(chat_id, "Вы выполнили дневную норму воды!")
    except ValueError:
        bot.reply_to(message, 'Введите правильно количество миллилитров (только числа).')
@bot.message_handler(commands=['status'])
def status(message):
    chat_id = message.chat.id
    if chat_id not in userdrank:
        userdrank[chat_id] = 0
    current_drank = userdrank[chat_id]
    left_water = dailywater - current_drank
    if left_water > 0:
        bot.reply_to(message, f"Ваш статус:\nВыпито: {current_drank} мл.\nОсталось выпить: {left_water} мл.")
    else:
        bot.reply_to(message,
                     f"Ваш статус:\nВыпито: {current_drank} мл.\nНорма {dailywater} мл выполнена!")
bot.infinity_polling()