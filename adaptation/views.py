from django.shortcuts import render
from django.views.generic.base import View
from adaptation.forms import ProtoAdaptionForm


class ProtoAdaptionCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {'adaptation_create_form': ProtoAdaptionForm()}
        return render(request, 'adaptation/adaptation_create.html', context)
