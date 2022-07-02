from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from shortener.models import Url
from .serializers import UrlSerializer, TokenSerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, ])
def obtain_auth_token(request):
    if request.method == "POST":
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key}, status=201)

    tokens = Token.objects.filter(user=request.user)
    serializer = TokenSerializer(tokens, many=True)

    return Response(serializer.data, status=200)


@api_view(["DELETE"])  # Add "GET" if 'method not allowed'
@authentication_classes([SessionAuthentication, ])
def delete_auth_token(request, key):
    n, _ = Token.objects.filter(user=request.user, key=key).delete()
    if n == 0:
        return Response({'errors': ['Key not found']}, status=404)
    return Response(status=200)


@api_view(["GET"])
def get_routes(request):
    routes = [
        {'GET': '/api/links'},
        {'POST': '/api/links'},
        {'GET': '/api/link_info'},
    ]

    return Response(routes)


@api_view(["GET", "POST"])
def links(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return Response({'errors': ['Invalid email parameter']}, status=400)
        # TODO Check if Authenticate token belongs to the email owner; if not - Access denied
        # try:
        #     owner = User.objects.get(email=email)
        # except:
        #     return JsonResponse({'errors': ['User not found']})

        links = Url.objects.filter(owner__email=email)
        serializer = UrlSerializer(links, many=True, context={'request': request})

        return Response({'links': serializer.data})


@api_view(["GET"])
def link_info(request):
    path = request.GET.get('path')
    if not path:
        return Response({'errors': ['Invalid path parameter']}, status=400)
    # TODO Check if Authenticate token belongs to the url owner
    try:
        link = Url.objects.get(hash_url=path)
    except Url.DoesNotExist:
        return Response({'errors': ['Link not found']})

    serializer = UrlSerializer(link, many=False, context={'request': request})
    return Response(serializer.data)
