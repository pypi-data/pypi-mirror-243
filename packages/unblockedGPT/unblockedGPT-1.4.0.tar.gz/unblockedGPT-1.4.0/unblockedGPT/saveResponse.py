import os

from unblockedGPT.rephrase import rephrase_2, rephrase_1

def saveResponse(text:str, dir:str) -> bool:
    """
        Saves file in dir, with name save.txt, if save.txt exists, saves as save1.txt, save2.txt, etc.
        input: text to save, dir to save in
    """
    try:
        fileDir = dir
        file = "save"
        fileSuffix = ".txt"
        extra = 0
        if os.path.exists(fileDir + "/" + file + fileSuffix):
            extra += 1
            while os.path.exists(fileDir + "/" + file + str(extra) + fileSuffix):
                extra += 1
            file = file + str(extra)
        with open(fileDir + "/" + file + fileSuffix, 'w') as file:
            file.write(text)
    except:
        return False
    
    return True


def heroSave(input:str, cwd: str):
    """
    run file through gpthero api and save response
    """
    path = ""
    if os.path.exists(input):
        path = input
    elif os.path.exists(os.path.join(cwd, input)):
        path = os.path.join(cwd, input)
    else:
        print("File path provided does not exist. Use -h for help")


    with open(path, 'r') as file:
        text = file.read()
    text = rephrase_2(text)
    if not text['status']:
        print(text['msg'])
        return
    text = text['msg']
    print("Saving...")
    if saveResponse(text, cwd):
        print("Saved")
    else:
        print("Error saving file")

def stealthSave(input:str, cwd: str):
    """
    run file through stealth api and save response
    """
    path = ""
    if os.path.exists(input):
        path = input
    elif os.path.exists(os.path.join(cwd, input)):
        path = os.path.join(cwd, input)
    else:
        print("File path provided does not exist. Use -h for help")


    with open(path, 'r') as file:
        text = file.read()
    text = rephrase_1(text)
    if not text['status']:
        print(text['msg'])
        return
    text = text['msg']
    print("Saving...")
    if saveResponse(text, cwd):
        print("Saved")
    else:
        print("Error saving file")
        