from .models import Todo
from rest_framework import viewsets, permissions
from .serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = {
        permissions.AllowAny
    }
    serializer_class = TodoSerializer

    def list(self, request):
        print("CALL GET REQUEST")
        queryset = Todo.objects.all()
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print("CREATE NEW RECORD")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
