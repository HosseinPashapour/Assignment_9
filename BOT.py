
import random
import telebot
from telebot import types
from khayyam import JalaliDate
import gtts
import qrcode


bot_keyboard = types.ReplyKeyboardMarkup(row_width=3)
key1 = types.KeyboardButton('/start')
key2 = types.KeyboardButton('/game')
key3 = types.KeyboardButton('/help')
key4 = types.KeyboardButton('/age')
key5 = types.KeyboardButton('/voice')
key6 = types.KeyboardButton('/max')
key7 = types.KeyboardButton('/argmax')
key8 = types.KeyboardButton('/qrcode')
bot_keyboard.add(key1, key2, key3, key4, key5, key6, key7, key8)


def create_game_keyboard():
    game_keyboard = types.ReplyKeyboardMarkup(row_width=1)
    new_game_key = types.KeyboardButton('/New_game')
    exit_key = types.KeyboardButton('/Exit')
    game_keyboard.add(new_game_key, exit_key)
    return game_keyboard


bot=telebot.TeleBot("7053797766:AAENOwx4R5TnhWzi4DQIwLWbtNTg7zqnzvM",parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global flag
    flag="start"
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    bot.reply_to(message,"👋 سلام "+str(first_name+" "+last_name)+"  به بات من خوش اومدی 😍",reply_markup=bot_keyboard)


@bot.message_handler(commands=['game'])
def game(message):
    global flag
    global win
    flag="game"
    win=False
    global game_number
    game_number = random.randint(1, 100)
    bot.send_message(message.chat.id, "من یک عدد بین 1 تا 100 انتخاب کردم حدس بزن عدد من چیه🤭", reply_markup=create_game_keyboard())

@bot.message_handler(func=lambda message: message.text == '/Newgame')
def new_game(message):
    global flag
    global win
    flag="game"
    win=False
    global game_number
    game_number = random.randint(1, 100)
    bot.send_message(message.chat.id, " من به یک عدد بین 1 تا 100 فکر میکنم حدس بزن عدد من چیه", reply_markup=create_game_keyboard())

@bot.message_handler(func=lambda message: message.text == '/Exit')
def exit_game(message):
    global game_number
    game_number = None
    global win
    win=False
    bot.send_message(message.chat.id, "🫤بازی کنسل شد ", reply_markup=bot_keyboard)

@bot.message_handler(commands=['age'])
def calculate_age(message):
    global flag
    flag="age"
    bot.send_message(message.chat.id, "تاریخ تولد سال شمسی خود را مثلا به صورت 1379/04/08 وارد کنید", reply_markup=bot_keyboard)


    
@bot.message_handler(commands=['voice'])
def send_voice(message):
    global flag
    flag="voice"
    bot.send_message(message.chat.id, " متن خود را برای تبدیل به صدا وارد کنید")
    bot.send_message ( message.chat.id , " متن باید به زبان انگلیسی باشد " , reply_markup = bot_keyboard )



@bot.message_handler(commands=['max'])
def find_max(message):
    global flag
    flag="max"
    bot.send_message(message.chat.id, "آرایه اعداد را وارد کنید تا بزرگترین آن را پیدا کنم")
    bot.send_message(message.chat.id, "لطفا برای جدا کردن اعداد از , استفاده کنید")



@bot.message_handler(commands=['argmax'])
def find_argmax(message):
    global flag
    flag="argmax"
    bot.send_message(message.chat.id, "آرایه اعداد را وارد کنید تا بزرگترین اندیس  آن ها را پیدا کنم")
    bot.send_message(message.chat.id, "لطفا برای جدا کردن اعداد از , استفاده کنید")



@bot.message_handler(commands=['qrcode'])
def generate_qrcode(message):
    global flag
    flag="qrcode"
    bot.send_message(message.chat.id, "لطفا رشته مورد نظر خود را وارد کنید")


@bot.message_handler(commands=['help'])
def display_help(message):
    send_help_message(message)  



@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    if flag=="game":
        global game_number
        global win
        win=False
        count=1
        try:
            if count<=10 and win==False:
                guess = int(message.text)
                if guess < game_number:
                    bot.reply_to(message, "برو بالاتر ☝")
                elif guess > game_number:
                    bot.reply_to(message, "بیا پایین تر 👇")
                else:
                    bot.reply_to(message, " 🥳 آفرین به تو 🎉 برنده  شدی 🎉 ")
        except ValueError:
            bot.reply_to(message, "🫨 این بازی حدس عدداست، باید عدد وارد کنی  😠 ")
            
    
    elif flag=="age":
        try:
            birthday = (message.text)
            birth_year, birth_month, birth_day = map(int, birthday.split('/'))

            today = JalaliDate.today()
        
            age = today.year - birth_year - 1 if (today.month, today.day) < (birth_month, birth_day) else today.year - birth_year
            month = today.month - birth_month if today.month >= birth_month else 12 - birth_month + today.month
            day = today.day - birth_day if today.day >= birth_day else JalaliDate(today.year, today.month - 1, today.day).days_in_month - birth_day + today.day
            
            bot.send_message(message.chat.id,f"سن شما برابر {age} سال و {month} ماه و {day} روز است" )

        except ValueError:
            bot.send_message(message.chat.id,"❌ لطفاً تاریخ تولد را به درستی وارد کنید")

    elif flag=="voice":
        text = (message.text) 
        x = gtts.gTTS(text, lang="en", slow=False)
        x.save("output.mp3") 
            
        audio_file = open("output.mp3", "rb")
        bot.send_voice(message.chat.id, audio_file)
        audio_file.close()
    
    elif flag=="max":      
        text = (message.text) 
        numbers = text.split(',')
        numbers = [int(num.strip()) for num in numbers]
        max_value = max(numbers)
        bot.send_message(message.chat.id, f"بزرگترین عدد: {max_value}")
 
    elif flag=="argmax":
        text=(message.text)
        numbers = text.split(',')
        numbers = [int(num.strip()) for num in numbers]
        max_index = numbers.index(max(numbers))
        bot.send_message(message.chat.id, f"اندیس بزرگترین عدد: {max_index}")
    
    elif flag=="qrcode":
        text=(message.text)
        img_QR = qrcode.make(text)
        img_QR.save("YouQrCode.png")

        qr_file=open("YouQrCode.png","rb")
        bot.send_photo(message.chat.id, qr_file)     
 
    else:
        ...


def send_help_message(message):
    help_text = '''لیست دستورات:
    /start - شروع کار با بات
    /game - بازی حدس عدد
    /age - محاسبه سن شمسی
    /voice - ارسال پیام به صورت صوتی
    /max - یافتن بزرگترین عدد در آرایه
    /argmax - یافتن اندیس بزرگترین عدد در آرایه
    /qrcode - تولید کد QR از یک رشته
    /help - نمایش این راهنما'''

    bot.send_message(message.chat.id, help_text)

bot.infinity_polling()

