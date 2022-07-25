import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


class Player(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.pack()
        mixer.init()

        self.current = 0
        self.paused = True
        self.played = False

        if os.path.exists("songs.pickle"):
            with open("songs.pickle","rb") as f:
                self.playlist=pickle.load(f)
        else:       
            self.playlist = []


        self.createFrame()
        self.track_screen()
        self.control_screen()
        self.tracklist_screen()
        

    def createFrame(self):
        self.track = tk.LabelFrame(self,text="Track",
                    font = ("times new roman",15 ,"bold"),
                    bg ="grey",fg="white",bd=5,relief=tk.GROOVE)
        self.track.configure(width=410,height=300)
        self.track.grid(row=0,column=0,padx=10) 

        self.trackList = tk.LabelFrame(self,text=f'Playlist : {len(self.playlist)}',
                                font = ("times new roman",15 ,"bold"),
                                bg ="grey",fg="white",bd=5,relief=tk.GROOVE)
        self.trackList.configure(width=190,height=600)
        self.trackList.grid(row=0,column=1,rowspan=14,pady=5)


        self.controls = tk.LabelFrame(self,text="Control",
                                font = ("times new roman",15 ,"bold"),
                                bg ="white",fg="white",bd=5,relief=tk.GROOVE)
        self.controls.configure(width=410,height=300)
        self.controls.grid(row=1,column=0,padx=10)

    def track_screen(self):     
        self.canvas = tk.Label(self.track,image=img)
        self.canvas.configure(width=400,height=240)
        self.canvas.grid(row=0,column=0)

        self.songtrack = tk.Label(self.track,font=("times new roman",15,"bold"),bg="black",fg="Dark Red")
        self.songtrack.configure(width=30,height=1)
        self.songtrack['text'] = "HSPlayer"
        self.songtrack.grid(row=1,column=0)


    def tracklist_screen(self):
        self.scrollbar = tk.Scrollbar(self.trackList,orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=0,rowspan=5,sticky="ns")

        self.list = tk.Listbox(self.trackList,selectmode=tk.SINGLE,
                            yscrollcommand=self.scrollbar.set,selectbackground="green")
        self.enumerate_()
        self.list.config(height=22)
        self.list.bind('<Double-1>',self.play_song)
        self.scrollbar.config(command=self.list.yview )
        self.list.grid(row=0,column=1,rowspan=5)
    
    def enumerate_(self):
        for song1,song2 in enumerate(self.playlist):
            self.list.insert(song1,os.path.basename(song2))

    def control_screen(self):
        self.loadTrack = tk.Button(self.controls,bg="black",fg="white",font =10)
        self.loadTrack["text"] = "Load Track"
        self.loadTrack["command"] = self.Song_finder
        self.loadTrack.grid(row=0,column=0,padx=10)

        self.prev = tk.Button(self.controls,image=prev)
        self.prev["command"] = self.prev_song
        self.prev.grid(row=0,column=1)

        self.pause = tk.Button(self.controls,image=pause)
        self.pause["command"] = self.pause_song
        self.pause.grid(row=0,column=2)

        self.next = tk.Button(self.controls,image=next_)
        self.next["command"] = self.next_song
        self.next.grid(row=0,column=3)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls,from_=0 ,to= 10,orient=tk.HORIZONTAL)
        self.slider["variable"] = self.volume
        self.slider["command"] = self.change_vol
        self.slider.set(5)
        mixer.music.set_volume(0.5)
        self.slider.grid(row=0,column=4)
        
    def Song_finder(self):
        self.found = []
        directory = filedialog.askdirectory()
        for root_,dir,song in os.walk(directory):
            for songs in song:
                if os.path.splitext(songs)[1] == ".mp3":
                    songs_path = (root_ + "/" + songs).replace("\\", "/")
                    self.found.append(songs_path) 
        with open("songs.pickle","wb") as f:
            pickle.dump(self.found,f)

        self.playlist = self.found
        self.trackList["text"] = f"Playlist : {len(self.playlist)}"
        self.list.delete(0,tk.END)
        self.enumerate_()
    
    def play_song(self,event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i,bg='white')
        mixer.music.load(self.playlist[self.current])

        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.songtrack["anchor"]  = "w" 
        self.songtrack["text"] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg="sky blue")
        mixer.music.play()

    
    def prev_song(self):
        if self.current >0:
            self.current -= 1
        else :
            self.current == 0
        self.list.itemconfigure(self.current+1,bg="white")
        self.play_song()
    
    def next_song(self):
        if self.current < len(self.playlist) -1:
            self.current +=1
        else :
            self.current == 0 
            self.play_song()
        self.list.itemconfigure(self.current-1,bg="white")
        self.play_song() 

    def pause_song(self):
        if self.paused == False:
            self.paused = True
            mixer.music.pause()
            self.pause["image"] = pause
        else :
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause["image"] = play

    def change_vol(self,event=None):
        self.vol=self.volume.get()
        mixer.music.set_volume(self.vol / 10)
     
#tarting of the main loop of the palyer


root = tk.Tk()
root.geometry("600x400")
root.wm_title("HSPlayer")

img = PhotoImage(file='images/music.gif')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')

 
HSPlayer = Player(master=root)
HSPlayer.mainloop()

