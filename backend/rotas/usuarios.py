# ============================================================
# rotas/usuarios.py — Cadastro de Usuários
# Descrição: Cadastra usuários guardando a senha como hash.
# ============================================================

import bcrypt
from fastapi import APIRouter, HTTPException
from mysql.connector.errors import IntegrityError
from pydantic import BaseModel
from database import conectar

router = APIRouter()


# Modelo de dados — define os campos que o usuário deve ter
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str


# POST /usuarios — cadastra usuário sem armazenar a senha original
@router.post("")
def criar_usuario(usuario: Usuario):
    senha_bytes = usuario.senha.encode("utf-8")
    if len(senha_bytes) > 72:
        raise HTTPException(
            status_code=422,
            detail="A senha deve ter no máximo 72 bytes para ser processada pelo bcrypt.",
        )

    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, senha_hash),
        )
        conn.commit()
    except IntegrityError as erro:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não foi possível cadastrar. Verifique se esse e-mail já está em uso.",
        ) from erro
    finally:
        cursor.close()
        conn.close()

    return {"mensagem": "Usuário cadastrado com sucesso"}
