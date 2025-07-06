from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
 
class Signup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    contact = models.CharField(max_length=11)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=15)
    image = models.ImageField(upload_to="images/img", default="")
    upvotesuser = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username+str(self.user_id)

class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=30)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField(null=True)
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=15)
    upvotes = models.IntegerField(default=0)
    details = models.CharField(default='',max_length=500)
    def __str__(self):
        return self.user.username+" "+self.status


class Contact(models.Model):
    fullname = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=15, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.email

class Checkvotes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likedNote = models.ForeignKey(Notes,on_delete=models.CASCADE)
    action = models.CharField(max_length=10)

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    note = models.ForeignKey(Notes,on_delete=models.CASCADE,default="")
    cmnt = models.CharField(max_length=200)
    dates = models.CharField(max_length=30)
    