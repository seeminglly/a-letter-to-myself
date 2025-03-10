from django.shortcuts import render

# Create your views here.
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from commons.forms import UserForm

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
            form=UserForm()
    return render(request, 'commons/signup.html', {'form':form})