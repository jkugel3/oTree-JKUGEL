from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

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

    orgs = ["Hunger Project","Mental Health America","National Military Family Association",\
            "Ronald McDonald House","Wildlife Conservation Society"]

    # Dual Giver: DG, Volunteer: VL
    treatments = ['DG', 'VL']

class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config['treatment'] in Constants.treatments, "THERE IS NO SUCH TREATMENT!!!"
        if self.round_number == 1:
            self.session.vars['questions2'] = Constants.questions2

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']
            p.solution = question_data['solution']

class Group(BaseGroup):

    pass

class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(blank=True)
    is_correct = models.BooleanField()
    dictator = models.CurrencyField()
    sent_amount = models.CurrencyField()
    charity_fund = models.CurrencyField()
    direct_donation = models.CurrencyField()
    total_correct = models.CurrencyField()
    org_choice = models.StringField(choices=Constants.orgs,blank=True)

    def current_question(self):
        return self.session.vars['questions2'][self.round_number - 1]

    def check_correct(self):

        self.is_correct = self.submitted_answer == self.solution
        if self.session.config == 'VL' or self.is_correct==1:
            if self.id_in_group==1:
                self.dictator =+ Constants.right_answer
            elif self.id_in_group==2:
                self.charity_fund =+ Constants.right_answer
            elif self.id_in_group==3:
                self.direct_donation =+ Constants.right_answer
        elif self.session.config == 'DG' or self.is_correct == 1:
            if self.id_in_group==1:
                self.dictator =- Constants.right_answer
            elif self.id_in_group==2:
                self.charity_fund =- Constants.right_answer
            elif self.id_in_group==3:
                self.direct_donation =- Constants.right_answer
        else:
            pass
        return self.dictator or self.charity_fund or self.direct_donation

    def sent_money(self):
        self.sent_amount = abs(self.dictator) * c(0.5)
        return self.sent_amount

    def set_payoffs(self):
        if self.session.config == 'DG':
            if self.id_in_group == 1:
                self.payoff = self.dictator
            elif self.id_in_group == 2:
                self.payoff = self.charity_fund + self.sent_amount
            else:
                self.payoff = self.direct_donation + self.sent_amount
        else:
            if self.id_in_group == 2:
                self.payoff = self.sent_amount
            elif self.id_in_group == 3:
                self.payoff = self.sent_amount


    def fix_payment(self):
        if self.payoff < 2.00:
            self.payoff == 2.00
        else:
            pass
