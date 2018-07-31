from otree.api import (models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer)
from otree.api import Currency as c, currency_range
import random

author = 'Jonathan Kugel'

doc = """
Examining Variant Penalty Regimes on Auditor JDM
"""

"""For the class constants, we will define the number of rounds, the base revenue each participant receives
for every round, and the type I error penalty (rejecting a correct box)"""


class Constants(BaseConstants):
    name_in_url = 'test_instrument'
    #Because all players complete all screens, participants = players
    players_per_group = None
    #Each player receives a 50 points per round endowment
    round_revenue = 30
    #This app represents the "real" experiment. A duplicate app without payment will be used for 5 practice rounds.
    num_rounds = 50
    #This is the Deterministic penalty regime for type II errors (Accept an invalid shipment)
    det_penalty = 200
    #This is the type I error penalty (Reject a valid shipment)
    TypeI_Error_Penalty = 30
    #This defines the upper bound range of the box for reference in the functions below
    ub = 100
    #This defines the lower bound range of the box for reference in the functions below
    lb = 1
    #This describes the margin of error for the difference between the three metrics
    t = 5
    # fixed: FX, skewed: SK, symmetric: SM
    treatments = ['FX', 'SK', 'SM']
    # Since when real game starts?:
    real_game_round = 6

class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config['treatment'] in Constants.treatments, "THERE IS NO SUCH TREATMENT!!!"
        for p in self.get_players():
            p.bol_correct = random.choice([True, False])
            p.croissant = random.randrange(Constants.lb, Constants.ub)
            if p.bol_correct:
                range_to_choose = list(range(max(p.croissant - Constants.t,
                                                 Constants.lb),
                                        min(p.croissant + Constants.t, Constants.ub)))
            else:
                range_left = list(range(Constants.lb,
                                        max(p.croissant - Constants.t, Constants.lb)))

                range_right = list(range(min(p.croissant + Constants.t,
                                             Constants.ub),
                                         Constants.ub))
                range_to_choose = range_left + range_right
            p.bol = random.choice(range_to_choose)

class Group(BaseGroup):

    pass

class Player(BasePlayer):

    #These two penalty regimes involve randomization and are player/round specific
    #The first is the skewed, stochastic penalty which mimics the threat of a lawsuit. The
    #second is the symmetric, stohastic penalty which mimics the potential for (but not guarantee of) a regulatory fine

    def skew_penalty(self):
        if random.random() <= 0.05:
            return 3050
        return 50

    def sym_penalty(self):
        sym_penalty = (random.randint(0, 200))
        return sym_penalty

    def fixed(self):
        return Constants.det_penalty

    def set_payoffs(self):
        treatment_penalties = [self.fixed, self.skew_penalty, self.sym_penalty]
        treatment_index = Constants.treatments.index(self.session.config['treatment'])
        self.treatment_penalty = treatment_penalties[treatment_index]()
        self.payoff = Constants.round_revenue - self.items_sampled
        if self.items_sampled == 0:
            self.accept = True
        else:
            self.extrapolated_n_croissants = round(self.croissants_sampled/self.items_sampled * Constants.ub, 0)
            self.accept = abs(self.bol - self.extrapolated_n_croissants)<= Constants.t

        self.payoff -= Constants.TypeI_Error_Penalty * (1 - self.accept) * \
            self.bol_correct + self.treatment_penalty * self.accept * (1 - self.bol_correct)


    treatment_penalty = models.PositiveIntegerField()
    items_sampled = models.PositiveIntegerField(min=0, max=30)
    croissant = models.PositiveIntegerField()
    bol = models.PositiveIntegerField()
    bol_correct = models.BooleanField()
    croissants_sampled = models.PositiveIntegerField()
    extrapolated_n_croissants = models.PositiveIntegerField()
    accept = models.BooleanField()
