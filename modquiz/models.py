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
    name_in_url = 'modquiz'
    players_per_group = None

    with open('modquiz/charity_quiz.csv') as f:
        questions = list(csv.DictReader(f))

    num_rounds = len(questions)

    right_answer = c(0.25)

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.questions

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
    submitted_answer = models.StringField(widget=widgets.RadioSelect())
    is_correct = models.BooleanField()
    total_correct = models.CurrencyField()

    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = self.submitted_answer == self.solution
        if self.is_correct == 1:
            self.total_correct =+ Constants.right_answer
        else:
            pass
        return self.total_correct

    def set_payoffs(self):
        self.payoff = self.total_correct
