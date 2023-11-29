
import json 
import requests
from pydantic import BaseModel

import vectorshift

from vectorshift.consts import API_AGENT_FETCH_ENDPOINT, API_AGENT_SAVE_ENDPOINT, API_AGENT_RUN_ENDPOINT

class ToolDefinition(BaseModel):
    name: str
    description: str
    type: str
    id: str

class Agent():
    def __init__(self, name: str, task: str, tools: list[ToolDefinition], llm: str = "gpt-3.5-turbo", framework: str = "ReAct", inputs: dict = None, outputs: dict = None, id : str = None):
        self.name = name
        self.task = task
        self.tools = tools
        self.llm = llm
        self.framework = framework
        self.inputs = inputs
        self.outputs = outputs
        self.id = id 

    @classmethod
    def from_json_rep(cls, json_data: dict[str, any]) -> 'Agent':
        return cls(
            name = json_data['name'],
            task = json_data['task'],
            tools = json_data['tools'],
            llm = json_data['llm'],
            framework = json_data['framework'],
            inputs = json_data['inputs'],
            outputs = json_data['outputs'],
            id = json_data['id']
        )


    @staticmethod
    def from_json(json_str: str) -> 'Agent':
        json_data = json.loads(json_str)
        return Agent.from_json_rep(json_data)

    def to_json_rep(self) -> dict:
        return {
            'name': self.name,
            'task': self.task,
            'tools': self.tools,
            'llm': self.llm,
            'framework': self.framework,
            'inputs': self.inputs,
            'outputs': self.outputs
        }
    

    @staticmethod
    def fetch(agent_name: str = None, 
             agent_id: str = None, 
             username: str = None, 
             org_name: str = None, 
             public_key=None, 
             private_key=None) -> 'Agent':
        """Load an already existing agent from the VS platform, Specify the agent id, agent name or both.
        
        Args:
            agent_id (str): The ID of the agent to load.
            agent_name (str): The name of the agent to load.
            public_key (str): The public key for authentication.
            private_key (str): The private key for authentication.
        
        Returns:
            Agent: The loaded agent object.
        """
        if agent_id is None and agent_name is None:
            raise ValueError("Must specify either agent_id or agent_name.")
        
        response = requests.get(
            API_AGENT_FETCH_ENDPOINT,
            data={
                'agent_id': agent_id,
                'agent_name': agent_name,
                'username': username, 
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return Agent.from_json_rep(response)
    
    
    def to_json(self) -> str:
        return json.dumps(self.to_json_rep(), indent=4)


    def save(self, public_key=None, private_key=None, update_existing=False) -> dict:
        """
        Save the agent to the VS platform. If update_existing is True, then will overrite an existing pipeline

        Args:
            update_existing (bool, optional): Update existing pipeline. Defaults to False.
        """
        if update_existing and not self.id:
            raise ValueError("Cannot update a agent that has not been saved yet.")
        
        if not update_existing:
            self.id  = None 

        response = requests.post(
            API_AGENT_SAVE_ENDPOINT,
            data={'agent': self.to_json()},
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        self.id = response.get('id')
        return response

    def run(self, inputs={}, public_key: str=None, private_key: str=None) -> dict:
        if not self.id:
            raise ValueError("Agent must be saved before it can be run.")
        
        response = requests.post(
            API_AGENT_RUN_ENDPOINT,
            data = ({
                'agent_id': self.id,
                'inputs': json.dumps(inputs),
            }),
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    def __repr__(self) -> str:
        return str(self.to_json_rep())
    

    def __str__(self) -> str:
        agent_str = f"Agent: {self.name}\n Task: {self.task}"
        agent_str += f"\n LL Model: {self.llm}"
        agent_str += f"\n Framework: {self.framework}"
        agent_str += f"\n Inputs: {self.inputs}"
        agent_str += f"\n Outputs: {self.outputs}"
        agent_str += "\n Tools: "
        for tool in self.tools:
            agent_str += f"\n\t Tool:{tool.name}"
            agent_str += f"\n\t\t Description: {tool.description}"
            agent_str += f"\n\t\t Type: {tool.type}"
            agent_str += f"\n\t\t ID: {tool.id}"