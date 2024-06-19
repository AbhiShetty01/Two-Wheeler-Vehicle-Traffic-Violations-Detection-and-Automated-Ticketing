import os
from django.shortcuts import render, redirect
from TrafficRuleDetector import start_detecttion
from TrafficRuleDetectorImg import start_detecttion as start_detecttion_img
from main_app.utils import send_challan
# Create your views here.


def index_homepage(request):
    context = {}
    if not request.session.get("username"):
        return redirect("login") 
    
    if "all_data" in request.session:
        del request.session["all_data"]
        del request.session["data_record"]

    if request.method == "POST":
        requested_files = request.FILES
        data = request.POST

        uploaded_file = requested_files['file']
        file_full_path = os.path.join('uploads', uploaded_file.name)
        destination = open(file_full_path, 'wb+')
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
        destination.close()


        select_type = data.get("select_type")
        if select_type == "video":
            is_success, all_data = start_detecttion(file_full_path)
            context["type"] = "video"
            request.session["type"] = context["type"]
            request.session["all_data"] = all_data
            request.session["data_record"] = 1
            print('➡ main_app/views.py:31 all_data:', all_data)
            context["data"] = all_data[0]
            return render(request, "homepage/processed.html", context=context)
        else:
            context["is_success"], context["data"] = start_detecttion_img(file_full_path)
            context["type"] = "image"
            request.session["type"] = context["type"]
            context["data"]["img"] = "test.png"
            request.session["all_data"] = [context["data"]]
            request.session["data_record"] = 1
            return render(request, "homepage/processed.html", context=context)

    return render(request, "homepage/index.html", context=context)


def index_processed(request):
    context = {}


    context["type"] = "video"
    all_data = request.session["all_data"]
    if len(all_data)>request.session["data_record"]:
        context["data"] = all_data[request.session["data_record"]]
        request.session["data_record"] = request.session["data_record"] + 1
    else:
        context["data"] = {}
        context["data"]["not_more"] = True

    
    return render(request, "homepage/processed.html", context=context)
    


def index_login(request):
    context = {}
    if request.session.get("username"):
        return redirect("homepage") 
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if username=="admin" and password=="pass123":
            request.session["username"] = username
            request.session["password"] = password
            return redirect("/")
        
        context["error"] = "Username/Password is incorrect."

    return render(request, "login/index.html", context)

def logout_view(request):
    del request.session["username"]
    del request.session["password"]

    return redirect("login")


def send_challan_view(request):
    context = {}
    context["type"] = request.session["type"]
    all_data = request.session["all_data"]
    if len(all_data)>=request.session["data_record"]:
        context["data"] = all_data[request.session["data_record"]-1]
        is_success = send_challan(context["data"])
        context["data"]["is_challan_send"] = is_success
    else:
        context["data"] = {}
        context["data"]["not_more"] = True

    return render(request, "homepage/processed.html", context=context)

