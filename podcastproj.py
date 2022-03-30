
from tkinter import filedialog, font
from typing import List
from moviepy.audio.AudioClip import concatenate_audioclips
import numpy as np  # for numerical operations
import math
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, CompositeAudioClip
from tkinter import *
from tkinter import ttk

win = Tk()

win.geometry("900x520")			#Size of GUI window
audio_list = ["nothing yet"]	#List of inputted audio files
vid_list = ["nothing yet"]		#List of inputted Video files

def open_file():	#Function that opens a audio file and adds it to the audio list. 
   file_path = filedialog.askopenfilename(parent=win, title='Choose a File')
   audio_list.append(file_path)

def open_file2():	#Function that opens a video file and adds it to the video list
   file_path = filedialog.askopenfilename() 
   vid_list.append(file_path)

def files_Added():	#function that is checking if a vid or audio clip was added to th list. 
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

label6 = Label(win, text = "Instructions: ", font = ('Aerial'))
label6.place(x = 400, y = 30)
message ='''
This program is made to automatically edit a podcast 
with multiple camera angles. 
Right now the program can only handle 3 angles. 
Two angles facing two people and a middle 
angle that should show both people in frame."
I plan to make the program allow 
for more angles in the future. 
The way to add the video and audio 
files properly is as follows,
You must click the respective buttons 
to add the video and auio files. 
You can oly add .mp3 for audio and .mp4 for video.
You must add the files in the same 
order for both. So add person 1's audio file before
person 2's and same goes for video. 
Then add the midle video file last/ 3rd to the 
video file button. 
To check if you did this right you can 
click the button under the text on the left side
and it will tell you what file is in what spot.
If everything looks correct to you then 
close the window and the final file will 
end up in the folder where the program is. 
	'''
text_box = Text(
    win,
    height=25,
    width=120
)
text_box.pack(expand=True)
text_box.insert('end', message)
text_box.config(state='disabled')
text_box.place(x = 400, y = 50)	


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


person1clips = []	#splitting the clip up into sections of 5 seconds
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



person2clips = []	#splitting the clip up into sections of 5 seconds
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



middleClips = []	#splitting the clip up into sections of 5 seconds
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

def cut(i): return audioclip1.subclip(i, i+1).to_soundarray(fps=22000)	#fucntion that is cutting the audio up second by second for the first persons audio. 
def cut2(i): return audioclip2.subclip(i, i+1).to_soundarray(fps=22000)	#fucntion that is cutting the audio up second by second for the second persons audio. 
def volume(array1): return np.sqrt(((1.0*array1)**2).mean())	#fucntion returning the volume of inputted clip. 


volumes1 = [volume(cut(i)) for i in range(0, int(audioclip1.duration-1))] 	#Array of the volume every second of the clip for audio clip 1.
volumes2 = [volume(cut2(i)) for i in range(0, int(audioclip2.duration-1))]	#Array of the volume every second of the clip for audio clip 1.

averaged_volumes1 = np.array([sum(volumes1[i:i+5])/5	#gets the average volume of every 5 seconds for audio clip1. 
                              for i in range(len(volumes1)-5)])

averaged_volumes2 = np.array([sum(volumes2[i:i+5])/5	#gets the average volume of every 5 seconds for audio clip2. 
                              for i in range(len(volumes2)-5)])

secondsDiviedBy5= int(audioclip1.duration / 5)	#audioclip1's time in seconds divded by 5. 
final = middleClips[0]

for x in range(secondsDiviedBy5):	# going through every 5 seconds of the audio clips. 	
	personClip1 = person1clips[x + 1]	#If average volume from audio clip 1 is 30% lounder than average volume over 5 seconds of audio clip 2 then...
	personClip2 = person2clips[x + 1]	#the 5 second video clip associated with that audio clip will be added to the final video. The same goes for if...
	middleClip = middleClips[x + 1] 	#auio clip 2 is t least 30% louder than audio clip 1. If neither are at least 30% louder than the other than...
	if averaged_volumes1[x] * 1.3 <= averaged_volumes2[x]: #teh middle clip of 5 seconds is added to the video in it's respective spot instead.
		print("2 is louder by at least 30%")
		final = concatenate_videoclips([final, personClip2])
	elif averaged_volumes2[x] * 1.3 <= averaged_volumes1[x]:
		print("1 is louder by at least 30%")
		final = concatenate_videoclips([final, personClip1])
	else:
		print("middle camera")
		final = concatenate_videoclips([final, middleClip])	


finalAudio = CompositeAudioClip([audioclip1, audioclip2]) #Final audio is just a combination of the two audios
final2 = final.set_audio(finalAudio)
final2.write_videofile('finalPodcastVideo.mp4', audio_bitrate="1000k", bitrate="4000k") #This creates the final video and adds it to the folder you are in. 