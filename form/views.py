from django.shortcuts import render
from rest_framework.views import APIView
from .models import Lead, Agent, User
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeadSerializer, LeadSerializerAll
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated




class LeadView(APIView):
    '''
    View class to either view all unclaimed leads or to create a new lead.
    '''

    def get(self, request):
        '''
        GET all unclaimed leads.
        '''
        queryset = Lead.objects.filter(
            Q(claimed=None)
            or Q(claimed="")
        ).all()
        serialized = LeadSerializer(queryset, many=True)

        return Response(
            serialized.data,
            status=status.HTTP_302_FOUND
        )

    def post(self, request):
        '''
        POST/create a new questionare/lead.
        '''
        try:
            data = LeadSerializer(data=request.data)
        except Exception as err:
            return Response(
                {
                    "error": str(err)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if data.is_valid():
            data.save()
            return Response(
                data.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "error": str(data.errors)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AgentView(APIView):
    '''
    View class to assign a lead/questionare to an agent/employee.
    '''
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        '''
        GET a single unclaimed lead or a lead claimed by the requesting user.
        '''
        agent = Agent.objects.filter(user=request.user).first()
        try:
            lead = Lead.objects.filter(
                (Q(claimed=None) or Q(claimed=agent)) and Q(id=id)).first()
            lead_serialized = LeadSerializerAll(lead)
        except Lead.DoesNotExist:
            return Response(
                {
                    "error": "Lead claimed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            lead_serialized.data,
            status=status.HTTP_202_ACCEPTED
        )

    def post(self, request, id: int):
        
        agent = Agent.objects.filter(user=request.user).first()
        try:
            lead = Lead.objects.get(pk=id)
        except Lead.DoesNotExist:
            return Response(
                {
                    "error": "This lead does not exist."
                },
                status=status.HTTP_204_NO_CONTENT
            )
        if not lead.claimed:
            lead.claime = agent
            lead.save()
            serialized = LeadSerializerAll(lead)

            return Response(
                serialized.data,
                status=status.HTTP_202_ACCEPTED
            )
        elif lead.claimed != agent:
            return Response(
                {
                    "error": "Lead already claimed."
                },
                status=status.HTTP_306_RESERVED
            )
        elif lead.claimed == agent:
            return Response(
                {
                    "error": "You have already claimed this."
                },
                status=status.HTTP_400_BAD_REQUEST
            )