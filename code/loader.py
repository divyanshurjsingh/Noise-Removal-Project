import os
def get_files(path="noise",file_type='.wav'):
    datalist={}
    data=os.listdir(path)  #  os.listdir() method in python is used to get the list of all files and directories in the specified directory.
    data=list(filter(lambda i:i.endswith(file_type),data))
    #print(data)
    for item in data:
        datalist.update({item.split('.')[0]: os.path.join(path,item)})
    return datalist

if __name__ == "__main__":
    print(get_files())