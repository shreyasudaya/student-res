from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=10,null=True)
    branch = models.CharField(max_length=50,null=True)
    role = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.user.username

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=30)
    branch = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    notesfile = models.FileField(null=True)
    filetype = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=15)
    
    def average_rating(self) -> float:
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.signup.user.username+" "+self.status
    
class Review(models.Model):
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    def __str__(self):
        return f"{self.user.username}:{self.rating}"