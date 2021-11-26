from django import forms
import datetime
from adaptation.models import Adaptation

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
    
class ProtoAdaptionForm(forms.ModelForm):
    NULL_TUPPLE =  [
    ('', '---------'),
    ]
    faculty = forms.ChoiceField(choices=NULL_TUPPLE, required=True)
    science = forms.ChoiceField(choices=NULL_TUPPLE, required=True)

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
                print(name)
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
            'decision_date': DateInput()
        }