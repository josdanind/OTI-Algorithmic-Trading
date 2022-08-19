# Python
from os import getcwd, listdir, remove

# FastAPI
from fastapi import APIRouter, Depends, status, UploadFile, File, Path
from fastapi.responses import FileResponse, JSONResponse

# Interaction with the database
from sqlalchemy.orm import Session
from database import get_db

# Utils
from utils.OAuth import oauth2_schema
from utils.validate_token import check_permits

router = APIRouter()

# -------
#  Utils
# -------
public_path = getcwd() + "/assets/upload/"


def file_manage_error(message: str):
    return JSONResponse(
        content={"massage": message},
        status_code=status.HTTP_404_NOT_FOUND,
    )


# -------------
#  Upload File
# -------------
@router.post(path="/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    file: UploadFile = File(...),
):
    check_permits(db, token, 1)
    try:
        with open(public_path + file.filename, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception:
        return file_manage_error("There was an error uploading the file")
    finally:
        file.file.close()

    return {"message": "The file was uploaded successfully"}


# ---------------
#  Show File
# ---------------
@router.get(path="/show/{name_file}", status_code=status.HTTP_201_CREATED)
async def download_file(name_file: str = Path(...)):
    if name_file in listdir(public_path):
        return FileResponse(public_path + name_file)
        # Descargar directamente eel archivo
        #  return FileResponse(path + name_file, media_type="application/octet-stream", filename=name_file)

    else:
        return file_manage_error("The file doesn't exists!")


# ---------------
#  List files
# ---------------
@router.get(path="/list", status_code=status.HTTP_200_OK)
async def list_files():
    return listdir(public_path)


# ---------------
#  Remove file
# ---------------
@router.delete(path="/delete/{name_file}", status_code=status.HTTP_200_OK)
async def delete_file(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    name_file: str = Path(...),
):
    check_permits(db, token, 1)
    try:
        remove(public_path + name_file)
        return {"message": f"The file {name_file} was deleted!"}
    except FileNotFoundError:
        return file_manage_error("Error deleting file")
