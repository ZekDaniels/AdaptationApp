from django import forms
import datetime
from adaptation.models import AdapatationClass, Adaptation, Faculty, Science, StudentClass

STYLES = {
    "date-input":{
        "class": 'form-control'
    },
     "else": {
        'class': 'form-control'
    }
}

class DateInput(forms.DateInput):
    input_type = 'date'

class StyledFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            if self.fields[name].required is True:
                    self.fields[name].label +="*"
            if hasattr(self, "FIELDS"):
                if name in self.FIELDS:
                    self.fields[name].widget.attrs.update(self.FIELDS[name])
            # add some special classes depend on the element
            if self.fields[name].widget.__class__.__name__ in STYLES:
                self.fields[name].widget.attrs.update(STYLES[self.fields[name].widget.__class__.__name__])
            else:
                self.fields[name].widget.attrs.update(STYLES["else"])

class DisableForm(forms.ModelForm, StyledFormMixin):
    
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['disabled'] = True

                
class ProtoAdaptionForm(forms.ModelForm,StyledFormMixin):
    NULL_TUPPLE =  [
    ('', '---------'),
    ]
    faculty = forms.ChoiceField(choices=NULL_TUPPLE, required=True, label="Fakülte")
    science = forms.ChoiceField(choices=NULL_TUPPLE, required=True, label="Bölüm")

    FIELDS = {
        'decision_date':{
            'id':"decision_date",
            'value':"01/01/2021",
        },
        
    }
    

    class Meta:
       model = Adaptation
       exclude = ['is_closed','user','created_at','update_at']
       widgets = {
            'decision_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select Date','type': 'date'})
        }


class AdaptationUpdateForm(ProtoAdaptionForm, StyledFormMixin):
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].choices = [(None, "---------")]
        self.fields['science'].choices = [(None, "---------")]
       
        self.fields['faculty'].choices += [(faculty.id, faculty.name) for faculty in self.instance.university.faculties.all()]
        self.fields['science'].choices += [(science.id, science.name) for science in self.instance.faculty.sciences.all()]

class StudentClassForm(forms.ModelForm, StyledFormMixin):
    
    class Meta:
        model = StudentClass
        exclude = ['adaptation', 'created_at', 'updated_at']


class DisableStudentClassForm(DisableForm):
   
    class Meta:
        model = StudentClass
        exclude = ['adaptation', 'grade','adaptation_class', 'created_at', 'updated_at']

class DisableAdaptationClassForm(DisableForm):
   
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'id':f"id_{name}_adaptation_class"})
   
    class Meta:
        model = AdapatationClass
        exclude = ['is_active', 'education_time', 'class_name_english','user','created_at', 'updated_at']




