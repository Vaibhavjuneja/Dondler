from django.utils.text import slugify
import re
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from .scrapper import *
# Create your models here.
from django.contrib.auth import get_user_model
import time
User=get_user_model()

class Subject(models.Model):
    subject_name=models.CharField(max_length=200)
    subject_code=models.CharField(max_length=120,unique=True)
    # unit1=models.CharField(max_length=200,null=True,blank=True)
    unit1_syllabus=models.TextField(max_length=1000,null=True,blank=True)
    # unit2=models.CharField(max_length=200,null=True,blank=True)
    unit2_syllabus=models.TextField(max_length=1000,null=True,blank=True)
    # unit3=models.CharField(max_length=200,null=True,blank=True)
    unit3_syllabus=models.TextField(max_length=1000,null=True,blank=True)
    # unit4=models.CharField(max_length=200,null=True,blank=True)
    unit4_syllabus=models.TextField(max_length=1000,null=True,blank=True)
    exam_date=models.DateTimeField()
    semester = models.IntegerField()
    text_book_1=models.TextField(max_length=1000,null=True,blank=True)
    text_book_2=models.TextField(max_length=1000,null=True,blank=True)
    slug=models.SlugField()

    def __str__(self):
        return self.subject_name
    def get_units(self):
        return self.subjects.all()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_name)
        super(Subject, self).save(*args, **kwargs)

class Unit(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subjects')
    unit_name=models.CharField(max_length=200)
    unit_part_1=models.CharField(max_length=500)
    unit_part_1_syllabus=models.TextField(max_length=1000)
    unit_part_2=models.CharField(max_length=500,null=True,blank=True)
    unit_part_2_syllabus=models.TextField(max_length=1000,null=True,blank=True)
    unit_part_3=models.CharField(max_length=500,null=True,blank=True)
    unit_part_3_syllabus=models.TextField(max_length =1000,null=True,blank=True)
    slug=models.SlugField()
    def __str__(self):
        return self.unit_name+" - " + self.subject.subject_name
    def get_unit_parts(self):
        return self.unit_parts.all()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject.subject_name + self.unit_name)
        super(Unit, self).save(*args, **kwargs)

class UnitParts(models.Model):
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE,related_name="unit_parts")
    part_head=models.CharField(max_length=500)
    part_syllabus=models.TextField(max_length=1000)
    
    def __str__(self):
        return self.part_head + " - " + str(self.unit)
    def get_topics(self):
        return self.topics.all()



class Topic(models.Model):
    unit_part=models.ForeignKey(UnitParts,on_delete=models.CASCADE,related_name="topics")
    topic_name=models.CharField(max_length=500,null=True,blank=True)
    slug=models.SlugField()
    google_data=models.CharField(max_length=5000,null=True,blank=True)

    def __str__(self):
        return self.topic_name + "  " + str(self.unit_part)
    def get_absolute_url():
        return ("topicdetail",[self.slug, ])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic_name)
        super(Topic, self).save(*args, **kwargs)



class Related(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject=models.ManyToManyField(Subject)
    subject_done=models.BooleanField(default=False)
    unit_1_done=models.BooleanField(default=False)
    unit_2_done=models.BooleanField(default=False)
    unit_3_done=models.BooleanField(default=False)
    unit_4_done=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.username)

class TopicUser(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    count=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return self.topic.topic_name + " - "+self.user.name

class TopicResources(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name="topic_links")
    title=models.CharField(max_length=500)
    description=models.CharField(max_length=1500,null=True,blank=True)
    url=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)
    endorsed=models.IntegerField(default=0)
    def __str__(self):
        return self.topic.topic_name

def post_save_topic_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        s=instance.topic_name + " " + instance.unit_part.unit.subject.subject_name
        url="https://www.google.com/search?q={}".format(s)
        soup=getsoup(url)
        data=getdata(soup)
        u=User.objects.get(id=3)
        count=0
        if data:
            for i in data:
                if(count>4):
                    break
                if(len(i)!=0):
                    a=TopicResources.objects.create(user=u,topic=instance,title=i[0],description=i[2],url=i[1])
                    a.save()
                    count+=1




def post_save_subject_model_receiver(sender, instance, created, *args, **kwargs):
    if instance.unit1_syllabus:
        create_unit(instance,instance.unit1_syllabus,"1")
    if instance.unit2_syllabus:
        create_unit(instance,instance.unit2_syllabus,"2")
    if instance.unit3_syllabus:
        create_unit(instance,instance.unit3_syllabus,"3")
    if instance.unit4_syllabus:
        create_unit(instance,instance.unit4_syllabus,"4")

def post_save_unit_parts_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            string=instance.part_syllabus
            topics=string.split(',')
            for item in topics:
                topic_name=item.lstrip()
                Topic.objects.create(unit_part=instance, topic_name=topic_name)
        except Exception as e:
            print(e)    



def create_unit(instance,string,ut):
    l=string.split('.')
    length_l=len(l)
    if l[length_l-1]  is '':
        length_l=length_l-1
    if length_l is 1:
        parts=re.findall('(.*):', l[0])
        if len(parts) < 1:
            unit_part_1=" "
        else:
            unit_part_1=parts[0]
        unit_part_2=" "
        unit_part_3=" "
        s=re.findall(':(.*)', l[0])
        if len(s) < 1:
            unit_part_1_syllabus=" "
        else:
            unit_part_1_syllabus=s[0]
        unit_part_2_syllabus=" " 
        unit_part_3_syllabus=" "                              
    if length_l is 2:
        parts=re.findall('(.*):', l[0])
        parts1=re.findall('(.*):', l[1])
        if len(parts) < 1:
            unit_part_1=" "
        else:
            unit_part_1=parts[0]
        if len(parts1) < 1:
            unit_part_2=" "
        else:
            unit_part_2=parts1[0]
        unit_part_3=" "
        s=re.findall(':(.*)', l[0])
        s1=re.findall(':(.*)', l[1])
        if len(s)<1:
            unit_part_1_syllabus=" "
        else:
            unit_part_1_syllabus=s[0]
        if len(s1)<1:
            unit_part_2_syllabus=" "
        else:
            unit_part_2_syllabus=s1[0]
        unit_part_3_syllabus=" "                              
    if length_l is 3:
        parts=re.findall('(.*):', l[0])
        parts1=re.findall('(.*):', l[1])
        parts2=re.findall('(.*):', l[2])
        if len(parts) < 1:
            unit_part_1=" "
        else:
            unit_part_1=parts[0]
        if len(parts1) < 1:
            unit_part_2=" "
        else:
            unit_part_2=parts1[0]
        if len(parts2) < 1:
            unit_part_3=" "
        else:
            unit_part_3=parts2[0]        
        s=re.findall(':(.*)', l[0])
        s1=re.findall(':(.*)', l[1])
        s2=re.findall(':(.*)', l[2])
        if len(s)<1:
            unit_part_1_syllabus=" "
        else:
            unit_part_1_syllabus=s[0]
        if len(s1)<1:
            unit_part_2_syllabus=" "
        else:
            unit_part_2_syllabus=s1[0]
        if len(s2)<1:
            unit_part_3_syllabus=" "
        else:
            unit_part_3_syllabus=s2[0]
    unit_name="Unit "+ ut
    unit_created = Unit.objects.create(
        subject=instance,
        unit_name=unit_name,
        unit_part_1=unit_part_1,
        unit_part_1_syllabus=unit_part_1_syllabus,
        unit_part_2=unit_part_2,
        unit_part_2_syllabus=unit_part_2_syllabus,
        unit_part_3=unit_part_3,
        unit_part_3_syllabus=unit_part_3_syllabus
    )
    if length_l is 1:
        part_head=unit_part_1
        part_syllabus=unit_part_1_syllabus
        unit_part_created_1=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )

    if length_l is 2:
        part_head=unit_part_1
        part_syllabus=unit_part_1_syllabus
        unit_part_created_1=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )
        part_head=unit_part_2
        part_syllabus=unit_part_2_syllabus
        unit_part_created_2=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )

    if length_l is 3:
        part_head=unit_part_1
        part_syllabus=unit_part_1_syllabus
        unit_part_created_1=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )
        part_head=unit_part_2
        part_syllabus=unit_part_2_syllabus
        unit_part_created_2=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )
        part_head=unit_part_3
        part_syllabus=unit_part_3_syllabus
        unit_part_created_3=UnitParts.objects.create(
            unit=unit_created,
            part_head=part_head,
            part_syllabus=part_syllabus
        )

post_save.connect(post_save_subject_model_receiver, sender=Subject)
post_save.connect(post_save_unit_parts_model_receiver, sender=UnitParts)
post_save.connect(post_save_topic_model_receiver, sender=Topic)