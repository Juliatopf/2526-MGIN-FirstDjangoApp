from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from patientapp.models import Patient
from django.shortcuts import redirect

# Create your views here.
def add_patient(request: HttpRequest):
    #todo check svnr
    isSVNRValid = True

    if(request.method == "POST"):
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

    
    if(request.method == "POST"):
        Patient.objects.filter(id=id).update(
            first_name=request.POST.get('firstname'),
            last_name=request.POST.get('lastname'),
            birthday=request.POST.get('birthday'),
            svnr=request.POST.get('svnr')
            )
        return redirect('/patients/')
    
    targetPatient=Patient.objects.get(id=id)

    return render(request, 'addpatient.html', context={"patient": targetPatient})

