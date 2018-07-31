from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Debrief(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'manip_check',
                   'volunteer_orgs',
                   'donate_orgs',
                   'dualgiver_orgs',
                   'comments']


class ExperimentEnds(Page):
    form_model = 'player'
    form_fields = ['puid']

page_sequence = [
    Debrief,
    ExperimentEnds
]
