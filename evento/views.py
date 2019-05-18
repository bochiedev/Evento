from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    template = 'home.html'
    title = "Evento | Welcome"

    def get(self, request):

        context = {
            'title':self.title,
        }

        return render(request=request,
                      template_name=self.template,
                      context=context)
