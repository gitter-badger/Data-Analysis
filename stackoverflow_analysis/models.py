from mongoengine import *

connect("stack_overflow")

class Question(Document):
    question_id = IntField(unique=True)
    title = StringField(max_length = 300)
    link = StringField(max_length = 300)
    creation_date = DateTimeField()
    tag = StringField(max_length=30)

class Answer(Document):
    question = ReferenceField(Question, reverse_delete_rule=CASCADE, unique=True)
    answers = ListField(DictField())
