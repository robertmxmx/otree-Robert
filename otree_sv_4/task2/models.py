from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import constants


class Constants(BaseConstants):
    name_in_url = 'task2'
    players_per_group = None
    num_rounds = 1

    min_bid = constants.min_bid
    max_bid = constants.max_bid
    opt_out_text = constants.opt_out_text
    statements = constants.statements


class Subsession(BaseSubsession):
    
    def creating_session(self):
        for player in self.get_players():
            order = list(Constants.statements.keys())
            random.shuffle(order)
            player.order = str(order)
            player.participant.vars['order'] = order
            player.participant.vars['current_statement'] = 0
            player.participant.vars['statements'] = dict()
            player.participant.vars['statements_bid'] = dict()


class Group(BaseGroup):
    pass

def make_field(choices):
    return models.IntegerField(
        label="",
        widget=widgets.RadioSelect,
        choices=choices
    )

class Player(BasePlayer):
    order = models.LongStringField()
    Vax_1               = make_field(Constants.statements['Vax_1'])
    MaleCirc_2          = make_field(Constants.statements['MaleCirc_2'])
    LiePromotion_3      = make_field(Constants.statements['LiePromotion_3'])
    MentKids_4          = make_field(Constants.statements['MentKids_4'])
    Genocide_5          = make_field(Constants.statements['Genocide_5'])
    ProLife_6           = make_field(Constants.statements['ProLife_6'])
    PreemptStrike_7     = make_field(Constants.statements['PreemptStrike_7'])
    LethalDef_8         = make_field(Constants.statements['LethalDef_8'])
    MaritalRape_9       = make_field(Constants.statements['MaritalRape_9'])
    Espionage_10        = make_field(Constants.statements['Espionage_10'])
    AssistSuic_11       = make_field(Constants.statements['AssistSuic_11'])
    TaxCheat_12         = make_field(Constants.statements['TaxCheat_12'])
    PaySex_13           = make_field(Constants.statements['PaySex_13'])
    GodPrayer_14        = make_field(Constants.statements['GodPrayer_14'])
    HurtAnimal_15       = make_field(Constants.statements['HurtAnimal_15'])
    FlagUrine_16        = make_field(Constants.statements['FlagUrine_16'])
    RacistVote_17       = make_field(Constants.statements['RacistVote_17'])
    DeathPen_18         = make_field(Constants.statements['DeathPen_18'])
    ReligionID_19       = make_field(Constants.statements['ReligionID_19'])
    HeteroSex_20        = make_field(Constants.statements['HeteroSex_20'])
    RacistVote2_21      = make_field(Constants.statements['RacistVote2_21'])
    NukeCiv_22          = make_field(Constants.statements['NukeCiv_22'])
    InsultNation_23     = make_field(Constants.statements['InsultNation_23'])
    SchoolPrayer_24     = make_field(Constants.statements['SchoolPrayer_24'])
    WorkSabotage_25     = make_field(Constants.statements['WorkSabotage_25'])
    MuslimMigrate_26    = make_field(Constants.statements['MuslimMigrate_26'])
    SpeedLimit_27       = make_field(Constants.statements['SpeedLimit_27'])
    PopControl_28       = make_field(Constants.statements['PopControl_28'])
    MoneySex_29         = make_field(Constants.statements['MoneySex_29'])
    LieCourtFriend_30   = make_field(Constants.statements['LieCourtFriend_30'])
    SupportPoor_31      = make_field(Constants.statements['SupportPoor_31'])
    SpouseCheat_32      = make_field(Constants.statements['SpouseCheat_32'])
    TestCheat_33        = make_field(Constants.statements['TestCheat_33'])
    InsultRel_34        = make_field(Constants.statements['InsultRel_34'])
    LieCourtChurch_35   = make_field(Constants.statements['LieCourtChurch_35'])
    WomenPower_36       = make_field(Constants.statements['WomenPower_36'])
    WhitesRacist_37     = make_field(Constants.statements['WhitesRacist_37'])
    NorthKorea_38       = make_field(Constants.statements['NorthKorea_38'])
    Torture_39          = make_field(Constants.statements['Torture_39'])
    KillInnocent_40     = make_field(Constants.statements['KillInnocent_40'])
    EmbryoUse_41        = make_field(Constants.statements['EmbryoUse_41'])
    GunLaws_42          = make_field(Constants.statements['GunLaws_42'])
    BlvGod_43           = make_field(Constants.statements['BlvGod_43'])
    InterracialRel_44   = make_field(Constants.statements['InterracialRel_44'])
    GoogleYahoo_45      = make_field(Constants.statements['GoogleYahoo_45'])
    GlobWarm_46         = make_field(Constants.statements['GlobWarm_46'])
    InsultEthnicity_47  = make_field(Constants.statements['InsultEthnicity_47'])
    ProudCitizen_48     = make_field(Constants.statements['ProudCitizen_48'])
    PolOrient_49        = make_field(Constants.statements['PolOrient_49'])
    MedTestAnimal_50    = make_field(Constants.statements['MedTestAnimal_50'])
    EnviroProtect_51    = make_field(Constants.statements['EnviroProtect_51'])
    SellChild_52        = make_field(Constants.statements['SellChild_52'])
    HomoRights_53       = make_field(Constants.statements['HomoRights_53'])
    HomoChoice_54       = make_field(Constants.statements['HomoChoice_54'])
    SexChild_55         = make_field(Constants.statements['SexChild_55'])
    RaceHiring_56       = make_field(Constants.statements['RaceHiring_56'])
    GayMarriage_57      = make_field(Constants.statements['GayMarriage_57'])
    BlackLives_58       = make_field(Constants.statements['BlackLives_58'])
    HomoSex_59          = make_field(Constants.statements['HomoSex_59'])
    Israel_60           = make_field(Constants.statements['Israel_60'])
    FGM_61              = make_field(Constants.statements['FGM_61'])
    RightsWartime_62    = make_field(Constants.statements['RightsWartime_62'])
    Litter_63           = make_field(Constants.statements['Litter_63'])
    Vote_64             = make_field(Constants.statements['Vote_64'])
    Jaywalk_65          = make_field(Constants.statements['Jaywalk_65'])
    Shoplift_66         = make_field(Constants.statements['Shoplift_66'])
    CheatGame_67        = make_field(Constants.statements['CheatGame_67'])
    GiveSeat_68         = make_field(Constants.statements['GiveSeat_68'])
    Vax_1_bid               = models.StringField(label="Your bid")
    MaleCirc_2_bid          = models.StringField(label="Your bid")
    LiePromotion_3_bid      = models.StringField(label="Your bid")
    MentKids_4_bid          = models.StringField(label="Your bid")
    Genocide_5_bid          = models.StringField(label="Your bid")
    ProLife_6_bid           = models.StringField(label="Your bid")
    PreemptStrike_7_bid     = models.StringField(label="Your bid")
    LethalDef_8_bid         = models.StringField(label="Your bid")
    MaritalRape_9_bid       = models.StringField(label="Your bid")
    Espionage_10_bid        = models.StringField(label="Your bid")
    AssistSuic_11_bid       = models.StringField(label="Your bid")
    TaxCheat_12_bid         = models.StringField(label="Your bid")
    PaySex_13_bid           = models.StringField(label="Your bid")
    GodPrayer_14_bid        = models.StringField(label="Your bid")
    HurtAnimal_15_bid       = models.StringField(label="Your bid")
    FlagUrine_16_bid        = models.StringField(label="Your bid")
    RacistVote_17_bid       = models.StringField(label="Your bid")
    DeathPen_18_bid         = models.StringField(label="Your bid")
    ReligionID_19_bid       = models.StringField(label="Your bid")
    HeteroSex_20_bid        = models.StringField(label="Your bid")
    RacistVote2_21_bid      = models.StringField(label="Your bid")
    NukeCiv_22_bid          = models.StringField(label="Your bid")
    InsultNation_23_bid     = models.StringField(label="Your bid")
    SchoolPrayer_24_bid     = models.StringField(label="Your bid")
    WorkSabotage_25_bid     = models.StringField(label="Your bid")
    MuslimMigrate_26_bid    = models.StringField(label="Your bid")
    SpeedLimit_27_bid       = models.StringField(label="Your bid")
    PopControl_28_bid       = models.StringField(label="Your bid")
    MoneySex_29_bid         = models.StringField(label="Your bid")
    LieCourtFriend_30_bid   = models.StringField(label="Your bid")
    SupportPoor_31_bid      = models.StringField(label="Your bid")
    SpouseCheat_32_bid      = models.StringField(label="Your bid")
    TestCheat_33_bid        = models.StringField(label="Your bid")
    InsultRel_34_bid        = models.StringField(label="Your bid")
    LieCourtChurch_35_bid   = models.StringField(label="Your bid")
    WomenPower_36_bid       = models.StringField(label="Your bid")
    WhitesRacist_37_bid     = models.StringField(label="Your bid")
    NorthKorea_38_bid       = models.StringField(label="Your bid")
    Torture_39_bid          = models.StringField(label="Your bid")
    KillInnocent_40_bid     = models.StringField(label="Your bid")
    EmbryoUse_41_bid        = models.StringField(label="Your bid")
    GunLaws_42_bid          = models.StringField(label="Your bid")
    BlvGod_43_bid           = models.StringField(label="Your bid")
    InterracialRel_44_bid   = models.StringField(label="Your bid")
    GoogleYahoo_45_bid      = models.StringField(label="Your bid")
    GlobWarm_46_bid         = models.StringField(label="Your bid")
    InsultEthnicity_47_bid  = models.StringField(label="Your bid")
    ProudCitizen_48_bid     = models.StringField(label="Your bid")
    PolOrient_49_bid        = models.StringField(label="Your bid")
    MedTestAnimal_50_bid    = models.StringField(label="Your bid")
    EnviroProtect_51_bid    = models.StringField(label="Your bid")
    SellChild_52_bid        = models.StringField(label="Your bid")
    HomoRights_53_bid       = models.StringField(label="Your bid")
    HomoChoice_54_bid       = models.StringField(label="Your bid")
    SexChild_55_bid         = models.StringField(label="Your bid")
    RaceHiring_56_bid       = models.StringField(label="Your bid")
    GayMarriage_57_bid      = models.StringField(label="Your bid")
    BlackLives_58_bid       = models.StringField(label="Your bid")
    HomoSex_59_bid          = models.StringField(label="Your bid")
    Israel_60_bid           = models.StringField(label="Your bid")
    FGM_61_bid              = models.StringField(label="Your bid")
    RightsWartime_62_bid    = models.StringField(label="Your bid")
    Litter_63_bid           = models.StringField(label="Your bid")
    Vote_64_bid             = models.StringField(label="Your bid")
    Jaywalk_65_bid          = models.StringField(label="Your bid")
    Shoplift_66_bid         = models.StringField(label="Your bid")
    CheatGame_67_bid        = models.StringField(label="Your bid")
    GiveSeat_68_bid         = models.StringField(label="Your bid")

    def get_current_statement(self):
        order = self.participant.vars['order']
        return order[self.participant.vars['current_statement']]