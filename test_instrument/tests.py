from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

import random
class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Sampling, {'items_sampled': random.randint(1,30)})
        yield (pages.SampleResults)
