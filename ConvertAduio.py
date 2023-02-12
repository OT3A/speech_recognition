import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os 
import shutil
# from playsound import p
dest = "test.wav"

# # initialize the recognizer
r = sr.Recognizer()


# files
src = "amr.mp3"

# os.system(f"""ffmpeg -i {src} -acodec pcm_u8 -ar 22050 {src[:-4]}.wav""")
# convert wav to mp3
sound = AudioSegment.from_mp3(src)
# sound = AudioSegment.from_file(src,  format= 'm4a')
# sound = AudioSegment.from_ogg(src)

# sound = AudioSegment.from_file(src,  format= 'wav')
sound.export(dest, format="wav")



chunks = split_on_silence(sound,
        # must be silent for at least 0.5 seconds
        # or 500 ms. adjust this value based on user
        # requirement. if the speaker stays silent for 
        # longer, increase this value. else, decrease it.
        min_silence_len = 400,
  
        # consider it silent if quieter than -40 dBFS
        # adjust this per requirement
        silence_thresh = -40
    )


try:
    os.mkdir('audio_chunks')
except(FileExistsError):
    pass
  
    # move into the directory to
    # store the audio files.
os.chdir('audio_chunks')
  
i = 0


for chunk in chunks:
              
    # Create 0.5 seconds silence chunk
     chunk_silent = AudioSegment.silent(duration = 10)
  
     # add 0.5 sec silence to beginning and 
     # end of audio chunk. This is done so that
     # it doesn't seem abruptly sliced.
     audio_chunk = chunk_silent + chunk + chunk_silent
  
     # export audio chunk and save it in 
     # the current directory.
     print("saving chunk{0}.wav".format(i))
     # specify the bitrate to be 192 k
     audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
  
     # the name of the newly created chunk
     filename = 'chunk'+str(i)+'.wav'
  
     print("Processing chunk "+str(i))
  
     # get the name of the newly created chunk
     # in the AUDIO_FILE variable for later use.
     file = filename

     # open the file
     with sr.AudioFile(file) as source:
         # listen for the data (load audio to memory)
         audio_data = r.record(source)
         # recognize (convert from speech to text)
         text = r.recognize_google(audio_data,language='ar-AR',show_all = True)
         print(text)
     i += 1
  
os.chdir('..')

# shutil.rmtree('audio_chunks')




# with sr.Microphone() as source:   
#     # read the audio data from the default microphone
#     audio_data = r.record(source, duration=5)
#     print("Recognizing...")
#     # convert speech to text
#     text = r.recognize_google(audio_data,language='ar-AR')
#     print(text)
    
