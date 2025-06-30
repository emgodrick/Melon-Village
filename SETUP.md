# Configuration du Bot Discord

## Variables d'environnement requises

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Configuration Discord
DISCORD_TOKEN=votre_token_discord_ici
GUILD_ID=1293979587264380928
OWNER_ID=829064566742057020

# Configuration OpenAI (pour la commande /broadcast)
OPENAI_API_KEY=votre_clé_api_openai_ici
```

## Où trouver ces informations :

1. **DISCORD_TOKEN** : Dans le portail développeur Discord
2. **GUILD_ID** : ID de votre serveur Discord (clic droit sur le serveur → Copier l'ID)
3. **OWNER_ID** : Votre ID utilisateur Discord (clic droit sur votre nom → Copier l'ID)
4. **OPENAI_API_KEY** : Dans votre compte OpenAI (https://platform.openai.com/api-keys)

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python Bot.py
```

## Sécurité

⚠️ **IMPORTANT** : Ne partagez jamais votre fichier `.env` ou vos tokens ! 