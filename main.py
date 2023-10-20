import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6606602467:AAHU3BHMm1QweqqsPg1fMw0dIQE3TjgJrGc",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Расскажи о себе"  # Можно менять текст
text_button_1 = "Полезные видео"  # Можно менять текст
text_button_2 = "Планнеры и чеклисты"  # Можно менять текст
text_button_3 = "Приложения"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Здравствуйте, как к вам можно обращаться?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id,
                     'Рады знакомству! Этот бот содержит в себе полезные материалы, которые помогут вам, если вы увлекаетесь саморазвитием. Чем вы заниаетесь сейчас?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id) \
 \
    @ bot.message_handler(state=PollState.name)


def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Очень интересно. Какие сферы жизни вас привлекают?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id) \
 \
    @ bot.message_handler(state=PollState.age)


def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Вы очень интересная личность! Благодарим за регистрацию',
                     reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Основы тайм-менеджемта от Умскул] (https://www.youtube.com/watch?v=oPW_TPRMM_Q)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Мини-помощники] (https://disk.yandex.com.am/d/mEl-LEGrvxMqRA)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "1.  Forest: Будь сосредоточенным 2. Todoist: планы и задачи 3. Notion - notes, docs, tasks 4. Трекер привычек Loop 5. Duolingo: уроки иностранного",
                     reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

