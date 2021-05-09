from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

RATING=(

   (1,'1'),
   (2,'2'),
   (3,'3'),
   (4,'4'),
   (5,'5'),


)



class posts(models.Model):
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    content=models.TextField()
    Date_posted=models.DateTimeField(default=timezone.now)
    Subject=models.TextField(default='General')
    report = models.BooleanField(default=False)
    avg_rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=4)
    times_rated = models.IntegerField(default=0)



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

class Rating(models.Model):

    rater=models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(choices=RATING)





