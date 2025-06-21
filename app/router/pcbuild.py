from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.scheme.pcbuild import PCBuild as PCBuildSchema
from app.models.pcbuild import PCBuild as PCBuildModel

router = APIRouter(prefix="/api/pcbuilds", tags=["PC Builds"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_pc_build(build: PCBuildSchema, db: Session = Depends(get_db)):
    db_build = PCBuildModel(**build.dict())
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    return {"message": "Build saved", "id": db_build.id}
