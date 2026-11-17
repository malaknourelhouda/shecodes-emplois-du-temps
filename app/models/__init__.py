from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Enseignant(Base):
    __tablename__ = "enseignants"
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    grade = Column(String(50), nullable=True)


class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    intitule = Column(String(200), nullable=False)
    volume_horaire = Column(Integer, default=0)
    type = Column(String(20), default="cours")


class Groupe(Base):
    __tablename__ = "groupes"
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    effectif = Column(Integer, default=0)
    section = Column(String(50), nullable=True)


class Salle(Base):
    __tablename__ = "salles"
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), unique=True, nullable=False)
    type = Column(String(20), default="td")
    capacite = Column(Integer, default=0)
    equipements = Column(String(200), nullable=True)


class Creneau(Base):
    __tablename__ = "creneaux"
    id = Column(Integer, primary_key=True)
    jour = Column(String(20), nullable=False)
    heure_debut = Column(String(5), nullable=False)
    heure_fin = Column(String(5), nullable=False)


class Seance(Base):
    __tablename__ = "seances"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    enseignant_id = Column(Integer, ForeignKey("enseignants.id"), nullable=False)
    groupe_id = Column(Integer, ForeignKey("groupes.id"), nullable=False)
    salle_id = Column(Integer, ForeignKey("salles.id"), nullable=False)
    creneau_id = Column(Integer, ForeignKey("creneaux.id"), nullable=False)
    publie = Column(Boolean, default=False)
    cree_le = Column(DateTime, default=datetime.utcnow)

    module = relationship("Module")
    enseignant = relationship("Enseignant")
    groupe = relationship("Groupe")
    salle = relationship("Salle")
    creneau = relationship("Creneau")
