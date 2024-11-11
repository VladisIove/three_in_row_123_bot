from django.views.generic import TemplateView


class MainPageWebApp(TemplateView):
    template_name = 'index.html'