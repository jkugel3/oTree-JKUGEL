from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class BeginExp(Page):

    def is_displayed(self):
        return self.round_number == Constants.real_game_round

    def before_next_page(self):
        if self.player.set_payoffs != 0:
            self.player.set_payoffs = 0

class Sampling(Page):

    timeout_seconds = 30

    form_model = 'player'
    form_fields = ['items_sampled', ]
    def before_next_page(self):
        if self.player.round_number == Constants.real_game_round:
            for p in self.player.in_previous_rounds():
                p.payoff = 0
        if self.player.items_sampled != 0:
            total_party = [1] * self.player.croissant + [0] * (Constants.ub - self.player.croissant)
            subsample = random.sample(total_party,self.player.items_sampled)
            self.player.croissants_sampled = sum(subsample)

        self.player.set_payoffs()


class SampleResults(Page):

    pass

page_sequence = [BeginExp,
                 Sampling,
                 SampleResults, ]

#< p > ACCEPT / REJECT:: {{player.accept | yesno: 'ACCEPT, REJECT'}} < / p >
#< p > WAS
#THE
#BOL
#CORRECT:: {{player.bol_correct | yesno: 'CORRECT, INCORRECT'}} < / p >
#< p > < / p >
