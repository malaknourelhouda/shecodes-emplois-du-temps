from sqlalchemy.orm import Session
from app.models import Seance, Salle, Groupe


def detecter_conflits(db: Session, seance_data: dict, ignorer_seance_id: int | None = None):
    """Retourne la liste des conflits détectés (vide = OK)."""
    conflits = []
    q = db.query(Seance).filter(Seance.creneau_id == seance_data["creneau_id"])
    if ignorer_seance_id is not None:
        q = q.filter(Seance.id != ignorer_seance_id)
    meme_creneau = q.all()

    for s in meme_creneau:
        if s.enseignant_id == seance_data["enseignant_id"]:
            conflits.append({
                "type": "enseignant_occupe",
                "message": f"L'enseignant id={s.enseignant_id} a déjà un cours sur ce créneau",
            })
        if s.salle_id == seance_data["salle_id"]:
            conflits.append({
                "type": "salle_occupee",
                "message": f"La salle id={s.salle_id} est déjà occupée sur ce créneau",
            })
        if s.groupe_id == seance_data["groupe_id"]:
            conflits.append({
                "type": "groupe_occupe",
                "message": f"Le groupe id={s.groupe_id} a déjà un cours sur ce créneau",
            })

    salle = db.query(Salle).filter(Salle.id == seance_data["salle_id"]).first()
    groupe = db.query(Groupe).filter(Groupe.id == seance_data["groupe_id"]).first()
    if salle and groupe and salle.capacite < groupe.effectif:
        conflits.append({
            "type": "capacite_insuffisante",
            "message": f"Salle {salle.nom} (capacité {salle.capacite}) trop petite pour le groupe {groupe.nom} (effectif {groupe.effectif})",
        })

    return conflits