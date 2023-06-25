from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives, message, send_mail
from datetime import date
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse,HttpRequest,HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
# Create your views here.
#Basic login forms 
def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')


def Logout(request) :
    logout(request)
    return redirect('index')


# User authentication
def userlogin(request) :
    error=""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'login.html',d)

#Login for admin
def login_admin(request) :
    error=""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'login_admin.html',d)
#Sign up
def signup1(request) :
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c,branch=b,role=r)
            error="no"
            user.save()
        except:
            error="yes"
    d={'error':error}
    return render(request, 'signup.html',d)

#admin home



def admin_home(request) :
    if not request.user.is_staff:
        return redirect('login_admin')

    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accepted").count()
    rn = Notes.objects.filter(status="Rejected").count()
    aln = Notes.objects.all().count()
    d={'pn':pn,'an':an,'rn':rn,'aln':aln}
    return render(request, 'admin_home.html')

#Profile and all profile actions
def profile(request) :
    if not request.user:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    d = {'data':data,'user':user}
    return render(request, 'profile.html',d)
#Edit profile 

def edit_profile(request) :
    if not request.user:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error=False
    if request.method=='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        b=request.POST['branch']

        user.first_name=f
        user.last_name=l
        datacontact=c
        data.branch=b

        user.save()
        data.save()
        error=True
    d = {'data':data,'user':user,'error':error}
    return render(request, 'edit_profile.html',d)
#Password change
def changepassword(request):
    if not request.user:
        return redirect('login')
    error=""
    if request.method=="POST":
        o=request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request, 'changepassword.html',d)

#Notes and actions
def upload_notes(request) :
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method == 'POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(), branch=b, subject=s,
            notesfile=n,filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request, 'upload_notes.html', d)

# View own notes
def view_usernotes(request) :
    if not request.user:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)
    d = {'notes':notes,}
    return render(request, 'view_usernotes.html',d)

#Show all uploads
def viewall_usernotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status="Accepted")
    d = {'notes':notes}
    return render(request, 'viewall_usernotes.html', d)

#If admin, delete notes 

def delete_usernotes(request,pid) :
    if not request.user:
        return redirect('login')
    notes = Notes.objects.get(id = pid)
    notes.delete()
    return redirect('view_usernotes')

"""Following are for the admin actions which can be accessed through admin login"""
#View users
def view_users(request) :
    if not request.user.is_staff:
        return redirect('login')
    users = Signup.objects.all()

    d = {'users':users}
    return render(request, 'view_users.html', d)

#Delete users who post idiotic things

def delete_users(request,pid) :
    if not request.user:
        return redirect('login')
    users = User.objects.get(id = pid)
    users.delete()
    return redirect('view_users')

# Notes requiring approval 

def pending_notes(request) :
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Notes.objects.filter(status = "pending")
    d = {'notes':notes,}
    return render(request, 'pending_notes.html',d)

# Decide whether notes pending, approved or rejected

def assign_status(request,pid) :
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id = pid)
    error=""
    if request.method=='POST':
        s = request.POST['status']
        try:
            notes.status=s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'notes':notes,'error':error}
    return render(request, 'assign_status.html',d)



# Notes which are accepted 

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status="Accepted")
    d = {'notes':notes}
    return render(request, 'accepted_notes.html', d)

# Notes which are rejected
def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status="Rejected")
    d = {'notes':notes}
    return render(request, 'rejected_notes.html', d)

# Show all notes

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.all()
    d = {'notes':notes}
    return render(request, 'all_notes.html', d)

# Delete the notes by admin

def delete_notes(request, pid):
    try:
        notes = Notes.objects.get(id=pid)
        if notes.user == request.user:
            notes.delete()
        else:
            return HttpResponseBadRequest("Cannot delete the notes.")
    except :
        return HttpResponseBadRequest("Cannot delete the notes.")
    return redirect('all_notes')


#Make Review
'''Review options'''
#Rating
def rate(request: HttpRequest, notes_id: int, rating: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=notes_id)
    Review.objects.filter(notes=notes, user=request.user).delete()
    notes.rating_set.create(user=request.user, rating=rating)
    return index(request)
#Make review
def review(request, notes_id):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method == 'POST':
        r = request.POST['rating']
        d = request.POST['description']
        n = get_object_or_404(Notes, pk=notes_id)
        u = User.objects.filter(username=request.user.username).first()
        try:
            Review.objects.create(user=u,description=d,rating=r,notes=n)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request, 'review.html', d)
#See review
def see_review(request, notes_id):
    if not request.user.is_authenticated:
        return redirect('login')
    reviews =  Review.objects.all()
    notes = get_object_or_404(Notes, pk=notes_id)
    reviews =  Review.objects.filter(notes=notes)
    context = {
        'reviews': reviews,
        'notes': notes
    }
    return render(request, "see_review.html", context)

#Admin and actions on reviews

def delete_review(request,pid) :
    if not request.user:
        return redirect('login')
    try:
        review = Review.objects.get(id=pid)
        if review.user == request.user:
            review.delete()
        else:
            return HttpResponseBadRequest("Cannot delete the notes.")
    except:
        return HttpResponseBadRequest("Cannot delete the notes.")
    return redirect('viewall_usernotes')


def delete_review_admin(request,pid) :
    if not request.user:
        return redirect('login')
    try:
        review = Review.objects.get(id=pid)
        if request.user.is_staff:
            review.delete()
        else:
            return HttpResponseBadRequest("Cannot delete the notes.")
    except:
        return HttpResponseBadRequest("Cannot delete the notes.")
    return redirect('admin_reviews')

#Admin review

def admin_reviews(request, pid):
    if not request.user.is_staff:
        return redirect('login_admin')
    reviews =  Review.objects.all()
    notes = get_object_or_404(Notes, pk=pid)
    reviews =  Review.objects.filter(notes=notes)
    context = {
        'reviews': reviews,
        'notes': notes
    }
    return render(request, "admin_reviews.html", context)
