from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def landing(request):
    return render(request,'app/landing.html')

def loginuser(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request,'app/parenthome.html', {'first_name':first_name})
        else:
            return render(request, "app/parentloginregister.html", {"message": "Incorrect username or password!"})
    return render(request, "app/parentloginregister.html.html")

def logoutuser(request):
    logout(request)
    user = None
    return render(request, "app/landing.html", {"message": "You have been logged out"})


def parentregister(request):
    if request.method == "POST":
        email = request.POST['email']
        nric = request.POST['nric']
        password  = request.POST['password']
        confirm_password = request.POST['confirm_password']
        dob = request.POST['date_of_birth']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = 'parent'
        myuser = User.objects.create_user(email, nric, password, dob, first_name, last_name, role)
        myuser.save()
    
    return render(request, "app/parentloginregister.html")





def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['nric'] , request.POST['password'], request.POST['dob'], request.POST['role'] ])
                return redirect('index')    
            else:
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