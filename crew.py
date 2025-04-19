from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    # FirecrawlSearchTool,
    FirecrawlScrapeWebsiteTool,
    SerperDevTool,
    FileReadTool
)

import os
os.environ['FIRECRAWL_API_KEY'] = ''
os.environ['SERPER_API_KEY'] = ''
os.environ['OPENAI_API_KEY'] = ''


gpt4 = 'openai/gpt-4o-mini'
gpt3 = 'gpt-3.5-turbo-0125'
MODEL = gpt4
serper_tool = SerperDevTool()
firecrawl_tool = FirecrawlScrapeWebsiteTool(
        page_options= {'onlyMainContent' :True}
        )
file_read_tool = FileReadTool(file_path= 'links.md')

@CrewBase
class ImmigrationCanResearchCrew():
    """ImmigrationCanResearchCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher_links(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_links'],
            llm=MODEL,
            tools =[serper_tool],
            verbose=True
        )

    @agent
    def information_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['information_analyzer'],
            llm=MODEL,
            tools = [file_read_tool,firecrawl_tool],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_online_links(self) -> Task:
        return Task(
            config=self.tasks_config['research_online_links'],
            output_file="links.md"
        )

    @task
    def analyze_links(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_links'],
            context =[self.research_online_links()],
            output_file='info.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ImmigrationCanResearchCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            planning = True,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
