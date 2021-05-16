from rest_framework.response import Response
from rest_framework.views import APIView
from .models import NoteSerializer, Note
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateNote(APIView):
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
