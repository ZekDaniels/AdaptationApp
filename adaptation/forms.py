from django import forms
import datetime
from adaptation.models import Adaptation, Faculty, Science, StudentClass

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
            if hasattr(self, "FIELDS"):
                if name in self.FIELDS:
                    self.fields[name].widget.attrs.update(self.FIELDS[name])
            # add some special classes depend on the element
            if self.fields[name].widget.__class__.__name__ in STYLES:
                self.fields[name].widget.attrs.update(STYLES[self.fields[name].widget.__class__.__name__])
            else:
                self.fields[name].widget.attrs.update(STYLES["else"])
                
class ProtoAdaptionForm(forms.ModelForm):
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            
            if name in self.FIELDS:
                self.fields[name].widget.attrs.update(self.FIELDS[name])
            # add some special classes depend on the element
            if self.fields[name].widget.__class__.__name__ in STYLES:
                self.fields[name].widget.attrs.update(STYLES[self.fields[name].widget.__class__.__name__])
            else:
                self.fields[name].widget.attrs.update(STYLES["else"])

    class Meta:
       model = Adaptation
       exclude = ['created_at','update_at','user']
       widgets = {
            'decision_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select Date','type': 'date'})
        }


class AdaptationUpdateForm(ProtoAdaptionForm):
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].choices = [(None, "---------")]
        self.fields['science'].choices = [(None, "---------")]
       
        self.fields['faculty'].choices += [(faculty.id, faculty.name) for faculty in self.instance.university.faculties.all()]
        self.fields['science'].choices += [(science.id, science.name) for science in self.instance.faculty.sciences.all()]

class StudentClassForm(forms.ModelForm, StyledFormMixin):
    
    class Meta:
        model = StudentClass
        exclude = ['user','adapatation_class', 'created_at', 'updated_at']



