import asyncio
import aioschedule
import googletrans

from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, start_times, l
from logging import basicConfig, INFO
from parser import update_excels
from re import match
from wwExcel import para_info
from wwSQL import SQL


basicConfig(level=INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = SQL('db.db')

translator = googletrans.Translator()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, message.from_user.first_name, False)
        language = 'ru'
    else:
        language = (db.get_subscriber_language(message.from_user.id))[0][0]
    m = translator.translate("Привет", src='ru', dest=language).text + ", " + message.from_user.first_name + "!\n"
    m += translator.translate("Я бот, который будет напоминать тебе о занятиях", src='ru', dest=language).text + "\n"
    m += translator.translate("Вот основные команды", src='ru', dest=language).text + ":\n"
    m += "/language - " + translator.translate("указать язык", src='ru', dest=language).text + ":\n"
    m += "/subscribe - " + translator.translate("подключить рассылку", src='ru', dest=language).text + "\n"
    m += "/group - " + translator.translate("указать номер группы", src='ru', dest=language).text + "\n"
    m += "/unsubscribe - " + translator.translate("отключить рассылку", src='ru', dest=language).text + "\n"
    m += "/info - " + translator.translate("информация о разработчике", src='ru', dest=language).text + "\n"
    await message.answer(m)



@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    language = (db.get_subscriber_language(message.from_user.id))[0][0]
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, message.from_user.first_name)
        await message.answer(translator.translate("Рассылка подключена. Не забывайте ботать!",
                                                  src='ru', dest=language).text)
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer(translator.translate("Рассылка подключена", src='ru', dest=language).text)


@dp.message_handler(commands=['group'])
async def group_is(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        language = 'ru'
    else:
        language = (db.get_subscriber_language(message.from_user.id))[0][0]
    text = message.text.split()
    if len(text) == 2:
        group = text[1]
        if match(r"[БСМ]\d{2}-\d{3}", group) and len(group) == 7:
            if not db.subscriber_exists(message.from_user.id):
                db.add_subscriber(message.from_user.id, message.from_user.first_name, False)
                db.set_group(message.from_user.id, group)
                await message.answer(translator.translate("Вы ещё не подключили рассылку, но я запомнил, что Ваша группа",
                                                          src='ru', dest=language).text + " - " + group + "!")
            else:
                db.set_group(message.from_user.id, group)
                await message.answer(translator.translate("Я запомнил, Ваша группа - " + group + "!",
                                                          src='ru', dest=language).text)
        else:
            await message.answer(translator.translate("Произошла ошибка, номер группы указан не верно!",
                                                      src='ru', dest=language).text)
    else:
        await message.answer(translator.translate("Произошла ошибка, укажите номер группы!",
                                                  src='ru', dest=language).text)



@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        language = 'ru'
    else:
        language = (db.get_subscriber_language(message.from_user.id))[0][0]
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer(translator.translate("Вы ещё не подключили рассылку!", src='ru', dest=language).text)
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer(translator.translate("Рассылка отключена", src='ru', dest=language).text)



@dp.message_handler(commands=['update'])
async def update_timetables(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        language = 'ru'
    else:
        language = (db.get_subscriber_language(message.from_user.id))[0][0]
    language = (db.get_subscriber_language(message.from_user.id))[0][0]
    update_excels()
    await message.answer(translator.translate("Расписание обновлено", src='ru', dest=language).text)


@dp.message_handler(commands=['info'])
async def update_g(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        language = 'ru'
    else:
        language = (db.get_subscriber_language(message.from_user.id))[0][0]
    m = translator.translate("Привет, я - бот с расписанием", src='ru', dest=language).text
    m += ", " + translator.translate("меня написал студент первого курса ФПМИ", src='ru', dest=language).text + ", "
    name = translator.translate("Могилёв Георгий", src='ru', dest=language).text
    m += '[{}](https://vk.com/10gilyov)'.format(name)
    await message.answer(m, parse_mode='Markdown')


@dp.message_handler(commands=['language'])
async def language_is(message: types.Message):
    text = message.text.split()
    if not db.subscriber_exists(message.from_user.id):
        l0 = 'ru'
    else:
        l0 = (db.get_subscriber_language(message.from_user.id))[0][0]
    if len(text) == 2:
        language = text[1]
        if language in l.keys():
            language_tag = l[language]
            if not db.subscriber_exists(message.from_user.id):
                db.add_subscriber(message.from_user.id, False)
                db.set_language(message.from_user.id, language_tag)
                await message.answer(
                    translator.translate("Вы ещё не подключили рассылку, но я запомнил Ваш язык",
                                         src='ru', dest=l[language]).text + " - " + language + "!")
            else:
                db.set_language(message.from_user.id, language_tag)
                await message.answer(
                    translator.translate("Я запомнил, Ваш язык",
                                         src='ru', dest=l[language]).text + " - " + language + "!")
        else:
            await message.answer(translator.translate("Произошла ошибка, я не знаю этого языка!",
                                                      src='ru', dest=l0).text)
    else:
        await message.answer(translator.translate("Произошла ошибка, укажите язык!", src='ru', dest=l0).text)


async def as_excel_update():
    update_excels()



async def send_para_info(para_number):
    subscriptions = db.get_subscriptions()
    for s in subscriptions:
        # проверяем чтобы группа была указана
        if s[3] is not None:
            language = s[5]
            a = para_info(s[3], start_times[1][para_number-1])
            # проверяем чтобы группа была указана верно
            if a[0] == "bad":
                await bot.send_message(s[1], translator.translate("Я не нашёл Вашу группу!",
                                                                  src='ru', dest=l[language]).text)
            # проверяем, это две одинаковые пары подряд? если да, то затираем её
            if para_number > 1:
                b = para_info(s[3], start_times[1][para_number-2])
                if a[0] == b[0]:
                    a[0] = ""
            # проверяем, есть пара, или окно?
            if len(a) >= 1 and a[0] != "":
                m = s[4] + ", " + translator.translate("у тебя начнется пара в",
                                                       src='ru', dest=l[language]).text
                m += start_times[0][para_number - 1] + "\n\n" + translator.translate(a[0],
                                                                                     src='ru', dest=l[language]).text
                # проверяем дополнительную информацию о паре
                if len(a) > 1:
                    m += " (" + translator.translate(a[1], src='ru', dest=l[language]).text
                    # проверяем дополнительную информацию о паре
                    if len(a) > 2:
                        m += " " + translator.translate(a[2], src='ru', dest=l[language]).text
                    m += ")"
                await bot.send_message(s[1], m)


async def first_para():
    await send_para_info(1)


async def second_para():
    await send_para_info(2)


async def third_para():
    await send_para_info(3)


async def fourth_para():
    await send_para_info(4)


async def fifth_para():
    await send_para_info(5)


async def sixth_para():
    await send_para_info(6)


async def seventh_para():
    await send_para_info(7)


async def scheduler():
    aioschedule.every().day.at("8:00").do(as_excel_update)

    aioschedule.every().day.at("08:45").do(first_para)
    aioschedule.every().day.at("10:30").do(second_para)
    aioschedule.every().day.at("12:05").do(third_para)
    aioschedule.every().day.at("13:40").do(fourth_para)
    aioschedule.every().day.at("15:15").do(fifth_para)
    aioschedule.every().day.at("16:55").do(sixth_para)
    aioschedule.every().day.at("18:25").do(seventh_para)


    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
