from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from user import user_about
from random_task import choice_task, version_1_1_choice_task
from image import *
import os
API_TOKEN = '8190196884:AAHxx2BINdFFgt5HoJK58mwCovVvsTQUDIU'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum!\n"
        "Men sizga yordam berish uchun tayyorman. Quyidagilarni sinab ko'ring:\n\n"
        "🔹 /user_about <username> - Foydalanuvchi haqida ma'lumot\n"
        "🔹 /random_task <username> <difficult min> <difficult max> - Tasodifiy topshiriq\n\n"
        "Yordam kerak bo'lsa, menga xabar bering! 😊")

@dp.message_handler(commands=["user_about"])
async def user_about_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Iltimos, foydalanuvchi nomini kiriting! Misol: /user_about <username>")
        return
    
    username = args.strip() 
    ans = user_about(username)
    if len(ans) == 1:
        await message.reply(*ans)
        return
    img_url = search_picture_img(username)
    await bot.send_photo(chat_id=message.chat.id, photo=img_url, caption=f"Sizni natijalaringiz:\n🏆 o'rin: {ans[0]}\n📊 Reyting: {ans[1]}\n📊 Max Reyting: {ans[2]}\n🏆 Rating name: {ans[-1]}")

@dp.message_handler(commands=["random_task"])
async def random_task_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Iltimos, foydalanuvchi nomi va qiyinchilik darajasini kiriting! Misol: /random_task <username> <min> <max>")
        return
    
    try:
        parts = args.split()
        username = parts[0]
        diff_mn = int(parts[1])
        diff_mx = int(parts[2])
        if diff_mn < 1 or diff_mx < 1:
            await message.reply('Siz manfiy yoki 0 reytingli masala kiritdingiz!!!')
            return
        if diff_mn > diff_mx:
            await message.reply('Afsuski siz xato kiritdingiz minimal reyting maksimal reytingdan katta boldi!!! Qayta urining!!!')
            return
        
        ans = version_1_1_choice_task(username, diff_mn, diff_mx)
        if len(ans) == 1:
            await message.reply(*ans)
            return
        await message.reply(f'Sizga Random qilganimizda shu masala tushdi -> {ans[1]} <- bu masala {ans[0]} Qiyinchilikda.')
    except (IndexError, ValueError):
        await message.reply("Xatolik! To'g'ri format: /random_task <username> <min> <max>")
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        '/start -> Bu botni tanishtirib beradi.\n/user_about <username> -> Bu sizning profilingiz haqida malumotlarni olib beradi.\n/random_task <username> <min_difficult> <max_difficult> -> Bu sizga aytgan oraliqlaringizdagi masalani random qilib beradi.'
    )
@dp.message_handler()
async def error(message: types.Message):
    await message.answer('Xato buyruq yozdingiz!!! buyruqlarni korishingiz uchun /help buyrugidan foydalaning.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
