from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random

author = 'Jonathan Kugel'

doc = """
A quiz app that reads its questions from a spreadsheet
There is 1 question per page; the number of pages in the game
is determined by the number of questions in the CSV.
See the comment below about how to randomize the order of pages.
"""


class Constants(BaseConstants):
    name_in_url = 'mathquiz'
    players_per_group = 3

    with open('mathquiz/math_quiz.csv') as f:
        questions2 = list(csv.DictReader(f))

    num_rounds = len(questions2)

    right_answer = c(0.25)

    orgs = ["Hunger Project", "Mental Health America", "National Military Family Association", \
            "Ronald McDonald House", "Wildlife Conservation Society"]

    # Dual Giver: DG, Volunteer: VL
    treatments = ['DG', 'VL']


class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config['treatment'] in Constants.treatments, "THERE IS NO SUCH TREATMENT!!!"
        if self.round_number == 1:
            self.session.vars['questions2'] = Constants.questions2
            # PH The next two lines are needed FOR DEBUG ONLY: otherwise in the development you won't be able to run
            # mathquiz app without modquiz app, because total_modquiz_questions_correct etc. won't be set.
            # setdefault is a python command that set a value in a dict if it is not yet set. So if it is already there
            # which will be the case when they run modquiz first, the next two lines won't do anything
            for p in self.get_players():
                p.participant.vars.setdefault('total_modquiz_questions_correct', random.randint(0, 3))
                p.participant.vars.setdefault('modquiz_earnings',
                                              p.participant.vars['total_modquiz_questions_correct'] *
                                              Constants.right_answer)
                p.total_modquiz_questions_correct = p.participant.vars.get('total_modquiz_questions_correct')
                p.modquiz_earnings = p.participant.vars.get('modquiz_earnings')
                # DELETE NEXT LINE!!!! FOR DEBUG ONLY!!!!!
                p.participant.payoff = p.modquiz_earnings
        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']
            p.solution = question_data['solution']


class Group(BaseGroup):
    generic_charity_donation = models.CurrencyField(doc='info about money sent to gen.charity')
    specific_charity_donation = models.CurrencyField(doc='info about money sent to spec.charity chosen by a player')
    org_choice = models.StringField(choices=Constants.orgs, blank=True)

    def set_payoffs(self):
        double_giver = self.get_player_by_role('double_giver')
        generic_charity = self.get_player_by_role('generic_charity')
        specific_charity = self.get_player_by_role('specific_charity')
        for p in self.get_players():
            p.total_correct = sum([i.is_correct for i in p.in_all_rounds()])
            p.money_sent = p.total_correct * Constants.right_answer
        self.generic_charity_donation = generic_charity.money_sent
        self.specific_charity_donation = specific_charity.money_sent
        if self.session.config['treatment'] == 'DG':
            for p in self.get_players():
                p.payoff -= p.money_sent

        dg_share = double_giver.money_sent / 2
        generic_charity.payoff += dg_share
        specific_charity.payoff += dg_share


class Player(BasePlayer):
    total_modquiz_questions_correct = models.IntegerField()
    modquiz_earnings = models.CurrencyField()
    question_id = models.PositiveIntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(blank=True)
    is_correct = models.BooleanField(initial=False)
    money_sent = models.CurrencyField()
    total_correct = models.IntegerField()

    def current_question(self):
        return self.session.vars['questions2'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = self.submitted_answer == self.solution

    def role(self):

        if self.id_in_group == 1:
            return 'double_giver'
        if self.id_in_group == 2:
            return 'generic_charity'
        if self.id_in_group == 3:
            return 'specific_charity'
