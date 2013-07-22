from chartit import DataPool, Chart
from myproject.models import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from myproject.forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import itertools


def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Vraboteni.objects.all()},
              'terms': [
                'id',
                'broj']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'id': [
                    'broj',]
                  }}],
            chart_options =
              {'title': {
                   'text': 'Broj na vraboteni po pol'},
               'xAxis': {
                    'title': {
                       'text': 'Pol'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('base.html', {'weatherchart': cht})

def subject(requesti, subject):

    subject = Subject.objects.filter(url_id = subject)

    return render_to_response('subject.html',{'subject':subject})


def research(request):

    researches = Research.objects.all()
   
    return render_to_response('list.html',{'researches': Research.objects.all(),})

def home(request):

    return render_to_response('index.html',{'subject':Subject.objects.all(),})

def unique(iter):
    s = set()
    for i in iter:
	if i.name not in s:
	    s.add(i.name) 
	    yield i


def list_objects(request, subject, types):

    subject_object = Subject.objects.filter(url_id=subject)
    all = []

    if types == 'data': 
        researches = Research.objects.filter(subject=subject_object)
    if types == 'graphs': 
        #distinct_researches = Graph.objects.filter(subject=subject_object).exclude(type='infografik').values_list('name', flat=True).distinct()
        #researches = Graph.objects.filter(subject=subject_object).exclude(type='infografik').values('name').distinct()
        all = Graph.objects.filter(subject=subject_object).exclude(type='infografik')
        researches = unique(Graph.objects.filter(subject=subject_object).exclude(type='infografik').order_by('-code'))
        #researches = objects.values_list('name', flat=True).distinct()
     
    if types == 'infographs': 
        researches = Graph.objects.filter(subject=subject_object, type='infografik')

    researches = list(researches)
    count = len(researches)

    paginator = Paginator(researches, 5)
    page = request.GET.get('page')
 
    try:
        researches = paginator.page(page)
    except PageNotAnInteger:
        researches = paginator.page(1)
    except EmptyPage:
        researches = paginator.page(paginator.num_pages)

    graphs = unique(Graph.objects.all())
    researches_all = Research.objects.all()[:4]
 

    return render_to_response('list.html',{'researches':researches, 'subject':subject_object, 'graphs':graphs, 'type':types, 'researches_all':researches_all, 'all':all, 'count':count,}) 

def single(request, subject, types, slug):

    subject_object = Subject.objects.filter(url_id=subject)

    if types == 'data': 
        researches = Research.objects.filter(slug=slug)
        graphs = list(unique(Graph.objects.filter(research = researches).exclude(type='infografik')))
    if types == 'graphs': 
        researches = Graph.objects.filter(slug=slug)
        graphs = Graph.objects.all().exclude(type='infografik')
    if types == 'infographs': 
        researches = Graph.objects.filter(type='infografik', slug=slug)
        graphs = Graph.objects.all()
    
        
    researches_all = Research.objects.all()[:4]

    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
	    message = form.cleaned_data['message']
	    sender = form.cleaned_data['sender']

	    recipients = ['info@reactor.org.mk']

	    from django.core.mail import send_mail
	    send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
     

    return render_to_response('single-graph.html',{'researches':researches, 'subject':subject_object, 'type':types, 'graphs':graphs, 'researches_all':researches_all,'form':form,}, context_instance = RequestContext(request)) 
   
def all_data(request, types):

    if types == 'data': 
        researches = Research.objects.all() 
    if types == 'graphs': 
        researches = list(unique(Graph.objects.all().exclude(type='infografik')))
    if types == 'infographs': 
        researches = Graph.objects.filter(type='infografik')


    paginator = Paginator(researches, 5)
    page = request.GET.get('page')
    try:
        researches = paginator.page(page)
    except PageNotAnInteger:
        researches = paginator.page(1)
    except EmptyPage:
        researches = paginator.page(paginator.num_pages)

    return render_to_response('all.html',{'researches':researches, 'type':types,}) 

def all_graphs_from_research(request, slug):

    research = Research.objects.filter(slug = slug)
    researches = unique(Graph.objects.filter(research = research).exclude(type='infografik'))

    researches = list(researches)
    count = len(researches)
    
    paginator = Paginator(researches, 5)
    page = request.GET.get('page')
 
    try:
        researches = paginator.page(page)
    except PageNotAnInteger:
        researches = paginator.page(1)
    except EmptyPage:
        researches = paginator.page(paginator.num_pages)

    return render_to_response('all_from_research.html',{'researches':researches, 'research':research, 'count':count,})
 
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
	    message = form.cleaned_data['message']
	    sender = form.cleaned_data['sender']

	    recipients = ['info@reactor.org.mk']

	    from django.core.mail import send_mail
	    send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    }) 


def all_researcher(request, researcher):

    r = Researchers.objects.filter(name=researcher)
    researches = Research.objects.filter(researchers=r) 

    count = len(researches)

    paginator = Paginator(researches, 5)
    page = request.GET.get('page')
    try:
        researches = paginator.page(page)
    except PageNotAnInteger:
        researches = paginator.page(1)
    except EmptyPage:
        researches = paginator.page(paginator.num_pages)

    return render_to_response('researcher.html', {'researches':researches, 'count':count,}) 


