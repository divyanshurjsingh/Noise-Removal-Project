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
from helper import convert_mp3_to_wav
import analyser as m
import SessionState
from scipy.io import wavfile
from noise_remover import removeNoise

# data base code
engine=create_engine('sqlite:///audio_database.sqlite3') 
Session=sessionmaker(bind=engine)   # connects to database
sess=Session()


BASE_DIR = os.path.join('C:\\','Users','divya','OneDrive','Desktop','Noise Removal Project') 
UPLOAD_DIR = os.path.join(BASE_DIR,'uploads')
NOISE_DIR = os.path.join(BASE_DIR,'noise','wav')

st.title("Noise removal application")
st.sidebar.title("Audio Uploader")
upload= st.sidebar.file_uploader("select an audio file")
btnclicked= st.sidebar.button("Upload Audio File")

noise_picked = None
state = SessionState.get(name='')                       # initially the name variable we keep empty
audio_clip = SessionState.get(audio='')

if btnclicked and upload:
    data=upload.read()
    name=upload.name                                    # here we assinged our empty name variable to name of the file uploaded.
    ext=os.path.splitext(name)[1]                       # this will split the name of the file for eg if the file name is abc.mp3 then it will split it as ['abc', 'mp3'] and by opting [1] we will get extension of the file.
    if ext in ['.mp3','.mp4','.ogg','.wav','.WAV']:
        with open(f'{UPLOAD_DIR}/{name}','wb') as f:    # The wb indicates that the file is opened for writing in binary mode. 
            f.write(data)
            state.name = name                           # we are keeping the value of our name variable inside state.name    
        entry=AudioFile(file_name=name, file_path=f'uploads/{name}', file_extension=os.path.splitext(name)[1])
        sess.add(entry)
        sess.commit()
        st.success("file uploaded")
    else:
        st.error("only audio files are accepted")
else:
    if not state.name:
        st.warning("please upload a file to begin")
    else:
        st.subheader('step 1')
        st.success('file uploaded, ready to work')

name = state.name         # again we are loading name variable with the content of state.name. This prevent us from  uploading the audio files again and again.           
if name:


    audio_file = os.path.join(UPLOAD_DIR,name)
    SessionState.audio = audio_file
    st.sidebar.text(f'file at : {audio_file}')
    st.audio(audio_file)
    st.subheader('step 2')
    option = st.selectbox('Select a category',('pick a category to start processing','Audio Visualization','Noise Removal'))
    if option == 'Audio Visualization':
        st.subheader('step 3')
        choice=st.selectbox('choose a visualization',('click here to select','waveform','spectrogram','spectrum','MFCC'))
        if choice=='waveform' and name:
            x,sr=librosa.load(audio_file)
            fig,ax=plt.subplots()                            
            librosa.display.waveplot(x,sr=sr)
            st.title('waveform')
            st.pyplot(fig)

        elif choice=='spectrogram' and name:
            x,sr=librosa.load(audio_file)
            fig,ax=plt.subplots()                           
            stft=librosa.core.stft(x,hop_length=512,n_fft=2048)
            librosa.display.specshow(librosa.amplitude_to_db(np.abs(stft)),y_axis='log',x_axis='time',ax=ax)
            st.title('spectrogram')
            st.pyplot(fig)

        elif choice=='spectrum' and name:
            x,sr=librosa.load(audio_file)
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
            x,sr=librosa.load(audio_file)
            fig,ax=plt.subplots()                          # MFCCs
            mfcc=librosa.feature.mfcc(x,n_fft=2048,hop_length=512,n_mfcc=13) 
            librosa.display.specshow(mfcc,sr=sr, hop_length=512,x_axis='time')
            st.title('MFCC')
            st.pyplot(fig)

    if option == 'Noise Removal':
        st.subheader('step 3')
        noise_files = get_files(path=NOISE_DIR)
        noise = st.selectbox('Please select a type of noise , that you would like to filter from the audio',
            ["click here to select noise option"]+list(noise_files.keys()))
        noise_picked = noise_files.get(noise)
        st.audio(noise_picked)

audio_clip = SessionState.audio

if name and noise_picked and os.path.exists(noise_picked):
    st.subheader('step 4')
    st.warning('Processor intensive step, this will take a lot of time!!')
    n_std_thresh = st.slider('how many frequency channels to smooth over with the mask',min_value=1,max_value=3,value=2)
    prop_decrease = st.slider('To what extent should you decrease noise',min_value=0.0,max_value=1.0,value=0.95)
    processbtn = st.button('Remove Noise from Audio')
    convert_mp3_to_wav(audio_clip,'out.wav')
    if processbtn:
        rate, data = wavfile.read('out.wav')
        noise_rate, noisedata = wavfile.read(noise_picked)
        noisedata = noisedata.astype(np.float) # convertedArray = sampleArray.astype(np.float)
        st.write(f'working on {name} {audio_clip} {type(data)} {type(noisedata)} {noisedata.dtype}')
        output = removeNoise(
            audio_clip=data,
            noise_clip=noisedata,
            n_std_thresh = n_std_thresh,
            prop_decrease=prop_decrease,
            visual=False,
        )
        st.write(output)


        
    