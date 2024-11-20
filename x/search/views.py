from django.shortcuts import render
from account.models import User

def search_users(request):
    query = request.GET.get('query', '')
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'searchs/search_form.html', {'results': results, 'query': query})