from django.contrib import admin
from .models import ImgInput, ImgOutput, Job

# Register your models here.
admin.site.register(ImgInput)
admin.site.register(ImgOutput)
# admin.site.register(Job)


class JobAdmin(admin.ModelAdmin):
    list_display = ("time", "status", "input_img", "prompt", "strength", "output_img")


admin.site.register(Job, JobAdmin)
