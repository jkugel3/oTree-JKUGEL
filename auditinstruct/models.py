from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jonathan Kugel'

doc = """
Base Instructions for Sampling Game
"""


class Constants(BaseConstants):
    name_in_url = 'auditinstruct'
    players_per_group = None
    num_rounds = 1

    treatments = ['FX', 'SK', 'SM']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):
    pass
