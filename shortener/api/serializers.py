from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from shortener.models import Url


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UrlSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return reverse('redirectURL', request=self.context.get('request'), kwargs={'hash_url': obj.hash_url})

    class Meta:
        model = Url
        exclude = ('hash_url', )
