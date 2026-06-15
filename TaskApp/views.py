from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .utils import send_email_to_employee,send_task_assignment_email
from .forms import TaskForm
from .forms import ContactForm
from django.http import HttpResponse
from .forms import DepartmentForm
from .forms import EmployeeForm  
from django.core.files.storage import FileSystemStorage

def HOME(request):
    return render(request,"HOME.html")


def REGIEMP(request):
    departments = Department.objects.all()
    if request.method == "POST":
        try:
            name = request.POST.get("firstname")
            department = request.POST.get("department")
            employee_id = request.POST.get("id")
            address = request.POST.get("address")
            contact_number = request.POST.get("number")
            destination = request.POST.get("dest")
            date_of_birth = request.POST.get("dob")
            date_of_joining = request.POST.get("doj")
            email = request.POST.get("email")
            newemail = request.POST.get("newemail")
            password = request.POST.get("pass")
            designation = request.POST.get("des")
            description = request.POST.get("desc")
            if 'pictureInput' in request.FILES:
                picture = request.FILES['pictureInput']
                fs = FileSystemStorage()
                filename = fs.save(picture.name, picture)
                picture_url = fs.url(filename)
            else:
                picture_url = None
            send_email_to_employee(email, newemail)
            employee = Employee.objects.create(
                name=name,
                department=department,
                employee_id=employee_id,
                address=address,
                contact_number=contact_number,
                destination=destination,
                date_of_birth=date_of_birth,
                date_of_joining=date_of_joining,
                email=email,
                newemail=newemail,
                password=password,
                designation=designation,
                description=description,
                picture=picture_url  
            )
            return redirect("AdminDashboard")
        except Exception as e:
            error_message = "An error occurred while processing your request."
            return render(request, "error.html", {'error_message': error_message})
    return render(request, "REGIEMP.html", {'departments': departments })

def employeesignuplogin(request):
    if request.method == "POST":
        email = request.POST.get("LOGINEmail")
        password = request.POST.get("LOGINPassword")
        if email and password:
            try:
                user = EmployeeSignUp.objects.get(email=email)
                if password == user.password:
                    print("Authentication successful")
                    request.session['EmployeeEmail'] = email
                    request.session['EmployeeUsername'] = user.name
                    return redirect("EMPDashboard")
                else:
                    print("Authentication failed: Invalid password")
                    return render(request, "LOGIN.html", {'error_message': "Invalid email or password"})
            except EmployeeSignUp.DoesNotExist:
                print("Authentication failed: User not found")
                return render(request, "LOGIN.html", {'error_message': "Invalid email or password"})
        else:
            name = request.POST.get("Name")
            email = request.POST.get("Email")
            password = request.POST.get("Password")
            if email and password:
                if EmployeeSignUp.objects.filter(email=email).exists():
                    return render(request, "LOGIN.html", {'error_message': "Email is already registered. Please use a different email."})
                new_user = EmployeeSignUp(name=name, email=email, password=password)
                new_user.save()
                return render(request, "LOGIN.html", {'success_message': "Sign up successful! Please log in"})
            else:
                print("No email or password provided")
                return render(request, "LOGIN.html", {'error_message': "Please provide email and password"})
    return render(request, "LOGIN.html")


def handle_login(request, data):
    email = data["Email"]
    password = data["Password"]
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        error_message = "Invalid email or password. Please try again."
        return render(request, "login.html", {"error_message": error_message})


def employee_list(request):
    try:
        query = request.GET.get('q')
        if query:
            employees = Employee.objects.filter(email__icontains=query)
        else:
            employees = Employee.objects.all()
        return render(request, 'emplist.html', {'employees': employees, 'query': query})
    except ValidationError as ve:
        error_message = "Validation Error: {}".format(ve)
        return render(request, "error.html", {'error_message': error_message})
    except Exception as e:
        error_message = "An error occurred while processing your request."
        return render(request, "error.html", {'error_message': error_message})



def search_employee(request):
    query_email = request.GET.get('email')
    query_emp_id = request.GET.get('emp_id')

    employees = Employee.objects.all()  

    if query_email:
        employees = employees.filter(email__icontains=query_email)
    if query_emp_id:
        employees = employees.filter(employee_id__icontains=query_emp_id)

    return render(request, 'emplist.html', {'employees': employees, 'query_email': query_email, 'query_emp_id': query_emp_id})


def delete_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return redirect('employee_list')


def edit_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'editemp.html', {'form': form})

def ABOUT(request):
    return render(request, "ABOUT.html")


def EMPDASHBOARD(request):
    email = request.session.get("EmployeeEmail")

    if not email:
        return render(request, "error.html", {
            'error_message': "Session expired. Please log in again."
        })

    try:
        tasks = Task.objects.filter(email=email)

        total_tasks = tasks.count()
        in_progress_tasks = tasks.filter(priority='High').count()
        completed_tasks = FinishedTask.objects.filter(
            email=email,
            finished=True
        ).count()

        return render(request, "EMPDashboard.html", {
            'total_tasks': total_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completed_tasks': completed_tasks,
        })

    except Exception as e:
        print("Dashboard error:", e) 
        return render(request, "error.html", {
            'error_message': "Something went wrong. Please try again."
        })
# def EMPDASHBOARD(request):
    try:
        email = request.session.get("EmployeeEmail")

        if email:
            tasks = Task.objects.filter(email=email)
            total_tasks = tasks.count()
            in_progress_tasks = tasks.filter(priority='High',).count()
            completed_tasks = FinishedTask.objects.filter(email=email, finished=True).count()
            return render(request, "EMPDashboard.html", {
                'total_tasks': total_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completed_tasks': completed_tasks,
            })
        else:
            error_message = "Session data missing. Please log in again."
            return render(request, "error.html", {'error_message': error_message})
    except Exception as e:
        error_message = "An error occurred while processing your request."
        return render(request, "error.html", {'error_message': error_message})
    
def REGIDMENT(request):
    return render(request, "REGIDMENT.html")


def logout(request):
    try:
        if 'admin_email' in request.session:
            del request.session['admin_email']
        if 'EmployeeEmail' in request.session:
            del request.session['EmployeeEmail']
        if 'EmployeeUsername' in request.session:
            del request.session['EmployeeUsername']
        return redirect('HOME')
    except Exception as e:
        error_message = "An error occurred while logging out."
        return render(request, "error.html", {'error_message': error_message})

 
def ADMINLOGIN(request):
    if request.method == "POST":
        admin_id = request.POST.get("email")
        password = request.POST.get("password")

        try:
            admin = Admin.objects.get(admin_id=admin_id)
        except Admin.DoesNotExist:
            return redirect("ADMINLOGIN")
        if admin.password == password:
            request.session['admin_email'] = admin.admin_id
            total_employees = Employee.objects.count()
            return redirect("AdminDashboard")
        else:
            return render(request, "adminlogin.html", {"error_message": "Invalid credentials"})
    admin_email = request.session.get('admin_email', None)

    return render(request, "adminlogin.html", {"admin_email": admin_email})


def AdminDashboard(request):
    try:
        admin_email = request.session.get('admin_email', None)
        if admin_email is None:
            return redirect('ADMINLOGIN')
        total_employees = Employee.objects.count()
        total_departments = Department.objects.count()
        finished_tasks_count = FinishedTask.objects.count()
        assigned_tasks_count = Task.objects.count()
        return render(request, "AdminDashboard.html", {
            'total_employees': total_employees,
            'total_departments': total_departments,
            'finished_tasks_count': finished_tasks_count,
            'assigned_tasks_count': assigned_tasks_count,
            'admin_email': admin_email,
        })
    except Exception as e:
        error_message = "An error occurred while loading the admin dashboard."
        return render(request, "error.html", {'error_message': error_message})


def REGIDMENT(request):
    try:
        admin_email = request.session.get('admin_email', None)
        if admin_email is None:
            return redirect('ADMINLOGIN')

        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('AdminDashboard')
        else:
            form = DepartmentForm()
        return render(request, 'REGIDMENT.html', {'form': form, 'admin_email': admin_email})
    except Exception as e:
        error_message = "An error occurred while processing department registration."
        return render(request, "error.html", {'error_message': error_message})


def department_list(request):
    departments = Department.objects.all()
    total_departments = departments.count()
    context = {
        'departments': departments,
        'total_departments': total_departments
    }
    return render(request, 'Dlist.html', context)



def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('Dlist')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form})


def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'AdminDashboard', {'department': department})



def search_department(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        departments = Department.objects.filter(name__icontains=name)
        return render(request,'Dlist.html', {'departments': departments})


def CONTACT(request):
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('HOME')
        else:
            form = ContactForm()
        return render(request, 'CONTACT.html', {'form': form})
    except Exception as e:
        error_message = "An error occurred while processing the contact form."
        return render(request, "error.html", {'error_message': error_message})

def assign_task(request):
    if request.method == 'POST':
        title=request.POST.get("title")
        description=request.POST.get("description")
        email=request.POST.get("email")
        priority=request.POST.get("priority")
        form = TaskForm(request.POST)
        print(form)
        if form.is_valid():
            form.save() 
            send_task_assignment_email(title, description, email)
            return redirect('AdminDashboard') 
    else:
        form = TaskForm()
    return render(request, 'assigntask.html', {'form': form})

def delete_task(request,pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('AdminDashboard')


def task_des(request):
    employees_with_tasks = Employee.objects.filter(
        task__isnull=False).distinct()
    return render(request, 'TaskDes.html', {'employees': employees_with_tasks})

def assigned_tasks(request):
    employees_with_tasks = Employee.objects.filter(
        task__isnull=False).distinct()
    return render(request, 'taskemployeelist.html', {'employees': employees_with_tasks})


def finish_task(request):
    finished_tasks = FinishedTask.objects.all()
    return render(request, 'finish_task.html', {'finished_tasks': finished_tasks})

def finish_task_delete(request,id):
    finished_tasks = get_object_or_404(FinishedTask, id=id)
    finished_tasks.delete()
    finished_task=FinishedTask.objects.all()
    return render(request, 'finish_task.html', {'finished_tasks': finished_task})

def finish_task_edit(request,id):
    finished_tasks = get_object_or_404(FinishedTask, id=id)
    if request.method == 'POST':
        form = FinishedTaskForm(request.POST, instance=finished_tasks)
        if form.is_valid():
            form.save()
            return redirect('finish_task')
    else:
        form = FinishedTaskForm(instance=finished_tasks)
    return render(request, 'finish_task_edit.html', {'form': form})



def mark_task_finished(request, task_id, email):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, assigned_to__email=email)
        finished_task = FinishedTask.objects.create(
            title=task.title,
            description=task.description,
            assigned_to=task.assigned_to,
            deadline_date=task.deadline_date,
            deadline_time=task.deadline_time,
            email=task.email,
            finished=True 
        )
        task.delete()
        return redirect('AdminDashboard')
    else:
        pass


def task_end_dates(request):
    tasks = Task.objects.all()
    return render(request, 'taskenddate.html', {'tasks': tasks})


def TaskDashboard(request):
    email = request.session.get("EmployeeEmail")
    assigned_tasks = Task.objects.filter(email=email)

    total_tasks = assigned_tasks.count()
    completed_tasks = FinishedTask.objects.filter(email=email, finished=True).count()
    completion_rate = 0
    if total_tasks > 0:
        if total_tasks == completed_tasks:
            completion_rate = 50  
        else:
            completion_rate = round((completed_tasks / total_tasks) * 100,2)
    performance_rate = completion_rate
    NoOfTasks=total_tasks + completed_tasks

    context = {
        'completion_rate': completion_rate,
        'total_tasks': NoOfTasks,
        'performance_rate': performance_rate,
    }

    return render(request, "EMPTaskDashboard.html", context)


def EMPTaskEndDate(request):
    try:
        email = request.session.get("EmployeeEmail", None)
        if email:
            tasks = Task.objects.filter(email=email)
        else:
            tasks = []

        return render(request, 'EMPTaskEndDate.html', {'tasks': tasks})
    except Exception as e:
        error_message = "An error occurred while loading the employee tasks."
        return render(request, "error.html", {'error_message': error_message})



def EmployeeTask(request):
    try:
        email = request.session.get("EmployeeEmail", None)
        username = request.session.get("EmployeeUsername", None)

        if email:
            tasks = Task.objects.filter(email=email)
        else:
            tasks = []

        return render(request, 'EmployeeTask.html', {'email': email, 'tasks': tasks, 'username': username})
    except Exception as e:
        error_message = "An error occurred while loading the employee tasks."
        return render(request, "error.html", {'error_message': error_message})
