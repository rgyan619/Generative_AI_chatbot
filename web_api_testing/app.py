from flask import Flask
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from threading import Thread
from pygame import mixer
import pygame
import time
from moviepy.editor import VideoFileClip


app = Flask(__name__,static_folder='static',template_folder='templates')
 
@app.context_processor
def handle_context():
    return dict(os=os)

def path_exists(path):
    return os.path.exists(path)

@app.route('/')

@app.route('/display/')
# def display_video():
#     mixer.init()
#     sound = mixer.Sound("../audio/response.wav")
#     filename = "shravya.mp4"
#     if path_exists('./static/result_voice.mp4'):
#         filename = "result_voice.mp4"
#         # file_found = True
#         return render_template('display.html',filename=filename,t=sound.get_length())
#     else:
#         # image = 'shravya.png'
#         return render_template('display.html',filename=filename,t=1)


def display_video():
    filename="./result_voice.mp4"
    clip = VideoFileClip(filename)
    duration = clip.duration
    clip.close()
    return render_template('display.html',filename=filename,t=duration)


# main driver function
if __name__ == '__main__':
    app.run()