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
        self.pause = False
        self.song_check = ''

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
        self.back_btn = Button(self.frame_btns, image=self.back_img, command=self.back)
        self.back_btn.grid(row=0, column=1)

        self.play_btn = Button(self.frame_btns, image=self.play_img, command=self.start_pause)
        self.play_btn.grid(row=0, column=2)

        self.forward_btn = Button(self.frame_btns, image=self.forward_img, command=self.forward)
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

        self.tab_file_add = Menu(self.tab_file, tearoff=0)
        self.tab_file_remove = Menu(self.tab_file, tearoff=0)
        self.tab_file.add_cascade(label='add music', menu=self.tab_file_add)
        self.tab_file.add_cascade(label='remove music', menu=self.tab_file_remove)

        self.tab_file_add.add_command(label='add music folder', command=self.add_music_folder)
        self.tab_file_add.add_command(label='add one music', command=self.add_one_music)
        self.tab_file_add.add_command(label='add many music', command=self.add_many_music)

        self.tab_file_remove.add_command(label='remove all musics', command=self.remove_all_music)
        self.tab_file_remove.add_command(label='remove selected music', command=self.remove_selected_music)

    def start_pause(self):
        self.lbl.grid_forget()
        if self.flg_play_pause and self.song_listbox.get(ACTIVE) != '':
            self.flg_play_pause = False
            self.play_btn.config(image=self.pause_img)
            try:
                name_music = self.song_listbox.get(ACTIVE)
                if name_music in self.list_avalible_music:
                    path_index = self.list_avalible_music.index(name_music)
                self.lbl.config(text=name_music)
                self.lbl.pack(anchor=N)
                music_volume = self.volume_btn.get()/100
                if self.pause and (self.song_listbox.get(ACTIVE) == self.song_check):
                    pygame.mixer.music.unpause()
                else:
                    self.song_check = self.list_avalible_music[path_index]
                    pygame.mixer.music.load(self.list_avalible_path[path_index])
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(loops=self.flg_loop)
            except:
                pass
        elif not self.flg_play_pause and self.song_listbox != '':
            self.flg_play_pause = True
            self.lbl.grid_forget()
            self.play_btn.config(image=self.play_img)
            try:
                pygame.mixer.music.pause()
                self.pause = True
            except:
                pass

    def forward(self):
        next_music_index = self.song_listbox.index(ACTIVE) + 1
        self.song_listbox.select_clear(0,END)
        self.song_listbox.activate(next_music_index)
        self.song_listbox.select_set(ACTIVE)

    def back(self):
        back_music_index = self.song_listbox.index(ACTIVE) - 1
        self.song_listbox.select_clear(0,END)
        self.song_listbox.activate(back_music_index)
        self.song_listbox.select_set(ACTIVE)
    
    def toggle_loop(self):
        if self.flg_play_pause:
            if self.flg_loop == -1:
                self.flg_loop = 0
                self.loops_btn.config(image=self.noloop_img)
            else:
                self.flg_loop = -1
                self.loops_btn.config(image=self.loop_img)

    def toggle_volume(self):
        music_volume = self.volume_btn.get()/100
        pygame.mixer.music.set_volume(music_volume)
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
                    if ((item[-4:] == '.mp3') or (item[-4:] == '.wav')) and (item not in self.list_avalible_music):
                        self.song_listbox.insert(END,item)
                        self.list_avalible_music.append(item)
                        path = self.music_list + '/' + item
                        self.list_avalible_path.append(path)
                    else:
                        pass
        except:
            pass

    def add_one_music(self):
        try:
            self.music_select = filedialog.askopenfilename(initialdir='music', title='select one music', filetypes=(('music file', '*.mp3'), ('music file', '*.wav')))
            self.music_select_2 = os.path.basename(self.music_select)
            if (self.music_select_2 not in self.list_avalible_music) and (self.music_select_2 != ''):
                self.song_listbox.insert(END, self.music_select_2)
                self.list_avalible_music.append(self.music_select_2)
                self.list_avalible_path.append(self.music_select)
        except:
            pass

    def add_many_music(self):
        music_many_2 = []
        self.music_many = filedialog.askopenfilenames(initialdir='music', title='select many music', filetypes=(('music files', '*.mp3'), ('music files', '*.wav')))
        for item in self.music_many:
            music_many_2.append(os.path.basename(item))
        for index, item in enumerate(music_many_2):
            if item not in self.list_avalible_music:
                self.song_listbox.insert(END, item)
                self.list_avalible_music.append(item)
                self.list_avalible_path.append(self.music_many[index])

    def remove_selected_music(self):
        pygame.mixer.music.stop()
        self.pause = False
        index = self.song_listbox.index(ACTIVE)
        self.list_avalible_music.pop(index)
        self.list_avalible_path.pop(index)
        self.song_listbox.delete(ACTIVE)
        self.song_listbox.select_set(ACTIVE)
        self.flg_play_pause = True
        self.play_btn.config(image=self.play_img)

    def remove_all_music(self):
        pygame.mixer.music.stop()
        self.pause = False
        self.list_avalible_music.clear()
        self.list_avalible_path.clear()
        self.song_listbox.delete(0,END)
        self.flg_play_pause = True
        self.play_btn.config(image=self.play_img)

App().mainloop()