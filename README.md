# 1. Social network API


### Description: 
Social network - API for registering users, creating posts, and giving likes. The user can also check the analytics, aggregated by day, on how many likes were made and the time of the user's last activity


## Usage:


### Run app

Clone the project and then go to the root directory and create .env file like in .env.example (You might want to change the credentials)

Now you can run app with the command below:

```commandline
make up
```
then apply migrations:
```commandline
make migrate
```
You can check the list of endpoints in postman_collection.json


# 2. Bot

### Description: 
The bot reads the configuration file and performs social network activity (registers users, creates a random number of posts and randomly likes them)

## Usage:

For running bot you need requests and Faker to be installed:

```commandline
pip install requests Faker
```

After installation is complete, you can run bot from cli like below:

```commandline
python bot.py
```


In this case bot running using bot_config.json, you can change the parameters of this file manually.

Or you can run bot with options:

```commandline
python bot.py --users_amount 10 --max_posts_amount 20 --max_likes_amount 15
```
