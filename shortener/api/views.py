from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.utils import json

from shortener.models import Url


@api_view(["GET", "POST"])
def links(request):
    if request.method == "GET":
        email = request.GET.get('email')
        if email:
            try:
                owner = User.objects.get(email=email)
            except:
                return JsonResponse({'success': False, 'message': 'User not found'})
            queryset = Url.objects.filter(owner=owner)

            # return JsonResponse({'success': True, 'urls': user_urls})
        return JsonResponse({'success': False, 'message': 'Pass the email'})

    if request.method == "POST":
        pass
