# Scraping des Données de Livres

## Description

Ce projet permet de scraper des données depuis le site "Books to Scrape", incluant des informations détaillées sur chaque livre ainsi que leurs images associées. Les données sont sauvegardées dans des fichiers CSV et les images sont stockées dans des répertoires par catégorie.

## Prérequis

- Python 3.x
- Les bibliothèques Python spécifiées dans `requirements.txt`

## Installation

Clonez le repository :

```bash
git clone https://github.com/LuuNa-JD/books-online-scraper.git
cd books-online-scraper
```

Créez un environnement virtuel et activez-le :

```bash
python -m venv venv
source venv/bin/activate # Linux
venv\Scripts\activate # Windows
```

Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez le script principal :

```bash
python scraper.py
```
Les données seront sauvegardées dans des fichiers CSV et les images seront stockées dans des répertoires sous 'images/'.


## Structure du Projet

scraper.py : Script principal pour lancer le scraping des données.
requirements.txt : Liste des dépendances Python.
README.md : Description du projet.
gitingore : Fichiers à ignorer pour le versionning.

## Auteur

Julien Denizot
