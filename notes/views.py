
import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from datetime import date
from django.shortcuts import get_object_or_404
# Create your views here.

def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fullname']
        em = request.POST['email']
        m = request.POST['mobile']
        s = request.POST['subject']
        msg = request.POST['message']
        try:

            Contact.objects.create(fullname=f, email=em, mobile=m, subject=s, message=msg,msgdate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def userlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
                return redirect(profile)
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', locals())

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error ="yes"
        except:
            error = "yes"
    return render(request,'login_admin.html', locals())

def signups(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        i = request.FILES['img']
       
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c,branch=b,role=r, image=i)
            error="no"
        except:
            error="yes"
    return render(request,'signup.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    contactur = Contact.objects.filter(isread="no")
    contactr = Contact.objects.filter(isread="yes")
    pn = Notes.objects.filter(status="pending").count()
    users = Signup.objects.all().count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()
    d = {'users':users, 'pn':pn,'an':an,'rn':rn,'alln':alln,'cu':contactur, 'cr':contactr}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    print(request.user.id)
    data = Signup.objects.get(user = user)
    #print(Signup.objects.values().get(user = user))

    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)   
    error = ""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        i = request.FILES.get('img')
        try:
            if i != None:
                data.image = i
            user.first_name = f
            user.last_name = l
            data.contact = c
            data.branch = b
            user.save()
            data.save()
            error="no"
        except:
            error="yes"

    print(error)
    d = {'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"

    return render(request,'changepassword.html', locals())

def upload_notes(request):
    if not request.user.is_authenticated and not request.user.is_staff:
        return redirect('login')
    error=""
    if request.method=='POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        de = request.POST['details']

        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,
                                 filetype=f,description=d,details=de,status='pending')
            error="no"
        except:
            error="yes"
    return render(request,'upload_notes.html', locals())

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.user.id)
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)
    print('tut')
    d = {'notes':notes}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('view_mynotes')



def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()

    d = {'users':users}
    print(d)
    return render(request,'view_users.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "pending")
    d = {'notes':notes}
    return render(request, 'pending_notes.html',d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes':notes}
    return render(request, 'accepted_notes.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Reject")
    d = {'notes':notes}
    return render(request, 'rejected_notes.html',d)

#admins
def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    
    notes = Notes.objects.all()
    d = {'notes':notes}
    return render(request, 'all_notes.html',d)
    
  

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method=='POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d = {'notes':notes,'error':error}
    return render(request, 'assign_status.html',d)

def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('all_notes')

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status='Accept').order_by("-upvotes")
    if request.method == 'GET':
        sub = request.GET.get('subject')
        keywords = request.GET.get('keywords')
        branch = request.GET.get('branch')
        filetype = request.GET.get('filetype')
        if sub != None:
            notes = notes.filter(subject__icontains=sub)
        if keywords != None:
            notes1 = notes.filter(details__icontains=keywords) 
            notes2 = notes.filter(description__icontains=keywords) 
            notes = notes1 | notes2
        if branch != None:
            notes = notes.filter(branch__icontains=branch) 
        if filetype != None:
            notes = notes.filter(filetype__icontains=filetype)
   
    d = {'notes':notes}
    return render(request, 'viewallnotes.html',d)


def NoteDetails(request,did):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        nid = request.POST['notesid']
        upvote = request.POST['val']
        state = request.POST['state']
       
    #updateNotes upvote
        getNote = Notes.objects.get(id=did)
        getNote.upvotes = upvote
        getNote.save()
        #update userUpvotes
        userofNotes = Notes.objects.values('user').get(id=did)
        
        user = Signup.objects.get(user=userofNotes['user'])
        print(user)
        getUpVoteUser = Signup.objects.values("upvotesuser").get(user=userofNotes['user'])
        if state == 'upvote':
            user.upvotesuser = getUpVoteUser['upvotesuser']+1
        else :
             user.upvotesuser = getUpVoteUser['upvotesuser']-1
             
        user.save()
        try:
            useraction = Checkvotes.objects.get(user=request.user,likedNote=getNote)
            error = True
        except:
            Checkvotes.objects.create(user=request.user,likedNote=getNote,action=state)
            error = False
        if(error):
            useraction.action = state
            useraction.save(update_fields=['action'])
            print('found')
        else:
            print('crate')
            
    notes = Notes.objects.get(id=did)
    cmnts = Comments.objects.filter(note=notes)
  

    try:
        action = Checkvotes.objects.values('action').get(user=request.user,likedNote=notes)
        action = action['action']
    except:
     action = ' '

    userReq = User.objects.get(id=request.user.id)
    return render(request,"detailNote.html",{'n' : notes,'action':action, 'cmnts':cmnts, 'user':userReq})  

def NoteComment(request,did):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        nid = request.POST['notesid']
        msg = request.POST['msg']
        time = request.POST.get('time')
        print(msg)
        getNote = Notes.objects.get(id=nid)
        Comments.objects.create(user=request.user,note=getNote,cmnt=msg,dates = time)
    return redirect("details",did=did)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        try:
            if user.check_password(o):
                user.set_password(n)

                user.save()

                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_passwordadmin.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

