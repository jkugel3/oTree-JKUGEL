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
        self.participant.vars['expiry'] = time.time() + (5 * 60)


class EndPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct2': sum([p.is_correct for p in player_in_all_rounds]),
        }


class Wait1(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class Direct(BasePage):
    form_model = 'group'
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
            'transcribe': 'mathquiz/{}.JPG'.format(self.round_number)
        }

    def is_displayed(self):
        if self.round_number == 1:
            return self.participant.vars['total_modquiz_questions_correct'] > 0
        num_previous_correct = sum([p.is_correct for p in self.player.in_previous_rounds()])
        return num_previous_correct < self.participant.vars['total_modquiz_questions_correct']


class BeforeResultsWP(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(EndPage):
    ...


class Payout(EndPage):
    pass


page_sequence = [
    Wait1,
    Direct,
    Question,
    BeforeResultsWP,
    Results,
    Payout,
]
