from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time

class BasePage(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.participant.vars['expiry'] = time.time() + (5*60)

class EndPage(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct2': sum([p.is_correct for p in player_in_all_rounds]),
        }

class Wait(WaitPage):

    def is_displayed(self):
        return self.round_number == 1

class Direct(BasePage):

    form_model = 'player'
    form_fields = ['org_choice']

class Question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']

    def before_next_page(self):
        self.player.check_correct()

    timer_text = 'Time left to complete this section:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return {
            'transcribe':'mathquiz/{}.JPG'.format(self.round_number)
        }

class Results(EndPage):

    pass

class Payout(EndPage):

   pass

page_sequence = [
    Wait,
    Direct,
    Question,
    Results,
    Payout,
]
