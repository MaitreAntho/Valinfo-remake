<p align="center">
    <a href="https://github.com/MaitreAntho/Valinfo-remake">
        <img src="docs/assets/images/logo/logo.svg" alt="Logo" width="500" height="100">
    </a>
<h5 align="center">Valinfo</h5>

<p align="center">
  🇬🇧 <a href="README.md">English</a> · 🇫🇷 Français (ce fichier)
</p>

> Ceci est une **continuation communautaire** de [McDaived/Valinfo](https://github.com/McDaived/Valinfo), qui n'est plus maintenu depuis environ 3 ans. Voir la section [Crédits](#crédits) ci-dessous.

## ![](https://img.icons8.com/?size=60&id=A1J30r5KcCb7&format=svg) Fonctionnalités :
|Groupe des adversaires|Skin actuel|Rang actuel|Rank Rating|Rang Max|Niveau du compte|
|:---:|:---:|:---:|:---:|:---:|:---:|
|![Groupes](docs/assets/Party.png)|![Skin](docs/assets/Skin.png)|![Rang](docs/assets/Rank.png)|![RR](docs/assets/Rating.png)|![Rang Max](docs/assets/PeakRank.png)|![Niveau](docs/assets/Level.png)|

- Interface anglais / français, changeable à tout moment depuis le configurateur
- Score de manche en direct, détection des groupes, alertes "déjà joué avec" pour les rencontres récentes
- Discord Rich Presence
- Corrigé pour fonctionner avec le client Valorant actuel et Python 3.10+ (y compris 3.13/3.14)

## ![](https://img.icons8.com/?size=60&id=y5gZPP6Eb5gS&format=svg) À propos :
Pour savoir ce que c'est, visite la page du projet original : [Valinfo](https://mcdaived.github.io/Valinfo)

## ![](https://img.icons8.com/?size=60&id=DWiebo2M1Bbt&format=svg) Utilisation :

1) Installe [Python 3.10 ou plus récent](https://www.python.org/downloads/) et [Git](https://git-scm.com/downloads), en cochant l'ajout au PATH pour les deux.
2) Clone le code source :
   ```
   git clone https://github.com/MaitreAntho/Valinfo-remake.git
   ```
   > Cloner avec git (plutôt que télécharger un zip) est nécessaire pour que `update.bat` fonctionne ensuite.
3) Double-clique sur **`launch.bat`** pour installer les dépendances et lancer Valinfo.

C'est tout — `launch.bat` installe automatiquement ce dont il a besoin au premier lancement.

### Les autres scripts .bat

| Script | Ce qu'il fait |
|---|---|
| `launch.bat` | Installe les dépendances (si besoin) et lance Valinfo |
| `config.bat` | Ouvre le configurateur interactif (langue, arme, colonnes du tableau, port, options...) |
| `update.bat` | Récupère la dernière version depuis git et met à jour les dépendances |

> `-` Tu peux aussi modifier les réglages directement dans `config.json`. Si quelque chose casse après une modification manuelle, supprime simplement `config.json` et Valinfo te reproposera la configuration (ou lance `config.bat`).

## ![](https://img.icons8.com/?size=60&id=42848&format=svg) C'est quoi :

 - [Valorant-API.com](https://valorant-api.com/)

`Cet outil utilise l'API locale du client Valorant — aucun risque de ban car il ne touche jamais à la mémoire ou aux fichiers du jeu.`

Ce projet n'est ni associé à, ni approuvé par RIOT GAMES. Riot Games et toutes les propriétés associées sont des marques commerciales ou déposées de Riot Games, Inc.
Bien que des efforts aient été faits pour respecter les règles de l'API de Riot, l'utilisation de ce logiciel se fait à tes propres risques.

## Crédits

Valinfo a été créé à l'origine par **[McDaived](https://github.com/McDaived)** — tout le mérite du concept original, de sa conception et de plusieurs années de travail lui revient.
Son projet n'est plus maintenu depuis 2023 ; ce dépôt en est une continuation indépendante qui le fait fonctionner avec le client Valorant actuel et y ajoute de nouvelles fonctionnalités (changement de langue, score de manche en direct, corrections pour l'API Riot actuelle, etc.), tout en gardant l'esprit original de l'outil.

Si tu cherches le projet original, non maintenu, il est ici : [McDaived/Valinfo](https://github.com/McDaived/Valinfo).
