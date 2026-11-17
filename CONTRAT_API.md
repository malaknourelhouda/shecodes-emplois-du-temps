# Contrat d'API — à respecter par tous

Base URL : http://localhost:8000

## Référentiels (Alyssa)

### Enseignants
- GET    /api/enseignants              → liste
- POST   /api/enseignants              → créer
- GET    /api/enseignants/{id}         → détail
- PUT    /api/enseignants/{id}         → modifier
- DELETE /api/enseignants/{id}         → supprimer
Champs : id, nom, prenom, email, grade

### Modules
- GET/POST /api/modules
- GET/PUT/DELETE /api/modules/{id}
Champs : id, code, intitule, volume_horaire, type (cours/td/tp)

### Groupes
- GET/POST /api/groupes
- GET/PUT/DELETE /api/groupes/{id}
Champs : id, nom, effectif, section

### Salles
- GET/POST /api/salles
- GET/PUT/DELETE /api/salles/{id}
Champs : id, nom, type (amphi/td/tp), capacite, equipements

### Créneaux
- GET/POST /api/creneaux
- GET/PUT/DELETE /api/creneaux/{id}
Champs : id, jour (lundi..dimanche), heure_debut, heure_fin

### Import CSV
- POST /api/import/csv?type=enseignants  (multipart/form-data, champ "file")
  Types acceptés : enseignants, modules, groupes, salles

## Séances et conflits (Malak)
- GET  /api/seances
- POST /api/seances     → 201 si OK, 409 si conflit (retourne les conflits)
- GET  /api/seances/{id}
- DELETE /api/seances/{id}
Champs séance : id, module_id, enseignant_id, groupe_id, salle_id, creneau_id

Réponse 409 (conflit) :
{ "detail": { "conflits": [ {"type": "enseignant_occupe", "message": "..."} ] } }

## Auth (Malak)
- POST /api/auth/login   { username, password } → { access_token, token_type, role }
- GET  /api/auth/me      → utilisateur courant

## Santé et métriques (Malak)
- GET /health  → { "status": "ok" }
- GET /metrics → { "seances_total": N, "conflits_detectes_total": N }

## Frontend (Yasmine)
- GET /  → page HTML emploi du temps
