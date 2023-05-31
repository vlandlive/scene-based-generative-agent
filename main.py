from agent.agent import GenerativeAgent
from agent.memory import GenerativeAgentMemory
from agent.simulation import LLM, create_new_memory_retriever
from vland.vlandapi import VlandAPI
from vland.eventbus import EventBus
from vland.data import agentData

import threading

import asyncio
import time
import random

from termcolor import colored

# protoc --python_out=pyi_out:./ ./vland/api.proto


class VlandAgent:
    areaList = None
    currentArea = {}
    playerInfo = {}
    runtime = 0

    def __init__(self, player, vland, eventbus):
        self.vland: VlandAPI = vland
        self.eventbus: EventBus = eventbus

        # Initialize player info
        self.playerInfo = player

        # Create new memory
        self.memory = GenerativeAgentMemory(
            llm = LLM,
            memory_retriever = create_new_memory_retriever(),
            verbose = False,
            reflection_threshold = 8 # we will give this a relatively low number to show how reflection works
        )
        # Create a new agent from data
        self.player = GenerativeAgent(
            name = self.playerInfo["name"],
            age = self.playerInfo["age"],
            # You can add more persistent traits here
            traits = self.playerInfo["personality"],
            # When connected to a virtual world, we can have the characters update their status
            status = self.playerInfo["current_status"],
            memory_retriever = create_new_memory_retriever(),
            llm = LLM,
            memory = self.memory
        )

         # Initialize memories from data
        # self._init_memory(self.playerInfo["memories"])
        print(colored(f"{self.player.name} generated successfully!", 'blue', attrs=['bold']))
        
        # Get area list map info
        self.areaList = self.vland.get_space_areas()
        self.vland.born_in_space(self.playerInfo, area="living room")
        
        # print(self.player.get_summary())

    def _init_memory(self, memories: list):
        # We can add memories directly to the memory object
        for observation in memories:
            self.memory.add_memory(observation)

    '''
    Continuously receive notifications from others.
    And run the agent according to your logic
    '''    
    def run(self):
        def __handle_other_action(data):
            if data["pid"] != self.playerInfo["pid"]:
                self.memory.add_memory(data["action"])

        self.eventbus.subscribe("action", __handle_other_action)

        while True:
            num = random.randint(0, 1)
            duration = random.randrange(3, 7)
            if num == 0:
                asyncio.run(self._observe_an_area())
            elif num == 1:
                self._explore_freely()

            time.sleep(duration)
            
    
    '''
    Explore this space.
    '''     
    def _explore_freely(self):
        observation = "There is still a lot of unexplored space on this island. Or you can try to find others to make some friends."
        _, reaction, area = self.player.generate_reaction(observation, self.areaList["names"])
        print(colored(observation, "green"), colored(area, "blue"), reaction)
        self.vland.operate_robot(self.playerInfo["pid"], area=area, message=reaction)
            
        notice = {}
        notice["pid"] = self.playerInfo["pid"]
        notice["action"] = reaction

        self.eventbus.publish("action", notice)

    '''
    Call the interface provided by vland to get all the agents in the current area.
    Record the acquired data into agent's observations.
    And respond to the observation.
    Then tell other agents about this action.
    '''        
    async def _observe_an_area(self):
        # call vland.get_all_in_area(area="living room") to get agents info in the current area
        self.currentArea = await self.vland.get_all_in_area(area="living room")

        # create an observation
        observation = "In the " + self.currentArea["name"] +  ", you met "
        hasOthers = False
        for pid in self.currentArea["data"]:
            if pid != self.playerInfo["pid"] and pid in agentData:
                observation += agentData[pid]["name"] + ", "
                hasOthers = True
        if hasOthers:
            # save this observation to memory
            self.memory.add_memory(observation)
            # generate reaction by observation
            _, reaction, area = self.player.generate_reaction(observation, self.areaList["names"])
            print(colored(observation, "green"), colored(area, "blue"), reaction)
            # call vland.operate_robot to command the agent to act
            self.vland.operate_robot(self.playerInfo["pid"], area=area, message=reaction)
                
            notice = {}
            notice["pid"] = self.playerInfo["pid"]
            notice["action"] = reaction
            # push to other agents
            self.eventbus.publish("action", notice)


def get_server_response(response):
    pass

def generate_agents_by_data():
    wsconfig = {
        "apiId": "your vland id",
        "apiKey": "event api key",
        "eventId": "event id",
        "spaceId": "space id",
        "environment": "release",
        "listener": get_server_response
    }
    eventbus =  EventBus()
    vland = VlandAPI(wsconfig)

    vland.clear_robot()
    
    for pid in agentData:
        player = agentData[pid]
        player["pid"] = pid

        agent = VlandAgent(player, vland, eventbus)
        
        thread = threading.Thread(target=agent.run, daemon=True)
        thread.start()

if __name__ == '__main__':
    generate_agents_by_data()
    while True:
        time.sleep(1)
    