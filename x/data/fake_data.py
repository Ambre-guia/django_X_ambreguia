import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'x.settings')

import django
django.setup()

import json
from django.core.files.base import ContentFile
from account.models import User
from post.models import Tweet
import requests

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'fake_accounts.json')

if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    print("Données chargées avec succès !")

    for account in data['users']:
        email = account['email']

        # Vérifier si l'utilisateur existe déjà
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': account['username'],
                'password': account['password']
            }
        )

        # Si l'utilisateur est créé, on définit son mot de passe
        if created:
            user.set_password(account['password'])
            user.save()

        # Ajouter la photo de profil si elle existe
        if account.get('profile_picture'):
            response = requests.get(account['profile_picture'])
            if response.status_code == 200:
                user.profile_picture.save(
                    f"{account['username']}_profile.jpg",
                    ContentFile(response.content),
                    save=True
                )

        # Créer les tweets associés à l'utilisateur
        for post in account['tweets']:
            tweet = Tweet.objects.create(
                user=user,
                content=post['content']
            )
            if post.get('image'):
                response = requests.get(post['image'])
                if response.status_code == 200:
                    tweet.image.save(
                        f"{user.username}_post_{tweet.id}.jpg",
                        ContentFile(response.content),
                        save=True
                    )

    print(f"Le fichier {json_file_path} a bien été importé")

else:
    print(f"Le fichier {json_file_path} n'existe pas.")
