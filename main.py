import asyncio
import logging
import os
import sys
from dataclasses import dataclass

from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from edu import selection2
from уваа import selection2
from dbase import new_human, count_person, del_person

person = {}

@dataclass
class Person:
    status: int = 0
    name: str = None
    phone_number: str = None
    city: str = None
    tg_user: str = None
    type_pet: str = None
    name_pet: str = None
    sex_pet: int = 0
    breed_pet: str = None
    describe: str = None
    photo: str = None


TOKEN = ""
dp = Dispatcher()


class FormState(StatesGroup):
    status = State()
    name = State()
    phone_number = State()
    city = State()
    type_pet = State()
    name_pet = State()
    sex_pet = State()
    breed_pet = State()
    describe = State()


@dp.message(CommandStart())
async def start_command_handler(message: types.Message):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(types.InlineKeyboardButton(text="Владелец", callback_data="owner"))
    keyboard_builder.add(types.InlineKeyboardButton(text="Нашедший", callback_data="finder"))
    await message.answer('Привет! Мне жаль, что вам пришлось обратиться ко мне, но я помогу решить вашу проблему. Для начала заполним анкету, пожалуйста отвечайте на вопросы без лишней информации и прямо, чтобы мне было легче помочь вам, если вы не знаете, что ответить, то пишите "не знаю". Если остались вопросы по заполнению - /info')
    if message.chat.id in person:
        if count_person(person[message.chat.id].status) != 0:
            matches = selection2(person[message.chat.id])
            if not matches:
                await message.answer(
                    'Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, попробуйте обратиться попозже')
            else:
                await message.answer(f'Я нашел {len(matches)} подходящих анкет:')
                for match in matches:
                    await message.answer_photo(
                        types.FSInputFile(match.pet_photo),
                        caption=f'Имя: {match.name}\nНомер телефона: {match.phone_number}\nТелеграм: {match.tg_user}\nГород: {match.city}\nЖивотное: {match.type_pet}\nКличка: {match.name_pet}\nОписание: {match.decribe}'
                    )
                await message.answer(
                    'Надеюсь я смог вам помочь! Если вы смогли вернуть питомца домой, то удалите свое объявление /del. Если же нет, то попробуйте чуть-чуть попозже, вдруг человек еще не выложил объявление!')
        else:
            await message.answer(
                'Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, попробуйте обратиться попозже')
    else:
        person[message.chat.id] = Person(tg_user=message.from_user.username)
        await message.answer("Итак, вы владелец или нашедший?", reply_markup=keyboard_builder.as_markup(), )


@dp.callback_query(lambda c: c.data in ["owner", "finder"])
async def process_status_selection(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "owner":
        person[callback.message.chat.id] = Person(status=0)
    elif callback.data == "finder":
        person[callback.message.chat.id] = Person(status=1)
    await callback.message.answer("Как вас зовут?")
    await state.set_state(FormState.name)
    await callback.answer()


@dp.message(Command("info"))
async def info_command_handler(message: types.Message):
    await message.answer(f'Пример ожидаемых ответов:\nСтатус: Владелец\nИмя и фамилия: Иванов Артем\nНомер телефона:89324445555\nГород:Сургут\nЖивотное: Собака\nИмя питомца: Дружок\nПол: Мужской\nПорода: Овчарка\nОписание: 3 декабря убежал со двора, не агрессивный и пугливый. Белые лапки и грудка, довольно крупный. Был в ошейнике')


@dp.message(Command("del"))
async def delete_command_handler(message: types.Message):
    if message.chat.id in person:
        del_person(person[message.chat.id], message.chat.id)
        await message.answer('Отлично, ваше объявление удалено!')
    else:
        await message.answer('Сначала заполните анкету!')


@dp.message(FormState.name)
async def process_full_name(message: types.Message, state: FSMContext):
    if message.text:
        person[message.chat.id].name = message.text.lower()
    await state.set_state(FormState.phone_number)
    await message.answer('Теперь введите ваш актуальный номер телефона:')


@dp.message(FormState.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    if len(message.text) == 11:
        person[message.chat.id].phone_number = message.text.lower()
        await state.set_state(FormState.city)
        await message.answer('В каком вы городе?')
    else:
        await message.answer('Некорректный номер, проверьте и отправьте еще раз')
        await state.set_state(FormState.phone_number)


@dp.message(FormState.city)
async def process_location(message: types.Message, state: FSMContext):
    if message.text:
        person[message.chat.id].city = message.text.lower()
    await state.set_state(FormState.type_pet)
    await message.answer('Какое животное вы нашли/потеряли?')


@dp.message(FormState.type_pet)
async def process_animal_type(message: types.Message, state: FSMContext):
    if message.text and ('не знаю' not in message.text.lower() or 'извест' not in message.text.lower()):
        person[message.chat.id].type_pet = message.text.lower()
    await state.set_state(FormState.name_pet)
    await message.answer('Как зовут питомца?')


@dp.message(FormState.name_pet)
async def process_pet_name(message: types.Message, state: FSMContext):
    if message.text and ('не знаю' not in message.text.lower() or 'извест' not in message.text.lower()):
        person[message.chat.id].name_pet = message.text.lower()
    await state.set_state(FormState.sex_pet)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(types.InlineKeyboardButton(text="Мужской", callback_data="male"))
    keyboard_builder.add(types.InlineKeyboardButton(text="Женский", callback_data="female"))
    await message.answer('Пол питомца?', reply_markup=keyboard_builder.as_markup())


@dp.callback_query(lambda c: c.data in ["male", "female"])
async def process_pet_sex_selection(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "male":
        person[callback.message.chat.id].pet_sex = 0
    elif callback.data == "female":
        person[callback.message.chat.id].pet_sex = 1
    await state.set_state(FormState.breed_pet)
    await callback.message.answer('Порода питомца?')
    await callback.answer()


@dp.message(FormState.breed_pet)
async def process_pet_breed(message: types.Message, state: FSMContext):
    if message.text and ('не знаю' not in message.text.lower() or 'извест' not in message.text.lower()):
        person[message.chat.id].breed_pet = message.text.lower()
    await state.set_state(FormState.describe)
    await message.answer('Поделитесь подробности (где, когда и во сколько вы нашли\потеряли питомца, особенности и отличительные черты питомцы и тд)')


@dp.message(FormState.describe)
async def process_description(message: types.Message, state: FSMContext):
    if message.text:
        person[message.chat.id].describe = message.text
    await state.set_state(None)
    await message.answer('Мы почти закончили. Отправьте фотографию питомца:')


@dp.message(F.photo)
async def handle_messages(message: types.Message, bot: Bot):
    photo_file_id = message.photo[-1].file_id
    photo_file = await bot.get_file(photo_file_id)
    photo_path = photo_file.file_path

    if not os.path.exists("d_photo"):
        os.makedirs("d_photo")

    destination = os.path.join("d_photo", f'{photo_file_id}.jpg')

    await bot.download_file(photo_path, destination)
    person[message.chat.id].photo = destination
    new_human(person[message.chat.id], message.chat.id)

    if count_person(person[message.chat.id].status) != 0:
        matches = selection2(person[message.chat.id])
        if not matches:
            await message.answer('Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, попробуйте обратиться попозже')
        else:
            await message.answer(f'Я нашел {len(matches)} подходящих анкет:')
            for match in matches:
                await message.answer_photo(types.FSInputFile(match.pet_photo), caption=f'Имя: {match.name}\nНомер телефона: {match.phone_number}\nТелеграм: {match.tg_user}\nГород: {match.city}\nЖивотное: {match.type_pet}\nКличка: {match.name_pet}\nОписание: {match.decribe}')
            await message.answer('Надеюсь я смог вам помочь! Если вы смогли вернуть питомца домой, то удалите свое объявление /del. Если же нет, то попробуйте чуть-чуть попозже, вдруг человек еще не выложил объявление!')
    else:
        await message.answer('Я не нашёл подходящие анкеты, возможно человек еще не выложил объявление. Мне очень жаль, попробуйте обратиться попозже')



@dp.message(F.text)
async def handle_random_message(message: types.Message):
    await message.answer('Не понимаю вас, ожидайте ответа')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
