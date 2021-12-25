from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from adaptation.forms import AdaptationUpdateForm, ClassForm, ProtoAdaptionForm
from adaptation.models import AdapatationClass, Adaptation

class AdaptationCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.adaptation is not None:
                return redirect('adaptation:adaptation_manage', request.user.adaptation.get().id)
        except:
            context = {'adaptation_create_form': ProtoAdaptionForm()}
            return render(request, 'adaptation/adaptation_create.html', context)
    
class AdaptationManageView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        if not request.user.adaptation:
             return redirect('adaptation:adaptation_create')
        adaptation = get_object_or_404(Adaptation, pk=id)
        adaptation_create_form = AdaptationUpdateForm(instance=adaptation)
        adaptation_classes = AdapatationClass.objects.order_by("id")
        class_form = ClassForm()
        context = {
            'adaptation_create_form': adaptation_create_form,
            'class_form': class_form,
            'adaptation':adaptation,
            'adaptation_classes':adaptation_classes,
            }
        return render(request, 'adaptation/adaptation_manage.html', context)
