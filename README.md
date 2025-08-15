# Discord Bot - Modération & IA

Un bot Discord moderne avec modération automatique par IA, protection anti-spam et outils d'administration.

## ✨ Fonctionnalités

- 🤖 **Modération automatique par IA** - Analyse et modère automatiquement les messages
- 🛡️ **Protection anti-spam** - Détecte et supprime le spam en temps réel
- ⚡ **Commandes de modération** - Ban, kick, timeout, warn, purge
- 📢 **Générateur d'annonces IA** - Crée des annonces formatées automatiquement
- 🔍 **Outils d'information** - Whois, statistiques utilisateur
- 🎛️ **Contrôle d'administration** - Activation/désactivation des modules

## 🚀 Installation

### Prérequis
- Python 3.8+
- Token Discord Bot
- Token OpenAI API

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/discord-bot.git
cd discord-bot
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration**
Créer un fichier `.env` à la racine :
```env
DISCORD_TOKEN=votre_token_discord
OPENAI_API_KEY=votre_token_openai
GUILD_ID=id_de_votre_serveur
OWNER_ID=votre_id_discord
```

4. **Lancer le bot**
```bash
python Bot.py
```

## 📋 Commandes

### Modération
| Commande | Description | Permission |
|----------|-------------|------------|
| `/ban` | Bannir un utilisateur | Admin |
| `/unban` | Débannir un utilisateur | Admin |
| `/kick` | Expulser un utilisateur | Admin |
| `/timeout` | Mettre en timeout | Modérateur |
| `/warn` | Avertir un utilisateur | Modérateur |
| `/purge` | Supprimer des messages | Modérateur |

### Administration
| Commande | Description | Permission |
|----------|-------------|------------|
| `/automod` | Activer/désactiver l'AutoMod | Owner |
| `/antispam` | Activer/désactiver l'anti-spam | Owner |
| `/broadcast` | Générer une annonce IA | Owner |
| `/shutdown` | Éteindre le bot | Owner |

### Information
| Commande | Description | Permission |
|----------|-------------|------------|
| `/whois` | Informations utilisateur | Tous |

## 🔧 Configuration

### Variables d'environnement
- `DISCORD_TOKEN` : Token de votre bot Discord
- `OPENAI_API_KEY` : Clé API OpenAI pour l'AutoMod
- `GUILD_ID` : ID de votre serveur Discord
- `OWNER_ID` : Votre ID Discord (pour les commandes owner)

### Permissions requises
Le bot nécessite les permissions suivantes :
- Gérer les messages
- Expulser des membres
- Bannir des membres
- Gérer les rôles
- Voir les salons
- Envoyer des messages

## 🛠️ Structure du projet

```
Discord_bot/
├── Bot.py                 # Fichier principal
├── commands/              # Modules de commandes
│   ├── ai.py             # Contrôle AutoMod
│   ├── auto_mod.py       # Modération automatique
│   ├── anti_spam.py      # Protection anti-spam
│   ├── broadcast.py      # Générateur d'annonces
│   ├── ban.py            # Commande ban
│   ├── kick.py           # Commande kick
│   ├── timeout.py        # Commande timeout
│   ├── warn.py           # Commande warn
│   ├── purge.py          # Commande purge
│   ├── whois.py          # Commande whois
│   ├── unban.py          # Commande unban
│   └── shutdown.py       # Commande shutdown
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── .gitignore           # Fichiers à ignorer
├── env.example          # Exemple de configuration
└── LICENSE              # Licence
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- 💬 Discord : @emgodrick
- 🐛 Issues : [GitHub Issues](https://github.com/votre-username/discord-bot/issues)

## 🙏 Remerciements

- [discord.py](https://discordpy.readthedocs.io/) - API Discord pour Python
- [OpenAI](https://openai.com/) - API d'intelligence artificielle
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Gestion des variables d'environnement

---

⭐ N'oubliez pas de mettre une étoile si ce projet vous a aidé ! 