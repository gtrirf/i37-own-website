from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import MainInfo, Career, SocialLink
from .serializers import MainInfoSerializer, CareerSerializer, SocialLinkSerializer


class MainInfoView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = MainInfoSerializer

    def get_object(self):
        return MainInfo.objects.first()


class CareerListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CareerSerializer
    queryset = Career.objects.all()


class SocialLinkListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SocialLinkSerializer
    queryset = SocialLink.objects.all()
