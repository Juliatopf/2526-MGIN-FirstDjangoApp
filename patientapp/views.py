from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from patientapp.models import Patient
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import login


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
            if not user.is_active:
                login(request, user)
                return redirect("/medical-status/")
            else:
                login(request, user)
                login_status = "SUCCESSFUL"
        else:
            login_status = "FAILED"
    return render(request, "login.html", context={"login_status": login_status})

def perform_logout(request: HttpRequest):
    logout(request)

    return redirect("/login/")

def register(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error_message = "Benutzername existiert bereits."
        elif User.objects.filter(email=email).exists():
            error_message = "E-Mail existiert bereits."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            # Kein automatisches Login, stattdessen Hinweis
            return render(request, "register.html", {"error_message": "Registrierung erfolgreich! Dein Account muss erst aktiviert werden."})

    return render(request, "register.html", {"error_message": error_message})

def medical_status(request: HttpRequest):
    message = ""
    if request.method == "POST":
        status = request.POST.get("status")
        # Hier kannst du die Daten speichern, z.B. im User-Profil oder einer eigenen Tabelle
        message = "Dein medizinischer Status wurde gespeichert."
        # Nach dem Speichern ggf. weiterleiten
        return render(request, "medical_status.html", {"message": message})
    return render(request, "medical_status.html", {"message": message})
