import tweepy
import boke
import random
import redis
import os


def make_api():
    crient = os.environ["ROBOT_KUN_CRIENT"]
    crient_secret = os.environ["ROBOT_KUN_CRIENT_SECRET"]
    access_token = os.environ["ROBOT_KUN_ACCESS_TOKEN"]
    access_secret = os.environ["ROBOT_KUN_ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(crient, crient_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def main():
    r = redis.Redis()
    api = make_api()
    mentions = api.mentions_timeline(count=1)
    if len(mentions) > 0:
        mention = mentions[0]
        mention_id = mention.id
        mention_text = mention.text.replace('@robot_kun', '')
        mention_user = mention.user.screen_name

        for i in range(10):
            answers = boke.question(mention_text, simple=True, return_boke=True)
            if len(answers):
                break

        if len(answers):
            random.shuffle(answers)
            selected_answer = answers.pop()
        else:
            selected_answer = "ごめん、それは意味がわからない"

        selected_answer = (
            "【答え】" + selected_answer + "\n\n" +
            "【問題】" + mention_text + "by @" + mention_user )

        if not r.get('already_reply_' + str(mention_id)):
            api.update_status(selected_answer, mention_id)
            r.set('already_reply_' + str(mention_id), 'true')
            print(selected_answer)


if __name__ == "__main__":
    main()
