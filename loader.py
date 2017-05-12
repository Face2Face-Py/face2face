# -*- coding: utf-8 -*-
import Tkinter as tk
import time
from threading import Thread

class Screen:
    def __init__(self):
        self.btnfn = None
        self.startTrigger = False
        print('Screen Started')
        self.window = tk.Tk()
        self.window.geometry('250x355')
        self.window.title('face2face')
        self.window.resizable(0, 0)
        for i in range(6):
            self.window.rowconfigure(i, minsize=50)

        self.window.columnconfigure(0, minsize=250)
        self.title = tk.Label(self.window)
        self.title.configure(text='face²face',fg='white',bg='#3b5998')
        self.title.configure(font=('calibri', 15, 'bold'))
        self.title.grid(row=0, rowspan=1, column=0, sticky='nsew')
        self.title2 = tk.Label(self.window)
        self.title2.configure(text= '👍 ❤️ 😂 😯 😢 😡',fg='white',bg='#8b9dc3')
        self.title2.configure(font=('calibri', 15, 'bold'))
        self.title2.grid(row=1, rowspan=1, column=0, sticky='nsew')
        self.warningLabel = tk.Label(self.window)
        self.warningLabel.configure(text='WARNING:\n\n This will open your camera \n and close Google Chrome',fg='red',bg='#f7f7f7')
        self.warningLabel.configure(font=('calibri', 12,'bold'))
        self.warningLabel.grid(row=2, rowspan=2, column=0, sticky='nsew')
        self.infoLabel = tk.Label(self.window)
        self.infoLabel.configure(text='Click on the button\n bellow to begin'.upper(),bg='#dfe3ee')
        self.infoLabel.configure(font=('calibri', 12,'bold'))
        self.infoLabel.grid(row=4, rowspan=2, column=0, sticky='nsew')
        self.startButton = tk.Button(self.window)
        self.startButton.configure(text='START', command=self.StartScript)
        self.startButton.configure(font=('pixelmix', 11))
        self.startButton.grid(row=6, rowspan=1, column=0, sticky='nsew')
        self.exitButton = tk.Button(self.window)
        self.exitButton.configure(text='EXIT', command=self.on_closing)
        self.exitButton.configure(font=('pixelmix', 11))
        self.exitButton.grid(row=7, rowspan=1, column=0, sticky='nsew')

    def updateText(self,txt):
        self.infoLabel.configure(text=txt.upper())


    def setFn(self,fn):
        self.btnfn = fn

    def onScriptStopped(self):
        self.startTrigger = False

    def StartScript(self):
        if not self.startTrigger:
            self.startTrigger = True
            # mainThread = Thread(target=self.btnfn)
            self.btnfn()
            # mainThread.start()

		# self.infoLabel.configure(text='Click "Close Connection" to\n\nstop accepting new players'.upper())
		# self.infoLabel.configure(font=('pixelmix', 8))
        # self.infoLabel.grid(row=2, rowspan=2, column=0, sticky='nsew')

    def stopAcpt(self):
        self.server.stopAccepting()
        self.StartWindow()

    def StartWindow(self):
        self.infoLabel.configure(text='Good Luck'.upper())
        self.infoLabel.configure(font=('pixelmix', 12))
        self.infoLabel.grid(row=2, rowspan=2, column=0, sticky='nsew')

        self.bot_start = tk.Button(self.window)
        self.bot_start.configure(text='START GAME', command=self.CommandStart)
        self.bot_start.configure(font=('pixelmix', 11))
        self.bot_start.grid(row=4, rowspan=2, column=0, sticky='nsew')

    def CommandStart(self):
        self.server.startGame()
        self.window.destroy()

    def start(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        self.window.destroy()
        raise SystemExit
