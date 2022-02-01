from django.urls import path

from .views import BasicFormView1, BasicFormView2, form_view, index_view, sample_json, sample_json2, register, auth, signin, logout_view

app_name = 'accounts'

urlpatterns = [
    path('welcome', index_view, name='welcome'),
    path('first-form', form_view, name='form1'),
    path('second-form', BasicFormView1.as_view(), name='form2'),
    path('third-form', BasicFormView2.as_view(), name='form3'),
    path('json-1', sample_json, name='json1'),
    path('json-2', sample_json2, name='json2'),
    #Auth endpoint
    path('register', register, name='register'),
    path('signin', signin, name='login'),
    # Authenticated endpoints
    path('auth', auth, name='auth'),
    path('logout', logout_view, name='logout')
]