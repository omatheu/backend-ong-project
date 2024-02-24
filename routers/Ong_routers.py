from fastapi import HTTPException, APIRouter, Form
from db import database
from schemas.Ongs import OngSchema
from models.Ong_model import Ong
from typing import Optional

router = APIRouter(prefix="/ongs")

@router.post("/inserir/", tags=["Ong"])
async def create_ong(ong: OngSchema):
    try:
        ong_obj = await Ong.objects.create(**ong.dict())
        return ong.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/filtrar-ongs/", tags=["Ong"])
async def filter_ongs():
    try:
        ongs = await Ong.objects.all()
        ongs_data = [{"id_ong": ong.id_ong, "cnpj": ong.cnpj, "senha": ong.senha} for ong in ongs]
        return ongs_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/listar-ongs/", tags=["Ong"])
async def get_ongs(logradouro: str = None):
    try:
        if logradouro:
            ongs = await Ong.objects.filter(logradouro=logradouro)
        else:
            ongs = await Ong.objects.all()
        return ongs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/deletar/{id_ong}", tags=["Ong"])
async def delete_ong(id_ong: int):
    try:
        ong = await Ong.objects.get(id_ong=id_ong)
        await ong.delete()
        return {"message": "Ong deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/atualizar/{id_ong}", tags=["Ong"])
async def update_ong(id_ong: int, ong: OngSchema):
    try:
        ong_obj = await Ong.objects.get(id_ong=id_ong)
        await ong_obj.update(**ong.dict())
        return {**ong.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")