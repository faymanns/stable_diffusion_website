from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from thumbnails.fields import ImageField

# Create your models here.

class ImgInput(models.Model):
    """
    Input images for the img2img conversion of stable diffusion. 
    """

    # Fields
    image = models.ImageField(upload_to="input")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ImgOutput(models.Model):
    image = models.ImageField(upload_to="output", null=True)

class Job(models.Model):
    """
    A single job for stable diffusion.
    """

    STATUS = (("p", "pending"), ("d", "done"))

    # Fields
    time = models.DateTimeField(auto_now_add=True)
    strength = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(9)])
    prompt = models.CharField(max_length=1000)
    input_img = models.ForeignKey(ImgInput, null=True, on_delete=models.SET_NULL)
    output_img = models.ForeignKey(ImgOutput, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default="p", help_text="Status of the job")

    def __str__(self):
        return f"{self.time}\t{status}\t{prompt}\t{strength}"
