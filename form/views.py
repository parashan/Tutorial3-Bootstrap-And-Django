from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .forms import EnterForm, RegisterForm, LoginForm
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
# from django.forms import EnterForm
# Build a form using Django 3 different ways
# We use templates for our data for now. https://docs.djangoproject.com/en/4.0/intro/tutorial03/

#Note we use shortcut 'render' instead of returning an HttpResponse or TemplateResponse

def index_view(request):
    return render(request, 'forms/index.html')

#Functional 
def form_view(request):
    if request.method == 'POST':

        print(request.POST)

        form = EnterForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('welcome')
        print(form.errors.as_json())
    else:
        form = EnterForm()
    
    return render(request, 'forms/form.html', {'form': form})

# Class Based View

class BasicFormView1(View):
    template_name = 'forms/form.html'
    form_class = EnterForm

    def get(self, request, *args, **kwargs):
        form  = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/welcome')

        return render(request, self.template_name, {'form': form})


# Class Based FormView

class BasicFormView2(FormView):
    template_name = 'forms/form.html'
    form_class = EnterForm
    success_url = '/welcome'
    
    def form_valid(self, form):

        return super().form_valid(form)
        

# JSON Responses

def sample_json2(request):
    if request.method == 'GET':
        responseData = {
            'id': 1,
            'name': 'Sample 2'
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

def sample_json(request):
    if request.method == 'GET':
        responseData = {
            'id': 1,
            'name': 'Hans Paras'
        }
        return JsonResponse(responseData)
    return JsonResponse({})



# Authentication
# settings.py contaisn a LOGIN_URL that will be the redirect url
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('signin')

@login_required
def auth(request):
    return render(request, 'forms/auth.html', {'user': request.user})

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user= authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('auth')
            else:
                form.add_error(None, "Incorrect Username or Password")
        return render(request, 'forms/signin.html', {'form': form})

    form = LoginForm()
    return render(request, 'forms/signin.html', {'form': form})

from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                user = form.cleaned_data['user_name']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                save_user = User.objects.create_user(user, email=email, password=password)
                
                save_user.save()
                
                return HttpResponseRedirect('signin')
            except Exception as error:
                print("This error is", error)
                form.add_error(None, "Generic Server Error")            
        

    else:
        form = RegisterForm()
    return render(request, 'forms/register.html', {'form': form})
        
    


