from user.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from adaptation.forms import AdaptationUpdateForm, DisableAdaptationClassForm, DisableAdaptationResultNoteForm, DisableStudentClassForm, DisableAdaptationForm, StudentClassForm, ProtoAdaptionForm, AdaptationResultNoteForm
from adaptation.models import AdapatationClass, Adaptation, StudentClass
from django.contrib import messages
from utilities.render_pdf import render_to_pdf
import re

from io import BytesIO
from django.core.files import File
class AdaptationCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.adaptation is not None:
                return redirect('adaptation:adaptation_manage', request.user.adaptation.get().id)
        except:
            context = {'adaptation_create_form': ProtoAdaptionForm()}
            return render(request, 'adaptation/student/adaptation_create.html', context)
    
class AdaptationManageView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        if not request.user.adaptation:
             return redirect('adaptation:adaptation_create')
        adaptation = get_object_or_404(Adaptation, pk=id, user=request.user)
        adaptation_create_form = AdaptationUpdateForm(instance=adaptation)
        adaptation_classes = AdapatationClass.objects.order_by("id")
        
        class_form = StudentClassForm()
        disable_student_class_form = DisableStudentClassForm()
        disable_adaptation_class_form = DisableAdaptationClassForm()

        context = {
            'adaptation_create_form': adaptation_create_form,
            'class_form': class_form,
            'disable_student_class_form': disable_student_class_form,
            'disable_adaptation_class_form': disable_adaptation_class_form,
            'adaptation':adaptation,
            'adaptation_classes':adaptation_classes,
            }
        return render(request, 'adaptation/student/adaptation_manage.html', context)


class AdaptationList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'adaptation/professor/adaptation_list.html', context)


class AdaptationConfirmationView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        adaptation = get_object_or_404(Adaptation, pk=id)
        adaptation_classes = AdapatationClass.objects.order_by("id")
        disable_student_class_form = DisableStudentClassForm()
        disable_adaptation_class_form = DisableAdaptationClassForm()
        disable_adaptation_form = DisableAdaptationForm(instance=adaptation)
        adaptation_result_note_form = AdaptationResultNoteForm(instance=adaptation)


        context = {
            'adaptation': adaptation,
            'adaptation_classes':adaptation_classes,
            'disable_student_class_form': disable_student_class_form,
            'disable_adaptation_class_form': disable_adaptation_class_form,
            'disable_adaptation_form': disable_adaptation_form,
            'adaptation_result_note_form': adaptation_result_note_form,
        }
        return render(request, 'adaptation/professor/adaptation_confirmation.html', context)

class AdaptationResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        adaptation = None
        if not request.user.adaptation:
             return redirect('adaptation:adaptation_create')

        adaptation = get_object_or_404(Adaptation, user=request.user)

        if not adaptation.is_closed:
            messages.error(request, 'İntibak başvurunuz bitirilmemiş. Lütfen bitirip öyle kontrol ediniz.')
            return redirect('adaptation:adaptation_create')

        disable_student_class_form = DisableStudentClassForm()
        disable_adaptation_class_form = DisableAdaptationClassForm()
        adaptation_result_note_form = DisableAdaptationResultNoteForm(instance=adaptation)

        context = {
            "adaptation": adaptation,
            'disable_student_class_form': disable_student_class_form,
            'disable_adaptation_class_form': disable_adaptation_class_form,
            'adaptation_result_note_form': adaptation_result_note_form,
        }
        return render(request, 'adaptation/student/adaptation_result.html', context)

class AdaptationBasicPDFView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        adaptation = get_object_or_404(Adaptation, user=request.user)
        response = render_to_pdf("adaptation/pdf/adaptation_basic/adaptation_basic.html", {
            'adaptation': adaptation,
        })
        filename = f"tester.pdf"
        content = f"attachment; filename={filename}" if request.GET.get("download") else f"inline; filename={filename}"
        response['Content-Disposition'] = content

        defaults = {'file': File(file=BytesIO(response.content),name=filename), 'adaptation': adaptation}          
       
                              
        return response

class AdaptationComplexPDFView(LoginRequiredMixin, View):
    
    def tr_upper(self, text):
        text = re.sub(r"i", "İ", text)
        text = re.sub(r"ı", "I", text)
        text = re.sub(r"ç", "Ç", text)
        text = re.sub(r"ş", "Ş", text)
        text = re.sub(r"ü", "Ü", text)
        text = re.sub(r"ğ", "Ğ", text)
        text = text.upper() # for the rest use default upper
        return text


    def tr_lower(self, text):
        text = re.sub(r"İ", "i", text)
        text = re.sub(r"I", "ı", text)
        text = re.sub(r"Ç", "ç", text)
        text = re.sub(r"Ş", "ş", text)
        text = re.sub(r"Ü", "ü", text)
        text = re.sub(r"Ğ", "ğ", text)
        text = text.lower() # for the rest use default lower
        return text
        
    def get(self, request, *args, **kwargs):
        adaptation = get_object_or_404(Adaptation, user=request.user)
        adaptation_classes = adaptation.get_adapatation_class_list()
        # translationTable = str.maketrans("ğıiöüşŞç", "ĞIİOuUsScC")

        upper = self.tr_upper(adaptation.user.profile.namesurname)

        response = render_to_pdf("adaptation/pdf/adaptation_complex/adaptation_complex.html", {
            'adaptation': adaptation,
            'adaptation_classes':adaptation_classes,
            'upper':upper,
        })
        filename = f"Form107 Öğrenci İntibak Formu.pdf"
        content = f"attachment; filename={filename}" if request.GET.get("download") else f"inline; filename={filename}"
        response['Content-Disposition'] = content

        defaults = {'file': File(file=BytesIO(response.content),name=filename), 'adaptation': adaptation}          
       
                              
        return response

