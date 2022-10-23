import tkinter as tk
#import tkinter.ttk as ttk
from tkVideoPlayer import TkinterVideo

purple_clickable_button= "#DCD0FF"
grey_not_clickable_button= "#B2B0B9"
app_bg = "#6D6A75"
button_text="#3A3541"

window = tk.Tk()
window.title("Subtitle remover")

window.geometry("1170x729")
window.minsize(912, 568)

videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"titulky.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

bottomframe = tk.Frame(window)
bottomframe.pack( side = tk.BOTTOM )

b_upload = tk.Button(bottomframe, text="Upload Video",bg=purple_clickable_button, fg=button_text,width=20, height=4).pack(side=tk.LEFT)
#b_upload.place(anchor=tk.CENTER,x=209, y=550)

b_selectarea = tk.Button(bottomframe, text="Select Area",bg=grey_not_clickable_button,fg=button_text,width=20, height=4).pack(side=tk.LEFT)
#b_selectarea.place(anchor=tk.CENTER,x=509, y=550)

b_deleteSub = tk.Button(bottomframe, text="Delete Subtitles",bg=grey_not_clickable_button,fg=button_text,width=20, height=4).pack(side=tk.LEFT)
#b_deleteSub.place(anchor=tk.CENTER,x=809, y=550)

window.mainloop()
