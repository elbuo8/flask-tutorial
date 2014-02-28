from flask import Flask, request, jsonify
from random import randint
from sendgrid import Mail, SendGridClient

app = Flask(__name__)
app.debug = True

tweets = []

@app.route('/tweet', methods=['POST', 'GET'])
def handle_create():
  if request.method == 'POST':
    new_tweet = {'id': randint(), 'text': request.form['tweet']}
    tweets.append(newtweet)
    return jsonify(newtweet)
  else:
    return jsonify({"tweets": tweets})


@app.route('/tweet/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def handle_single_tweet(id):
  for tweet in tweets:
    if tweet['id'] == id:
      if request.method == 'GET':
        return jsonify(tweet)
      elif request.method == 'PUT':
        tweet['text'] = request.form('text')
        return jsonify(tweet)
      else:
        removed = tweet
        tweets.remove(tweet)
        return jsonify(removed)
  return jsonify({"error": "Not found"})

@app.route('/tweet/emailhook', methods=['POST'])
def email_tweet():
  new_tweet = {'id': randint(), 'text': request.form['subject']}
  tweets.append(new_tweet)
  return jsonify(new_tweet)

if __name__ == '__main__':
  app.run()
