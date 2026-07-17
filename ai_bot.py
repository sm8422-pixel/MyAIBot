import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from openai import OpenAI

# إعدادات التوكن
TELEGRAM_TOKEN = "8804597208:AAF97O9BLyhVyL5AzAvOzdZrRtthOwBJpsQ"

# إعداد الذكاء الاصطناعي
client = OpenAI(api_key="ضع_مفتاح_OpenAI_هنا_إذا_كنت_تستخدم_سيرفر_خارجي")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أنا بوت الدردشة الذكي الخاص بك 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومرح في بوت تلجرام. رد باللغة العربية."},
                {"role": "user", "content": user_message}
            ]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text("عذراً، واجهت مشكلة. حاول مرة أخرى!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    application.run_polling()
