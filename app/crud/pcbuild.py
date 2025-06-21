from sqlalchemy.orm import Session
from app.models.pcbuild import PCBuild
from app.scheme.pcbuild import PCBuild

def create_pc_build(db: Session, build_data: PCBuild):
    db_build = PCBuild(**build_data.dict())
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    return db_build

def get_all_builds(db: Session):
    return db.query(PCBuild).all()
