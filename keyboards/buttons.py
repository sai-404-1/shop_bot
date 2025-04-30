from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

class Button:
    """Parent class for inline and keyboard buttons"""
    def __init__(self, text: str):
        self.text = text

    def create(self) -> InlineKeyboardButton | KeyboardButton:
        raise NotImplementedError("This method only for childs")


class InlineButton(Button):
    """
    Inline button class
    Child class for Button class
    text - text of button
    callback_data - callback data of button
    """
    def __init__(self, text: str, callback_data: str):
        super().__init__(text)
        self.callback_data = callback_data

    def create(self) -> InlineKeyboardButton:
        # print(f"[{self.text}:{self.callback_data}]")
        return InlineKeyboardButton(text=self.text, callback_data=self.callback_data)


class KeyboardButtonRegular(Button):
    """
    Regular button class
    Child class for Button class
    text - text of button
    """
    def __init__(self, text: str):
        super().__init__(text)

    def create(self) -> KeyboardButton:
        return KeyboardButton(text=self.text)