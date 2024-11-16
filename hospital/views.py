from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import *
# Create your views here.

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()

    d = 0
    p = 0
    a = 0
    for i in doctors:
        d+=1
    for i in patients:
        p+=1
    for i in appointments:
        a+=1
    d1 = {'d' : d, 'p': p, 'a':a}
    return render(request, 'index.html',d1)

def Login(request):
    error=""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error="no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html',d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request, 'view_doctor.html', d)

def Add_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    error=""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        sp = request.POST['special']
        try:
            Doctor.objects.create(name=n, mobile=c, special=sp)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_doctor.html',d)

def Delete_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login.html')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request, 'view_patient.html', d)

def Add_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    error=""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        addr = request.POST['address']
        gen = request.POST['gender']
        try:
            Patient.objects.create(name=n, mobile=c, gender = gen, address = addr)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_patient.html',d)

def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login.html')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appoint = Appointment.objects.all()
    d = {'appoint':appoint}
    return render(request, 'view_appointment.html', d)

from django.shortcuts import get_object_or_404

def Add_Appointment(request):
    if request.method == "POST":
        doctor_id = request.POST['doctor']
        patient_id = request.POST['patient']
        date = request.POST['date']
        time = request.POST['time']

        # Retrieve the Doctor and Patient instances
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        patient = get_object_or_404(Patient, pk=patient_id)

        # Check for overlapping appointment
        overlapping_appointment = Appointment.objects.filter(
            doctor=doctor, date1=date, time1=time
        ).exists()

        if overlapping_appointment:
            return render(request, 'add_appointment.html', {
                'doctor': Doctor.objects.all(),
                'patient': Patient.objects.all(),
                'error': "yes"
            })

        # Save the appointment if no overlap
        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date1=date,
            time1=time
        )
        return render(request, 'add_appointment.html', {
            'doctor': Doctor.objects.all(),
            'patient': Patient.objects.all(),
            'error': "no"
        })

    return render(request, 'add_appointment.html', {
        'doctor': Doctor.objects.all(),
        'patient': Patient.objects.all()
    })


def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_appointment')
