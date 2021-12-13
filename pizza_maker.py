import config
import telebot
import argparse
from transitions import Machine

parser = argparse.ArgumentParser()
parser.add_argument("-t","--transport", type=str, nargs='?', const='telegram', default='telegram',
                    help="To select a messenger, enter its name: Skype, VK, Facebook. Telegram is the default.")
args = parser.parse_args()

bot = telebot.TeleBot(config.token)

class Pizza(object):

    def __init__(self):

        self.bot_response  = 'Хочешь заказать пиццу?'
        self.pizza_payment = ''
        self.pizza_size = ''
        self.orders = {}
        self.user_id = ''


    def on_enter_start(self):
        self.bot_response = 'Хочешь заказать пиццу?'

    def on_enter_size(self):
        self.bot_response = "Какую вы хотите пиццу? Большую или маленькую?"

    def on_enter_payment(self):
        self.bot_response = 'Как вы будете платить? Картой или наличными?'

    def on_enter_confirmation(self):
        self.bot_response = f"Вы заказали {self.pizza_size} пиццу, оплата - {self.pizza_payment}?"

    def on_enter_finish(self):
        self.orders[self.user_id] = [self.pizza_size, self.pizza_payment]
        self.bot_response = f"Спасибо за заказ!"

    def set_pizza_size(self, value):
        self.pizza_size = value

    def set_pizza_payment(self, value):
        self.pizza_payment = value

    def get_text(self):
        return self.bot_response

    def set_user_id(self, value):
        self.user_id = value

pizza_hot = Pizza()

status = ['start', 'size', 'payment', 'confirmation', 'finish']

transitions = [
    {'trigger': 'да', 'source': 'start', 'dest': 'size'},
    {'trigger': 'большую', 'source': 'size', 'dest': 'payment'},
    {'trigger': 'маленькую', 'source': 'size', 'dest': 'payment'},
    {'trigger': 'наличными', 'source': 'payment', 'dest': 'confirmation'},
    {'trigger': 'картой', 'source': 'payment', 'dest': 'confirmation'},
    {'trigger': 'нет', 'source': 'confirmation', 'dest': 'size'},
    {'trigger': 'да', 'source': 'confirmation', 'dest': 'finish'},
    {'trigger': 'повтор', 'source': 'finish', 'dest': 'start'},
]

machine = Machine(pizza_hot, states=status, transitions=transitions, initial='start', ignore_invalid_triggers=True)


if args.transport == 'telegram':
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        pizza_hot.set_user_id(message.from_user.id)
        if pizza_hot.is_size():
            pizza_hot.set_pizza_size(message.text.lower())
        if pizza_hot.is_payment():
            pizza_hot.set_pizza_payment(message.text.lower())
        pizza_hot.trigger(message.text.lower())

        """Добавил проверку id чтобы во время тестов не шли сообщения в реальную телегую."""
        if message.from_user.id == 777:
            return pizza_hot.get_text()
        elif pizza_hot.is_finish():
            bot.send_message(message.from_user.id, pizza_hot.get_text())
            pizza_hot.trigger('повтор')
        else:
            bot.send_message(message.from_user.id, pizza_hot.get_text())



    bot.polling(none_stop=True, interval=0)

elif args.transport.lower() == 'skype':
    print('Скрипт для запуска Skype бота не реализован.')
elif args.transport.lower() == 'vk':
    print('Скрипт для запуска VK бота не реализован.')
elif args.transport.lower() == 'facebook':
    print('Скрипт для запуска Facebook бота не реализован.')