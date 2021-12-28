
from tkinter import filedialog, font
from typing import List
from moviepy.audio.AudioClip import concatenate_audioclips
import numpy as np  # for numerical operations
import math
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, CompositeAudioClip

# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()
# Set the geometry of tkinter frame

win.geometry("700x350")
audio_list = ["nothing"]
vid_list = ["stuff"]

def open_file():
   file_path = filedialog.askopenfilename(parent=win, title='Choose a File')
   audio_list.append(file_path)

def open_file2():
   file_path = filedialog.askopenfilename() 
   vid_list.append(file_path)

def files_Added():
	if(vid_list[1]) != None:
		label3.config(text= "Video File 1:" + vid_list[1])
	if(vid_list[2]) != None:
		label4.config(text= "Video File 2:" + vid_list[2])
	if(vid_list[3]) != None:
		label5.config(text= "Middle Camera Video File:" + vid_list[3])
	if(audio_list[1]) != None:
		label1.config(text= "Audio File 1:" + audio_list[1])
	if(audio_list[2]) != None:
		label2.config(text= "Audio File 2:" + audio_list[2])			
	



label = Label(win, text="Select the video and audio files from your podcast", font=('Aerial 11'))
label.pack(side = TOP)


label1 = Label(win, text = "Audio File 1: ", font =('Aerial 11'))
label1.place(x=30, y=60)
label2 = Label(win, text = "Audio File 2: ", font =('Aerial 11'))
label2.place(x=30, y=80)
label3 = Label(win, text = "Video File 1: ", font =('Aerial 11'))
label3.place(x =30, y=100)
label4 = Label(win, text = "Video File 2: ", font =('Aerial 11'))
label4.place(x=30, y=120)
label5 = Label(win, text = "Middle Camera Video File: ", font =('Aerial 11'))
label5.place(x=30,y=140)

# Add a Button Widget
input1 = ttk.Button(win, text="Select a Audio File", command= open_file).pack(side=BOTTOM)
input2 = ttk.Button(win, text="Select a Video File", command= open_file2).pack(side=BOTTOM)

input3 = ttk.Button(win, text="Check to see if the file was added successfully", command= files_Added).place(x = 30, y = 180)



win.mainloop()
print(vid_list[1])
 

person1 = VideoFileClip(vid_list[1])
person2 = VideoFileClip(vid_list[2])
middle = VideoFileClip(vid_list[3])
audioclip1 = AudioFileClip(audio_list[1])
audioclip2 = AudioFileClip(audio_list[2])


person1clips = []
x = 0
y = 0
def roundup(x):
   return int(math.ceil(x / 5.00)) * 5
person1duration = roundup(person1.duration) - 5
print(person1duration)

while x <= person1duration:
	newclip = person1.subclip(x, x + 5)
	person1clips.append(newclip)
	x = x + 5



person2clips = []
x = 0
y = 0
def roundup(x):
   return int(math.ceil(x / 5.00)) * 5
person2duration = roundup(person2.duration) - 5
print(person2duration)

while x <= person2duration:
	newclip = person2.subclip(x, x + 5)
	person2clips.append(newclip)
	x = x + 5



middleClips = []
x = 0
y = 0
def roundup(x):
   return int(math.ceil(x / 5.00)) * 5
middleCameraDuration = roundup(middle.duration) - 5
print(middleClips)

while x <= middleCameraDuration:
	newclip = middle.subclip(x, x + 5)
	middleClips.append(newclip)
	x = x + 5	

def cut(i): return audioclip1.subclip(i, i+1).to_soundarray(fps=22000)
def cut2(i): return audioclip2.subclip(i, i+1).to_soundarray(fps=22000)
def volume(array1): return np.sqrt(((1.0*array1)**2).mean())


volumes1 = [volume(cut(i)) for i in range(0, int(audioclip1.duration-1))]
volumes2 = [volume(cut2(i)) for i in range(0, int(audioclip2.duration-1))]

averaged_volumes1 = np.array([sum(volumes1[i:i+5])/5
                              for i in range(len(volumes1)-5)])

averaged_volumes2 = np.array([sum(volumes2[i:i+5])/5
                              for i in range(len(volumes2)-5)])

secondsDiviedBy10= int(audioclip1.duration / 5)
final = middleClips[0]

for x in range(secondsDiviedBy10):
	personClip1 = person1clips[x + 1]
	personClip2 = person2clips[x + 1]
	middleClip = middleClips[x + 1]
	if averaged_volumes1[x] * 1.3 <= averaged_volumes2[x]:
		print("2 is louder by at least 30%")
		final = concatenate_videoclips([final, personClip2])
	elif averaged_volumes2[x] * 1.3 <= averaged_volumes1[x]:
		print("1 is louder by at least 30%")
		final = concatenate_videoclips([final, personClip1])
	else:
		print("middle camera")
		final = concatenate_videoclips([final, middleClip])	


finalAudio = CompositeAudioClip([audioclip1, audioclip2])
final2 = final.set_audio(finalAudio)
final2.write_videofile('mark.mp4', audio_bitrate="1000k", bitrate="4000k")