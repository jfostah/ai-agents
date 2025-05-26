import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dispatcher import dispatch_role

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class RoleRequest(BaseModel):
    role: str
    data: dict

# API endpoint for executing a specific agent role
@app.post("/run-role")
def run_role(request: RoleRequest):
    result = dispatch_role(request.role, **request.data)
    return result