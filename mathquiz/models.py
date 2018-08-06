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

    pass

class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(blank=True)
    is_correct = models.BooleanField()
    total_correct = models.CurrencyField()
    org_choice = models.StringField(choices=Constants.orgs,blank=True)

    def current_question(self):
        return self.session.vars['questions2'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = self.submitted_answer == self.solution

    def total(self):
        if self.is_correct == 1:
            self.total_correct =+ Constants.right_answer
        return self.total_correct

    def volunteer(self):
        return c(0)
    
    def set_payoffs(self):
        p1 = self.id_in_group == 1
        p2 = self.id_in_group == 2
        p3 = self.id_in_group == 3
        treatment_type = [self.total, self.volunteer]
        treatment_index = Constants.treatments.index(self.session.config['treatment'])
        self.treatment_type = treatment_type[treatment_index]()
        p1.payoff = sum([p1.payoff for p1 in self.in_all_rounds()]) - self.treatment_type
        p2.payoff = sum([p2.payoff for p2 in self.in_all_rounds()]) + (p1.self.total_correct/2) - self.treatment_type
        p3.payoff = sum([p3.payoff for p3 in self.in_all_rounds()]) + (p1.self.total_correct/2) - self.treatment_type
