from peewee import *

db = SqliteDatabase('vote_orm.db')

class BaseModel(Model):
    class Meta:
        database = db

class Topics(BaseModel):
    topic_id = CharField(max_length=100, null=False, primary_key=True)
    topic_name = TextField()

class Votes(BaseModel):
    vote_id = AutoField(primary_key=True,null=False)
    topic_id = ForeignKeyField(Topics, backref='topic')
    choice_name = TextField()
    choice_count = IntegerField(default=0)

    