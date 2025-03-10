from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup


from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
from myUtils import Json

class MessageGenerator:
    def __init__(self, data: str):
        self.data = data
        self.dataset = Json.getMainDataset()
    
    def getText(self):
        try:
            return self.dataset["message_texts"][self.data]
        except:
            return self.dataset["message_texts"]["NaN"]

    def getButtons(self) -> list[Button]:
        try:
            return self.dataset[self.data]
        except:
            return self.dataset["NaN"]
    
    def getInlineKeyboard(self) -> InlineKeyboardMarkup:
        buttons = []
        for button_data in self.getButtons():
            buttons.append(InlineButton(button_data[0], button_data[1]))
        
        return keyboardFabric.createCustomInlineKeyboard(buttons)
    
    def getReplyKeyboard(self) -> ReplyKeyboardMarkup:
        """
        we don't use this now
        TODO: add this function
        """
        pass