# ============================================================
# rotas/login.py — Login com Token JWT
# Descrição: Confere e-mail e senha e devolve um token assinado.
# ============================================================

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import conectar

router = APIRouter()
ALGORITMO = "HS256"
MENSAGEM_LOGIN_INVALIDO = {"erro": "E-mail ou senha inválidos"}


# Modelo de dados — define os campos que o formulário de login deve enviar
class Login(BaseModel):
    email: str
    senha: str


# POST /login — valida as credenciais e devolve um JWT com validade de duas horas
@router.post("/login")
def login(dados: Login):
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT email, senha, tipo FROM usuario WHERE email = %s",
                (dados.email,),
            )
            usuario = cursor.fetchone()
        finally:
            cursor.close()
    finally:
        conn.close()

    senha_bytes = dados.senha.encode("utf-8")
    if (
        not usuario
        or len(senha_bytes) > 72
        or not bcrypt.checkpw(senha_bytes, usuario["senha"].encode("utf-8"))
    ):
        return JSONResponse(status_code=401, content=MENSAGEM_LOGIN_INVALIDO)

    chave_secreta = os.getenv("SECRET_KEY")
    if not chave_secreta:
        raise HTTPException(
            status_code=500,
            detail="A SECRET_KEY não está configurada no arquivo .env.",
        )

    expira_em = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {
        "sub": usuario["email"],
        "tipo": usuario["tipo"],
        "exp": expira_em,
    }
    token = jwt.encode(payload, chave_secreta, algorithm=ALGORITMO)

    return {"access_token": token, "token_type": "bearer"}
