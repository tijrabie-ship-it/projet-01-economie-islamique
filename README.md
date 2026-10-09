# Projet 01 — Économie islamique

Application académique développée en Python avec Flask.

## Fonctionnalités
- Analyse des textes de contrats par règles textuelles et AraBERT.
- Calcul de la valeur ajoutée selon le type de transaction.
- Simulation de l’impact de la zakat.
- Comparaison entre financement à intérêt et partage des profits.

## Fichiers
- `app.py` : routes Flask et traitement des entrées.
- `models.py` : fonctions de calcul, simulations et analyse textuelle.
- `templates/` : pages HTML.
- `static/` : fichiers CSS et JavaScript.
- `requirements.txt` : dépendances Python.

## Exécution locale
```bash
pip install -r requirements.txt
python app.py
```
Ouvrir ensuite http://127.0.0.1:5000 dans le navigateur.
Le premier lancement nécessite Internet pour télécharger AraBERT.

## État du prototype
Le code charge un modèle AraBERT de base avec trois classes.
Le dépôt ne contient pas de fine-tuning spécialisé ni d’évaluation
des performances de cette classification.
