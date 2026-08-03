import os
import sys
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

TOKEN_SEGURO = "TK-ATOMIC-360-ALFA-OMEGA"
api_key_header = APIKeyHeader(name="X-Tokyo-Token", auto_error=False)

app = FastAPI(title="Ecuación Autónoma API", version="25.2")

class DataInput(BaseModel):
    variables: list[float]

def verificar_token(token: str = Depends(api_key_header)):
    if token != TOKEN_SEGURO:
        raise HTTPException(status_code=403, detail="Acceso denegado.")
    return token

@app.post("/v1/execute", dependencies=[Depends(verificar_token)])
async def ejecutar_ecuacion_autonoma(data: DataInput):
    resultado = [x * 1000 + 1 for x in data.variables]
    return {"status": "INMACULADO", "owner": "José Arturo Orozco Jaime", "data_output": resultado}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
