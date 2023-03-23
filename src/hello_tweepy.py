import os
import itertools
import tweepy
import config
import get_logger
import pandas as pd
from get_args import args
logger = get_logger.get_logger("hellotweepy")


def get_auth():

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)

    auth.set_access_token(config.access_token, config.access_token_secret)

    return auth


def init_list(filename):
    """取得済みのツイート（画像）を無視するために，取得済みのURLを初期値にセット
    """
    https_list = []
    if not os.path.isfile(filename):
        return https_list

    df = pd.read_csv(filename, index_col=0)
    ls = df.values.tolist()
    return list(itertools.chain.from_iterable(ls))


def get_https_list_of_1user_tweet(api, q, min_rt, max_rt, counts_tweets, filename):

    def have_media(tweet):
        if "media" in tweet.entities:
            return True
        return False

    def is_already_load(media, https_list):
        if media["media_url_https"] in https_list:
            return True
        return False

    logger.info("Sart Search")

    https_list = init_list(filename)
    logger.debug("init_list:{}".format(https_list))
    count_https = 0

    tweets = api.user_timeline(screen_name=q, count=counts_tweets)
    for tweet in tweets:

        if have_media(tweet):

            if tweet.retweet_count >= min_rt and tweet.retweet_count <= max_rt:
                logger.debug("[Entity]:{}".format(tweet.entities))
                logger.debug("[User]  :{}".format(tweet.user.name))
                logger.debug("[RT]    :{}".format(tweet.retweet_count))

                for media in tweet.entities["media"]:

                    if is_already_load(media, https_list):
                        continue

                    https_list.append(media["media_url_https"])
                    count_https += 1

                    if count_https % 10 == 0:
                        save_csv(https_list, filename)

    return https_list


def save_csv(data, save_file_name):

    df = pd.DataFrame(data)
    df.to_csv(save_file_name, mode="w")
    logger.debug("save csv:{}".format(df.shape))


def get_img(filename):

    df = pd.read_csv(filename, index_col=0)
    logger.debug("load csv:{}".format(df.shape))


def main():

    logger.info("start")

    auth = get_auth()

    api = tweepy.API(auth)

    https = get_https_list_of_1user_tweet(api, args.q, args.min_rt, args.max_rt, args.max_count_page, args.f)

    get_img(args.f)

    logger.info("end")


if __name__ == "__main__":

    main()
