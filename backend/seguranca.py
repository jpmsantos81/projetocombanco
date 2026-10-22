# ============================================================
# seguranca.py — Verificação de tokens JWT
# Descrição: Valida o token antes de executar rotas protegidas.
# ============================================================

import os
from typing import Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

esquema_token = HTTPBearer()


# Verifica assinatura e validade do token enviado na requisição
def verificar_token(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_token),
) -> dict[str, Any]:
    chave_secreta = os.getenv("SECRET_KEY")
    if not chave_secreta:
        raise HTTPException(
            status_code=500,
            detail="A SECRET_KEY não está configurada no arquivo .env.",
        )

    try:
        return jwt.decode(
            credenciais.credentials,
            chave_secreta,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as erro:
        raise HTTPException(
            status_code=401,
            detail="Token expirado, faça login de novo.",
        ) from erro
    except jwt.InvalidTokenError as erro:
        raise HTTPException(status_code=401, detail="Token inválido.") from erro
