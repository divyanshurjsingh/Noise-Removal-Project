from os import path
from pydub import AudioSegment
def convert_mp3_to_wav (src, dst):
    if path.exists(src):
        try:
            sound=AudioSegment.from_mp3(src)
            sound.export(dst, format='wav')
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

if __name__ == "__main__":
    src='../noise/police-sirens.mp3'
    dst='../noise/police-sirens.wav'
   


# option = st.selectbox('Select Functions?',('Noise Removal','Analysis'))
# st.write('You selected:', option)
# if option=='Analysis':
#    btnclicked=st.button('start processing)
# elif option=='Noise Removal':
#    new_opt=st.selectbox('choose the noise you want to remove', ('Fan','Traffic','Rain','Wind','Turbine'))