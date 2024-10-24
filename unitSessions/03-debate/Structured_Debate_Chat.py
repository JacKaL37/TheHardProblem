# Structured Debate Chat

# Goal: Get LLM agents personifying different consciousness philosophers to chat in a structured debate.
# Various phases and steps follow:
# - defining personas and debate topic
# - personas generate main points and argument notes
# - personas see each other's main points and prepare talking points for the debate
#   - add talking points for opponent
# - Actual debate occurs in turns:
#   - opening remarks
#   - responses
#   - etc (look up actual debate patterns)
#   - Moderator comments and continues the debate.

# !pip install pyautogen, dotenv

# pip install requirements.txt

import autogen  # noqa: E402
import os
import json

import dotenv

print("Starting Structured Debate Chat")

# Load environment variables
dotenv.load_dotenv()
print("Environment variables loaded")

# LLM Configuration
openai_key = os.getenv("OPENAI_API_KEY")
config_list = [{
    "model": "gpt-4o-mini",
    "api_key": openai_key
}]

llm_config = {
    "timeout": 600,
    "cache_seed": 342,  # change the seed for different trials
    "config_list": config_list,
    "temperature": 1,
}
print("LLM Configuration set")

# Persona Setup
penrose_assistant = autogen.AssistantAgent(
    "Rodger-Penrose",
    system_message="""
    I am Rodger Penrose, and I am debating my Orchestrated objective reduction theory of consciousness.
    I'll speak, then wait to hear my opponent's reply. I won't try to generate the reply of my opponent.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)
print("Penrose Assistant created")

searle_assistant = autogen.AssistantAgent(
    "John-Searle",
    system_message="""I am John R. Searle, and I am debating my theory of consciousness. I'll speak, then wait to hear my opponent's reply. I won't try to generate the reply of my opponent.""",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)
print("Searle Assistant created")

moderator_assistant = autogen.AssistantAgent(
    "Moderator",
    system_message="""
    I am the moderator, and my role is to summarize the points that are still up for debate, and keep the conversation on-topic.
    I shouldn't be too heavy-handed, but prevent conversational drift.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda x: False,
)
print("Moderator Assistant created")

# Debate setup

debating_agents = [penrose_assistant, searle_assistant]
debate_dir = "./debate_sessions/01"
os.makedirs(debate_dir, exist_ok=True)
print(f"Debate directory created: {debate_dir}")



# Get the agents to articulate their main points
points_articulation_prompt = """
Please articulate the main points of your theory of consciousness. Your points will be researched by a research swarm, and then debated by you and your opponent.
Each point must contain the central idea, and give enough information that the research swarm can find any evidence that supports it in the research literature.
Consider the Rhetorical Triangle: ethos, pathos, and logos.
Consider the logical structure of your argument: premise, evidence, conclusion.
You'll also need to provide a brief explanation of the point, and why it is important to your theory, and how it supports your theory.

Each point should be structured as follows:

```markdown
# Point 1: [Title of the point]
## Central Idea
[The main idea of the point]
## Explanation
[An explanation of the point]
## Relevance to the theory
[How this point is important to your theory]
## Evidence
[What evidence supports this point that you know of, the research swarm will find citations to support this point]
## Ethos
[Why should we trust you?]
## Pathos
[Why is this point emotionally resonant?]
## Logos
[Why is this point logically sound?]
```

Put each point in a separate markdown cell, and label them as "Point 1", "Point 2", etc. This will be parsed by a python script which will send the points to the research swarm.
"""

for agent in debating_agents:
    print(f"Processing main points for {agent.name}")

    points_file = debate_dir + "/" + agent.name + "_main_points.md"
    print(f"Writing main points to file: {points_file}")

    point = agent.generate_oai_reply([{
        "role": "system",
        "content": points_articulation_prompt
    }])
    print(f"Generated main points for {agent.name}:")
    print(point[1])
    agent.point = point

    with open(points_file, "w", encoding="utf-8") as f:
        f.write(point[1])
    print(f"Main points for {agent.name} have been written to file")

    print(f"Finished processing main points for {agent.name}\n")




# Counterpoints Preparation
counterpoints_preparation_prompt = """
You have received your opponent's main points regarding their theory of consciousness. It's now your turn to prepare counterpoints for each of their main points. Each counterpoint should address the central idea, provide a counter-argument, and present any evidence that contradicts or challenges their point.

Remember to consider the Rhetorical Triangle: ethos, pathos, and logos. Your counterpoints should be well-structured, logically sound, and emotionally resonant where applicable.

Each counterpoint should be structured as follows:
```markdown
# Opponent Point [Number]: [Title of the opponent's point VERBATIM, DO NOT ALTER]
## Central Idea
[Restate the main idea of the opponent's point, in your own words. Do not state your counter-argument.]
## Counter-Argument
[Present your counter-argument to this point]
## Explanation
[Explain why your counter-argument is valid and relevant]
## Evidence
[Provide any evidence that supports your counter-argument, the research swarm will find citations to back this up]
## Ethos
[Why should we trust you?]
## Pathos
[Why is this counter-argument emotionally resonant?]
## Logos
[Why is this counter-argument logically sound?]```

Put each counterpoint in a separate markdown cell, and label them as "Counterpoint 1", "Counterpoint 2", etc. This will be parsed by a python script which will send the counterpoints to the research swarm."""

# Load opponent's points from file and assign to agents
for agent in debating_agents:
    opponent = searle_assistant if agent.name == "Rodger-Penrose" else penrose_assistant
    opponent_points_file = opponent.name + "_main_points.md"

    print(f"Loading opponent points for {agent.name} from {opponent_points_file}")
    with open(debate_dir + "/" + opponent_points_file, "r", encoding="utf-8") as f:
        opponent_points = f.read()


    agent.opponent_points = opponent_points
    print(f"Opponent points loaded for {agent.name}")
    print(agent.opponent_points)


# Prepare counterpoints
for agent in debating_agents:
    print(f"Preparing counterpoints for {agent.name}")

    counterpoints = agent.generate_oai_reply([{
        "role": "system",
        "content": counterpoints_preparation_prompt
    }, {
        "role": "system",
        "content": "Reminder of your own points should you need to reference them: " + agent.point[1]
    }, {
        "role": "system",
        "content": "Your opponent's points: " + agent.opponent_points
    }])

    counterpoints_file = debate_dir + "/" + agent.name + "_counterpoints.md"
    with open(counterpoints_file, "w", encoding="utf-8") as f:
        f.write(counterpoints[1])
    print(f"Counterpoints for {agent.name} have been written to file: {counterpoints_file}")

    print(f"Finished preparing counterpoints for {agent.name}\n")

# Debate task
task = "Your roles are to debate your respective theories on consciousness until you are satisfied."
user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    is_termination_msg=lambda x: False,
)



groupchat = autogen.GroupChat(agents=[user_proxy, penrose_assistant, searle_assistant, moderator_assistant], messages=[], max_round=30, speaker_selection_method="round_robin")

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message=task)

# Write the chat to a file
with open("chat.txt", "w") as f:
    f.write(str(groupchat.messages))
