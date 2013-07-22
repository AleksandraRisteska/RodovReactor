from haystack.indexes import *
from haystack import site
from myproject.models import *

class ResearchersIndex(SearchIndex):
    text = NgramField(document=True, use_template=True)
    name = NgramField(model_attr='name')

class SubjectIndex(SearchIndex):
    short_name = NgramField(model_attr='short_name')
    name = NgramField(model_attr='name')
    text = NgramField(document=True, use_template=True)

class ResearchIndex(SearchIndex):
    text = NgramField(document=True, use_template=True)
    abstract = NgramField(model_attr='abstract')
    methodology = NgramField(model_attr='methodology')
    year = NgramField(model_attr='year')
    name = NgramField(model_attr='name')
    slug = NgramField(model_attr='slug')
    

class GraphIndex(SearchIndex):
    text = NgramField(document=True, use_template=True)
    explanation = NgramField(model_attr='explanation')
    type = NgramField(model_attr='type')
    name = NgramField(model_attr='name')
    slug = NgramField(model_attr='slug')

site.register(Researchers, ResearchersIndex)
site.register(Subject, SubjectIndex)
site.register(Research, ResearchIndex)
site.register(Graph, GraphIndex)


