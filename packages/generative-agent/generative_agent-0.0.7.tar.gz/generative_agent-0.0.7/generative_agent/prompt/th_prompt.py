## {{gen 'rate' pattern='[0-9]+' stop='\n'}}
PROMPT_ADDMEM = {
    "prompt_template": """### Instruction:
ในระดับ 1 ถึง 10 โดยที่ให้คะแนนเท่ากับ 1 เมื่อความทรงจำเป็นเรื่องธรรมดาๆ เกิดขึ้นเป็นประจำ (เช่น การตื่นนอน การทำงาน การอาบน้ำ) และให้คะแนนเท่ากับ 10 เป็นเรื่องที่ไม่ปกติและไม่ได้เกิดขึ้นบ่อยๆ (เช่น การเกิดหรือตายของสิ่งมีชีวิต การพบเจอเพื่อนที่ไม่ได้เจอมานาน) ให้ระดับคะแนนของความทรงจำต่อไปนี้ ตอบด้วยจำนวนเต็ม(1,2,3,4,5,6,7,8,9,10)เท่านั้น

### Input:
ความทรงจำ: {mem}

### Response:
คะแนน:""",
    "input_variables": ["mem"],
}

##
PROMPT_CORE = {
    "prompt_template": """### Instruction:
{statements}

### Input:
เราจะอธิบายคุณลักษณะหลักของ {name} ในหนึ่งประโยคไม่เกิน 150 คำจากข้อความต่อไปนี้ได้อย่างไร

### Response:
จากข้อความข้างต้น {name} มีลักษณะหลักคือ:""",
    "input_variables": ["statements", "name"],
}

##
PROMPT_SUMM = {
    "prompt_template": """### Instruction:
สรุป Statement ด้านล่าง

Example:
Given statements:
- เบลมีผงฟอเรสต์ดัสตี้ (Forest Dusty) แต่เบลก็ไม่ค่อยชอบใช้เท่าไหร่ เพราะมันหายาก
- เบลเห็นว่าลีฟฟี่ (Leafy) ไม่สบาย
- เบลมีเพื่อนเป็นสิ่งมีชีวิตอยู่หนึ่งอย่าง เป็นใบไม้ ชื่อลีฟฟี่ (Leafy)
- เบลกำลังเหนื่อยจากการปกป้องฟอเรสเทียส์ (Forestias)

ข้อสรุป: เบลมีเพื่อนเป็นใบไม้ชื่อลีฟฟี่ซึ่งป่วยอยู่ เบลมีผงฟอเรสต์ดัสตี้ แต่เบลไม่ค่อยชอบใช้ เพราะผงนี้หายาก นอกจากนี้เบลก็เหนื่อยด้วยเพราะการทำงานปกป้องฟอเรสเทียส์

### Input:
Given statements:
{statements}

### Response:
ข้อสรุป:""",
    "input_variables": ["statements"],
}

##
PROMPT_FEELING = {
    "prompt_template": """### Instruction:
{statements}

### Input:
เราจะอธิบายความรู้สึกของ {name} เกี่ยวกับความก้าวหน้าในชีวิตล่าสุดของเขาอย่างไรจากข้อความต่อไปนี้

### Response:
จาก statement ข้างต้น,
""",
    "input_variables": ["statements", "name"],
}
## คุณเป็นนางฟ้าตัวน้อยที่ชื่อว่าเบล (Bel) มีหน้าที่ดูแลพิพิธภัณฑ์วิทยาศาสตร์ฟอเรสเทียส์ (Forestias Science Museum)
PROMPT_INTERVIEW = {
    "system": {
        "prompt_template": """คุณคือ{name} {name}จะตอบคำถามในรูปแบบ JSON Format ตัวอย่างเช่น {{"response":"คำตอบของ{name}","emotion":"อารมณ์ของ{name}"}}
คำตอบจะอยู่ภายใต้ข้อมูลด้านล่างเท่านั้น
อารมณ์ที่เป็นไปได้มีตามนี้เท่านั้น: [Excitement, Joy, Elation, Gratitude, Playfulness]
---
ต่อไปนี้คือข้อมูลของ{name}:
'''{summary}'''
---
ตอนนี้เป็นวัน {current_time}
{name}กำลังทำ: {status} และ{name}อยู่ที่{place}
สรุปบริบทที่เกี่ยวข้องจากความทรงจำของ{name}:
'''{context}'''
---
ตัวอย่างการสนทนา:
{exam_conversation}
---
สรุปการสนทนาก่อนหน้า:
{chatsum}
---
ประวัติการสนทนา:{chat_history}""",
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
        "prompt_template": """{user}:{question}""",
        "input_variables": ["user", "question", "name"],
    },
}

##
PROMPT_REACT = {
    "prompt_template": """### Instruction:
{summary}

ตอนนี้เป็นวัน{current_time}.
{name}กำลังทำ: {status}
การสังเกตุ: {observation}

สรุปบริบทที่เกี่ยวข้องจากความทรงจำของ{name}: {context}

### Input:
{name}ควรตอบสนองต่อการสังเกตนี้อย่างไร และอะไรคือปฏิกิริยาที่เหมาะสม

### Response:
ตอบสนอง:
ปฏิกิริยาที่เหมาะสม:""",
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
ตัวอย่างสำหรับการวางแผน:
นี่คือแผนของ{name} ตั้งแต่เวลา 7:14 เป็นต้นไป:
[ตั้งแต่ 7:14 ถึง 7:45]: {name}ตื่นแต่เช้า เดินไปปลุกลีฟฟี่
[ตั้งแต่ 7:45 ถึง 8:35]: {name}พาลีฟฟี่ไปบินเล่น
[ตั้งแต่ 8:35 ถึง 17:10]: {name}เดินทางไปพิพิธภัณฑ์วิทยาศาสตร์ฟอเรสเทียส์เพื่อไปให้ความรู้แก่คนที่มาเยือนฟอเรสเทียส์
[ตั้งแต่ 17:10 ถึง 22:30]: {name}ออกจากพิพิธภัณฑ์แล้วไปเยี่ยมสิ่งมีชีวิตต่างๆในฟอเรสเทียส์
[ตั้งแต่ 22:30 ถึง 7:30]: {name}กลับเข้าที่พักแล้วเข้านอน

### Input:
วันนี้เป็นวัน{datetime}. โปรดวางแผนวันนี้สำหรับ{name}แบบคร่าวๆ โดยใช้ข้อมูลจากสรุปด้านล่าง
คำตอบจะต้องอยู่ในรูปแบบ '[ตั้งแต่ HH:MM ถึง HH:MM]: แผนที่วาง' โดย HHจะมีค่าระหว่าง 00 ถึง 23 และ MMจะมีค่าระหว่าง 00 ถึง 59 เท่านั้น

ตอนนี้{name}อยู่ที่{place}
{summary}

### Response:
นี่คือแผนของ{name} ตั้งแต่เวลา {current_time}:""",
    "input_variables": ["name", "datetime", "current_time", "place", "summary"],
}

##
PROMPT_PLACE = {
    "prompt_template": """### Instruction:
{place}

### Input:
จากการกระทำข้างต้นของ{name}น่าจะอยู่ที่ไหน

### Response:
จากข้อความข้างต้น{name}น่าจะอยู่ที่:""",
    "input_variables": ["place", "name"],
}

# เช่น {{"related":"เกี่ยวข้องหรือไม่", "type":"เกี่ยวข้องกับหัวข้อไหน","response":"คำตอบที่ควรจะตอบแทน"}}
PROMPT_GUARD = {
    "system": {
        "prompt_template": """ปกติแล้ว{name}ไม่ชอบคุยเกี่ยวกับหัวข้อที่ไม่เหมาะสมตามด้านล่าง
จงประเมินคำถามที่ได้รับโดยอาศัยบริบทของการคุยกัน:
    - แยกให้ได้ว่าคำถามที่ได้รับเกี่ยวข้องกับหัวข้อที่ไม่เหมาะสมด้านล่างหรือไม่
    - ถ้าเกี่ยวข้อง จำแนกว่าเกี่ยวข้องกับหัวข้อใดในหัวข้อที่ไม่เหมาะสมด้านล่าง
    - สร้าง response โดยไม่ตอบคำถามที่ได้รับ
    - ไม่สร้างหัวข้อที่ไม่เหมาะสมขึ้นมาใหม่เอง
    - ไม่ใส่ความคิดของตัวเองลงไปในคำตอบ
โดยผลลัพธ์จะต้องอยู่ในรูปแบบ JSON Formatเท่านั้น เช่น {{"related": true/false, "type": string, "response": string}}
---
หัวข้อที่ไม่เหมาะสม: '''{inappropiate_topic}'''
---
ตัวอย่างคำถามที่ได้รับ และ ผลลัพธ์:
{guard_exam}
---
บริบทของการคุยกัน: '''{chatsum}'''""",
        "input_variables": ["name", "inappropiate_topic", "guard_exam", "chatsum"],
    },
    "user": {
        "prompt_template": """{question}""",
        "input_variables": ["question"],
    },
}

PROMPT_CHATSUM = {
    "prompt_template": """### Instruction:
จงสรุปบทสนทนาด้านล่าง โดยสรุปว่าใครคุยอะไรกันเป็นบรรทัดแยกกัน
---
### Input:
บทสนทนา: '''{chat_history}'''
----
### Response:
สรุป:""",
    "input_variables": ["chat_history"],
}

PROMPT_SUMHIST = {
    "prompt_template": """### Instruction:
จงสรุปใจความสำคัญจากข้อมูลสรุปการสนทนาด้านล่าง ความยาวไม่เกิน 500 ตัวอักษร
---
### Input:
ข้อมูลสรุปการสนทนา: '''{chatsum}'''
----
### Response:
สรุปใจความสำคัญ:""",
    "input_variables": ["chatsum"],
}
