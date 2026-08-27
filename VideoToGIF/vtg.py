from moviepy import VideoFileClip

clip = VideoFileClip("main.mp4")

clip.write_gif("output.gif")
