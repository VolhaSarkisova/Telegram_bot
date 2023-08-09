from aiogram import Bot, Dispatcher, types, executor
import administration
import datetime
from user import User
import os
from dotenv import load_dotenv
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
cafe = administration.Cafe()
text_day: list = ['button_today', 'button_tomorrow', 'button_after_tomorrow']
text_duration: list = ['button_1_hour', 'button_2_hours', 'button_3_hours']
text_hours: list = []
text_tables: list = []

def list_generation(date: datetime) -> None:
    # генерация листа (декартово произведение возможных часов бронирования и всевозможных столов), если записи на указанный день отсутствуют
    exist_date: bool = cafe.select_reserve_by_date_bool(date)
    user.set_date(date)
    if exist_date is False:
        cafe.insert_reserve_by_date(date)

def keyboard_check_days() -> types.InlineKeyboardMarkup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сегодня", callback_data="button_today"))
    keyboard.add(types.InlineKeyboardButton("Завтра", callback_data="button_tomorrow"))
    keyboard.add(types.InlineKeyboardButton("Послезавтра", callback_data="button_after_tomorrow"))
    return keyboard
def keyboard_check_duration() -> types.InlineKeyboardMarkup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1 час", callback_data="button_1_hour"))
    keyboard.add(types.InlineKeyboardButton("2 часа", callback_data="button_2_hours"))
    keyboard.add(types.InlineKeyboardButton("3 часа", callback_data="button_3_hours"))
    return keyboard
def keyboard_check_hour(hours: list) -> types.InlineKeyboardMarkup():
    keyboard = types.InlineKeyboardMarkup()
    for hour in hours:
        name = str(hour[0])+':00'
        button_name = "button_"+str(hour[0])
        text_hours.append(button_name)
        keyboard.add(types.InlineKeyboardButton(name, callback_data=button_name))
    return keyboard
def keyboard_send_admin() -> types.ReplyKeyboardMarkup():
    # , input_field_placeholder = "Введите номер телефона для обратной связи"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Забронировать"))
    return keyboard
def keyboard_send_user() -> types.ReplyKeyboardMarkup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Подтвердить бронь"))
    keyboard.add(types.KeyboardButton("Отменить бронь"))
    return keyboard
def keyboard_check_table(tables: list) -> types.InlineKeyboardMarkup():
    keyboard = types.InlineKeyboardMarkup()
    for table in tables:
        name = str(table[1])+', столик № '+str(table[2])
        button_name = "button_table_"+str(table[0])
        text_tables.append(button_name)
        keyboard.add(types.InlineKeyboardButton(name, callback_data=button_name))
    return keyboard
def keyboard_phone() -> types.ReplyKeyboardMarkup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Отправить свой контакт', request_contact=True))
    return keyboard


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    print(message.chat.id)
    if message.chat.id not in [admin[0] for admin in cafe.select_admins_client_id()]:
        user.set_name(message.from_user.username)
        user.set_client_id(message.chat.id)

        await message.answer(f"Рады приветствовать Вас, {user.get_name()}!\n"
                             f"Предлагаем ознакомиться с планом расстановки наших столов:")
        await bot.send_photo(chat_id=user.get_client_id(),
                             photo="https://potolok-novosibirsk.portal-spectr.ru/attachments/Image/Plan-kafe-natyazhnye-potolki-s-fotopechatyu-ceny.gif?template=generic")
        await message.answer(
            "Укажите желаемую дату и время, а мы подскажем Вам, какие столики доступны к бронированию.\n"
            "Итак, желаемая дата:", reply_markup=keyboard_check_days())
    else:
        await message.answer(
            f"Рады приветствовать Вас, {message.from_user.username}! Дожидайтесь запроса на подтверждение бронирования.\n")


@dp.callback_query_handler(text = text_day)
async def today_handler(callback: types.CallbackQuery):
    day = callback.data[7:]
    match day:
        case 'today':
            list_generation(datetime.date.today())
        case 'tomorrow':
            list_generation(datetime.date.today()+datetime.timedelta(days=1))
        case 'after_tomorrow':
            list_generation(datetime.date.today()+datetime.timedelta(days=2))

    await bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"*{user.get_date()}*",
                           reply_markup=None, parse_mode='Markdown')

    await bot.send_message(chat_id=user.get_client_id(),
                           text="Продолжительность бронирования:",
                           reply_markup=keyboard_check_duration())

@dp.callback_query_handler(text = text_duration)
async def button_hour_handler(callback: types.CallbackQuery):
    print(callback.data)
    hour: str = callback.data[7:8]
    print(hour)
    match hour:
        case '1':
            user.set_duration(1)
        case '2':
            user.set_duration(2)
        case '3':
            user.set_duration(3)

    await bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"*{user.get_duration()} ч.*",
                           reply_markup=None, parse_mode='Markdown')

    hours = cafe.select_unreserved_hours_by_date(user.get_date(), datetime.datetime.now().hour, user.get_duration())
    await bot.send_message(chat_id=user.get_client_id(),
                           text="Удобное для Вас время:",
                           reply_markup=keyboard_check_hour(hours))

@dp.callback_query_handler(text = text_hours)
async def button_8_handler(callback: types.CallbackQuery):
    hh: str = callback.data[-2:]
    print(hh)
    user.set_hour(int(hh.replace('_', '')))
    await bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"*{user.get_hour()}:00 ч.*",
                           reply_markup=None, parse_mode='Markdown')
    tables = cafe.select_unreserved_tables_by_date_duration_hour(user.get_date(), int(user.get_hour()), int(user.get_duration()))
    await bot.send_message(chat_id=user.get_client_id(),
                           text="Ваш выбор столика (из доступных к бронированию):",
                           reply_markup=keyboard_check_table(tables))

@dp.callback_query_handler(text = text_tables)
async def button_table_1_handler(callback: types.CallbackQuery):
    table: str = callback.data[-2:]
    user.set_id_table(int(table.replace('_', '')))
    await bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"*столик № {cafe.select_table_by_id(user.get_id_table())[1]} ({cafe.select_table_by_id(int(user.get_id_table()))[0]})*",
                           reply_markup=None, parse_mode='Markdown')
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"Нажмите кнопку 'Отправить свой контакт' для возможности обратной связи",
                           reply_markup=keyboard_phone())
    # keyboard_send_admin())

@dp.message_handler(content_types=['contact'])
async def handle_contact(message):
    user.set_phone(message.contact.phone_number)
    await bot.send_message(chat_id=user.get_client_id(),
                           text=f"{user.get_name()}, вы желаете забронировать столик № {cafe.select_table_by_id(user.get_id_table())[1]} ({cafe.select_table_by_id(int(user.get_id_table()))[0]}) {user.get_date()} с {user.get_hour()}:00  на {user.get_duration()}ч.\nЧтобы забронировать столик нажмите кнопку 'Забронировать'. Дожидайтесь ответа от администратора в чате. Спасибо, что с нами!",
                           reply_markup=keyboard_send_admin())

@dp.message_handler(lambda message: message.text=="Забронировать")
async def button_send_admin(callback: types.CallbackQuery):
    hour = user.get_hour()
    for dur in range(int(user.get_duration())):
        cafe.update_reserve_client_by_id_table_date_hour(user.get_date(), user.get_id_table(), hour, user.get_name()+' '+user.get_phone(), user.get_client_id(), 1)
        hour += 1

    for admin in cafe.select_admins_client_id():
        print(admin[0])
        await bot.send_message(chat_id=admin[0],
                               text=f"Подтвердите, пожалуйста, бронирование столика № {cafe.select_table_by_id(user.get_id_table())[1]} ({cafe.select_table_by_id(int(user.get_id_table()))[0]}) {user.get_date()} с {user.get_hour()}:00  на {user.get_duration()} ч.",
                               reply_markup=keyboard_send_user())

@dp.message_handler(lambda message: message.text)
async def button_send_user(message: types.CallbackQuery):
    hour = user.get_hour()
    message_text = ""
    reserved = 1
    match message.text:
        case 'Подтвердить бронь':
            reserved = 2
            message_text = f"Бронирование столика {cafe.select_table_by_id(user.get_id_table())[1]} ({cafe.select_table_by_id(int(user.get_id_table()))[0]}) {user.get_date()} с {user.get_hour()}:00  на {user.get_duration()} ч. подтверждено администратором {cafe.select_admins_username_by_client_id(message.from_user.id)[0]}! Ждем Вас!"
        case 'Отменить бронь':
            reserved = 0
            message_text = f"К сожалению, администратор {cafe.select_admins_username_by_client_id(message.from_user.id)[0]} отменил бронирование столика {cafe.select_table_by_id(user.get_id_table())[1]} ({cafe.select_table_by_id(int(user.get_id_table()))[0]}) {user.get_date()} с {user.get_hour()}:00  на {user.get_duration()} ч. "

    for dur in range(int(user.get_duration())):
        cafe.update_reserve_client_by_id_table_date_hour(user.get_date(), user.get_id_table(), hour, user.get_name()+' '+user.get_phone(),
                                                         user.get_client_id(), reserved)
        hour += 1
    await bot.send_message(chat_id=user.get_client_id(),
                           text=message_text,
                           reply_markup=types.ReplyKeyboardRemove())

    for admin in cafe.select_admins_client_id():
        if message.from_user.id == admin[0] and user.get_client_id() != admin[0]:
            await bot.send_message(chat_id=admin[0],
                                   text=message_text,
                                   reply_markup=types.ReplyKeyboardRemove())



if __name__ == "__main__":
    user = User()
    executor.start_polling(dp, skip_updates=True)
