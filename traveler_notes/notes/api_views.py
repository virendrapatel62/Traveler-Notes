from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import NoteSerializer, Note
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


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
