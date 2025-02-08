# 📊 DataBot

## Description
DataBot est une application interactive développée avec **Streamlit** et le modèle **Claude 3.5 Sonnet**, permettant aux utilisateurs d'analyser et de visualiser leurs données tabulaires grâce à l'intelligence artificielle.

## 🌐 View the App

You can access the Streamlit-hosted application here:  
➡️ [DataBot](https://databotyba.streamlit.app/)




## Fonctionnalités 🚀
- **Chat interactif** : Un chatbot intelligent qui guide l'utilisateur dans l'exploration de ses données.
- **Importation de données** : Téléchargement de fichiers **CSV** pour analyse.
- **Nettoyage des données** :
  - Remplacement des valeurs nulles :
    - Variables numériques : médiane
    - Variables catégorielles : mode
  - Suppression des colonnes dupliquées.
- **Exploration et visualisation** :
  - Description générale des données.
  - Analyse spécifique de certaines colonnes ou variables.
  - Génération automatique de graphiques pertinents avec une interprétation détaillée.

## Structure du projet 📂

Voici une vue d'ensemble des fichiers et dossiers principaux du projet :

```plaintext    
├── docs/                     # Documentation du projet  
├── images/                   # Aperçu de l'application  
├── src/                      # Code source principal de l'application  
│   ├── dataexplorer/         # Dossier principal  
│   │   ├── app.py           # Implementation de l'application
│   │   ├── chat.py           # Implementation du chatbot
│   │   ├── utils.py          # Fichier responsable du nettoyage des données  
├── tests/                    # Tests unitaires et fonctionnels  
│   │   ├── test_clean_dataset.py # Fichier pour tester le netoyage des données
│   │   ├── test_datachatbot.py # Fichier pour tester le chatbot  
├── .coverage                 # Rapport de couverture des tests  
├── .gitignore                # Liste des fichiers ignorés par Git  
├── .pre-commit-config.yaml   # Configuration pour pre-commit  
├── poetry.lock               # Verrouillage des dépendances Python  
├── pyproject.toml            # Fichier de configuration pour Poetry  
├── README.md                 # Documentation principale du projet  
 
```

## Installation 🛠️
### Prérequis
- Python 3.12
- Poetry
- Clé API **Anthropic** pour pourvoir accéder au modèle **Claude 3.5 Sonnet**


### Étapes d'installation
1. **Cloner le projet**
   ```bash
   git clone https://github.com/nadyby/Databot.git
   cd Databot
   ```
2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   poetry env use python
   poetry shell
   poetry build
   ```
3. **Installer les dépendances**
   ```bash
   poetry install
   ```
4. **Configurer la clé API Claude**
   - Créer un fichier `.env` à la racine du projet et y ajouter la clé API :
     ```ini
     ANTHROPIC_API_KEY=ta_clé_API
     ```
   - Ajouter `.env` au fichier `.gitignore` pour éviter de commettre la clé API dans le dépôt Git.


## Utilisation 🖥️
1. **Lancer l'application**
   ```bash
   cd src
   cd databot
   poetry run streamlit run chat.py
   ```
2. **Page d'accueil** : Cliquer sur le bouton pour commencer l'exploration de vos données.
![accueil](images/accueil.png)

3. **Charger un fichier CSV** : L'application propose un bouton pour effectuer un nettoyage des données avant de permettre l'analyse et la visualisation.
![chatbot](images/chat.png)
![dataset](images/dataset.png)

4. **Interagir avec le chatbot** pour explorer et visualiser les données.
![plot](images/exemple_plot.jpeg)


## Exemples de requêtes 💡
- "Donne-moi une description générale des données."
- "Affiche-moi un histogramme de la colonne 'âge'."
- "Y a t-il les valeurs manquantes dans mon dataset ?"
- "Génère un scatter plot entre 'revenu' et 'score_credit'."

## Auteur
- **Yassine Ben Abdallah**

## Licence 📜
Ce projet est sous licence **MIT**.
