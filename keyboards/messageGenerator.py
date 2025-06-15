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

    def findBackAction(self) -> str:
        for key in self.dataset:
            try:
                value = self.dataset[key]
                actions = [v[1] for v in value]
                if self.data in actions:
                    return key
            except:
                pass
        return None

    def getInlineKeyboard(self) -> InlineKeyboardMarkup:
        buttons = []
        backAction = self.findBackAction()
        for button_data in self.getButtons():
            buttons.append(InlineButton(button_data[0], button_data[1]))
        # TODO: add condition: if getBackAction is not None -> create back button : if it is None -> not create custom keyboard
        if self.data == "main" or backAction is None:
            return keyboardFabric.createCustomInlineKeyboard(buttons)
        else:
            return keyboardFabric.createKeyboardWithBackButton(buttons, backAction)
    
    def getReplyKeyboard(self) -> ReplyKeyboardMarkup:
        """
        we don't use this now
        TODO: add this function
        """
        pass

class TextGenerator:
    def __init__(self, data):
        self.data = data
        self.buttonTexts = Json.getButtonPartsDataset()
        self.messageDataset = Json.getMessagePartsDataset()
    
    def getButtonPart(self):
        try:
            return self.buttonTexts[self.data]
        except:
            return self.buttonTexts["NaN"]
    
    def getMessagePart(self):
        try:
            return self.messageDataset[self.data]
        except:
            return self.messageDataset["NaN"]
            