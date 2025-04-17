import json
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
#from secret import initialize_api_keys


from crew import ImmigrationCanResearchCrew
from datetime import date

#initialize_api_keys()
#initialize api key here

class QueryInformation(BaseModel) :
    topic : str = Field(description='the topic of the input')
    goal : str = Field(description='the goal of the input')
    isAboutImCan : bool = Field(description='if it is about immigration to canada or not')

class Ircc_exp_state(BaseModel) :
    query : str = '',
    #query_info : QueryInformation = None

class IRcc_exp_flow(Flow[Ircc_exp_state]) :
    """Flow getting details about a specific topic for Imm Canada"""

    @start()
    def get_user_input(self) :
        print('===== What do you want to ask?')
#self.state.query = input('What do you want to ask ?')
#self.state.query = 'how to get a pr as a french speaking person in Canada?'
        return self.state.query

    @listen(get_user_input)
    def get_topic(self, state) :
        print('=== define query : topic and goal')
#llm call
        llm = LLM(model="openai/gpt-4o-mini", response_format=QueryInformation)
        messages = [
            {'role' : 'system', 'content': 'You are a helpful assistant designed to output JSON.'},
            {'role' : 'user' , 'content' : f"""
          Find the goal and the topic conveyed by the following query :
          {self.state.query}
          and define if the topic is about Immigration to canada or not.
        """}
            ]

        response = llm.call(messages=messages)

        query_info_dict = json.loads(response)
        #self.state.query_info = QueryInformation(**query_info_dict)

        #return self.state.query_info
        return query_info_dict

    @listen(get_topic)
    def get_info(self, query_info) :
        print("====get info with :",query_info)
        if(query_info["isAboutImCan"]) :
            print('fire the crew')
            result = ImmigrationCanResearchCrew().crew().kickoff(inputs = {
                "topic" : query_info["topic"],
                "goal" : query_info["goal"],
                "year" : date.today().year - 1
                });
            print('result ,', result)
            return result
        else :
            print('apologize respectfully')
            return 'ask something on topic'

def kickoff(query) :
    return IRcc_exp_flow().kickoff(
            inputs = { 'query' : query }
            )

def plot() :
    flow = IRcc_exp_flow()
    flow.plot('IRCC expert flow')

