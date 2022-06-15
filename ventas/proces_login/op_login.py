from re import template
from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def iniciar_session(request):
    url='op_login/login.html'
    form_session=AuthenticationForm()
    if request.method=='POST':
        form_session=AuthenticationForm(data=request.POST)
        if form_session.is_valid():
            username=form_session.cleaned_data['username']
            password=form_session.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('store:index')
    
    context={
        'form':form_session
    }
    
    return render(
        request, 
        url, 
        context
    )

def cerrar_session(request):
    template_name="op_login/logout.html"
    logout(request)
    return render(
        request,
        template_name
    )