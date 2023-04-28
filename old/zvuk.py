from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

path_s = r"C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\dom.mp4"
path_bez = r"C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\dom_bez_tit.mp4"
path_novy = r"C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\vysledok.mp4"

audio_clip = AudioFileClip(path_s)   #audio ziskavam lebo cv2 nepouziva
modified_clip = VideoFileClip(path_bez)
final_clip = modified_clip.set_audio(audio_clip)
final_clip.write_videofile(path_novy)