from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_job/", views.newjob, name="add_job"),
    path("add_input_img/", views.newimginput, name="add_input_img"),
    path("jobs/", views.JobListView.as_view(), name="jobs"),
    path("job/<int:pk>", views.JobDetailView.as_view(), name="job_detail"),
    path("inputs/", views.display_input_images, name="inputs"),
    # path("outputs/", views.ImgOutputListView.as_view(), name="outputs"),
]
