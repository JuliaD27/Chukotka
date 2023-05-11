from tkinter import *
from collections import deque
from dataclasses import dataclass


# _____________________________________________________classes__________________________________________________________

class Window_class:
    global fighter1
    global fighter2

    def __init__(self, size, title, text, btn_list: list, field_for_input=None):
        self.wind = Toplevel(root)
        self.wind['bg'] = 'LightCyan'
        self.wind.title(title)
        self.wind.geometry(size)
        self.wind.grab_set()
        self.wind.resizable(False, False)

        self.quest = Label(self.wind, text=text, bg='LightCyan', fg='SteelBlue',
                           font=('Times New Roman', 18))
        self.quest.pack(padx=95, pady=30)

        if field_for_input:
            self.field = Entry(self.wind)
            self.field.pack(anchor=NW)
            self.field.focus()

        self.frame = Frame(self.wind, width=600, height=50, bg='LightCyan')
        self.frame.pack()

        for btn in btn_list:
            Button(self.frame, text=btn[0], bg='Plum', fg='purple', command=btn[1]).pack(side=LEFT, padx=10)

    def crash(self):
        self.wind.destroy()


class Character:
    def __init__(self, name: str, color='green'):
        self.name = name
        self.color = color

    # for all
    def utter(self, line):
        lab = Label(f, fg=self.color, font=20, wraplength=500, justify=LEFT, text=self.name + ': ' + line)
        Q.append(lab)

    def __str__(self):
        return self.name


class Monster(Character):
    def __init__(self, name: str, hp=0):
        self.name = name
        self.color = 'red'
        self.hp = hp


class Friends(Character):
    heal = 0
    shield = 0
    buff = 0
    kill = 0
    skill = ''
    # battle
    friendship_with_player = 0
    atk = 2
    hp = 10
    is_alive = True
    # knowledge
    morph = 0
    sem = 0
    synth = 0

    def rise_friendship(self):
        self.friendship_with_player += 1
        
    def down_friendship(self):
        self.friendship_with_player -= 1

    def take_academic_leave(self):
        self.is_alive = False


class Player(Friends):
    skills = []


# ___________________________________________________main functions____________________________________________________


def OUT():
    global canv
    global fighter1
    global fighter2
    if Q:
        line = Q.popleft()
        line_text = line['text']
        canv.configure(height=canv.winfo_height() + 20)
        if line_text[-1] == '@':
            # вызов окна с вводом имени
            line.config(text=line_text[:-1])
            line.pack(anchor='nw')
            player_name("$? Отличное имя!")
        if line_text[-1] == '^':
            # вызов окна для боя
            function_index = int(line_text[-2])
            line.config(text=line_text[:-3])
            line.pack(anchor='nw')
            if function_index == 1:
                # выбор союзников
                choose_your_fighter('$ выбраны для боя')
            elif function_index == 2:
                # выбор активного персонажа
                choose_active()
            elif function_index == 3:
                # выбор действия player
                choose_skill_for_player()
        if line_text[-1] == '%':
            # начало боя
            function_index = int(line_text[-2])
            line.config(text=line_text[:-3])
            line.pack(anchor='nw')
            if function_index == 1:
                FIGHT_with_morphology()
        else:
            line.pack(anchor='nw')
        if line_text[-1] == '*':
            function_index = int(line_text[-2])
            line.config(text=line_text[:-3])
            line.pack(anchor='nw')
            if function_index == 1:
                fedya_question()
            if function_index == 2:
                answer_back()
        canv.yview_scroll(19, 'units')
    else:
        STORY()


def tell(line):
    Q.append(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT, text=line))


# _____________________________________________________battle_________________________________________________________


def FIGHT_with_morphology():
    global fighter1
    global fighter2
    global chosen
    global base
    global buff_count
    global buff_count_player
    global shield_count
    global shield_count_player
    global current_buff
    global current_player_buff
    global current_shield
    global current_player_shield
    global chosen_player_skill
    global stage
    global stage_save_story
    global stage_fight

    if stage_fight == 'choose active':
        print('i m in choose active')
        stage_fight = 'friends take action'
        tell('Вы с друзьями переглядываетесь...^2^')
    elif stage_fight == 'friends take action':
        base = 1
        print(f'i have chosen {chosen}')
        if chosen.name == 'Даня':
            current_buff = chosen.buff + chosen.morph
            buff_count = 2
            stage_fight = 'damage'
        elif chosen.name == 'Лиза':
            fighter1.hp += chosen.heal + chosen.morph
            fighter2.hp += chosen.heal + chosen.morph
            PLAYER.hp += chosen.heal + chosen.morph
            stage_fight = 'damage'
        elif chosen.name == 'Федя':
            print('i m in fedya')
            current_shield = chosen.shield + chosen.morph
            shield_count = 2
            stage_fight = 'damage'
        elif chosen.name == 'Моня':
            base = chosen.kill + chosen.morph
            stage_fight = 'damage'
        else:
            stage_fight = 'player take action'
            tell('Вы вспоминаете, все, чему научили вас друзья.^3^')
    elif stage_fight == 'player take action':
        if chosen_player_skill == 'Подлечить команду':
            fighter1.hp += chosen.heal + chosen.morph
            fighter2.hp += chosen.heal + chosen.morph
            PLAYER.hp += chosen.heal + chosen.morph
        elif chosen_player_skill == 'Подбодрить всех':
            current_player_buff = chosen.buff + chosen.morph
            buff_count_player = 2
        elif chosen_player_skill == 'Защитить друзей':
            current_player_shield = chosen.shield + chosen.morph
            shield_count_player = 2
        else:
            base = chosen.kill + chosen.morph
        stage_fight = 'damage'
    elif stage_fight == 'damage':
        damage_dealt = base + chosen.atk
        if buff_count > 0:
            damage_dealt += current_buff
            buff_count -= 1
        if buff_count_player > 0:
            damage_dealt += current_player_buff
            buff_count_player -= 1
        damage_taken = 4
        if shield_count >= 0:
            damage_taken -= current_shield
            shield_count -= 1
        if shield_count_player > 0:
            damage_taken -= current_player_shield
            shield_count_player -= 1
        tell(f'{chosen.name} наносит Морфологии {damage_dealt} урона!!')
        MORPH.hp -= damage_dealt
        if MORPH.hp <= 0:
            tell('Морфология испуганно прижимает уши в форме различных суффиксов. Затем, она, поджав окончание ('
                 'хвост), убегает.')
            stage = stage_save_story
            stage_fight = None
            return
        tell(f'Морфология смотрит на обидчика. {chosen.name} получает {damage_taken} урона.')
        chosen.hp -= damage_taken
        if chosen.hp <= 0:
            tell(f'{chosen.name} больше не может выдержать. {chosen.name} уходит в академ.')
            chosen.is_alive = False
        stage_fight = 'choose active'
    FIGHT_with_morphology()


# _________________________________________________BEGINNING>________________________________________________________
root = Tk()
root.geometry('800x600')
root.resizable(False, False)
root.title('имя позже придумаем')

frm1 = LabelFrame(root, width=800, height=500)

canv = Canvas(frm1, width=800, height=500)
canv.pack(fill="both", expand=True)

scrlbar = Scrollbar(canv, orient="vertical", command=canv.yview)
scrlbar.pack(side="right", fill="y")

canv.configure(yscrollcommand=scrlbar.set)

canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox('all')))

f = Frame(canv, width=800, height=500)
canv.create_window((0, 0), window=f, anchor='nw')

frm2 = Frame(root, width=800, height=70)
btn = Button(frm2, text='Продолжить', bg='PaleGreen', fg='ForestGreen', command=OUT)

Q = deque()
LISA = Friends('Лиза', 'green')
LISA.heal = 4
LISA.skill = 'Подлечить команду'
LISA.synth = 1
DAN = Friends('Даня', 'blue')
DAN.buff = 2
DAN.skill = 'Подбодрить всех'
DAN.morph = 1
MONYA = Friends('Моня', 'red')
MONYA.kill = 2
MONYA.skill = 'Хорошенько вдарить!'
MONYA.synth = 1
FEDYA = Friends('Федя', 'orange')
FEDYA.shield = 2
FEDYA.skill = 'Защитить друзей'
FEDYA.sem = 1
PLAYER = Player('=', 'black')
IB = Character('Инна Бисер', 'HotPink')
YL = Character('Юрий Ландыш', 'purple')

FILLER = Friends('filler', 'black')
fighter1 = FILLER
fighter2 = FILLER
chosen = FILLER
base = 1
buff_count = 0
buff_count_player = 0
shield_count = 0
shield_count_player = 0
current_buff = 0
current_player_buff = 0
current_shield = 0
current_player_shield = 0
chosen_player_skill = ''
fight_with_morph_finished = False
fight_with_synth_finished = False
fight_with_sem_finished = False
MORPH = Monster('Морфология', 20)
SYNTH = Monster('Синтаксис', 150)
SEM = Monster('Семантика', 200)


# ______________________________________________window functions_____________________________________________________


def player_name(text_out):  # это строка, которая реагирует на введённое имя
    def button():
        name = info.field.get()
        PLAYER.name = name
        info.crash()
        # в принимаемой строке $ заменяется введённым именем
        Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                           text=f"{text_out.replace('$', name)}"))

    info = Window_class(size='350x150+500+100', title='Ввод', text='Имя...', field_for_input=True,
                        btn_list=([('Принять!', button)]))


def choose_your_fighter(fighters):
    global fighter1, fighter2, button_chosen
    button_chosen = 0
    fighter1 = ''
    fighter2 = ''

    def choose_lisa_for_fight():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = LISA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = LISA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('$', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def choose_dan_for_fight():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = DAN
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = DAN
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('$', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def choose_fedya_for_fight():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = FEDYA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = FEDYA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('$', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def choose_monya_for_fight():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = MONYA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = MONYA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('$', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    fight_choice = Window_class(size='500x190+500+100', title='Пора в бой!', text='Кого возьмешь в команду?',
                                btn_list=([('Лиза', choose_lisa_for_fight), ('Федя', choose_fedya_for_fight),
                                           ('Даня', choose_dan_for_fight), ('Моня', choose_monya_for_fight)]))


def choose_active():
    global fighter1
    global fighter2
    global chosen

    def choose_fighter1_as_active():
        global chosen
        chosen = fighter1
        active_choice.crash()

    def choose_fighter2_as_active():
        global chosen
        chosen = fighter2
        active_choice.crash()

    def choose_player_as_active():
        global chosen
        chosen = PLAYER
        active_choice.crash()

    print('i m choosing')

    active_choice = Window_class(size='500x190', title='', text='Выберете персонажа, который будет действовать',
                                 btn_list=([(fighter1.name, choose_fighter1_as_active),
                                            (fighter2.name, choose_fighter2_as_active),
                                            (PLAYER.name, choose_player_as_active)]))


def choose_skill_for_player():
    global chosen_player_skill

    def choose_first_skill():
        global chosen_player_skill
        chosen_player_skill = PLAYER.skills[0]
        w.crash()

    def choose_second_skill():
        global chosen_player_skill
        chosen_player_skill = PLAYER.skills[1]
        w.crash()

    def choose_third_skill():
        global chosen_player_skill
        chosen_player_skill = PLAYER.skills[2]
        w.crash()

    def choose_fourth_skill():
        global chosen_player_skill
        chosen_player_skill = PLAYER.skills[3]
        w.crash()

    if len(PLAYER.skills) == 2:
        w = Window_class(size='500x190', title='', text='Выберете, что вы будете делать',
                         btn_list=([(PLAYER.skills[0], choose_first_skill),
                                    (PLAYER.skills[1], choose_second_skill)]))
    elif len(PLAYER.skills) == 3:
        w = Window_class(size='500x190', title='', text='Выберете, что вы будете делать',
                         btn_list=([(PLAYER.skills[0], choose_first_skill),
                                    (PLAYER.skills[0], choose_second_skill),
                                    (PLAYER.skills[1], choose_third_skill)]))
    else:
        w = Window_class(size='500x190', title='', text='Выберете, что вы будете делать',
                         btn_list=([(PLAYER.skills[0], choose_first_skill),
                                    (PLAYER.skills[1], choose_second_skill),
                                    (PLAYER.skills[2], choose_third_skill),
                                    (PLAYER.skills[3], choose_fourth_skill)]))
        
#_________________________________________________interactions_______________________________________________________

def fedya_question():
    
    def fed_privet():
        FEDYA.utter('О, ты запомнил мое имя!')
        FEDYA.rise_friendship()
        call.crash()

    def fed_zdrv():
        FEDYA.utter('Не называй меня так!*2*')
        FEDYA.down_friendship()
        call.crash()

    call = Window_class(size='500x190+500+100', title='Надо позвать Федю', text='Как позовёшь Федю?',
                        btn_list=([('Федя, привет!', fed_privet), ('Фердинанд, здравствуй!', fed_zdrv)]))
    
def answer_back():

    def sorry():
        FEDYA.utter('Ладно, проехали')
        FEDYA.rise_friendship()
        answer.crash()

    def not_sorry():
        FEDYA.utter(f'Ну и иди лесом, {PLAYER.name}!')
        FEDYA.down_friendship()
        answer.crash()

    answer = Window_class(size='500x190+500+100', title='', text='Что ответить?',
                          btn_list=([('Прости, больше не буду', sorry), ('Всё равно будешь Фердинандом', not_sorry)]))


# _________________________________________________<BEGINNING________________________________________________________

stage_fight = None
stage_save_story = 0
stage = 1


def STORY():
    global stage
    global stage_save_story
    global stage_fight
    if stage < 0:
        return
    if stage == 1:
        tell('это история 4 ребят и вас')
        # tell('это Лиза Андреева')
        # LISA.utter('здравствуйте')
        # tell('это Даня Михаэль')
        # DAN.utter('приввввввввввеееееееееееет роакупущ шкгсаьку чгшсарсь шучфугрч ашщйгкя ьашыкпаьшйк нщчпаькйайц шщкчп'
        #           'аькушнп аьшапйуц шгчпцгшап ьцгшщачпькйшща пчтуцншщапчкща')
        # tell('это Федя Сосся')
        # FEDYA.utter("Я Фердинанд")
        # tell('это Моня Мохская')
        # MONYA.utter('йоу')
        # tell("познакомимсся также с Инной Бисер и Юрием Ландышем")
        # IB.utter('здравствуйте детишки')
        # YL.utter('здравствуйте детишки')
        tell('теперь введите ваше имя:@')
    elif stage == 2:
        tell('Подошёл Федя*1*')
    elif stage == 3:
        tell('Пора в бой!^1^')
    elif stage == 4:
        tell(f'{fighter1} и вы стали ближе!')
        tell(f'{fighter2} и вы стали ближе!')
        fighter1.friendship_with_player += 1
        if fighter1.friendship_with_player == 1:
            PLAYER.heal += fighter1.heal // 2
            PLAYER.buff += fighter1.buff // 2
            PLAYER.shield += fighter1.shield // 2
            PLAYER.kill += fighter1.kill // 2
            PLAYER.skills.append(fighter1.skill)
        fighter2.friendship_with_player += 1
        if fighter2.friendship_with_player == 1:
            PLAYER.heal += fighter2.heal // 2
            PLAYER.buff += fighter2.buff // 2
            PLAYER.shield += fighter2.shield // 2
            PLAYER.kill += fighter2.kill // 2
            PLAYER.skills.append(fighter2.skill)
        stage_save_story = stage + 1
        stage = -1
        stage_fight = 'choose active'
        tell('Морфология наступает...%1%')
        return
    elif stage == 5:
        tell('Вы победили!!')
    stage += 1


# ___________________________________________________END>_____________________________________________________________
frm1.pack(fill="both", expand=True)
frm2.pack(anchor='s')
btn.pack(anchor='ne', padx=10, pady=10)
root.mainloop()
# ___________________________________________________<END_____________________________________________________________
