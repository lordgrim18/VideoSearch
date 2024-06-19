from django.shortcuts import render

from rest_framework.renderers import TemplateHTMLRenderer
from api.view import SearchAPIView 


def home(request):
    return render(request, "frontend/home.html")

class SearchView(SearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/search_results.html'