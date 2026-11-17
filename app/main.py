from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import engine, Base, get_db
from app import models
from app.services.conflits import detecter_conflits

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SheCodes - Emplois du temps", version="1.0.0")


class SeanceIn(BaseModel):
    module_id: int
    enseignant_id: int
    groupe_id: int
    salle_id: int
    creneau_id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    total = db.query(models.Seance).count()
    return {"seances_total": total}


@app.get("/api/seances")
def lister_seances(db: Session = Depends(get_db)):
    return db.query(models.Seance).all()


@app.post("/api/seances", status_code=201)
def creer_seance(payload: SeanceIn, db: Session = Depends(get_db)):
    data = payload.model_dump()
    conflits = detecter_conflits(db, data)
    if conflits:
        raise HTTPException(status_code=409, detail={"conflits": conflits})
    seance = models.Seance(**data)
    db.add(seance)
    db.commit()
    db.refresh(seance)
    return seance


@app.delete("/api/seances/{seance_id}", status_code=204)
def supprimer_seance(seance_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Seance).filter(models.Seance.id == seance_id).first()
    if not s:
        raise HTTPException(404, "Séance introuvable")
    db.delete(s)
    db.commit()
