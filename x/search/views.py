from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User

class UserSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'searchs/search_form.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
