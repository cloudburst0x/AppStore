from typing import List
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .forms import ParentRegistrationForm, UserLoginForm, JobCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import jobs, usersext
#from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, CreateView)

# Create your views here.
def index(request):
    return render(request,'app/landing.html')

def parentloginregister(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        userregister_form = ParentRegistrationForm(request.POST)
        userlogin_form = UserLoginForm(request.POST)
        # Check if the form is valid:
        if userregister_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            user = User.objects.create_user(username=userregister_form.cleaned_data['email'], password=userregister_form.cleaned_data['password'], first_name=userregister_form.cleaned_data['first_name'], last_name=userregister_form.cleaned_data['last_name'])
            ue = usersext(user=user, nric=userregister_form.cleaned_data['nric'], dob=userregister_form.cleaned_data['date_of_birth'], role='parent')
            ue.save()
            messages.info(request, 'Your registration is successful! Login with your credentials below to continue.')
            return redirect('/parent#login')
        if userlogin_form.is_valid():
            messages.info(request, 'Login Successful')
            return redirect('/parent#login')
    # If this is a GET (or any other method) create the default form.
    else:
        
        userregister_form = ParentRegistrationForm
        userlogin_form = UserLoginForm

    return render(request, 'app/parentloginregister.html',{'userregister_form': userregister_form, 'userlogin_form':userlogin_form})

def parentcreatejob(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        createjob_form = JobCreationForm(request.POST)
        # Check if the form is valid:
        if createjob_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)     
            u = User.objects.get(username='email@email.com')            
            job = jobs(user=u, start_date=createjob_form.cleaned_data['start_date'], 
                        start_time=createjob_form.cleaned_data['start_time'],
                        end_date=createjob_form.cleaned_data['end_date'],
                        end_time=createjob_form.cleaned_data['end_time'],
                        rate=createjob_form.cleaned_data['rate'],
                        experience_req=createjob_form.cleaned_data['experience_req'],
                        job_requirement=createjob_form.cleaned_data['job_requirement'])
            job.save()
            messages.info(request, 'Your job creation is successful! Eligible nannies can now see the job you created')
            return redirect('app/parentcreatejob.html')
    # If this is a GET (or any other method) create the default form.
    else:
        createjob_form = JobCreationForm
        
    return render(request, 'app/parentcreatejob.html',{'createjob_form': createjob_form})



#class JobsListView(ListView):
#    model = jobs
#    template_name = '/jobs.html'
#    context_object_name = 'jobs'
#    ordering = ['-date_posted'] #from newest to oldest

#class CreateJobs(CreateView):
#    model = jobs
#    #u = User.objects.get(username='email@email.com')
#    #jobs.user = u
#    fields = ['start_date','start_time','end_date','end_time','rate','experience_req','job_requirement']



# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

#@login_required
def parentmakeoffer(request):
    if not request.user.is_authenticated:
        return render(request, "app/parentloginregister.html", {"message": "Please login first!"})
    if request.POST:
        #Get user data
        u = User.objects.get(username='email@email.com')
        role = u.usersext.role
        if role == 'babysitter':
            return render(request, "app/parentloginregister.html", {"message": "Please login with a Parent Account to post jobs!" })
        #Insert user post into jobs db
        cursor.execute("INSERT INTO jobs VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        , u, [request.POST['start_date'], request.POST['start_time'], request.POST['end_date'],
                           request.POST['end_time'] , request.POST['rate'], request.POST['expirience_req'], request.POST['job_requirement'] ])
        return redirect('app/parentmakeoffer.html', {"message":"Job Created!"})       
        #formresults = request.POST
        #createjob = jobs(user=u, start_date=formresults['start_date'], start_time=formresults['start_time'], date=formresults['date'], time = formresults['time'], duration=formresults['duration'], price=formresults['price'], status = 'Available')
        #createtask.save()
        #return render(request, "task/home.html", {"message": "Task Created!"})
    return render(request, "app/parentmakeoffer.html")
    

    if request.POST:
        ## Check if customerid is already in the table (CHANGE TO JOBID)
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['jobid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO jobs VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['start_date'], request.POST['start_time'], request.POST['end_date'],
                           request.POST['end_time'] , request.POST['rate'], request.POST['expirience_req'], request.POST['job_requirement'] ])
                return redirect('index')    
            else: #FOR JOB ID
                status = 'Customer with ID %s already exists' % (request.POST['jobid'])

 
    return render(request, "app/parentmakeoffer.html")


def add(request):
    """Shows the main page"""
    context = {}
    status = ''
    #Authenticate User
    ##################

    if request.POST:
        ## Check if customerid is already in the table (CHANGE TO JOBID)
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO jobs VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['start_date'], request.POST['start_time'], request.POST['end_date'],
                           request.POST['end_time'] , request.POST['rate'], request.POST['expirience_req'], request.POST['job_requirement'] ])
                return redirect('index')    
            else: #FOR JOB ID
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)


# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)