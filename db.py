from os import cpu_count
import sqlite3
from uuid import uuid4


class VoteDB:
    def __init__(self):
        self.conn = sqlite3.connect('vote.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        create_topic_query = """
        CREATE TABLE IF NOT EXISTS Topics (
        topic_id VARCHAR(50) NOT NULL PRIMARY KEY,
        topic_name VARCHAR(100) )
        """
        create_vote_query = """
        CREATE TABLE IF NOT EXISTS Votes (
        vote_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        topic_id VARCHAR(50),
        choice_name VARCHAR(100),
        choice_count INT,
        FOREIGN KEY (topic_id) REFERENCES Topics(topic_id))
        """
        self.conn.execute(create_topic_query)
        self.conn.execute(create_vote_query)
        self.conn.commit()

    def add_topic(self, topic_name):
        topic_id = str(uuid4())
        query = """
        INSERT INTO Topics (topic_id,topic_name)
        VALUES (?, ?)
        """
        self.conn.execute(query,(topic_id,topic_name))
        self.conn.commit()

    def get_topic_name(self):
        """
        [
            {
                'topic_id' : str,
                'topic_name' : str
            }
        ]
        """
        query = """
        SELECT * FROM Topics
        """

        result = self.conn.execute(query)
        ret = []
        for data in result:
            print(data)
            ret.append({
                'topic_id' : data[0],
                'topic_name' : data[1]
            })

        return ret

    def get_topic(self,topic_id):
        """
        (
            [
            (vote_id,choice_name,choice_count)
            ],
            topic_name
        )
        """
        topic_name_query = """
        SELECT topic_name FROM Topics
        WHERE Topics.topic_id = ?
        """
        topic_name_result = self.conn.execute(topic_name_query,(topic_id,)).fetchone() #เอาอันเดียว
        topic_name = topic_name_result[0]
        query = """
        SELECT vote_id, choice_name, choice_count
        FROM Votes v
        WHERE v.topic_id = ?
        """
        result = self.conn.execute(query,(topic_id,))
        ret = []
        for data in result:
            cid, cname, ccount = data
            ret.append((cid, cname, ccount))
        return ret, topic_name

    def add_choice(self, choice_name, topic_id):
        query = """
        INSERT INTO Votes (topic_id,choice_name,choice_count)
        VALUES (?,?,?)
        
        """
        self.conn.execute(query,(topic_id,choice_name,0))
        self.conn.commit()

    def vote(self,choice_id, topic_id):
        query = """
        UPDATE Votes SET choice_count = choice_count + 1
        WHERE topic_id = ? AND vote_id = ?
        """
        self.conn.execute(query,(topic_id,choice_id))
        self.conn.commit()