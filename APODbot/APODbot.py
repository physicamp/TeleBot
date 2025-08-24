import telebot
from telebot import apihelper
apihelper.proxy = {'https':'socks5h://127.0.0.1:1080'}
import requests
bot = telebot.TeleBot("8172840033:AAEco7T3K0rNs-b3uYKoFWurYXvZXngEbE0",parse_mode=None)
#CHANNEL_ID = "@apodtestt"
#APOD API
NASA_API_KEY = "4SqVVdy28cXIfULcZyhZSycdn31AmfS3oheBoq2Y"
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

def get_apod():
    params = {"api_key": NASA_API_KEY}
    response = requests.get(NASA_APOD_URL, params=params)
    data = response.json()
    exp = data["explanation"] #for telegram caption limt
    exp = exp[:500] +"..."+"\n\n"+"https://apod.nasa.gov/apod/astropix.html"  # for telegram caption limit and nasa link
    
    return data["url"], data["title"],exp


def openrai(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "Explain it more  with more scientefic in persian"},
            {"role": "user", "content":str(text) }
        ]
        ,"max_tokens": 2000
    }
    response = requests.post(url, headers=headers, json=data)
    return(response.json()["choices"][0]["message"]["content"])


#Start bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! برای دریافت عکس روز ناسا دستور /apod رو بفرست 🚀")
#show photo and its caption

@bot.message_handler(commands=['apod'])
def send_apod(message):
   # print(message.chat.id)
    #print('@',message.from_user.username)
    #print(message.from_user.first_name)
    url, title, explanation = get_apod()
    ai_exp = openrai(explanation)
    bot.send_photo(message.chat.id, photo=url, caption=f"{title}\n\n{explanation}")
    bot.send_message(message.chat.id,text=ai_exp)

print("BOT STARTED")
bot.infinity_polling()