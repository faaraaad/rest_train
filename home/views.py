from rest_framework.response import Response
from rest_framework.views import APIView
import json
from .serializers import CreateUserSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import CustomeAuth
from .models import CommentModel

class TestShow(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated, CustomeAuth]
    def get(self, request, who):
        return Response({'user': str(request.user), 'auth':str(request.auth)})
    # validatio
    def post(self, request,who):
        return Response({'name': request.data['name'],
            'family': request.query_params['value'],
            'who': who})
            
class CreateUser(APIView):
    def post(self, request):
        validation= CreateUserSerializer(data=request.data)
        if validation.is_valid():
            vd= validation.validated_data
            User.objects.create_user(username=vd['username'], password=vd['password'],
                                    email=vd['email'])
            return Response({'value': 'successful'})
        return Response(validation.errors)

        
class HomeView(APIView):
    def get(self, request):
        posts= CommentModel.objects.all()
        data= CommentSerializer(instance=posts, many=True).data
        return Response(data)