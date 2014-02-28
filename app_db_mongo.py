from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from sendgrid import Mail, SendGridClient
import os

sg = SendGridClient(os.getenv('SG_USER'), os.getenv('SG_PWD'))
tweets = MongoClient().tweets.tweets
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def view_tweets():
  return render_template('index.html', tweets=list(tweets.find()))

@app.route('/tweet', methods=['POST'])
def create_tweet():
  return jsonify({'_id': str(tweets.insert({'text': request.form['tweet']}))})

@app.route('/tweet', methods=['GET'])
def all_tweets():
  return jsonify({'tweets': list(tweets.find())})

@app.route('/tweet/<string:id>', methods=['DELETE', 'GET', 'PUT'])
def single_tweet(id):
  id = ObjectId(id)
  tweet = request.form['tweet']
  if request.method == 'DELETE':
    return jsonify(tweets.remove({'_id': id}))
  elif request.method == 'PUT':
    return jsonify(tweets.update({'_id': id}, {'$set': {'text': tweet}}))
  else:
    return jsonify(tweets.find_one({'_id': id}))

@app.route('/emailhook', methods=['POST'])
def create_tweet_email():
  return jsonify({'_id': str(tweets.insert({'text': request.form['subject']}))})

@app.route('/tweet/email/<string:email>', methods=['GET'])
def email_twets(email):
  mail = Mail(from_email='yamil@sendgrid.com',
    to=email, subject='Tweets', text=str(list(tweets.find())))
  sg.send(mail)
  return jsonify({})

if __name__ == '__main__':
  app.run()
