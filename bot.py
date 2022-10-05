import json
import os
import requests
import argparse
import sys
from faker import Faker
from random import randint, choice


class Bot:
    _user_data = []
    created_posts_id = []

    def __init__(self, users_amount, max_posts_amount, max_likes_amount):
        self.users_amount = users_amount
        self.max_posts_amount = max_posts_amount
        self.max_likes_amount = max_likes_amount
        self.faker = Faker()

    def run(self):
        self._create_users_data()
        self._sign_up_users()
        self._create_posts()
        self._like_posts()

    def _create_users_data(self):
        for _ in range(self.users_amount):
            user = {
                "username": self.faker.first_name() + self.faker.last_name(),
                "email": self.faker.email(),
                "password": self.faker.pystr(min_chars=15, max_chars=25),
            }
            self._user_data.append(user)

    def _sign_up_users(self):
        for user in self._user_data:
            request = requests.post("http://127.0.0.1:8000/api/v1/sign-up/", data=user)
            user["id"] = request.json()["id"]

    def _create_posts(self):
        url = "http://127.0.0.1:8000/api/v1/posts/"
        posts_per_user = randint(0, self.max_posts_amount)
        for user in self._user_data:
            headers = self.get_headers_with_jwt(user["username"], user["password"])
            for _ in range(posts_per_user):
                request = requests.post(
                    url=url,
                    data={
                        "user": user["id"],
                        "body": self.faker.paragraph(6),
                        "title": self.faker.sentence(),
                    },
                    headers=headers,
                )
                self.created_posts_id.append(request.json()["id"])

    def _like_posts(self):
        url = "http://127.0.0.1:8000/api/v1/likes/"
        likes_per_user = randint(0, self.max_likes_amount)
        for user in self._user_data:
            headers = self.get_headers_with_jwt(user["username"], user["password"])
            for j in range(likes_per_user):
                requests.post(
                    url=url,
                    data={"user": user["id"], "post": {choice(self.created_posts_id)}},
                    headers=headers,
                )

    @staticmethod
    def get_headers_with_jwt(username, password):
        request = requests.post(
            "http://127.0.0.1:8000/api/token/",
            data={"username": username, "password": password},
        )
        jwt = request.json()
        headers = {
            "Authorization": f"Bearer {jwt['access']}",
        }
        return headers

    @classmethod
    def bot_from_config(cls, file_path):
        with open(file_path, "r") as config_file:
            config = json.load(config_file)

        users_amount = int(config["NUMBER_OF_USERS"])
        max_posts_amount = int(config["MAX_POST_PER_USER"])
        max_likes_amount = int(config["MAX_LIKE_PER_USER"])
        bot = cls(
            users_amount=users_amount,
            max_posts_amount=max_posts_amount,
            max_likes_amount=max_likes_amount,
        )
        return bot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users_amount", type=int)
    parser.add_argument("--max_posts_amount", type=int)
    parser.add_argument("--max_likes_amount", type=int)
    if len(sys.argv) == 1:
        bot = Bot.bot_from_config(os.path.join("bot_config.json"))
        bot.run()
    else:
        args = parser.parse_args()
        bot = Bot(args.users_amount, args.max_posts_amount, args.max_likes_amount)
        bot.run()
