import os
import enum
import time
import queue
import threading
from enum import Enum
from datetime import datetime, timedelta
import hashlib

def generate_unique_id(original_string: str):
    unique_id = hashlib.sha256(original_string.encode()).hexdigest()
    return unique_id[:16]

def text_from_inapp_list(list_of_inapp):
    text = "- "
    for i in range(len(list_of_inapp)):
        if i == 0:
            text += list_of_inapp[i]
        else:
            text += "\n- " + list_of_inapp[i]
    return text


def text_chat_hist(chat_history):
    text = ""
    for i in range(len(chat_history)):
        if i == 0:
            text += chat_history[i]
        else:
            text += "\n" + chat_history[i]
    return text


def get_text_from_docs(list_docs, include_time=False):
    texts = ""
    for i, doc in enumerate(list_docs):
        if include_time:
            time_t = doc.metadata["created_at"].strftime("%A %B %d, %Y, %H:%M") + ": "
        else:
            time_t = ""
        if i == 0:
            texts += "- " + time_t + doc.page_content
        else:
            texts += "\n- " + time_t + doc.page_content
    return texts


def get_thai_datetime():
    current_datetime = datetime.now().strftime("%Aที่ %d %B %Y เวลา %H:%M")
    thai_current_datetime = current_datetime
    dates = {
        "Sunday": "อาทิตย์",
        "Monday": "จันทร์",
        "Tuesday": "อังคาร",
        "Wednesday": "พุธ",
        "Thursday": "พฤหัสบดี",
        "Friday": "ศุกร์",
        "Saturday": "เสาร์",
    }
    months = {
        "January": "มกราคม",
        "February": "กุมภาพันธ์",
        "March": "มีนาคม",
        "April": "เมษายน",
        "May": "พฤษภาคม",
        "June": "มิถุนายน",
        "July": "กรกฎาคม",
        "August": "สิงหาคม",
        "September": "กันยายน",
        "October": "ตุลาคม",
        "November": "พฤศจิกายน",
        "December": "ธันวาคม",
    }

    # replace date
    for date in list(dates.keys()):
        if date in thai_current_datetime:
            thai_current_datetime = thai_current_datetime.replace(date, dates[date])
    # replace month
    for month in list(months.keys()):
        if month in thai_current_datetime:
            thai_current_datetime = thai_current_datetime.replace(month, months[month])
    # update year
    split_date = thai_current_datetime.split(" ")
    split_date[3] = str(int(split_date[3]) + 543)
    thai_current_datetime = " ".join(split_date)

    return thai_current_datetime


class Mem_Type(Enum):
    BEHAVIOR = "BEHAVIOR"
    KNOWLEDGE = "KNOWLEDGE"


class Vector_Database_Type(Enum):
    PINECONE = "PINECONE"
    CHROMA = "Chroma"


# Define the RateLimiter class with request queue and backoff mechanism
class RateLimiter:
    def __init__(self, rate_limit, time_window):
        self.rate_limit = rate_limit
        self.total_docs = 0
        self.time_window = time_window
        self.lock = threading.Lock()
        self.calls = []
        self.last_checked = datetime.now()
        self.request_queue = queue.Queue()
        self.queue_processing_thread = threading.Thread(
            target=self.process_queue_continuously
        )
        self.queue_processing_thread.start()

    def within_limit(self):
        with self.lock:
            current_time = datetime.now()
            self.calls = [
                call for call in self.calls if call > current_time - self.time_window
            ]
            if len(self.calls) < self.rate_limit:
                self.calls.append(current_time)
                return True
            else:
                return False

    def add_to_queue(self, request):
        self.request_queue.put(request)

    def process_queue(self):
        while not self.request_queue.empty():
            request = self.request_queue.get()
            if self.within_limit():
                request["function"](**request["kwargs"])
                # self.total_docs -= 1
            else:
                self.add_to_queue(request)
                # self.total_docs += 1
                time.sleep(1)  # Adjust the sleep time as needed

    def process_queue_continuously(self):
        while True:
            self.process_queue()
            time.sleep(3)  # Adjust the sleep time as needed
