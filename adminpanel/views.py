from django.shortcuts import render
from django.views.generic import View


class AdminPanel(View):

    def get(self, request):
        return render(request, 'adminpanel/adminpanel.html', {})

    def post(self):
        pass
