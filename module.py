import json
from model import *
import os
def writeSaveFile(filename, content):
    with open(filename, "w") as myfile:
        json.dump(content, myfile, indent=4)
        
def readSaveFile(filename):
    with open(filename, "r") as myfile:
        return json.load(myfile)
    

def idManager(lists: list):
    if lists == []:
        return 1
    else:
        return lists[len(lists) -1]["id"] + 1
    

def addAnObjetTotheLists(fichier: Fichier, filename):
    try: 
        lists = list(readSaveFile(filename))
    except:
        writeSaveFile(filename, [])
        lists = list(readSaveFile(filename))

    fichier.id = idManager(lists)
    monfichier = dict(fichier)
    monfichier['chemin'] = None
    lists.append(monfichier)
    writeSaveFile(filename, lists)

async def uploadFileToSaveFolder(file, categorieDossier):
    with open("saveFile/"+categorieDossier+"/"+file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)

def changeFilePath(id: int, filepath, filename):
    lists = list(readSaveFile(filename))
    if lists==[]:
        return {"message": "List empty"}
    else: 
        for objet in lists:
            if id == objet["id"]:
                objet["chemin"] = filepath
                writeSaveFile(filename, lists)
                return objet
    
    return {"message": "objet introuvable"}


def getAfile(id: int, lists):
    for file in lists:
        if file["id"] == id:
            return file
        
    return {"message":"le fichier n'existe pas"}

def updateFichier(id:int, filename: str, nouveauFichier):
    lists = list(readSaveFile(filename))
    for fichier in lists: 
        if fichier['id'] == id :
            nouveauFichier = dict(nouveauFichier)
            for cle in nouveauFichier.keys():
                if cle !=  None:
                    fichier[cle] = nouveauFichier[cle]
                
            writeSaveFile(filename, lists)
            return fichier
        
async def deleteFile(id: int, filename):
    lists = list(readSaveFile(filename))
    for objet in lists:
        if id == objet["id"]:
            os.remove(objet["chemin"])
            lists.remove(objet)
            writeSaveFile(filename, lists)

