from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView

from .forms import ClaimCreateForm, ClaimUpdateForm
from .models import Claim


class PageNameMixin:
    page_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_name
        context['page_header'] = self.page_name
        return context


class HomePageView(PageNameMixin, TemplateView):
    template_name = "claims/home.html"


class ClaimDetailView(PageNameMixin, DetailView):
    model = Claim
    page_name = 'Заявление'


class ClaimListView(PageNameMixin, ListView):
    model = Claim
    page_name = 'Мои заявления'
    context_object_name = 'claims'
    paginate_by = 15


class ClaimCreateView(PageNameMixin, CreateView):
    model = Claim
    page_name = 'Новое заявление'
    success_url = reverse_lazy('claim_list')
    form_class = ClaimCreateForm


class ClaimUpdateView(PageNameMixin, UpdateView):
    model = Claim
    page_name = 'Редактирование заявления'
    success_url = reverse_lazy('claim_list')
    form_class = ClaimUpdateForm
