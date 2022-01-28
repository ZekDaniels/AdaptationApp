from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user.models import Profile


STYLES = {
     "else": {
        'class': 'form-control'
    }
}


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
                
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
    

class UserPasswordResetForm(StyledFormMixin, PasswordResetForm):
     
    FIELDS = {}

class UserSetPasswordForm(StyledFormMixin, SetPasswordForm):

    FIELDS = {}


class NewUserForm(UserCreationForm, StyledFormMixin):    
    email = forms.EmailField(required=True)
                     
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewProfileForm(forms.ModelForm, StyledFormMixin):
    
    student_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'type':'number'}) )
    
    def clean_student_number(self):
        student_number = self.cleaned_data['student_number']
        if len(student_number) != 9:
            raise ValidationError('Eksik veya fazla karakter girdiniz..')
        
        if Profile.objects.filter(student_number=student_number).count() > 0:
            raise ValidationError('Bu numara ile daha önce kayıt olunmuş..')
        return student_number
    
    class Meta:
        model = Profile
        fields = ['namesurname', 'student_number', 'education_time', 'phone_number']
