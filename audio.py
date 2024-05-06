import gtts
import playsound
text = input("Enterhalo")

sound = gtts.gTTS(text, lang="en")

sound.save("query.mp3")
playsound.playsound("query.mp3")