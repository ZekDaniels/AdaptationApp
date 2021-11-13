from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import login


from user.forms import NewUserForm, NewProfileForm, UserLoginForm

# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user/dashboard.html', context)


class LoginPageView(LoginView):
    template_name = '../templates/login.html'
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
        return render(request, 'register.html', context)
    
    def post(self, request, *args, **kwargs):
        userform = NewUserForm(request.POST)
        profileform = NewProfileForm(request.POST)
        
        if userform.is_valid() and profileform.is_valid():
            userform.instance.username = profileform.instance.student_number
            user = userform.save()    
            profileform = NewProfileForm(request.POST or None, instance=user.profile)
            profileform.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
        else:
            messages.error(request, "Kayıt Başarısız.")
            return render (request, "register.html", context={"userform":userform, "profileform":profileform})

