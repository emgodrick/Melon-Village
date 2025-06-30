# Bot Discord

Ce bot Discord offre plusieurs fonctionnalités utiles pour gérer votre serveur.

## Prérequis

- Python 3.8 ou supérieur
- Un token Discord (à obtenir via le [Portail Développeur Discord](https://discord.com/developers/applications))
- Un token OpenAI (à obtenir via le [Portail OpenAI](https://platform.openai.com/api-keys))

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

2. Créez un fichier `.env` à la racine du projet et ajoutez vos tokens :
```
DISCORD_TOKEN=votre_token_discord_ici
OPENAI_API_KEY=votre_token_openai_ici
```

## Démarrage

Pour lancer le bot, exécutez :
```bash
python bot.py
```

## Fonctionnalités
- **Auto Mod** : Assistant AI automatique
- **Modération** : Commandes de modération pour gérer votre serveur
- **Sondages** : Création de sondages interactifs


## Commandes

### Commandes de Modération
- `/ban [utilisateur] [raison]` : Bannir un utilisateur du serveur
- `/unban [id_utilisateur] [raison]` : Débannir un utilisateur
- `/kick [utilisateur] [raison]` : Expulser un utilisateur du serveur
- `/timeout [utilisateur] [durée] [raison]` : Mettre un utilisateur en timeout
- `/warn [utilisateur] [raison]` : Avertir un utilisateur et le mute pendant 5 minutes
- `/purge [utilisateur] [nombre]` : Supprimer les derniers messages d'un utilisateur

### Commandes d'Information
- `/whois [utilisateur]` : Affiche les informations détaillées d'un utilisateur

### Commandes d'Administration
- `/automod [on/off]` : Active ou désactive la modération automatique (Admin uniquement)
- `/antispam [on/off]` : Active ou désactive la protection anti-spam (Admin uniquement)
- `/shutdown` : Éteint le bot (Admin uniquement)


## Support

Si vous rencontrez des problèmes ou avez des questions, n'hésitez pas à :
1. Ouvrir une issue sur GitHub
2. Contactez moi sur Discord (@emgodrick)

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 