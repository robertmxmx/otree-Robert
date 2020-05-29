from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, os


class Constants(BaseConstants):
    name_in_url = 't2_parta'
    players_per_group = None
    num_rounds = 1

    instructions_content = 't2_parta/InstructionsContent.html'
    s_pairs = [
        ["You support mandatory vaccinations", "You do not support mandatory vaccinations"],
        ["Male circumcision should be decided by the individual", "Male circumcision should be decided by the parents"],
        ["You would lie to get a promotion", "You would not lie to get a promotion"],
        ["You believe that mentally handicapped people should be allowed to have kids", "You believe that mentally handicapped people should not be allowed to have kids"],
        ["You believe that all Jews should have been killed in WWII", "You do not believe that all Jews should have been killed in WWII"],
        ["You are Pro-Life", "You are Pro-Choice"],
        ["You support pre-emptive military attacks", "You do not support pre-emptive military attacks"],
        ["You would use lethal violence to defend a member of your family from a rapist", "You would not use lethal violence to defend a member of your family from a rapist"],
        ["You think that marital rape is a crime", "You think that there is no such thing as rape within a marriage"],
        ["You would give secret information about your home nation to a hostile foreign government", "You would not give secret information about your home nation to a hostile foreign government"],
        ["You think that assisted suicide should be legal", "You think that assisted suicide should be illegal"],
        ["You are willing to cheat on your taxes if you know that you would not get caught", "You are not willing to cheat on your taxes even if you know that you wouldn't get caught"],
        ["You would not pay for sex", "You would pay for sex"],
        ["You do not believe that God hears all prayers", "You believe that God hears all prayers"],
        ["You like to hurt animals", "You do not like to hurt animals"],
        ["You would urinate on your national flag", "You would not urinate on your national flag"],
        ["You would vote for a racist as your political leader, if you agreed with their economic policies", "You would not vote for a racist as your political leader, even if you agreed with their economic policies"],
        ["You do not support the use of the death penalty", "You support the use of the death penalty"],
        ["Your religion is an important part of your identity", "Your religion is not an important part of your identity"],
        ["You would have sex with a person of the opposite sex", "You would not have sex with a person of the opposite sex"],
        ["You would not vote for a politician who had previously made racist comments", "You would vote for a politician who had previously made racist comments"],
        ["It is not ok to use nuclear weapons on civilians", "It is ok to use nuclear weapons on civilians"],
        ["You would tell a joke which insulted people from your nation.", "You would not tell a joke which insulted people from your nation."],
        ["You do not believe that mandatory school prayer should be instated", "You believe that mandatory school prayer should be instated"],
        ["You would not sabotage a team of coworkers just to get an individual promotion", "You would sabotage a team of coworkers to get an individual promotion"],
        ["There should not be special restrictions on Muslim migration to western nations.", "There should be special restrictions on Muslim migration to western nations."],
        ["You do not drive above the speed limit", "You drive above the speed limit"],
        ["It is OK to sterilize people for population control", "It is not OK to sterilize people for population control"],
        ["You would accept money for sex", "You would not accept money for sex"],
        ["You would not lie to a Court in order to keep your friend out of jail.", "You would lie to a Court in order to keep your friend out of jail."],
        ["You do not give money to the poor", "You give money to the poor"],
        ["You would not cheat on your spouse even if there was no chance of getting caught", "You would cheat on your spouse if there was no chance of getting caught"],
        ["You would not cheat on a test even if there was no chance that you would get caught", "You would cheat on a test if there was no chance that you would get caught"],
        ["You would tell a joke which insulted people who share your religious background.", "You would not tell a joke which insulted people who share your religious background."],
        ["You would not lie to a Court in order to keep a member of your congregation out of jail.", "You would lie to a Court in order to keep a member of your congregation out of jail."],
        ["Women should not be in positions of political power.", "Women should be in positions of political power."],
        ["All whites are not racists", "All whites are racists"],
        ["North Korea should be nuked", "North Korea should not be nuked"],
        ["You support the use of torture to gain intelligence", "You do not support the use of torture to gain intelligence"],
        ["You are not willing to kill an innocent human being", "You are willing to kill an innocent human being"],
        ["You support the use of embryos for stem cell research", "You do not support the use of embryos for stem cell research"],
        ["You believe that there are too many restrictions on gun ownership", "You believe that there are not enough restrictions on gun ownership"],
        ["You believe in God", "You do not believe in God"],
        ["You believe that interracial relationships are wrong", "You do not believe that interracial relationships are wrong"],
        ["You believe that Google is superior to Yahoo", "You believe that Yahoo is superior to Google"],
        ["You believe that global warming is real", "You do not believe that global warming is real"],
        ["You would not tell a joke which insulted people of your ethnicity.", "You would tell a joke which insulted people of your ethnicity."],
        ["You are proud to be a citizen of your home nation", "You are not proud to be a citizen of your home nation"],
        ["You are a political conservative", "You are a political progressive"],
        ["You do not support medical testing on animals", "You support medical testing on animals"],
        ["You are not willing to give part of your income for environmental protection", "You are willing to give part of your income for environmental protection"],
        ["You think that it is ok to sell a child", "You think it is not ok to sell a child"],
        ["You think that homosexual couples should not have the same rights as heterosexual couples", "You think that homosexual couples should have the same rights as heterosexual couples"],
        ["You do not believe that homosexuality is a choice", "You believe that homosexuality is a choice"],
        ["You would not have sex with a 4 year old child", "You would have sex with a 4 year old child"],
        ["You support hiring quotas based on race", "You do not support hiring quotas based on race"],
        ["You support gay marriage", "You do not support gay marriage"],
        ["Not just black lives matter.", "Black lives matter."],
        ["You would have sex with a person of the same sex", "You would not have sex with a person of the same sex"],
        ["Israel should have complete control of the West Bank and Gaza", "Palestine should have complete control of the West Bank and Gaza"],
        ["Female genital cutting is acceptable in some cultures", "Female genital cutting is never acceptable"],
        ["You support suspending people's constitutional rights during wartime", "You do not support suspending people's constitutional rights during wartime"]
    ]
    num_sp = len(s_pairs)


class Subsession(BaseSubsession):

    def creating_session(self):
        # randomize the order that the statements appear
        self.session.vars['s_order'] = random.sample(range(1, Constants.num_sp+1), Constants.num_sp)
        with open(os.path.abspath('output_files/' + self.session.code + '_s_order.csv'), 'w') as f:
            for x in self.session.vars['s_order']:
                f.write(str(x) + "\n")

        for p in self.get_players():
            p.participant.vars['sp_data'] = []      # stores statement info


class Group(BaseGroup):
    pass


def create_sp(op1, op2):
    return models.IntegerField(label="", choices=[[1, op1], [2, op2]], widget=widgets.RadioSelect)


class Player(BasePlayer):
    sp_count = models.IntegerField(initial=1)   # determines which statement pair to show
    sp1 = create_sp(Constants.s_pairs[0][0], Constants.s_pairs[0][1])
    sp2 = create_sp(Constants.s_pairs[1][0], Constants.s_pairs[1][1])
    sp3 = create_sp(Constants.s_pairs[2][0], Constants.s_pairs[2][1])
    sp4 = create_sp(Constants.s_pairs[3][0], Constants.s_pairs[3][1])
    sp5 = create_sp(Constants.s_pairs[4][0], Constants.s_pairs[4][1])
    sp6 = create_sp(Constants.s_pairs[5][0], Constants.s_pairs[5][1])
    sp7 = create_sp(Constants.s_pairs[6][0], Constants.s_pairs[6][1])
    sp8 = create_sp(Constants.s_pairs[7][0], Constants.s_pairs[7][1])
    sp9 = create_sp(Constants.s_pairs[8][0], Constants.s_pairs[8][1])
    sp10 = create_sp(Constants.s_pairs[9][0], Constants.s_pairs[9][1])
    sp11 = create_sp(Constants.s_pairs[10][0], Constants.s_pairs[10][1])
    sp12 = create_sp(Constants.s_pairs[11][0], Constants.s_pairs[11][1])
    sp13 = create_sp(Constants.s_pairs[12][0], Constants.s_pairs[12][1])
    sp14 = create_sp(Constants.s_pairs[13][0], Constants.s_pairs[13][1])
    sp15 = create_sp(Constants.s_pairs[14][0], Constants.s_pairs[14][1])
    sp16 = create_sp(Constants.s_pairs[15][0], Constants.s_pairs[15][1])
    sp17 = create_sp(Constants.s_pairs[16][0], Constants.s_pairs[16][1])
    sp18 = create_sp(Constants.s_pairs[17][0], Constants.s_pairs[17][1])
    sp19 = create_sp(Constants.s_pairs[18][0], Constants.s_pairs[18][1])
    sp20 = create_sp(Constants.s_pairs[19][0], Constants.s_pairs[19][1])
    sp21 = create_sp(Constants.s_pairs[20][0], Constants.s_pairs[20][1])
    sp22 = create_sp(Constants.s_pairs[21][0], Constants.s_pairs[21][1])
    sp23 = create_sp(Constants.s_pairs[22][0], Constants.s_pairs[22][1])
    sp24 = create_sp(Constants.s_pairs[23][0], Constants.s_pairs[23][1])
    sp25 = create_sp(Constants.s_pairs[24][0], Constants.s_pairs[24][1])
    sp26 = create_sp(Constants.s_pairs[25][0], Constants.s_pairs[25][1])
    sp27 = create_sp(Constants.s_pairs[26][0], Constants.s_pairs[26][1])
    sp28 = create_sp(Constants.s_pairs[27][0], Constants.s_pairs[27][1])
    sp29 = create_sp(Constants.s_pairs[28][0], Constants.s_pairs[28][1])
    sp30 = create_sp(Constants.s_pairs[29][0], Constants.s_pairs[29][1])
    sp31 = create_sp(Constants.s_pairs[30][0], Constants.s_pairs[30][1])
    sp32 = create_sp(Constants.s_pairs[31][0], Constants.s_pairs[31][1])
    sp33 = create_sp(Constants.s_pairs[32][0], Constants.s_pairs[32][1])
    sp34 = create_sp(Constants.s_pairs[33][0], Constants.s_pairs[33][1])
    sp35 = create_sp(Constants.s_pairs[34][0], Constants.s_pairs[34][1])
    sp36 = create_sp(Constants.s_pairs[35][0], Constants.s_pairs[35][1])
    sp37 = create_sp(Constants.s_pairs[36][0], Constants.s_pairs[36][1])
    sp38 = create_sp(Constants.s_pairs[37][0], Constants.s_pairs[37][1])
    sp39 = create_sp(Constants.s_pairs[38][0], Constants.s_pairs[38][1])
    sp40 = create_sp(Constants.s_pairs[39][0], Constants.s_pairs[39][1])
    sp41 = create_sp(Constants.s_pairs[40][0], Constants.s_pairs[40][1])
    sp42 = create_sp(Constants.s_pairs[41][0], Constants.s_pairs[41][1])
    sp43 = create_sp(Constants.s_pairs[42][0], Constants.s_pairs[42][1])
    sp44 = create_sp(Constants.s_pairs[43][0], Constants.s_pairs[43][1])
    sp45 = create_sp(Constants.s_pairs[44][0], Constants.s_pairs[44][1])
    sp46 = create_sp(Constants.s_pairs[45][0], Constants.s_pairs[45][1])
    sp47 = create_sp(Constants.s_pairs[46][0], Constants.s_pairs[46][1])
    sp48 = create_sp(Constants.s_pairs[47][0], Constants.s_pairs[47][1])
    sp49 = create_sp(Constants.s_pairs[48][0], Constants.s_pairs[48][1])
    sp50 = create_sp(Constants.s_pairs[49][0], Constants.s_pairs[49][1])
    sp51 = create_sp(Constants.s_pairs[50][0], Constants.s_pairs[50][1])
    sp52 = create_sp(Constants.s_pairs[51][0], Constants.s_pairs[51][1])
    sp53 = create_sp(Constants.s_pairs[52][0], Constants.s_pairs[52][1])
    sp54 = create_sp(Constants.s_pairs[53][0], Constants.s_pairs[53][1])
    sp55 = create_sp(Constants.s_pairs[54][0], Constants.s_pairs[54][1])
    sp56 = create_sp(Constants.s_pairs[55][0], Constants.s_pairs[55][1])
    sp57 = create_sp(Constants.s_pairs[56][0], Constants.s_pairs[56][1])
    sp58 = create_sp(Constants.s_pairs[57][0], Constants.s_pairs[57][1])
    sp59 = create_sp(Constants.s_pairs[58][0], Constants.s_pairs[58][1])
    sp60 = create_sp(Constants.s_pairs[59][0], Constants.s_pairs[59][1])
    sp61 = create_sp(Constants.s_pairs[60][0], Constants.s_pairs[60][1])
    sp62 = create_sp(Constants.s_pairs[61][0], Constants.s_pairs[61][1])
