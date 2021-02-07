
import matplotlib
import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Qt5Agg')

# Waveform
# Waveform--An audio waveform is a time domain display, a display of amplitude vs time.
def waveform(audio_file="uploads/simpleLoop.wav"):

    x,sr=librosa.load(audio_file, sr=22050)    # This returns an audio time series as a numpy array with 
                                           # a default sampling rate(sr) of 22KHZ mono. 'x' is audio time series. The sample rate 
                                           # is the number of samples of audio carried per second, measured in Hz or kHz.

                  

                             
    
    return librosa.display.waveplot(x, sr=sr) 
   

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Spectrum
# Spectrum--An audio spectrum is a frequency domain display, a display of amplitude vs frequency.
# To move from time domain to frequency domain we need to perform fast fourier transform(fft).
# The Fourier Transform is a mathematical operation that changes the domain (x-axis) of a signal from time to frequency.
def spectrum(audio_file="uploads/simpleLoop.wav"): 
    x,sr=librosa.load(audio_file, sr=22050)
    fft=np.fft.fft(x)      # this gives complex values and so we need to convert it to absolute values.
     

    magnitude=np.abs(fft)  # here we are performing absolute value on the complex value and we end up at this magnitude 
                           # and this magnitude indicate the contribution of each frequency been to the overall sound

    frequency=np.linspace(0,sr,len(magnitude)) # np.linspace return evenly spaced numbers over a specified interval.
                                               # numpy.linspace(start, stop, num=50) here start=0, stop=sr and the 
                                               # number of evenly spaced=length of magnitude.

    # we need not to plot whole frequency vs magnitude graph as it would be symetric
    #  hence we only need to plot first half of frequency and first half of magnitude

    left_frequency=frequency[:int(len(frequency)/2)]  # ploting only first half of frequency
    left_magnitude=magnitude[:int(len(magnitude)/2)]  # ploting only first half of magnitude

    return plt.plot(left_frequency,left_magnitude)
    #plt.title("Spectrum") 
    #plt.xlabel("Frequency")
    #plt.ylabel("Magnitude")
    #plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Spectrogram
# Spectrogram --A spectrogram is a detailed view of audio, able to represent time, frequency, and amplitude all on one graph.
# A waveform displays changes in a signal’s amplitude over time. A spectrogram, however, displays changes in the signal's frequencies 
# over time. To get spectrogram we use stft i.e short time fourier transform.
# STFT divides a time signal into short segments of equal length and then the Fourier transform of
# each segment is computed. The resulting segment-frequency content can be plotted against time and it is called spectrogram. 
n_fft=2048
hop_length=512
def spectrogram(audio_file="uploads/simpleLoop.wav"):
    x,sr=librosa.load(audio_file, sr=22050) 
    n_fft=2048      # defaul value. n_fft is frame size, i.e. the size of the FFT

    hop_length=512  # default value. hop_length is the frame increment

    stft=librosa.core.stft(x,hop_length=hop_length,n_fft=n_fft)
    spectrogram=np.abs(stft)
   
    log_spectrogram = librosa.amplitude_to_db(spectrogram)   # we can convert the frequency axis to a logarithmic one for better 
                                                         # visualisation, So we are converting the unit to decible.
                                                         

    return librosa.display.specshow(log_spectrogram,sr=sr,hop_length=hop_length)
    #plt.title("Spectrogram") 
   #plt.xlabel("Time")
    #plt.ylabel("Frequency")
    #plt.colorbar()
    #plt.show()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------

# MFCCs
# The Mel frequency cepstral coefficients (MFCCs)-- the MFCCs of a signal are a small set of features (usually about 10–20) 
# which describe the overall shape of a spectral envelope. It models the characteristics of the human voice.
def mfcc(audio_file="uploads/simpleLoop.wav"):
    x,sr=librosa.load(audio_file, sr=22050)
    mfcc=librosa.feature.mfcc(x,n_fft=n_fft,hop_length=hop_length,n_mfcc=13)
    librosa.display.specshow(mfcc,sr=sr, hop_length=hop_length)

    #print(mfcc.shape)  # o/p-> (13, 460) this means that here mfcc computed 13 MFCCs over 460 frames.

    #plt.title("MFCCs") 
    #plt.xlabel("Time")
    #plt.ylabel("MFCCs")
    #plt.colorbar()
    #plt.show()
