from pathlib import Path
import urllib.request

def read_url()->str:
    while True:
        url=input('URL: ').strip()

        if len(url)>0:
            return url
        else:
            print('Please enter an URL')
def read_local_path()->Path:
    while True:
        path_text=input('Path: ')
        try:
            file_path=Path(path_text)
            return file_path
        except:
            print('Not a valid path')

def get_response(url:str)->str:
    response=None
    try:
        
        response=urllib.request.urlopen(url)
        content_bytes=response.read()
        content_text=content_bytes.decode(encoding='utf-8')
        return content_text
    finally:
        if response !=None:
            response.close()

def write_file(local_path:Path, content_text:str)->None:
    local_file=None
    try:
        
        local_file=local_path.open('w')
        local_file.write(content_text)
        local_file.close()
    finally:
        if local_file !=None:
            local_file.close()
        

def download_file(url: str, local_path:Path)->None:
    content_text=get_response(url)
    write_file(local_path,content_text)


if __name__=='__main__':
    url=read_url()
    local_path=read_local_path()
    download_file(url,local_path)
