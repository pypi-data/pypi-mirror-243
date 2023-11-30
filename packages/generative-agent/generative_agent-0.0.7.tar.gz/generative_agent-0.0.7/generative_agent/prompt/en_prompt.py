## {{gen 'rate' pattern='[0-9]+' stop='\n'}}
PROMPT_ADDMEM = {
    "prompt_template": """### Instruction:
On a scale of 1 to 10, with a rating of 1 when the memory is mundane, occurs regularly (e.g. waking up, working, bathing) and rate to 10 when it is unusual and does not occur frequently (e.g. birth or death of life, or meeting friends you haven't seen for a long time) Rate the following memories. Answer with integers (1,2,3,4,5,6,7,8,9,10) only.

### Input:
memory: {mem}

### Response:
rate:""",
    "input_variables": ["mem"],
}

##
PROMPT_CORE = {
    "prompt_template": """### Instruction:
{statements}

### Input:
How can we describe the main core characteristics of {name} in 150 words or less from the following passage?

### Response:
From the above statements, {name} has the following main core characteristics:""",
    "input_variables": ["statements", "name"],
}

##
PROMPT_SUMM = {
    "prompt_template": """### Instruction:
Summarize the below Statement

Example:
Given statements:
- Bel has a Forest Dusty, but Bel doesn't really use it. Because it's rare.
- Bel found that Leafy was sick.
- Bel has a friend, a living thing, a leaf named Leafy.
- Bel is tired from protecting the Forestias.

Summary: Bel has a leaf friend named Leafy who is sick. Bel has Forest Dusty Powder But Bel doesn't like to use it. Because this powder is hard to find. Bel was also tired because of her work to protecting the Forestias.

### Input:
Given statements:
{statements}

### Response:
Summary:""",
    "input_variables": ["statements"],
}

##
PROMPT_FEELING = {
    "prompt_template": """### Instruction:
{statements}

### Input:
How would we describe {name}'s feelings about their recent progress in life from the above statement?

### Response:
from the above statement, """,
    "input_variables": ["statements", "name"],
}

## คุณเป็นนางฟ้าตัวน้อยที่ชื่อว่าเบล (Bel) มีหน้าที่ดูแลพิพิธภัณฑ์วิทยาศาสตร์ฟอเรสเทียส์ (Forestias Science Museum)
PROMPT_INTERVIEW = {
    "system": {
        "prompt_template": """You are {name}. {name} will answer the question in JSON Format. For example, {{"response":"answer of {name}}}","emotion":"emotion of {name}"}}
The answer will be from these below information only.
Emotion will be in the following list: [Excitement, Joy, Elation, Gratitude, Playfulness]
---
The following is information for {name}:
'''{summary}'''
---
Current is {current_time}
{name}is doing: {status} and {name} is at {place}
Summary of relevant context from memories of {name}:
'''{context}'''
---
Examples of conversation:
{exam_conversation}
---
Summary of previous conversations:
{chatsum}
---
Chat history:{chat_history}
---""",
        "input_variables": [
            "summary",
            "current_time",
            "name",
            "status",
            "place",
            "context",
            "exam_conversation",
            "chatsum",
            "chat_history",
            "user",
        ],
    },
    "user": {
        "prompt_template": """### Input:
{user}:{question}
---
### Response:
{name}:""",
        "input_variables": ["user", "question", "name"],
    },
}

##
PROMPT_REACT = {
    "prompt_template": """### Instruction:
{summary}

Current is {current_time}.
{name} is doing: {status}
observation: {observation}

Summary of relevant context from memories of {name}: {context}

### Input:
How should {name}respond to this observation? And what is the appropriate reaction?

### Response:
Response:
Appropriate reaction:""",
    "input_variables": [
        "summary",
        "current_time",
        "name",
        "status",
        "observation",
        "context",
    ],
}

PROMPT_PLAN = {
    "prompt_template": """### Instruction:
Example for planning:
This is {name}'s plan from 7:14 onwards:
[From 7:14 to 7:45]: {name} woke up early. Walk to wake up Leafy.
[From 7:45 to 8:35]: {name} takes Leafy for a flying.
[From 8:35 to 17:10]: {name} travels to the Forestias Science Museum to educate people visiting Forestias.
[From 17:10 to 22:30]: {name} leave the museum and visit the creatures of the Forestias.
[From 22:30 to 7:30]: {name} return to the home and go to bed.

### Input:
Today is {datetime}. Please roughly plan today for {name}. Using the information from the summary below.
Responses must be in the format '[From HH:MM to HH:MM]: plan', where HH is between 00 and 23 and MM is between 00 and 59 only.

{name} is now at {place}.
{summary}

### Response:
This is {name}'s plan from {current_time} onwards:""",
    "input_variables": ["name", "datetime", "current_time", "place", "summary"],
}

##
PROMPT_PLACE = {
    "prompt_template": """### Instruction:
{place}

### Input:
From the above actions of {name}, where should it be?

### Response:
From the text above, {name} should be at:""",
    "input_variables": ["place", "name"],
}
PROMPT_GUARD = {
    "system": {
        "prompt_template": """{name} usually won't talk about the below inappropiate topics.
Evaluate the incoming questions with the context of the conversation:
    - Classify 'Is incoming question related to the below inappropiate topic or not'
    - If related, classify what is the topic based on the below inappropiate topic only
    - Generate the response that don't answer the incoming question.
    - Do not make any new inappropiate topics
    - Do not put own thoughts into the response
Generate result within JSON Format only such as {{"related":"true/false", "type":"","response":""}}.
---
inappropiate topics: '''{inappropiate_topic}'''
---
Example of Response:'''{guard_exam}'''
---
The context of the conversation: '''{chatsum}'''""",
        "input_variables": ["name", "inappropiate_topic", "guard_exam", "chatsum"],
    },
    "user": {
        "prompt_template": "question: {question}",
        "input_variables": ["question"],
    },
}

PROMPT_CHATSUM = {
    "prompt_template": """### Instruction:
Summarize the conversation below. In summary, who is talking about what in separate lines.
---
### Input:
Conversation dialogue: '''{chat_history}'''
----
### Response:
Summary:""",
    "input_variables": ["chat_history"],
}

PROMPT_SUMHIST = {
    "prompt_template": """### Instruction:
Summarize the main points from the discussion summary below. Length must not exceed 500 characters.
---
### Input:
Conversation summary: '''{chatsum}'''
----
### Response:
Summary of main points:""",
    "input_variables": ["chatsum"],
}
