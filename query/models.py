from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class posts(models.Model):
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    content=models.TextField()
    Date_posted=models.DateTimeField(default=timezone.now)
    Subject=models.TextField(default='General')
    rating=models.DecimalField(default=0.00, decimal_places=2, max_digits=4)
    times_rated=models.IntegerField(default=0)
    report = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comment_create', kwargs={'pk': self.pk})


class comments(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    Date_posted=models.DateTimeField(default=timezone.now)
    post=models.ForeignKey(posts,on_delete=models.CASCADE)
    comment=models.TextField()


    def __str__(self):
        return self.comment

