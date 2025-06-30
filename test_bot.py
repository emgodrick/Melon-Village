#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration du bot
"""

import os
from dotenv import load_dotenv

print("🔍 Test de configuration du bot Discord")
print("=" * 50)

# Charger les variables d'environnement
load_dotenv()

# Vérifier les variables requises
required_vars = {
    'DISCORD_TOKEN': 'Token Discord',
    'GUILD_ID': 'ID du serveur',
    'OWNER_ID': 'ID du propriétaire',
    'OPENAI_API_KEY': 'Clé API OpenAI'
}

print("\n📋 Vérification des variables d'environnement :")
print("-" * 40)

all_good = True
for var_name, description in required_vars.items():
    value = os.getenv(var_name)
    if value:
        # Masquer les valeurs sensibles
        if 'TOKEN' in var_name or 'KEY' in var_name:
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"✅ {description}: {display_value}")
    else:
        print(f"❌ {description}: MANQUANT")
        all_good = False

print("\n🔧 Test des imports :")
print("-" * 20)

try:
    import discord
    print("✅ discord.py")
except ImportError as e:
    print(f"❌ discord.py: {e}")
    all_good = False

try:
    import openai
    print("✅ openai")
except ImportError as e:
    print(f"❌ openai: {e}")
    all_good = False

try:
    from commands import broadcast, ai, shutdown, anti_spam
    print("✅ modules de commandes")
except ImportError as e:
    print(f"❌ modules de commandes: {e}")
    all_good = False

print("\n" + "=" * 50)
if all_good:
    print("🎉 Tous les tests sont passés ! Le bot devrait fonctionner correctement.")
else:
    print("⚠️  Certains tests ont échoué. Vérifiez la configuration.")
print("=" * 50) 