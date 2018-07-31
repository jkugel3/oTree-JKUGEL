from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class BasePage(Page):

    def is_displayed(self):
        return self.round_number == 1

class Intro01 (BasePage):
    pass

class Intro02(BasePage):
    pass

class Intro03(BasePage):
    pass

class Intro05(BasePage):
    pass

class Intro06(BasePage):
    pass

class Intro07(BasePage):
    pass

class Intro08(BasePage):
    pass

class Intro09 (BasePage):
    pass

class Intro10 (BasePage):
    pass

class Intro11 (BasePage):
    pass

class Intro12 (BasePage):
    pass

class Intro13 (BasePage):
    pass

class Intro14 (BasePage):
    pass

class Intro15 (BasePage):
    pass

class Intro16 (BasePage):
    pass

page_sequence = [
                #  Intro01, Intro02, Intro03, Intro05, Intro06, Intro07, Intro08,
                 Intro09,
                #  Intro10,Intro11,
                #  Intro12, Intro13, Intro14, Intro15, Intro16,
                ]

#The page "Intro04" was later found to be a duplicate. It was excised from the program but the remaining
#numbering was left the same due to ease.
