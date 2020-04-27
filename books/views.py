from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Q
from .forms import RelatedForm
from .models import Related,Subject,Topic,TopicResources,TopicUser

# Create your views here.

@login_required
def bookshome(request):
    context={}
    related_objects=Subject.objects.filter(semester=3)
    context['subjects'] = related_objects
    return render(request,'books/home.html',context)


def topicdetail(request,slug):
    context={}
    p=Topic.objects.get(slug=slug)
    context['subject']=p.unit_part.unit.subject
    context['topic']=p
    context['resources']=TopicResources.objects.filter(topic=p).order_by("-endorsed")
    n,created=TopicUser.objects.get_or_create(user=request.user, topic=p)
    if n.count>=1:
        context['done']=1
    else:
        context['done']=0
    if request.GET:
        temp=request.GET['q']
        return HttpResponseRedirect("/search?q={}".format(temp))
    if request.POST:
        print(request.POST)
        topic_id=int(request.POST['id'])
        obj=TopicResources.objects.get(id=topic_id)
        obj.endorsed+=1
        obj.save()
        t,created=TopicUser.objects.get_or_create(topic=p,user=request.user)
        t.count+=1
        t.save()
        return HttpResponseRedirect('#')

    return render(request,"books/topic.html",context)

def createrelated(request):
    context={}
    if request.user.is_authenticated:
        form = RelatedForm(request.POST or None)
        context['form']=form
        if form.is_valid():
            ok=form.cleaned_data.get('subject')
            subject1=Subject.objects.get(
                Q(subject_name__icontains=ok)
            )
            user=request.user
            r1,r2=Related.objects.get_or_create(user=user)
            r1.subject.add(subject1)
    return render(request,'books/related.html',context)

def searchview(request):
    context={}
    s=request.GET['q']
    if s is "":
        context['flag']=1
    else:
        context['flag']=0
        context['q']=s
        context['topics']=Topic.objects.filter(
            Q(topic_name__contains=s)
        )
        context['subjects']=Subject.objects.filter(
            Q(subject_name__contains=s)|
            Q(subject_code__contains=s)|
            Q(unit1_syllabus__contains=s)|
            Q(unit2_syllabus__contains=s)|
            Q(unit3_syllabus__contains=s)|
            Q(unit4_syllabus__contains=s)
        ).distinct()
    return render(request,"books/search.html",context)


