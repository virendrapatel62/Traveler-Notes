
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import NoteSerializer, Note
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from traveler_notes.settings import CLIENT_ID, CLIENT_SECRET, MAP_REST_API_KEY
import requests


AUTH_URL = 'https://outpost.mapmyindia.com/api/security/oauth/token'
GEOCODE_API_URL = 'https://atlas.mapmyindia.com/api/places/geocode'
ELOC_API_URL = f'https://apis.mapmyindia.com/advancedmaps/v1/{MAP_REST_API_KEY}/place_detail'
AUTH_CREDENTIALS = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}


class NoteListView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        user = request.user
        note = Note(title=title, comment=comment, lat=lat, lng=lng, user=user)
        note.save()
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


class NoteDetailView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class PlaceSearchApiView(APIView):
    def get(self, request):
        address = request.GET.get('address')
        print(address)

        authResult = requests.post(AUTH_URL, params=AUTH_CREDENTIALS).json()
        access_token = authResult['access_token']
        token_type = authResult['token_type']

        geocoding_params = {
            'address': address,
            'itemCount': 5
        }
        headers = {
            'Authorization': f'{token_type} {access_token}'
        }
        addressResponse = requests.get(GEOCODE_API_URL, params=geocoding_params,
                                       headers=headers).json()
        # generate Token

        return Response(addressResponse)


class ElocApiView(APIView):
    def get(self, request, placeid):
        authResult = requests.post(AUTH_URL, params=AUTH_CREDENTIALS).json()
        access_token = authResult['access_token']
        token_type = authResult['token_type']

        params = {
            'region': 'IND',
            'place_id': placeid
        }

        addressResponse = requests.get(ELOC_API_URL, params=params).json()
        # generate Token

        return Response(addressResponse)
