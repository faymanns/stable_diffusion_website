from django.forms import ModelForm
from .models import Job, ImgInput

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ["input_img", "prompt", "strength"]

class ImgInputForm(ModelForm):
    class Meta:
        model = ImgInput
        fields = ["image", "name"]
