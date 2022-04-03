from django.shortcuts import render

from .models import Claim


def index(request):
    all_claims = Claim.objects.all()
    context = {
        'all_claims': all_claims
    }

    return render(request, 'index.html', context=context)
