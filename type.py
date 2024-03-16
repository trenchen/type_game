from tkinter import *
import random

word_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
winWidth = 800
winHeight = 800

class down_word():
    def __init__(self, Pcanvas, wordRange, speed):
        self.canvas = Pcanvas
        self.speed = speed
        self.word = word_list[random.randint(0, wordRange-1)]
        self.id = self.canvas.create_text(random.randint(50, winWidth-100), 0, text=self.word, font=("Courier New", 12), fill='blue')

    def move_down(self):
        #print("speed:"+str(self.speed))
        self.canvas.move(self.id, 0, self.speed)
        

class my_canvas():
    def __init__(self, Pwin, wordRange):
        self.parentW = Pwin
        self.gameRunning = False
        self.gameover = False
        #self.createTime = 10
        self.scores = 0
        self.wordspeed = 5
        self.ConcuentWords = 1
        self.words = []
        self.wordRange = wordRange
        self.canvas = Canvas(Pwin, width=winWidth, height=winHeight/2, bg='pink')
        self.canvas.pack()
        self.canvas.bind("<Key>", self.check_input)
        self.canvas.focus_set()
        self.score_label = self.canvas.create_text(35, 10, text="Score: 0", font=("Courier New", 10), fill="white")
        
    def check_input(self, event):
        if self.gameRunning == True:
            input = event.char.upper()
            #print('input:'+input)
            if len(self.words) > 0 and input == self.words[0].word:
                #print('word match')
                self.canvas.delete(self.words[0].id)
                del self.words[0]
                self.scores += 5
                self.canvas.itemconfig(self.score_label, text="Score: "+str(self.scores))
                if len(self.words) > 0 :
                    self.canvas.itemconfig(self.words[0].id, fill="red")
                #check level
                if self.scores % 50 == 0:
                    self.wordspeed += 2
                    for Sword in self.words:
                        Sword.speed = self.wordspeed
                if self.scores % 100 == 0:
                    self.ConcuentWords += 1
                
                    
        
    def run_game(self):
        if self.gameRunning == True:
            #create word add to list
            #if len(self.words) == 0 or len(self.words) < self.ConcuentWords and self.createTime > 4:
            if len(self.words) == 0 or len(self.words) < self.ConcuentWords:
                self.words.append(down_word(self.canvas, self.wordRange, self.wordspeed))
                #self.createTime = 0
                if len(self.words) == 1:
                    self.canvas.itemconfig(self.words[0].id, fill="red")
            #move down
            for Sword in self.words:
                Sword.move_down()
                x1,y1,x2,y2 = self.canvas.bbox(self.words[0].id)
                if y2 > winHeight/2:
                    self.canvas.create_text(winWidth/2, winHeight/4, text="Game over", fill='red', font=("Courier New", 24), tag="game_over_text")
                    self.gameRunning = False
                    self.gameover = True
                    break
            #next run
            #self.createTime += 1
            self.parentW.after(500, self.run_game)
        
    def start_game(self):
        if self.gameover == False and self.gameRunning == False:
            self.gameRunning = True
            print('my canvas start')
            self.parentW.after(10, self.run_game)

    def stop_game(self):
        if self.gameRunning == True:
            self.gameRunning = False
            print('my canvas stop')

    def restart_game(self):
        self.gameRunning = False
        #clear canvas content
        for Sword in self.words:
            self.canvas.delete(Sword.id)
        self.canvas.itemconfig(self.score_label, text="Score: 0")
        self.canvas.delete("game_over_text")
        #init value
        del self.words[0:len(self.words)]
        self.scores = 0
        self.wordspeed = 5
        self.ConcuentWords = 1
        self.gameover = False
        self.parentW.after(1000, self.start_game)
        

def start_game_page(Pwin, maxword):
    print('maxword:')
    print(maxword)
    
    #clear 
    widgets = Pwin.winfo_children()
    for widget in widgets:
        widget.destroy()

    #new page
    mycanvas = my_canvas(Pwin, maxword)
    buttonStart = Button(Pwin, text='start game', bg='yellow', command=mycanvas.start_game)
    buttonStart.pack(side='top', fill='x', pady=5)
    buttonStop = Button(Pwin, text='stop game', bg='yellow', command=mycanvas.stop_game)
    buttonStop.pack(side='top', fill='x', pady=5)
    buttonRestart = Button(Pwin, text='restart game', bg='yellow', command=mycanvas.restart_game)
    buttonRestart.pack(side='top', fill='x', pady=5)


def menu_page(Pwin):
    buttonG = Button(Pwin, text='A~G', bg='yellow', command=lambda:start_game_page(Pwin, 7))
    buttonG.pack(side='top', fill='x', pady=5)
    buttonL = Button(Pwin, text='A~L', bg='yellow', command=lambda:start_game_page(Pwin, 12))
    buttonL.pack(side='top', fill='x', pady=5)
    buttonT = Button(Pwin, text='A~T', bg='yellow', command=lambda:start_game_page(Pwin, 20))
    buttonT.pack(side='top', fill='x', pady=5)
    buttonZ = Button(Pwin, text='A~Z', bg='yellow', command=lambda:start_game_page(Pwin, 26))
    buttonZ.pack(side='top', fill='x', pady=5)

window = Tk()
window.title("type game")
window.minsize(width=winWidth, height=winHeight)
window.resizable(width=False, height=False)
menu_page(window)
window.mainloop()
