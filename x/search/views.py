from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import User

@login_required
def search_users(request):
    query = request.GET.get('query', '')
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'searchs/search_form.html', {'results': results, 'query': query})