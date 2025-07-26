# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import networth, mutualfunds, epf, credit
from .routers.common.summary import router as summary_router
from .routers.agent_endpoints import router as agent_router
from .routers.security import router as security_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(networth.router, prefix="/networth")
app.include_router(mutualfunds.router, prefix="/mutualfunds")
app.include_router(epf.router, prefix="/epf")
app.include_router(credit.router, prefix="/credit")
app.include_router(summary_router, prefix="/common")
app.include_router(agent_router, prefix="/agent")
app.include_router(security_router, prefix="/security")
