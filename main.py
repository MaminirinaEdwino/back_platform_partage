from fastapi import FastAPI, UploadFile, File, Path
import uvicorn
from module import * 
from model import *
import os
app = FastAPI(title="Plateforme de partage")

FILENAME_OUTILS = "data/outils.json"
FILENAME_COURS = "data/cours.json"

@app.get("/fichiers", tags=["Fichier"])
def getAll():
    try:
        return {"outils": readSaveFile(FILENAME_OUTILS), "cours": readSaveFile(FILENAME_COURS)}
    except:
        writeSaveFile(FILENAME_OUTILS, [])
        writeSaveFile(FILENAME_COURS, [])
        return {"outils": readSaveFile(FILENAME_OUTILS), "cours": readSaveFile(FILENAME_COURS)}

@app.get("/fichier/outils/{id}", tags=["Outils"])
def getAFileOutils(id:  int):
    lists = list(readSaveFile(FILENAME_OUTILS))
    return getAfile(id, lists)

@app.get("/fichier/cours/{id}", tags=["Cours"])
def getAFileCours(id:  int):
    lists = list(readSaveFile(FILENAME_COURS))
    return getAfile(id, lists)

@app.get("/fichier/outils", tags=["Outils"])
def getAllOutils():
    return readSaveFile(FILENAME_OUTILS)

@app.get("/fichier/cours", tags=["Cours"])
def getAllCours():
    return readSaveFile(FILENAME_COURS)

@app.post("/fichier", tags=["Fichier"])
def postFichier(fichier: Fichier):
    if fichier.categorie == 1:
        filename = FILENAME_OUTILS
        addAnObjetTotheLists(fichier, filename)
        return readSaveFile(filename)
    elif fichier.categorie == 2:
        filename = FILENAME_COURS
        addAnObjetTotheLists(fichier, filename)
        return readSaveFile(filename)
    else: 
        return {"message": "choisir la bonne categorie"}

@app.post("/fichier/{id}/{categorie}/upload", tags=["Fichier"])
async def uploadFile(id: int = Path(gt=0),categorie: int = Path(gt=0, lt=3), file: UploadFile = (...)):
    if categorie == 1:
        filename = FILENAME_OUTILS
        await uploadFileToSaveFolder(file, "outils")
        return changeFilePath(id, "saveFile/outils"+file.filename, filename)
    elif categorie == 2:
        filename = FILENAME_COURS
        await uploadFileToSaveFolder(file, "cours")
        return changeFilePath(id, "saveFile/cours"+file.filename, filename)
    
    return {"message": "choisir la bonne categorie"}

@app.put("/fichier/outils/{id}", tags=["Outils"])
def putFichier(id: int, categorie: int, file: FichierUpdate):
    return updateFichier(id, FILENAME_OUTILS, file)

@app.put("/fichier/outils/upload/{id}", tags=["Outils"])
async def putUploadFile(id:int, file: UploadFile = File(...)): 
    lists = list(readSaveFile(FILENAME_OUTILS))
    actual_file = getAfile(id , lists)
    if actual_file["chemin"] != None:
        os.remove(actual_file["chemin"])
    await uploadFileToSaveFolder(file, "outils")
    changeFilePath(id, "saveFile/outils/"+file.filename, FILENAME_OUTILS)
    return {"message": "file updated"}

@app.put("/fichier/cours/upload/{id}", tags=["Cours"])
async def putUploadFile(id:int, file: UploadFile = File(...)): 
    lists = list(readSaveFile(FILENAME_COURS))
    actual_file = getAfile(id , lists)
    if actual_file["chemin"] != None:
        os.remove(actual_file["chemin"])
    await uploadFileToSaveFolder(file, "cours")
    changeFilePath(id, "saveFile/cours/"+file.filename, FILENAME_COURS)
    return {"message": "file updated"}  
    

@app.put("/fichier/cours/{id}", tags=["Cours"])
def putFichier(id: int, categorie: int, file: FichierUpdate):
    return updateFichier(id, FILENAME_COURS, file)


@app.delete("/fichier/outils/{id}", tags=["Outils"])
async def delete(id: int):
    await deleteFile(id, FILENAME_OUTILS)
    return readSaveFile(FILENAME_OUTILS)


@app.delete("/fichier/cours/{id}", tags=["Cours"])
async def delete(id: int):
    await deleteFile(id, FILENAME_COURS)
    return readSaveFile(FILENAME_COURS)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)