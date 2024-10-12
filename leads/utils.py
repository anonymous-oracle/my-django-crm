from random import randint
from .models import Agent

def assign_agent_for_lead():
    pk_id = randint(1, Agent.objects.count())
    return Agent.objects.filter(id=pk_id).first() or Agent.objects.filter(user_id = pk_id).first()