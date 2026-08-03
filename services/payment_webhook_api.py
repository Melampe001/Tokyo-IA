from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from real_monetization_core import NulogicMonetizationEngine, PRODUCTS_CATALOG
from okx_signals_engine import OKXSignalsEngine
from license_gatekeeper import FlaggShipGatekeeper

app = FastAPI(
    title="RascaCielos-Digital® & FlaggShip Apps - Ecosystem API",
    version="24.5",
    description="Backend unificado de Monetización, Señales OKX y Gatekeeper de Licencias"
)

engine = NulogicMonetizationEngine()
okx_engine = OKXSignalsEngine()
gatekeeper = FlaggShipGatekeeper()

class PurchaseRequest(BaseModel):
    product_key: str  # 'A', 'B', 'C' o 'D'
    customer_email: str
    customer_name: str = "Tokyo M."

class ValidateLicenseRequest(BaseModel):
    license_key: str
    developer_token: str = "DEV-FLAGGSHIP-CORE-2026"

@app.get("/catalog")
def get_catalog():
    return {"brand": "RascaCielos-Digital® / FlaggShip Apps", "catalog": PRODUCTS_CATALOG}

@app.post("/buy")
def buy_product(req: PurchaseRequest, bg_tasks: BackgroundTasks):
    if req.product_key not in PRODUCTS_CATALOG:
        raise HTTPException(status_code=400, detail="Código de producto inválido. Selecciona A, B, C o D.")
    
    bg_tasks.add_task(engine.deliver_product, req.product_key, req.customer_email, req.customer_name)
    return {
        "status": "PROCESSING",
        "message": f"Procesando entrega del producto {PRODUCTS_CATALOG[req.product_key]['name']} para {req.customer_email}."
    }

@app.get("/v1/signals/okx")
def get_okx_signal(license_key: str):
    result = okx_engine.generate_signal(license_key)
    if result.get("status") == "ERROR":
        raise HTTPException(status_code=403, detail=result.get("message"))
    return result

@app.post("/v1/gatekeeper/verify")
def verify_dev_license(req: ValidateLicenseRequest):
    result = gatekeeper.validate_remote_client(req.developer_token, req.license_key)
    if not result.get("authorized"):
        raise HTTPException(status_code=401, detail=result.get("reason"))
    return result
