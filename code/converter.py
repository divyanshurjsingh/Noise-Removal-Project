from loader import get_files
from helper import convert_mp3_to_wav
import os

def convert_all(curr_path='noise', des_path='noise/wav', filter='mp3', new_ext='.wav'):
    files=get_files(curr_path, file_type=filter)
    
    if not os.path.exists(des_path):
        os.mkdir(des_path)
    for src in files.values():
        name=os.path.splitext(os.path.basename(src))[0]
        dst=os.path.join(des_path,name+ new_ext)
        state=convert_mp3_to_wav(src,dst)
        
