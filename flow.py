import json
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.agent import Agent
from crewai.flow.flow import Flow, listen, start, router
#from secret import initialize_api_keys



from crew import ImmigrationCanResearchCrew
from datetime import date

#initialize_api_keys()
#initialize api key here

class QueryInformation(BaseModel) :
    topic : str = Field(description='the topic of the input'),
    goal : str = Field(description='the goal of the input'),
    isAboutImCan : bool = Field(description='if it is about immigration to canada or not')

class Ircc_exp_state(BaseModel) :
    query : str = '',



class IRcc_exp_flow(Flow[Ircc_exp_state]) :
    """Flow getting details about a specific topic for Imm Canada"""

    @start()
    def start_method(self):
        print('===== What do you want to ask?')
        return self.state.query

    @listen(start_method)
    def get_topic(self):
        print('=== define query : topic and goal')
        llm = LLM(model="openai/gpt-4o-mini", response_format=QueryInformation)
        messages = [
                {
                    'role' : 'system', 
                    'content': 'You are a helpful assistant designed to output JSON.'},
                {
                    'role' : 'user' , 
                    'content' : f"""
                      Find the goal and the topic conveyed by the following query :
                      {self.state.query}
                      and define if the topic is about Immigration to canada or not.
                    """
                 }
        ]
        response = llm.call(messages=messages)
        query_info_dict = json.loads(response)
        info = QueryInformation(**query_info_dict)
        return info

    @listen(get_topic)
    async def get_info(self, query_info) :
        print("====get info with :",query_info)
        if(query_info.isAboutImCan) :
            print('fire the crew')
            result = ImmigrationCanResearchCrew().crew().kickoff(inputs = {
                "topic" : query_info.topic,
                "goal" : query_info.goal,
                "year" : date.today().year - 1
                });
            print('result ,', result)
            return result
        else :
            print('apologize respectfully')
            apologizer = Agent(
                    role = "Apologize for the system should only be used to inquire topic on immigration to Canada",
                    goal = "tell the user that the question is off-topic",
                    backstory = "you are very respectful",
                    verbose = True,
                    );
            result = await apologizer.kickoff_async(self.state.query)
            return result;

def kickoff(query) :
    return IRcc_exp_flow().kickoff(
            inputs = { 'query' : query }
            )

def plot() :
    flow = IRcc_exp_flow()
    flow.plot('IRCC_expert_flow')

