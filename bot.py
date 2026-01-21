import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import google.generativeai as genai

# هذي الطريقة تقرأ المعلومات من إعدادات Render مباشرة للأمان
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY_GEMINI = os.getenv('API_KEY_GEMINI')
CH_ID = '@IQ_GB'

# إعداد الذكاء الاصطناعي
genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CH_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    await m.reply(f"هلو عيني {m.from_user.first_name}! 😍\nأني بوت حل الواجبات الذكي. دزيلي أي سؤال وأحله إلج بثواني.")

@dp.message_handler()
async def solve(m: types.Message):
    if await check_sub(m.from_user.id):
        wait = await m.answer("جاري التفكير بالحل... ⏳")
        try:
            prompt = f"حل هذا السؤال بدقة وباللغة العربية مع شرح بسيط: {m.text}"
            res = model.generate_content(prompt)
            await bot.edit_message_text(f"✅ الحل هو:\n\n{res.text}", m.chat.id, wait.message_id)
        except Exception as e:
            await bot.edit_message_text("عذراً، صار ضغط على عقل البوت. حاولي مرة ثانية.", m.chat.id, wait.message_id)
    else:
        await m.answer(f"⚠️ حبيبتي، البوت مخصص لمشتركي قناتنا فقط. اشتركي وتعالي:\n{CH_ID}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
