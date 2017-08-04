#ICS&32
#Project1:
#File Systems
# Qiao He : 16765414
# Anisha Arora : 26177906

def search_sub_dir(pathToSearch: 'Path')->[]:
    '''look for files in the directory recursively'''
    subDirList=[]
    subDirList.append(pathToSearch)

    for child in pathToSearch.iterdir():
        if child.is_dir():
            subDirList+=search_sub_dir(child)
        else:
            subDirList.append(child)
    return list(set(subDirList))

def get_first_input()->'Path':    
    '''get the first line of the input which is the path to the directory'''   
    while True:
        dir_input_str=input()
        dir_input=Path(dir_input_str)
        if dir_input.is_dir() and dir_input_str!='':
            break
        else:
            print('Error')
    return dir_input

def get_second_input(root_dir: 'Path')->[]:
    '''get the second line of input specifies the search characteristics that decide the interesting files'''
    allPaths=search_sub_dir(root_dir) #recursively search for all the paths according to the first input
    while True:
        second_input=input().strip()
        if len(second_input)>2:
            indicator=second_input[2:]  #the instruction after the space

            if second_input[0]=='N' and second_input[1]==' ':
                #search for files whose names exactly match a particular name
                return findSameNameFile(indicator, allPaths)
            elif second_input[0]=='E' and second_input[1]==' ':
                #search for paths with the given suffix under the given path
                suffix=find_suffix(indicator) 
                return findSameSuffixFile(suffix, allPaths)
            elif second_input[0]=='S' and second_input[1]==' ' and checkIfNonNegInt(indicator):
                #search for paths with size bigger than given size under the given path
                size=int(indicator)
                return findBiggerFile(size, allPaths)
            else:
                print('Error') 
        else:
            print('Error')           


def get_third_input(allPathFromSecondSearch: []):
    '''taking action on the intereting files from the second searching'''
    while True:
        third_input=input()
        if third_input is 'P':
            #print the path
            print_path(allPathFromSecondSearch)
            break
        elif third_input is 'F':           
            #read first line of the file
            readFirstlineOfFile(allPathFromSecondSearch)
            break
        elif third_input is 'D':           
            print_path(allPathFromSecondSearch)
            # copy and store in the same dir with suffix .dup
            copyFile(allPathFromSecondSearch)
            break
        elif third_input is 'T':           
            print_path(allPathFromSecondSearch)
            # touch the file: modify the timestamp
            touchFile(allPathFromSecondSearch)
            break
        else:
            print('Error')


#====================FUNCTIONS FOR SECOND INPUT=============================
            
def find_suffix(x:str)->str:   
    '''find suffix of a string input'''   
    if '.'in x:
        return x[x.find('.'):]
    else:
        return '.'+x[x.find(' ')+1:]
    

def checkIfNonNegInt(x:str):
    '''check if the given string can be converted to an non negative integer'''
    try:
        number=int(x)
        if number>0:
           return True
        return False
    except:
        return False


def findSameNameFile(name:str, allFiles:[])->[]:
    '''find files with the same name as the given name argument'''
    fileSameName=[]
    for i in allFiles:
        if i.is_file() and i.name==name:
            fileSameName.append(i)
    return fileSameName

def findSameSuffixFile(extension:str, allFiles:[])->[]:
    '''find files end with the same extension argument in a list of files'''
    fileSameSuffix=[]
    for i in allFiles:
        if i.is_file() and i.suffix==extension:
            fileSameSuffix.append(i)
    return fileSameSuffix

def findBiggerFile(size:int, allFiles:[])->[]:
    '''find files with size bigger than the given files'''
    biggerSizeFile=[]
    for i in allFiles:
        if i.is_file() and i.stat().st_size > size:
            biggerSizeFile.append(i)
    return biggerSizeFile

#=========================FUNCITONS FOR THIRD INPUT============================

def readFirstlineOfFile(allFiles:'Path'):
    file = None
    for i in allFiles:
        try:
            file=open(str(i),'r')
            firstline=file.readline()
            print(i)
            print(firstline)
        except:
            print('Cannot read the file: {}'.format(str(i)))
        finally:
            if file != None:
                file.close()

def copyFile(allFiles:'Path'):
    '''make a duplicate of the file with suffix .dup'''
    for i in allFiles:
        try:
            shutil.copy(str(i),str(i)+'.dup')
        except:
            print('The file: {} cannot be copied'.format(str(i)))
                

         
def touchFile(allFiles:'Path'):
    '''modify its last modified timestamp to be current date/time'''
    for i in allFiles:
        try:
            i.touch()
        except:
            print('The file: {} does not exist'.format(str(i)))

def print_path(allFiles: 'Path'):
    '''print the paths on its own line'''
    for i in allFiles:
        print(i)

#=========================MAIN=====================================
        
if __name__=='__main__':
    from pathlib import Path
    import shutil
    root_path=get_first_input() #get the path to the directory
    interestingFiles=get_second_input(root_path) #get all the interesting files under the chosen directory
    get_third_input(interestingFiles) #take action on those interesting files
