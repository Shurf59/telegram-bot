import unittest
from pizza_maker import Pizza, get_text_messages, pizza_hot

class Message:
    content_type = 'text'
    text = ''

    def set_text(arg):
        Message.text = arg

    class from_user:
        id = 777

test_message = Message
class Test_Pizza_Maker(unittest.TestCase, Message):
    test_pack = {
        'test1': ['test1', 'да', 'большую', 'картой', 'да'],
        'test2': ['test2', 'Да', 'Большую', 'Картой', 'Да'],
        'test3': ['test3', 'ДА', 'БОЛЬШУЮ', 'КАРТОЙ', 'ДА'],
        'test4': ['test4', 'нет', 'большую', 'картой', 'да'],
        'test5': ['test5', 'да', 'маленькую', 'наличными', 'да'],
        'test6': ['test6', 'Да', 'Маленькую', 'Наличными', 'Да'],
        'test7': ['test7', 'ДА', 'МАЛЕНЬКУЮ', 'НАЛИЧНЫМИ', 'ДА'],
        'test8': ['test8', 'ДА', 'МАЛЕНЬКУЮ', 'НАЛИЧНЫМИ', 'ДА'],
        'test9': ['test9', 'уже', 'да', 'надоело', 'МАЛЕНЬКУЮ', 'это', 'НАЛИЧНЫМИ', 'делать', 'ДА'],
        'test10': ['test10', 'да', 'большую', 'картой', 'да', 'еще', 'да', 'маленькую', 'наличными', 'да'],
        'test11': ['test11', 'да', 'большую', 'картой', 'нет', 'маленькую', 'наличными', 'да'],
        'test12': ['test12', 'да', 'большую', 'картой', 'нет', 'маленькую', 'наличными', 'да', 'еще', 'уже', 'да',
                   'надоело', 'МАЛЕНЬКУЮ', 'это', 'НАЛИЧНЫМИ', 'делать', 'ДА'],
    }

    def setUp(self):
        pass

    def test_get_text_messages(self):
        for i in Test_Pizza_Maker.test_pack:
            for f in Test_Pizza_Maker.test_pack[i]:
                Message.set_text(f)
                get_text_messages(Message)
                if pizza_hot.is_start():
                    self.assertEqual(pizza_hot.get_text(), 'Хочешь заказать пиццу?')
                elif pizza_hot.is_size():
                    self.assertEqual(pizza_hot.get_text(), 'Какую вы хотите пиццу? Большую или маленькую?')
                elif pizza_hot.is_payment():
                    self.assertEqual(pizza_hot.get_text(), 'Как вы будете платить? Картой или наличными?')
                elif pizza_hot.is_confirmation():
                    self.assertEqual(pizza_hot.get_text(), f"Вы заказали {pizza_hot.pizza_size} пиццу, оплата - {pizza_hot.pizza_payment}?")
                elif pizza_hot.is_finish():
                    self.assertEqual(pizza_hot.get_text(), 'Спасибо за заказ!')


if __name__ == "__main__":
    unittest.main()
