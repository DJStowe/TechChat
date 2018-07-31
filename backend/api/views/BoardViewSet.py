from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet
from api.models import Board, Thread
from api.serializers import BoardSerializer, ThreadSerializer
from api.permissions import IsAdminOrReadOnly
from api.response import NOT_FOUND

# Threads can be listed, created, retrieved, updated, and destroyed.
class BoardViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,) # Only allow admins to create, update, destroy
    serializer_class = BoardSerializer
    lookup_field = 'id'

    # Set of all Boards
    def get_queryset(self):
        return Board.objects.all()

    # When viewing a Board's details, display a list of associated Threads.
    def retrieve(self, request, id=None):
        context = {
            'request': request # Used to determine ip, author
        }
        try:
            serializer = BoardSerializer(Board.objects.get(id=id), context=context)
            threadSerializer = ThreadSerializer(Thread.objects.filter(board=id), context=context, many=True)
            return Response({
                **serializer.data,
                **{
                    'threads': threadSerializer.data
                }
            })
        except:
            return NOT_FOUND.as_response()
