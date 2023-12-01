""" ttkVideo: Python module for playing videos (with sound) inside tkinter Label widget using Pillow and imageio
works best & fast on small size videos however takes few seconds of time for larger videos files
Copyright © 2020 vishal sharma vishalsharma659615@gmail.com
Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md
"""
try:
    import Tkinter as tk  # for Python2 (although it has already reached EOL)
except ImportError:
    import tkinter as tk  # for Python3
import threading,os,time,pygame,ffmpeg,imageio
from PIL import Image, ImageTk


class Ttkvideos():
    """
        Main class of TtkVideos. Handles loading and playing
        the video inside the selected label.

        :keyword path:
            Path of video file
        :keyword label:
            Name of label that will house the player
        :param loop:
            If equal to 0, the video only plays once,
            if not it plays in an infinite loop (default 0)
        :param size:
            Changes the video's dimensions (2-tuple,
            default is 640x360)

    """

    def __init__(self, path, label, loop=0, size=(640, 360)):
        self.path = path
        self.label = label
        self.loop = loop
        self.size = size

    def prgress(self):
        from progress.bar import Bar

        with Bar('Processing...') as bar:
            for i in range(100):
                time.sleep(3)
                bar.next()
    def create_audio(self,path,thread):
        print("------------------This might take some time to start please wait------------------")
        thread3=threading.Thread()
        thread3.start()
        if "play_current.mp3" in os.listdir(os.getcwd()):
            os.remove("play_current.mp3")
            time.sleep(2)
        ffmpeg.input(path).output("play_current.mp3", loglevel="quiet").run()
        t1=time.time()
        thread.start()# video player thread initialising
# audio file thread playing
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("play_current.mp3")
        t2=time.time()
        pygame.mixer.music.play()
        print("difference",t2-t1)
    def load(self, path, label, loop):
        """
            Loads the video's frames recursively onto the selected label widget's image parameter.
            Loop parameter controls whether the function will run in an infinite loop
            or once.
        """
        frame_data = imageio.get_reader(path)

        if loop == 1:
            while True:
                for image in frame_data.iter_data():
                    time.sleep(0.002016782760620117)
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(self.size))
                    label.configure(image=frame_image)
                    label.image = frame_image

        else:
            for image in frame_data.iter_data():
                frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(self.size))
                label.config(image=frame_image)
                label.image = frame_image


    def play(self):
        """
            Creates and starts a thread as a daemon that plays the video by rapidly going through
            the video's frames.
        """
        thread = threading.Thread(target=self.load, args=(self.path, self.label, self.loop))
        thread_audio=threading.Thread(target=self.create_audio,args=(self.path,thread))
        thread_audio.start()
        thread.daemon = 1
