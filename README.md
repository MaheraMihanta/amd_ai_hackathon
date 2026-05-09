# Gestion Stock Vision

Prototype local de l'etape 1 du projet: gestion de stock, recherche d'article,
selection d'une image simulee et interface graphique pour le poste pharmacien.

## Installation locale

Python 3.12 est utilise pendant le developpement.

```powershell
python -m pip install -r requirements.txt
```

## Lancer l'interface graphique

```powershell
python gui.py
```

L'interface CustomTkinter contient:

- une liste du stock chargee depuis `data/inventory.csv`;
- une zone de demande client avec recherche par nom ou ID;
- une simulation de selection d'image et de deplacement robot;
- une zone "Assistant pharmacien LLM - futur" qui prepare le contexte a envoyer
  a un LLM, sans delivrer automatiquement un medicament.

## Lancer la simulation console

Afficher l'inventaire:

```powershell
python app.py --list
```

Rechercher un article par ID:

```powershell
python app.py --query MED-001 --quantity 2
```

Rechercher un article par nom:

```powershell
python app.py --query amoxicilline
```

Lancer le mode interactif:

```powershell
python app.py
```

## Point d'integration prioritaire: vision par ordinateur

Le premier branchement a faire apres l'etape 1 est dans `vision.py`, fonction:

```python
process_image(image_path)
```

Flux attendu:

1. `app.py` verifie l'article et le stock avec `prepare_selection(...)`.
2. `gui.py` recupere `article.image_path`.
3. `gui.py` appelle `vision.process_image(image_path)`.
4. Le futur modele de vision confirme ou refuse la detection du medicament.
5. Les modules suivants automatisent seulement si la vision confirme.

Pour l'instant, `vision.py` retourne volontairement "module non configure".
C'est le point exact a remplacer par YOLO, Qwen-VL, Llama Vision ou un modele
medical specialise quand le projet sera deploye sur le Cloud AMD.

## Ouverture LLM

Le fichier `llm_assistant.py` prepare un prompt pour un futur assistant
conversationnel. Role prevu: aider le pharmacien a structurer l'echange quand
le client n'a pas d'ordonnance et decrit seulement des symptomes.

Regle importante: le LLM doit assister le pharmacien, pas remplacer son avis.
La recommandation finale et la delivrance restent validees par le pharmacien.

## Tester

```powershell
python -m unittest discover -s tests
```

## Structure

- `app.py`: logique de simulation des modules 1 et 2.
- `gui.py`: interface graphique CustomTkinter pour finaliser l'etape 1.
- `vision.py`: point d'integration du futur module de vision par ordinateur.
- `llm_assistant.py`: preparation du contexte pour un futur LLM pharmacien.
- `data/inventory.csv`: inventaire de depart avec ID, nom, classe therapeutique, rayon, stock, prix et image.
- `images/`: visuels SVG generes pour la demonstration.
- `tests/`: tests des scenarios principaux.
