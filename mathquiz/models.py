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

    right_answer = c(0.5)

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

    amount_sent = models.CurrencyField(
        max=c(0)
    )
    charity_fund = models.CurrencyField(
        min=c(0)
    )
    direct_donation = models.CurrencyField(
        min=c(0)
    )

class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(blank=True)
    is_correct = models.BooleanField()
    org_choice = models.StringField(choices=Constants.orgs,blank=True)

    def role(self):
        if self.id_in_group == 1:
            return 'dictator'
        elif self.id_in_group == 2:
            return 'charity_fund'
        elif self.id_in_group ==3:
            return 'direct'

    def current_question(self):
        return self.session.vars['questions2'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = self.submitted_answer == self.solution

    def dual_giver(self):
        return self.is_correct * Constants.right_answer

    def volunteer(self):
        return c(0)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        treatment_type = [self.dual_giver, self.volunteer]
        treatment_index = Constants.treatments.index(self.session.config['treatment'])
        self.treatment_type = treatment_type[treatment_index]()
        if self.treatment_type == 'VL':
            p1.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) + p1.self.amount_sent()
            p2.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) - (p1.self.amount_sent() / 2)
            p3.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) - (p1.self.amount_sent() / 2)
        elif self.treatment_type == "DG":
            p1.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) + p1.self.amount_sent() - p1.self.dual_giver
            p2.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) - (p1.self.amount_sent() / 2)
            p3.payoff = sum([p.payoff for p in self.player.in_all_rounds()]) - (p1.self.amount_sent() / 2)
