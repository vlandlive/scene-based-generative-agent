
# Vland scene-based generative agent
This is a scene-based generative agent demo, based on the [Vland](https://us.vland.live/app) platform and the paper [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) by Park, et. al.

Thanks to [Harrison Chase](https://github.com/hwchase17) for the [agent_simulations demo](https://python.langchain.com/en/latest/use_cases/agent_simulations/characters.html#generative-agents-in-langchain) based on his own Langchain. We then packaged and fine-tuned on this basis. Looking forward to more interested developers can develop more in-depth based on this demo. Such as simulated town, social science experimental research, etc.

You can watch [Demo video](https://cocos.vland.live/docs/python/demo.mp4).

https://github.com/vlandlive/scene-based-generative-agent/assets/135107741/b206e9d5-dddb-4fb8-8b0e-77041fbe0879

Welome to join our discord group.

[![Discord](https://dcbadge.vercel.app/api/server/6Nb9VQP67m?compact=true)](https://discord.gg/6Nb9VQP67m)

## Quick Start

First, you need to configure your own `OPENAI_API_KEY`. You can get it from [OpenAI API Key](https://platform.openai.com/account/api-keys). It is recommended that you use a paid account, otherwise you will receive frequency restrictions during use. For details, please refer to [OpenAI rate limits](https://platform.openai.com/docs/guides/rate-limits/overview)

Set it in `agent/config.py`.
```python
os.environ["OPENAI_API_KEY"] = "your own key"
```

Next, you need to configure your own Vland config in `main.py`.

You can get `apiId`, `apiKey`, `eventId`, `spaceId` in [Vland](https://us.vland.live/app) platform. 

* The `apiId` is your user id. It is displayed in the account in the upper right corner of the page.

![Vland config](https://cocos.vland.live/docs/python/config1.png)

* The `apiKey` is for each different vland events. You can create and copy it in *Manage events*

![Vland config](https://cocos.vland.live/docs/python/config2.png)

* The `eventId` and `spaceId` is for each different space in the event. You can find them in the link after entering the space.

![Vland config](https://cocos.vland.live/docs/python/config3.png)


```python
wsconfig = {
    "apiId": "your vland id",
    "apiKey": "event api key",
    "eventId": "event id",
    "spaceId": "space id",
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

## Create your own spcae in Vland

The destination of the agent's movement is selected from the marked area in the space。

You can follow the steps below to create a space and edit the area.

1. Sign up and log in to Vland.

2. Create a space in the upper right corner of the page.
![Step](https://cocos.vland.live/docs/python/step1.png)

3. Enter your event name.
![Step](https://cocos.vland.live/docs/python/step2.png)

4. Add a new space under your event.
![Step](https://cocos.vland.live/docs/python/step3.png)

5. We provide many exquisite templates for you to quickly create your space. You can also create an empty map and use the materials we provide to decorate your space
![Step](https://cocos.vland.live/docs/python/step4.png)

6. Select the space you want to edit
![Step](https://cocos.vland.live/docs/python/step5.png)

7. Select the *Special interaction* in the *Effect*. Frame the area you want to mark on the map and enter a unique name.
![Step](https://cocos.vland.live/docs/python/step6.png)

8. Finally, remember to save the map, then you can enter your own space.
![Step](https://cocos.vland.live/docs/python/step7.png)

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

For support, you can join our discord group [![Discord](https://dcbadge.vercel.app/api/server/6Nb9VQP67m?compact=true)](https://discord.gg/6Nb9VQP67m). Or email vland.live@gmail.com


## References

1. https://arxiv.org/abs/2304.03442
2. https://python.langchain.com/en/latest/use_cases/agent_simulations/characters.html#create-a-generative-character