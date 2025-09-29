from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from patientapp.models import Patient
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser


# Create your views here.
def add_patient(request: HttpRequest):
    
    print(f"is user authenticated: {request.user.is_authenticated}")

    print(f"is user a staff memeber: {request.user.is_staff}")

    #todo check svnr
    isSVNRValid = True

    if request.method == "POST" and request.user.is_staff:
        
        Patient.objects.create(
            first_name=request.POST.get('firstname'),
            last_name=request.POST.get('lastname'),
            birthday=request.POST.get('birthday'),
            svnr=request.POST.get('svnr')
            )
        return redirect('/patients/')
    return render(request, 'addpatient.html', context={'isSVNRValid': isSVNRValid})

def list_patient(request: HttpRequest):

    if(request.method == 'POST'):

        Patient.objects.get(id=int(request.POST["idtodelete"])).delete()    


    return render(request, 'listpatients.html', context={'patients': Patient.objects.all()})

def edit_patient(request: HttpRequest, id: int):
    #print(request.path)
    
    if request.method == "POST" and request.user.is_staff:
        Patient.objects.filter(id=id).update(
            first_name=request.POST.get('firstname'),
            last_name=request.POST.get('lastname'),
            birthday=request.POST.get('birthday'),
            svnr=request.POST.get('svnr')
            )
        return redirect('/patients/')
    
    targetPatient=Patient.objects.get(id=id)

    return render(request, 'addpatient.html', context={"patient": targetPatient})

def perform_login(request:HttpRequest):
    login_status = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user : AbstractUser | None =  authenticate(request, username=username, password=password)
       
        if user is not None:
            login(request, user)

                #if

            login_status = "SUCCESSFUL"
        else:
            # user is None
            login_status = "FAILED"
    return render(request, "login.html", context={"login_status": login_status})

def perform_logout(request: HttpRequest):
    logout(request)

    return redirect("/login/")

def register(request: HttpRequest):
    
    pass

