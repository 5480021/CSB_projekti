import os
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



# ----------------------------------------
# FLAW 1: SQL Injection (OWASP A03)
# ----------------------------------------
def search_user(request):
    users = []
    query = ""

    if 'q' in request.GET:
        query = request.GET['q']

        # FLAW: allows SQL injection
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM auth_user WHERE username = '{query}'")
            rows = cursor.fetchall()

        # FIX: Parameterized query (commented out)
        #with connection.cursor() as cursor:
        #    cursor.execute("SELECT * FROM auth_user WHERE username = %s", [query])
        #    rows = cursor.fetchall()

        users = rows

    return render(request, 'main/search.html', {'users': users, 'query': query})


# ----------------------------------------
# FLAW 2: Broken Access Control (OWASP A01)
# ----------------------------------------

# FLAW: Doesnt require loggin in and shows too much information
# FIX: add @login_required 
#@login_required


def secret_page(request): # has information of users that is shown without loggin in
    users = User.objects.all().values('id', 'username') 
    return render(request, 'main/secret.html', {'users': users})


# ----------------------------------------
# FLAW 4: Security Misconfiguration (OWASP A05:2021)
# ----------------------------------------

def debug_demo(request):
    raise RuntimeError("DEBUG leak demo")

# ----------------------------------------
# FLAW 5: Software and Data Integrity Failures (OWASP A08)
# ----------------------------------------
def upload_file(request):
    message = ""
    if request.method == "POST" and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # FLAW: Executes uploaded file (extremely dangerous!)
        os.system(f"python {file_path}")
        message = f"File '{uploaded_file.name}' uploaded and executed!"

        # FIX: Never execute uploaded files
        #message = f"File '{uploaded_file.name}' uploaded but NOT executed."

    return render(request, 'main/upload.html', {'message': message})
