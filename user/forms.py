from pyexpat import model
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].required = True

    def clean_student_number(self):
        student_number = self.cleaned_data['student_number']

        if not student_number.isdigit():
            raise ValidationError('Sadece numerik karakter girebilirsiniz.')

        if len(student_number) != 9:
            raise ValidationError('Eksik veya fazla karakter girdiniz.')
        
        if Profile.objects.filter(student_number=student_number).count() > 0:
            raise ValidationError('Bu numara ile daha önce kayıt olunmuş.')
        return student_number
    
    def clean_identification_number(self):
        identification_number = self.cleaned_data['identification_number']

        if not identification_number.isdigit():
            raise ValidationError('Sadece numerik karakter girebilirsiniz.')

        if len(identification_number) != 11:
            raise ValidationError('Eksik veya fazla karakter girdiniz.')
        
        if Profile.objects.filter(identification_number=identification_number).count() > 0:
            raise ValidationError('Bu numara ile daha önce kayıt olunmuş.')
        return identification_number

    class Meta:
        model = Profile
        fields = ['namesurname', 'identification_number', 'student_number', 'education_time', 'phone_number', 'education_time']

class ProfileUpdateForm(NewProfileForm):

    class Meta:
        model=Profile
        exclude = ['namesurname', 'phone_number','address','identification_number','student_number','user_image']

class ProfileAdminForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ("created_at", "updated_at")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['namesurname'].widget.attrs['placeholder'] = "Komisyon üyelerini unvan ile beraber giriniz."

    def clean(self):
        cleaned_data = super(ProfileAdminForm, self).clean()
        user_role = cleaned_data.get('user_role')
        
        if user_role == Profile.commission_lead:
            profiles = Profile.objects.filter(user_role=Profile.commission_lead)
            if self.instance:
                profiles.exclude(pk=self.instance.pk)
            count = profiles.count()

            if count > 0:
                raise ValidationError('Birden fazla Komisyon Başkanı giremezsiniz.')

        if user_role == Profile.commission_member:
            profiles = Profile.objects.filter(user_role=Profile.commission_member)
            if self.instance:
                profiles.exclude(pk=self.instance.pk)
            count = profiles.count()
            
            if count > 2:
                raise ValidationError('ikiden fazla Komisyon Üyesi giremezsiniz.')
             
        return cleaned_data