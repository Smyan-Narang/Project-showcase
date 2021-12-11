from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Project

# Create your views here.
def home(request):
    projects = Project.objects.all()
    # for project in projects:
    #     project.delete()
    return render(request, "homeProjects.html", {'projects': projects})

def add(request):
    if request.method == "POST":
        name_1=request.POST['name_1']
        name_2=request.POST['name_2']
        name_3=" "
        return render(request, 'index.html', {'result':name_1+name_3+name_2})

def login(request):
    print("Login Function is Working")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid username or password")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name'].split(" ")
        if len(name) < 2:
            messages.info(request, 'Enter your full name')
            return render(request, 'login.html')
        elif len(name) > 2:
            messages.info(request, 'Enter your first and last name only')
            return render(request, 'login.html')
        else:
            firstName, LastName = name

        username=request.POST['username']
        password=request.POST['password']
        repeat_password=request.POST['repeat_password']
        email_address=request.POST['email']
        if password != repeat_password:
            messages.info(request, 'password doesnt match')
            return render(request, 'login.html')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return render(request, 'login.html')
        elif User.objects.filter(email=email_address).exists():
            messages.info(request, 'email already taken')
            return render(request, 'login.html')

            return render(request, 'login.html')
        else:
            user = User.objects.create_user(first_name=firstName, last_name=LastName, username=username, email=email_address, password=password)
            user.save()
            return redirect("/")
    else:
        return render(request, "login.html")
def logout(request):
    auth.logout(request)
    return redirect('/')

def dashboard(request):
    return render(request, 'editprofile.html')

def projects(request):
    allProject = Project.objects.filter(email=request.user.email)
    return render(request, 'projects.html', {'projects': allProject})



def add(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            if len(name) == 0:
                raise TypeError
        except:
            messages.info(request, 'Please add a name')
            return render(request, 'add_projects.html', {'msg_color': '#FF0000'})
        try:
            image = request.FILES['image']
        except:
            messages.info(request, 'Please add an image')
            return render(request, 'add_projects.html',{'msg_color': '#FF0000'})
        email = request.user.email
        try:
            description = request.POST['description']
            if len(description) == 0:
                raise TypeError
        except:
            messages.info(request, 'Please add a description')
            return render(request, 'add_projects.html', {'msg_color': '#FF0000'})
        try:
            code = request.POST['code']
            if len(code) == 0:
                raise TypeError
        except:
            messages.info(request, 'Please add a code')
            return render(request, 'add_projects.html', {'msg_color': '#FF0000'})
        developer_name = str(request.user.first_name).capitalize() + " " + str(request.user.last_name).capitalize()
        project = Project(name=name, image=image, email=email, developer_name=developer_name, description=description, code=code)
        project.save()
        messages.info(request, "Project Added")
        return render(request, 'add_projects.html', {'msg_color': '#28a745'})
    else:
        return render(request, 'add_projects.html')

def viewproject(request, pk):
    project = Project.objects.filter(id=pk)[0]
    return render(request, 'ViewProject.html', {'project': project})
def viewhomeproject(request, pk):
    project=Project.objects.filter(id=pk)[0]
    return render(request, 'Viewhomeproject.html', {'project': project})

def EditProject(request, pk):
    print()
    if request.method == 'POST':
        project = Project.objects.filter(id=pk)[0]
        project.name = request.POST['name']
        try:
            project.image = request.FILES['image']
        except:
            print('message')
        project.description = request.POST['description']
        project.code = request.POST['code']
        project.save()
        messages.info(request, "changes saved")
        return render(request, 'edit_project.html', {'project': project, 'msg_color':'#000'})
    else:
        project = Project.objects.filter(id=pk)[0]
        return render(request, 'edit_project.html', {'project': project})

def deleteproject(request, pk):
    project=Project.objects.filter(id=pk)[0]
    project.delete()
    return redirect('projects')

def deleteaccount(request):
    account = User.objects.filter(email=request.user.email)

    projects = Project.objects.filter(email=request.user.email)
    for project in projects:
        project.delete()
    auth.logout(request)
    account.delete()
    return redirect('/')
def saveaccount(request):
    if request.method == 'POST':
        old_password = request.POST['password']
        new_password = request.POST["new_password"]
        old_username = request.user.username
        user = auth.authenticate(username=old_username, password=old_password)
        if user is not None:
            account = User.objects.filter(email=request.user.email)[0]
            account.first_name = request.POST['firstname']
            account.last_name = request.POST['lastname']

            new_username = request.POST['username']
            if old_username != new_username:
                users = User.objects.filter(username=request.user.username)
                if len(users) > 0:
                    messages.info(request, "username already used")
                    return render(request, 'editprofile.html', {'msg_color': '#FF0000'})
                else:
                    account.username = new_username

            if len(new_password) > 0:
                account.set_password(new_password)

            auth.logout(request)
            account.save()
            auth.login(request, account)
            messages.info(request, "changes saved")
            return render(request, 'editprofile.html', {'msg_color':'#000'})
        else:
            messages.info(request, "Incorrect Password")
            return render(request, 'editprofile.html', {'msg_color': '#ff0000'})
def search(request):
    pass