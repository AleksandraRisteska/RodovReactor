#coding=utf-8
from django.db import models
from myproject.settings import MEDIA_ROOT

class Researchers(models.Model):

    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
             return "/home/%s/" % (self.name)
    class Meta:
         verbose_name = 'Истражувач'
         verbose_name_plural = 'Истражувачи' 

class Subject(models.Model):

    url_id = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='thumbnails/')
    description = models.TextField(max_length=1000)

    def __unicode__(self):
       return self.name

    def get_absolute_url(self):
             return "/subject/%s/" % (self.url_id)

    class Meta:
         verbose_name = 'Категорија'
         verbose_name_plural = 'Категории' 

class Research(models.Model):

    name = models.CharField(max_length=200)
    abstract = models.TextField(max_length=1000)
    methodology = models.TextField(max_length=1000)
    subject = models.ManyToManyField(Subject)
    researchers = models.ManyToManyField(Researchers)
    image = models.ImageField(upload_to='thumbnails/')
    year = models.IntegerField(null= True, blank=True)
    link = models.FileField(upload_to='publications/', blank=True, null=True)
    slug = models.SlugField(max_length=120, unique=True)
 
    def __unicode__(self):
        return self.name
  
    def get_absolute_url(self):
         for e in self.subject.all():
             return "/subject/%s/data/%s/" % (e.url_id, self.slug)

    class Meta:
         verbose_name = 'Истражување'
         verbose_name_plural = 'Истражувања' 

class Graph(models.Model):

    type = (
         ('stacked_column', 'повеќеслоен столб'),
         ('pie', 'пита'),
         ('line', 'линија'),
         ('infografik', 'инфографик'),
         ('column', 'столб'),
         ('bar', 'лента'),
         ('combined', 'комбиниран'),
    )

    name = models.CharField(max_length=100)
    research = models.ForeignKey('Research', null=True, blank=True)
    source = models.TextField(max_length=1000, null=True, blank=True)
    explanation = models.TextField(max_length=1000)
    path_to_file = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=type, null=True, blank=True)
    subject = models.ManyToManyField(Subject)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    slug = models.SlugField(max_length=120, unique=True)
    code = models.IntegerField(null=True, blank=True)
 
    def __unicode__(self):
        return self.name
  
    def get_absolute_url(self):
         for e in self.subject.all():
             return "/subject/%s/graphs/%s/" % (e.url_id, self.slug)
 
    def get_infographs_url(self):
         for e in self.subject.all():
             return "/subject/%s/infographs/%s/" % (e.url_id, self.slug)

    def ascii_explanation(self):
        return unicode(self.explanation, 'ascii')

    class Meta:
         verbose_name = 'График'
         verbose_name_plural = 'Графици' 
