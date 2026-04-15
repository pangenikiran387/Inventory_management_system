from django.shortcuts import redirect

def admin_only(func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_staff:
            return func(request,*args,**kwargs)
        else:
            return redirect('homepage')
    return wrapper_func

def user_only(func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return func(request,*args,**kwargs)
    return wrapper_func

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_staff(user):
    return user.groups.filter(name='Staff').exists()