from loader import get_files
from converter import convert_all
import matplotlib
import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.orm import sessionmaker
from audio_db import AudioFile
from sqlalchemy import create_engine
import streamlit as st
import os
import analyser as m
import SessionState
engine=create_engine('sqlite:///audio_database.sqlite3') 
Session=sessionmaker(bind=engine) # this line serves only one purpose i.e connect to database.
sess=Session()

st.title("Audio Analysis")

upload= st.file_uploader("select an audio file")
btnclicked= st.button("Start Processing")
state = SessionState.get(name='')            # initially the name variable we keep empty
if btnclicked and upload:
    
    data=upload.read()
    name=upload.name                        # here we assinged our empty name variable to name of the file uploaded.
    ext=os.path.splitext(name)[1]  # this will split the name of the file for eg if the file name is abc.mp3 then it will split it as 
                                   # ['abc', 'mp3'] and by opting [1] we will get extension of the file.
    if ext in ['.mp3','.mp4','.ogg','.wav','.WAV']:
        with open(f'uploads/{name}','wb') as f:       # The wb indicates that the file is opened for writing in binary mode. 
                                                      # When writing in binary mode, Python makes no changes to data as it is written to the file
            f.write(data)
            state.name = name              # we are keeping the value of our name variable inside state.name    
        entry=AudioFile(file_name=name, file_path=f'uploads/{name}', file_extension=os.path.splitext(name)[1])
        sess.add(entry)
        sess.commit()

        st.success("file uploaded")
    else:
        st.error("only audio files are accepted")
else:
    st .warning("please upload a file to begin")

name = state.name         # again we are loading name variable with the content of state.name. This prevent us from 
                          # uploading the audio files again and again.           
st.write(name)
choice=st.selectbox('choose',('waveform','spectrogram','spectrum','MFCC'))
if choice=='waveform' and name:


    x,sr=librosa.load(f'uploads/{name}',sr=22050)
    fig,ax=plt.subplots()                            # waveform
    librosa.display.waveplot(x,sr=sr)
    st.title('waveform')
    st.pyplot(fig)

elif choice=='spectrogram' and name:
    x,sr=librosa.load(f'uploads/{name}',sr=22050)
    fig,ax=plt.subplots()                           # spectrogram
    stft=librosa.core.stft(x,hop_length=512,n_fft=2048)
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(stft)),y_axis='log',x_axis='time',ax=ax)
    st.title('spectrogram')
    st.pyplot(fig)

elif choice=='spectrum' and name:
    x,sr=librosa.load(f'uploads/{name}',sr=22050)
    fig,ax=plt.subplots()                        # Spectrum
    fft=np.fft.fft(x)
    magnitude=np.abs(fft)    
    frequency=np.linspace(0,sr,len(magnitude))
    left_frequency=frequency[:int(len(frequency)/2)]  # ploting only first half of frequency
    left_magnitude=magnitude[:int(len(magnitude)/2)]  # ploting only first half of magnitude
    plt.plot(left_frequency,left_magnitude)
    st.title('spectrum')
    st.pyplot(fig)

elif choice=='MFCC' and name:
    x,sr=librosa.load(f'uploads/{name}',sr=22050)
    fig,ax=plt.subplots()                          # MFCCs
    mfcc=librosa.feature.mfcc(x,n_fft=2048,hop_length=512,n_mfcc=13) 
    librosa.display.specshow(mfcc,sr=sr, hop_length=512,x_axis='time')
    st.title('MFCC')
    st.pyplot(fig)
 