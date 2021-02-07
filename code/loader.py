import os
def get_files(path="noise",file_type='.wav'):
    datalist={}
    data=os.listdir(path)
    data=list(filter(lambda i:i.endswith(file_type),data))
    for item in data:
        datalist.update({item: os.path.join(path,item)})
    return datalist

if __name__ == "__main__":
    print(get_files())