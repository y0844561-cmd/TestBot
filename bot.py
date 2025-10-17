import asyncio
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

if not BOT_TOKEN:
    raise ValueError("❌ لم يتم العثور على التوكن في ملف .env")

if not CHANNEL_USERNAME:
    raise ValueError("❌ لم يتم العثور على معرف القناة في ملف .env")

async def like_new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message or update.channel_post
        
        if message and hasattr(message.chat, 'username'):
            chat_username = message.chat.username
            if chat_username and f"@{chat_username}".lower() == CHANNEL_USERNAME.lower():
                
                await context.bot.set_message_reaction(
                    chat_id=message.chat_id,
                    message_id=message.message_id,
                    reaction="❤️"
                )
                print(f"✅ تم وضع لايك على منشور جديد برقم: {message.message_id}")
    except Exception as e:
        print(f"❌ خطأ في وضع اللايك: {e}")

async def post_init(application: Application) -> None:
    print("🚀 البوت يعمل الآن وينتظر المنشورات الجديدة...")
    print(f"📱 القناة المستهدفة: {CHANNEL_USERNAME}")

def main():
    
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

  
    handler = MessageHandler(filters.ALL, like_new_post)
    application.add_handler(handler)


    print("⏳ جارٍ تشغيل البوت...")
    application.run_polling()

if __name__ == "__main__":
    main()
