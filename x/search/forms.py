from django import forms

class UserSearchForm(forms.Form):
    query = forms.CharField(label="Rechercher un utilisateur", max_length=100)
