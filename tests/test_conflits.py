import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Enseignant, Module, Groupe, Salle, Creneau, Seance
from app.services.conflits import detecter_conflits


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def _seed(db):
    db.add_all([
        Enseignant(id=1, nom="A", prenom="A", email="a@x.dz"),
        Module(id=1, code="M1", intitule="Math"),
        Groupe(id=1, nom="G1", effectif=30),
        Salle(id=1, nom="S1", capacite=50),
        Salle(id=2, nom="Petite", capacite=10),
        Creneau(id=1, jour="lundi", heure_debut="08:00", heure_fin="09:30"),
    ])
    db.commit()


def test_aucun_conflit(db):
    _seed(db)
    data = dict(module_id=1, enseignant_id=1, groupe_id=1, salle_id=1, creneau_id=1)
    assert detecter_conflits(db, data) == []


def test_enseignant_occupe(db):
    _seed(db)
    db.add(Seance(module_id=1, enseignant_id=1, groupe_id=1, salle_id=1, creneau_id=1))
    db.commit()
    data = dict(module_id=1, enseignant_id=1, groupe_id=1, salle_id=1, creneau_id=1)
    conflits = detecter_conflits(db, data)
    assert any(c["type"] == "enseignant_occupe" for c in conflits)


def test_salle_occupee(db):
    _seed(db)
    db.add(Seance(module_id=1, enseignant_id=1, groupe_id=1, salle_id=1, creneau_id=1))
    db.commit()
    db.add(Enseignant(id=2, nom="B", prenom="B", email="b@x.dz"))
    db.add(Groupe(id=2, nom="G2", effectif=20))
    db.commit()
    data = dict(module_id=1, enseignant_id=2, groupe_id=2, salle_id=1, creneau_id=1)
    conflits = detecter_conflits(db, data)
    assert any(c["type"] == "salle_occupee" for c in conflits)


def test_capacite_insuffisante(db):
    _seed(db)
    data = dict(module_id=1, enseignant_id=1, groupe_id=1, salle_id=2, creneau_id=1)
    conflits = detecter_conflits(db, data)
    assert any(c["type"] == "capacite_insuffisante" for c in conflits)
