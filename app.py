from flask import Flask, app, render_template, request, redirect
# from collections import defaultdict
from uuid import uuid4
from db import VoteDB
from model import db,Votes,Topics

app = Flask(__name__)
# db = VoteDB()


@app.route('/')
def index():
    # topics = db.get_topic_name()
    topics = list(Topics.select())
    print('---topics---')
    print(topics)
    return render_template('index.html', topics=topics)

@app.route('/addTopic',methods=['POST'])
def add_new_topic():
    topic_id = str(uuid4())
    print('new topic_id = '+ topic_id)
    name = request.form.get('name')
    print('All topics >> ')
    print(Topics.select())
    Topics.create(topic_id=topic_id,topic_name=name)
    
    return redirect('/')

@app.route('/newTopic')
def new_topic():
    return render_template('newtopic.html')

@app.route('/topic/<topic_id>')
def get_topic_page(topic_id):
    topic = list(Topics.select().where(Topics.topic_id==topic_id))
    votes = list(Votes.select().where(Votes.topic_id==topic[0]))
    print(topic)
    return render_template('topic.html',
            topic_id=topic_id,
            topic = topic[0],
            votes = votes,
            )

@app.route('/topic/<topic_id>/newChoice',methods=['POST'])
def new_choice(topic_id):
    choice_name = request.form.get('choice_name')
    Votes.create(topic_id=Topics.get_by_id(topic_id),choice_name=choice_name)
    return redirect(f'/topic/{topic_id}')

@app.route('/topic/<topic_id>/vote',methods=['POST'])
def vote_choice(topic_id):
    choice = request.form.get('choice')
    query = Votes.update(choice_count = Votes.choice_count+1).where(Votes.vote_id == choice)
    query.execute()
    return redirect(f'/topic/{topic_id}')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Topics,Votes])
    app.run('localhost',5000)