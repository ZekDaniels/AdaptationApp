from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib.auth import login
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from user.tokens import account_activation_token
from user.forms import NewUserForm, NewProfileForm, ProfileUpdateForm, UserLoginForm

# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user/dashboard.html', context)


class LoginPageView(LoginView):
    template_name = '../templates/registration/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(LoginPageView, self).form_valid(form)
    
    
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        userform = NewUserForm()
        profileform = NewProfileForm()
        context = {'userform':userform, 'profileform':profileform}
        return render(request, 'registration/register.html', context)
    
    def post(self, request, *args, **kwargs):
        userform = NewUserForm(request.POST)
        profileform = NewProfileForm(request.POST)
        
        if userform.is_valid() and profileform.is_valid():
            userform.instance.username = profileform.instance.student_number
            with transaction.atomic():
                user = userform.save(commit=False)  
                user.is_active = False
                user.save()  
                current_site = get_current_site(request)
                mail_subject = 'Hesabını aktif hale getir.'
                message = render_to_string('registration/mail/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                })
                to_email = userform.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                profileform = NewProfileForm(request.POST or None, instance=user.profile)
                profileform.save()
               
            return render (request, "registration/register_done.html")
        else:
            return render (request, "registration/register.html", context={"userform":userform, "profileform":profileform})

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        userform = NewUserForm()
        profileform = ProfileUpdateForm()
        context = {'userform':userform, 'profileform':profileform}
        return render(request, 'registration/register.html', context)

class ActivationView(View):
    def get(self, request, uidb64,token,*args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render (request, "registration/register_complete.html")
        else:
            return render (request, "registration/register_failed.html")
    