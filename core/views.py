from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UsuarioSerializer
from .models import Usuario
import jwt, datetime

# Create your views here.




class LoginView(APIView):
    def post(self, request):
        matricula = request.data['matricula']
        password = request.data['password']

        try:
            usuario = Usuario.objects.get(matricula=matricula)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuário com permissão não encontrado')

        if not usuario.check_password(password):
            raise AuthenticationFailed('Senha incorreta')

        payload = {
            'id': usuario.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class UsuarioView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Sem autenticação")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            raise AuthenticationFailed("Sem autenticação")

        usuario = Usuario.objects.filter(id=payload['id']).first()
        serializer = UsuarioSerializer(usuario)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'Logout com sucesso'
        }
        return response