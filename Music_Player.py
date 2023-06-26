from tkinter import *
from tkinter import filedialog, PhotoImage
import pygame, os


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x500')
        self.title('Music Player')
        self.config(bg='#00DDFD')

        pygame.init()

        # frames
        self.frame_listbox = Frame(self)
        self.frame_btns = Frame(self, border=3, relief='groove')
        self.frame_listbox.pack()
        self.frame_btns.pack(pady=20)

        # listbox
        self.song_listbox = Listbox(self.frame_listbox, width=90, height=18, bg='lightgreen', fg='black')
        self.song_listbox.pack()
        
        # variables
        self.flg_play_pause = True # true -> play /// false -> pause
        self.flg_volume_show = False # true -> show /// false -> hide
        self.flg_loop = 0
        self.list_avalible_music = []
        self.list_avalible_path = []

        self.create()

    def create(self):
        
        # find images
        self.play_img = PhotoImage(file='photo/play_img.png')
        self.pause_img = PhotoImage(file='photo/pause_img.png')
        self.forward_img = PhotoImage(file='photo/forward_img.png')
        self.back_img = PhotoImage(file='photo/back_img.png')
        self.loop_img = PhotoImage(file='photo/loop_img.png')
        self.noloop_img = PhotoImage(file='photo/noloop_img.png')
        self.volume_img = PhotoImage(file='photo/volume_img.png')
        self.volumeUp_img = PhotoImage(file='photo/volumeUp_img.png')

        # create btns
        self.back_btn = Button(self.frame_btns, image=self.back_img)
        self.back_btn.grid(row=0, column=1)

        self.play_btn = Button(self.frame_btns, image=self.play_img, command=self.start_pause)
        self.play_btn.grid(row=0, column=2)

        self.forward_btn = Button(self.frame_btns, image=self.forward_img)
        self.forward_btn.grid(row=0, column=3)

        self.loops_btn = Button(self.frame_btns, image=self.noloop_img, command=self.toggle_loop)
        self.loops_btn.grid(row=0, column=4)

        self.volume_show_btn = Button(self.frame_btns, image=self.volume_img, command=self.toggle_volume)
        self.volume_show_btn.grid(row=0, column=5)

        self.volume_btn = Scale(self.frame_btns, orient=HORIZONTAL)
        self.volume_btn.set(50)

        self.lbl = Label(self, font='black')

        # create menu
        self.tab = Menu(self)
        self.config(menu=self.tab)

        self.tab_file = Menu(self.tab, tearoff=0)
        self.tab.add_cascade(label='File', menu=self.tab_file)
        self.tab_file.add_command(label='add music folder', command=self.add_music_folder)

    def start_pause(self):
        self.lbl.grid_forget
        if self.flg_play_pause:
            self.flg_play_pause = False
            self.play_btn.config(image=self.pause_img)
            # try:
            name_music = self.song_listbox.get(ACTIVE)
            if name_music in self.list_avalible_music:
                path_index = self.list_avalible_music.index(name_music)
            self.lbl.config(text=name_music)
            self.lbl.pack(anchor=N)
            music_volume = self.volume_btn.get()/100
            pygame.mixer.music.load(self.list_avalible_path[path_index])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(loops=self.flg_loop)
            # except:
            #     pass
        else:
            self.flg_play_pause = True
            self.lbl.grid_forget
            self.play_btn.config(image=self.play_img)
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def toggle_loop(self):
        if self.flg_loop == -1:
            self.flg_loop = 0
            self.loops_btn.config(image=self.noloop_img)
        else:
            self.flg_loop = -1
            self.loops_btn.config(image=self.loop_img)

    def toggle_volume(self):
        if self.flg_volume_show:
            self.flg_volume_show = False
            self.volume_show_btn.config(image=self.volume_img)
            self.volume_btn.grid_forget()
        else:
            self.flg_volume_show = True
            self.volume_show_btn.config(image=self.volumeUp_img)
            self.volume_btn.grid(row=0, column=10)

    def add_music_folder(self):
        try:
            self.music_list = filedialog.askdirectory(initialdir='music', title='select one folder')
            self.music_list_2 = os.listdir(self.music_list)
            for item in self.music_list_2:
                    if (item[-4:] == '.mp3') or (item[-4:] == '.wav'):
                        self.song_listbox.insert(END,item)
                        self.list_avalible_music.append(item)
                        path = self.music_list + '/' + item
                        self.list_avalible_path.append(path)
                    else:
                        pass
        except:
            pass

App().mainloop()