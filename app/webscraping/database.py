import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_client():

    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

def insert_team_1(data, supabase):
    response = (supabase.table("val_stats").insert(
        { 
         'map_name': data['map_name'], 
         'total_score': data['teams'][0]['total_score'], 
         'ct_score': data['teams'][0]['ct_score'], 
         't_score': data['teams'][0]['t_score'],
         'agent_1': data['teams'][0]['agents'][0],
         'agent_2': data['teams'][0]['agents'][1],
         'agent_3': data['teams'][0]['agents'][2],
         'agent_4': data['teams'][0]['agents'][3],
         'agent_5': data['teams'][0]['agents'][4]
        }
    ).execute())
    return response

def insert_team_2(data, supabase):
    response = (supabase.table("val_stats").insert(
        { 
         'map_name': data['map_name'], 
         'total_score': data['teams'][1]['total_score'], 
         'ct_score': data['teams'][1]['ct_score'], 
         't_score': data['teams'][1]['t_score'],
         'agent_1': data['teams'][1]['agents'][0],
         'agent_2': data['teams'][1]['agents'][1],
         'agent_3': data['teams'][1]['agents'][2],
         'agent_4': data['teams'][1]['agents'][3],
         'agent_5': data['teams'][1]['agents'][4]
        }
    ).execute())
    return response

def insert_for_match(match_data, supabase):
    for data in match_data:
        insert_team_1(data, supabase)
        insert_team_2(data, supabase)