from tkinter import *
import time


def tell(line):
    Label(f, fg='grey', font=20, wraplength=500, justify=LEFT, text=line).pack(anchor='nw')
    # time.sleep(1)


class Character:
    def __init__(self, name: str):
        self.name = name
        self.color = 'green'
        # battle
        self.friendship_with_player = 0
        self.hp = 10
        self.defence = 0
        # knowledge
        self.phon = 0
        self.morph = 0
        self.synth = 0

    # for all
    def utter(self, line):
        lab = Label(f, fg=self.color, font=20, wraplength=500, justify=LEFT, text=self.name + ': ' + line)
        lab.pack(anchor='nw')
        # time.sleep(3)

    # npc only - unique for all
    def tell_skill_details(self):
        pass

    # unique for all
    def use_skill(self):
        pass

    def rise_friendship(self):
        self.friendship_with_player += 1


class Player:
    # inherited from all npc
    skills = []

    
#______________________________________________window for choice_____________________________________________________

root.bind('<Return>', dialogue)

def dialogue(event):
    def first_button:
        rise_friendship(MASHA)

    def second_button:
        tell_skill_details(MASHA)

    dial = Toplevel(window)
    dial['bg'] = 'LightCyan'
    dial.title('Что будем делать?')
    dial.geometry('200x150+500+100')
    dial.grab_set()
    question = tr.Label(dial, text = '???', bg = 'LightCyan', fg = 'SteelBlue', font = ('Times New Roman', 18))
    question.place(x = 76, y = 30)
    btn1 = tr.Button(dial, text = 'Подружимся!', bg = 'Orchid', fg = 'purple', command = first_button)
    btn1.place(x = 40, y = 80)
    btn2 = tr.Button(dial, text = 'Узнаем скиллы!', bg = 'SlateBlue', fg = 'Navy', command = second_button)
    btn2.place(x = 110, y = 80)
    

# _________________________________________________beginning_________________________________________________________
root = Tk()
root.geometry('800x500')
root.resizable(False, False)
root.title('имя позже придумаем')

canv = Canvas(root, width=800, height=500)

myscrollbar = Scrollbar(root, orient="vertical", command=canv.yview)
myscrollbar.pack(side="right", fill="y")

canv.configure(yscrollcommand=myscrollbar.set)

canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox('all')))

f = Frame(canv)
canv.create_window((0, 0), window=f, anchor='nw')
# _________________________________________________beginning_________________________________________________________

MASHA = Character('Masha')
tell('story')
for i in range(10):
    canv.after(300, tell('this is a story - jhyghwehb jkfjidhjbew nmdflgjhejwnmfd lkjihebwenmfsmdjkb hnemf ,ekjhfbnmkvjhfvb nmnvkjhfjmr kmsjbvfrmkjs bhvffnmrks fjrmv'))
    canv.after(300, MASHA.utter('I am Masha. I like iuhgyhjbjnk flfbhnksvjih ufjenkvfbhenk nvjsfkmcnfd jre grejk gewrug erukg erkugerwuguiewrg er ugre gu egue'))
# ___________________________________________________end_____________________________________________________________
canv.pack()
root.mainloop()
# ___________________________________________________end_____________________________________________________________
