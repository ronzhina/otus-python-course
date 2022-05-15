from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView
from django.views.generic.base import ContextMixin

from django.views.generic.base import TemplateResponseMixin

from .forms import ClaimCreateForm, ClaimUpdateForm
from .models import Claim


def accept_claim(request, pk):
    Claim.objects.filter(pk=pk).update(status=Claim.ClaimStatus.ACCEPTED)
    return redirect('claim_approve_list')


def reject_claim(request, pk):
    Claim.objects.filter(pk=pk).update(status=Claim.ClaimStatus.REJECTED)
    return redirect('claim_approve_list')


class PageNameMixin(ContextMixin):
    page_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['page_title'] = self.page_name
        context['page_header'] = self.page_name
        return context


class HomePageView(PageNameMixin, TemplateView):
    template_name = "claims/home.html"


class ClaimDetailView(LoginRequiredMixin, PageNameMixin, DetailView):
    model = Claim
    page_name = 'Заявление'


class ClaimListView(LoginRequiredMixin, PageNameMixin, ListView):
    model = Claim
    page_name = 'Мои заявления'
    context_object_name = 'claims'
    paginate_by = 15

    def get_queryset(self):
        return Claim.objects.filter(employee=self.request.user)


class ClaimApproveListView(LoginRequiredMixin, PageNameMixin, ListView):
    model = Claim
    page_name = 'Мои задания'
    context_object_name = 'claims'
    paginate_by = 15
    template_name = 'claims/claim_approve_list.html'
    body_size = 'col-10'

    def get_queryset(self):
        return Claim.objects.filter(agreed_with=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['body_size'] = self.body_size
        return context


# UserPassesTestMixin
class ClaimCreateView(LoginRequiredMixin, PageNameMixin, CreateView):
    model = Claim
    page_name = 'Новое заявление'
    success_url = reverse_lazy('claim_list')
    form_class = ClaimCreateForm


#    def test_func(self):
#        return True


class ClaimUpdateView(LoginRequiredMixin, PageNameMixin, UpdateView):
    model = Claim
    page_name = 'Редактирование заявления'
    success_url = reverse_lazy('claim_list')
    form_class = ClaimUpdateForm
