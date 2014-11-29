import requests
import sys
import time
from mongoengine import *

connect("stack_overflow")

QUESTION_URL =
"https://api.stackexchange.com/2.2/questions?key=%spage=%s&pagesize=100&fromdate=%s&todate=%s&order=desc&sort=creation&tagged=%s&site=stackoverflow"

ANSWER_URL =
"https://api.stackexchange.com/2.2/questions/%s/answers?order=asc&sort=activity&site=stackoverflow&key=%s"

def get_epoch_time_diff(start_date, num_of_days_to_negate):
    '''
    Convert start date and end_date to epoch and return it
    '''
    pass

class Question(Document):
    question_id = IntField(unique=True)
    title = StringField(max_length = 50)
    link = StringField(max_length = 100)
    creation_date = DateTimeField()
    tag = StringField(max_length=30)

class Answer(Document):
    question = ReferenceField(Question, reverse_delete_rule=CASCADE)
    answers = ListField(DictField())

def get_command_arg():
    pass

class API(object):
    def __init__(self, tag, start_date, end_date, key):
        self.tag = tag
        self.start_date = start_date
        self.end_date = end_date
        self.key = key
    
    def insert_to_mongo(self, question_dict, answer_dict_list=None):
        '''
        Insert to mongo
        '''
        # First insert into question collection
        question = Question()
        question.question_id = question_dict.get("question_id")
        question.title = question_dict.get("title")
        question.link = question_dict.get("link")
        creation_date = question_dict.get('creation_date') 
        question.tag = self.tag
        try:
            question.save()
        except NotUniqueError:
            '''
            If duplicate question found ignore it
            '''
            return False

        # Insert to answer info
        if answer_dict_list:
            answer = Answer(question = question)
            answer.answers = answer_dict_list
            answer.save()
        return True

    def process_question_data(self, page):
        '''
        Call this method recursively until it gets all pages
        '''
        question_url = QUESTION_URL%(self.key, page, self.start_date, self.end_date, self.tag)
        handle = requests.get(question_url)
        json_data = handle.json()

        record_list = json_data["items"]
        for record in record_list:
            question_dict = {}
            answer_dict = None
            question_dict['question_id'] = record["question_id"]
            question_dict['title'] = record["title"]
            question_dict['link'] = record["link"]
            question_dict['creation_date'] = record['creation_date']
            answer_count = record['answer_count']
            if (answer_count > 0):
                # If answer found then process_answer data
                time.sleep(1)
                answer_dict_list = self.process_answer_data(question_dict["question_id"])
            self.insert_to_mongo(question_dict, answer_dict)

        # If found more page found then call this method
        if (json_data['has_more']):
            time.sleep(2)
            page += 1
            self.process_question_data(page)
        return

    def process_answer_data(self, question_id):
        '''
        '''
        answer_url = ANSWER_URL%(question_id, self.key)
        handle = requests.get(answer_url)
        json_data = handle.json()
        records = json_data['items']
        answer_dict_list = []
        for record in records:
            answer_dict = {}
            answer_dict['creation_date'] = record['creation_date']
            answer_dict['answer_id'] = record['answer_id']
            answer_dict['is_accepted'] = record['is_accepted']
            answer_dict_list.append(answer_dict)
        return answer_dict_list

    def start(self):
        self.process_question_data(1)
        return
    def epilogue(self):
        pass

