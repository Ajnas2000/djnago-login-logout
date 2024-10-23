from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import RegisterUsere,EditForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.http import Http404
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

@never_cache
def login_page(request):
    result = ""
    # If user is already logged in, redirect to main page
    if 'username' in request.session:
        return redirect(main_page)
    
    # Handle POST request for login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # Authenticate the user
        
        if user is not None:
            # Log the user in (this is essential!)
            login(request, user)
            
            # Store the username in the session (optional, since login() handles session)
            request.session['username'] = username
            
            return redirect(main_page)
        else:
            result = "Username or Password not valid"
    
    return render(request, 'login.html', {'error': result})


@never_cache
def main_page(request):
    if 'username' in request.session:
        username=request.session['username']
        return render(request, 'home.html',{'username':username})
    else:
        return redirect(login_page)
      
@never_cache
def user_logout(request):
    if request.method != 'POST':
        raise Http404()
    if 'username' in request.session:
        request.session.flush()
    return redirect(login_page)


@user_passes_test(lambda u: u.is_superuser, login_url='login')
@never_cache
def cadmin(request):
    qs = request.GET.get('qs')
    if qs:
        users = User.objects.filter(username__istartswith=qs)
    else:
        users = User.objects.all()  # Get all users
    return render(request, 'admin.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser, login_url='login')
@never_cache
def user_detials(request, id):
    user =User.objects.get( id=id)  # Use get_object_or_404 for safety
    return render(request, 'detials.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser, login_url='login')
@never_cache
def delete_user(request, id):
    user =User.objects.get( id=id)  # Use get_object_or_404 for safety
    user.delete()  # Delete the user
    messages.success(request,'User Delete Successfully')
    return redirect('cadmin')  # Redirect to admin page

@user_passes_test(lambda u: u.is_superuser, login_url='login')
@never_cache
def user_creation(request):
    form=RegisterUsere()
    if request.method =='POST':
        form=RegisterUsere(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Creation Success')
            return redirect('cadmin')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
            return redirect('register')
    return render(request,'register.html',{'form':form}) 

@user_passes_test(lambda u: u.is_superuser, login_url='login')
@never_cache
def edit_user(request,id):
    user=User.objects.get(id=id)
    form=EditForm(instance=user)
    if request.method=='POST':
        form=EditForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'User Updated Successfully')
            return redirect('cadmin')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    return render(request,'edit.html',{'form':form})

@never_cache
def user_signup(request):
    form=RegisterUsere()
    if request.method =='POST':
        form=RegisterUsere(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
            return redirect('signup')
    return render(request,'signup.html',{'form':form}) 
