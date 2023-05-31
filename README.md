
# Vland scene-based generative agent
This is a scene-based generative agent demo, based on the [Vland](https://us.vland.live/app) platform and the paper [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) by Park, et. al.

Thanks to [Harrison Chase](https://github.com/hwchase17) for the [agent_simulations demo](https://python.langchain.com/en/latest/use_cases/agent_simulations/characters.html#generative-agents-in-langchain) based on his own Langchain. We then packaged and fine-tuned on this basis. Looking forward to more interested developers can develop more in-depth based on this demo. Such as simulated town, social science experimental research, etc.

You can watch [Demo video](https://cocos.vland.live/docs/python/demo.mp4).

https://github.com/vlandlive/scene-based-generative-agent/assets/135107741/b206e9d5-dddb-4fb8-8b0e-77041fbe0879



## Quick Start

First, you need to configure your own `OPENAI_API_KEY`. You can get it from [OpenAI API Key](https://platform.openai.com/account/api-keys). It is recommended that you use a paid account, otherwise you will receive frequency restrictions during use. For details, please refer to [OpenAI rate limits](https://platform.openai.com/docs/guides/rate-limits/overview)

Set it in `agent/config.py`.
```python
os.environ["OPENAI_API_KEY"] = "your own key"
```

Next, you need to configure your own Vland config in `main.py`.

You can get `apiId`, `apiKey`, `eventId`, `spaceId` in [Vland](https://us.vland.live/app) platform. 

Please join our discord group [![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/6Nb9VQP67m) to get early access to your config key.

```python
wsconfig = {
    "apiId": "your vland id",
    "apiKey": "event api key",
    "eventId": "event id",
    "spaceId": "space id",
    "environment": "release",
    "listener": get_server_response
}
```

We preset the data of 4 agents for you. You can modify the data in `vland/data.py` according to your needs.

The avatar in the data represents the number of the Vland avatar. You can fill in according to your preferences.

![Vland avatars](https://cocos.vland.live/docs/python/avatars.png)

```python
agentData = {
    "vlandagent1": {
        "name": "Tommie",
        "personality": "anxious, likes design, talkative",
        "age": 25,
        "memories": [
            "Tommie remembers his dog, Bruno, from when he was a kid",
            "Tommie feels tired from driving so far",
            "Tommie sees the new home",
            "The new neighbors have a cat",
            "The road is noisy at night",
            "Tommie is hungry",
            "Tommie tries to get some rest."
        ],
        "current_status": "looking for a job",
        "avatar": 1
    },
    ...
}
```

Then you need enter the Vland space, so that you can observe later.

Finally, run your `main.py`
```python
python main.py
# maybe your command to run python is different
```

## Screenshots
If you see the following in the console, it means that you have connected to the server and successfully generated the agent. 

![Console Screenshot](https://cocos.vland.live/docs/python/screenshot1.png)

And these agents will appear in your vland space.

![Space Screenshot](https://cocos.vland.live/docs/python/screenshot2.png)

You need to check the network and your Vland config, if it doesn't happen according to plan.

Then these agents will run according to your logic and ChatGPT

![Space Screenshot](https://cocos.vland.live/docs/python/screenshot3.png)
## DIY your script
Use the interface provided by vland and the method of generating agents.

You can define the logic that your agent runs in `main.py` like

```python
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

```

The Vland interface related to generating agents is written in `vland/vlandapi`

We will continue to add more interfaces.

And the functions that can be realized can also refer to [Vland websocket sdk (node.js)](https://cocos.vland.live/docs/)
## Support

For support, email vland.live@gmail.com


## References

1. https://arxiv.org/abs/2304.03442
2. https://python.langchain.com/en/latest/use_cases/agent_simulations/characters.html#create-a-generative-character
