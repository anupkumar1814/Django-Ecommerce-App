from ssl import AlertDescription
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes


from django.core.mail import EmailMessage
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is not matching")
            return render(request,'signup.html')
                            
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email,email,password)
        user.is_active=True
        user.save()
        
        return redirect('/auth/login')
    return render(request,"signup.html")


def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            # messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login')

    return render(request,'login.html')  

def handlelogout(request):
    logout(request)
    
    messages.success(request,"Logged Out Success")
    return redirect('/auth/login')