from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .serializers import UsuarioSerializer, FuncionarioSerializer
from .models import Usuario
import jwt, datetime
from django.http import JsonResponse
from .models import Funcionario




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


def buscar_funcionario_por_matricula(request, matricula):
    try:
        # Se a matrícula for um número, converte para inteiro
        try:
            matricula = int(matricula)
        except ValueError:
            pass  # Se não for número, mantém como string

        funcionario = get_object_or_404(Funcionario, matricula=matricula)

        return JsonResponse({
            'id': funcionario.id,
            'nome': funcionario.nome,
            'cargo': funcionario.cargo,
            'matricula': funcionario.matricula
        })
    except Funcionario.DoesNotExist:
        return JsonResponse({'erro': 'Funcionário não encontrado'}, status=404)

def patch( request, id):
    try:
        try:
            id = int(id)
        except ValueError:
            pass  # Se não for número, mantém como string
        funcionario = get_object_or_404(Funcionario,id=id)
        return JsonResponse({
            'id': funcionario.id,
            'nome': funcionario.nome,
            'cargo': funcionario.cargo,
            'matricula': funcionario.matricula,
            'total_alertas': funcionario.total_alertas,
            'duracao_segundos': funcionario.duracao_segundos,
        })
    except Funcionario.DoesNotExist:
        return JsonResponse({'error': 'Funcionário não encontrado!'}, status=404)

        # Atualiza os campos recebidos na requisição
        funcionario.duracao_segundos = request.data.get('duracao_segundos', funcionario.duracao_segundos)
        funcionario.total_alertas = request.data.get('total_alertas', funcionario.total_alertas)

        # Salva as alterações no banco de dados
        funcionario.save()

        # Retorna o funcionário atualizado
        return Response(FuncionarioSerializer(funcionario).data, status=200)

