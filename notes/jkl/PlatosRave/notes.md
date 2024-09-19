
currently have: 
- two philosophies debate
  - moderator keeps track

New structural ideas:
- 5x a day, generate new conversations
- load up moderators with fallacy knowledge

# debate structure
- write your notecards
- trade notecards
- construct main points
- rounds of debate with the moderator

# fact-researcher swarm
- could use Consensus or other AIs to give relevant papers to each central point
- research AIs to give relevant papers to each central

# top-level questions
- by default "what is consciousness?"
- but can accept new debates by way of user comments (extracted, submitted, who knows, whatevs)


# user experience
- summaries of completed debates


# tournament brackets, rotating doors





100 views in one day!




```python
counterpoints_preparation_prompt = """
You have received your opponent's main points regarding their theory of consciousness. It's now your turn to prepare counterpoints for each of their main points. Each counterpoint should address the central idea, provide a counter-argument, and present any evidence that contradicts or challenges their point. 

Remember to consider the Rhetorical Triangle: ethos, pathos, and logos. Your counterpoints should be well-structured, logically sound, and emotionally resonant where applicable. 

Each counterpoint should be structured as follows:
```markdown
# Point [Number]: [Title of the opponent's point]
## Central Idea
[Restate the main idea of the opponent's point]
## Counter-Argument
[Present your counter-argument to this point]
## Explanation
[Explain why your counter-argument is valid and relevant]
## Evidence
[Provide any evidence that supports your counter-argument, the research swarm will find citations to back this up]
##
# Ethos
[Why should we trust you?]
## Pathos
[Why is this counter-argument emotionally resonant?]
## Logos
[Why is this counter-argument logically sound?]```

Put each counterpoint in a separate markdown cell, and label them as "Counterpoint 1", "Counterpoint 2", etc. This will be parsed by a python script which will send the counterpoints to the research swarm."""





```

counterpoint