from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.PositiveIntegerField(
        verbose_name='What is your age?',
        min=18, max=125)

    gender = models.StringField(
        choices=['Male', 'Female'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect())

    manip_check = models.PositiveIntegerField(
        choices=[
            [1, 'Completely Disagree'],
            [2, 'Strongly Disagree'],
            [3, 'Midly Disagree'],
            [4, 'Neutral'],
            [5, 'Mildly Agree'],
            [6, 'Strongly Agree'],
            [7, 'Completely Agree']],
        widget = widgets.RadioSelectHorizontal(),
        verbose_name ='''
            To what extent do you agree with the following statement? - It was important to me to correctly complete 
            as many transcriptions as possible'''
    )

    volunteer_orgs = models.PositiveIntegerField(
        verbose_name='''
        In the last year, how many charitable organizations did you support by volunteering?''',
        min=0, max=100)

    donate_orgs = models.PositiveIntegerField(
        verbose_name='''
        In the last year, how many charitable organizations did you support by donating money or property?''',
        min=0, max=100)

    dualgiver_orgs = models.PositiveIntegerField(
        verbose_name='''
        In the last year, how many charitable organizations did you support by BOTH volunteering 
        AND donating money or property?''',
        min=0, max=100)

    comments = models.LongStringField(
        verbose_name='''Do you have any comments or feedback you would like to share regarding this study?'''
    )

    puid = models.StringField(verbose_name='''Please enter your code here:''')