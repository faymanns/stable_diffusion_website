from django.shortcuts import render
from .models import Job, ImgInput, ImgOutput
from .forms import JobForm, ImgInputForm
from django.views import generic
from django.contrib import messages

# Create your views here.


def index(request):

    num_jobs = Job.objects.all().count()
    num_jobs_pending = Job.objects.filter(status__exact="p").count()
    num_jobs_done = Job.objects.filter(status__exact="d").count()
    num_input_imgs = ImgInput.objects.all().count()

    context = {
        "num_jobs": num_jobs,
        "num_jobs_pending": num_jobs_pending,
        "num_jobs_done": num_jobs_done,
        "num_input_imgs": num_input_imgs,
    }

    return render(request, "index.html", context=context)


class JobListView(generic.ListView):
    model = Job


class ImgInputListView(generic.ListView):
    model = ImgInput


def display_input_images(request):
    all_images = ImgInput.objects.all()
    return render(request, "catalog/imginput_list.html", {"images": all_images})


class ImgOutputListView(generic.ListView):
    model = ImgOutput


def newjob(request):
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Form submission successful")
    else:
        form = JobForm()

    context = {"form": form}

    return render(request, "catalog/new.html", context)


def newimginput(request):
    if request.method == "POST":
        form = ImgInputForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Form submission successful")
    else:
        form = ImgInputForm()

    context = {"form": form}

    return render(request, "catalog/new.html", context)
