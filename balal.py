import tkinter as tk
#import tkinter.ttk as ttk
from tkVideoPlayer import TkinterVideo


purple_clickable_button= "#DCD0FF"
purple_clickable_button_clicked= "#C6B5FF"
grey_not_clickable_button= "#B2B0B9"
app_bg = "#6D6A75"
button_text="#3A3541"

font_buttons = ("Leelawadee UI Semilight", 17, "bold")

window = tk.Tk()
window.title("Subtitle remover")

window.geometry("1170x729")
window.minsize(912, 568)

videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"titulky.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

bottomframe = tk.Frame(window)
bottomframe.pack( side = tk.BOTTOM, pady = 12)

b_upload = tk.Button(bottomframe, relief="flat" ,text="Upload Video",activebackground =purple_clickable_button_clicked,font = font_buttons, bg=purple_clickable_button, fg=button_text,width=17, height=2, state="normal").pack(side=tk.LEFT,padx=30)
#b_upload.place(anchor=tk.CENTER,x=209, y=550)

b_selectarea = tk.Button(bottomframe,relief="flat", text="Select Area",font = font_buttons, bg=grey_not_clickable_button,fg=button_text,width=17, height=2, state="disabled").pack(side=tk.LEFT,padx=30)
#b_selectarea.place(anchor=tk.CENTER,x=509, y=550)

b_deleteSub = tk.Button(bottomframe, relief="flat",text="Delete Subtitles", font = font_buttons,bg=grey_not_clickable_button,fg=button_text,width=17, height=2, state="disabled").pack(side=tk.LEFT,padx=30)
#b_deleteSub.place(anchor=tk.CENTER,x=809, y=550)

window.mainloop()
