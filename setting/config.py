import argparse
import os
import sys

from dotenv import load_dotenv


class Config:
    def __init__(self, env: str):
        self.env = env
        self.load_environment()
        self.OPENAI_KEY = ""
        self.MONGO_USERNAME = ""
        self.MONGO_PASSWORD = ""
        self.MONGO_CLUSTER = ""
        self.DATABASE_NAME = ""
        self.set_parameters()

    def load_environment(self):
        filepath = '.env_prod' if self.env == 'prod' else '.env_dev'
        if os.path.exists(filepath):
            if self.env == 'prod':
                load_dotenv('.env_prod')
                print("Loaded environment variables from .env_prod")

            else:
                load_dotenv('.env_dev')
                print("Loaded environment variables from .env_dev")
        else:
            raise FileNotFoundError(f"Environment file '{filepath}' not found.")

    def set_parameters(self):
        if self.env == 'prod':
            self.MONGO_USERNAME = os.getenv("MONGO_USERNAME_PROD")
            self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD_PROD")
            self.MONGO_CLUSTER = os.getenv("MONGO_CLUSTER_PROD")
            self.OPENAI_KEY = os.getenv("OPENAI_KEY_PROD")
            self.DATABASE_NAME = os.getenv("DATABASE_NAME_PROD")
        else:
            self.MONGO_USERNAME = os.getenv("MONGO_USERNAME_DEV")
            self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD_DEV")
            self.MONGO_CLUSTER = os.getenv("MONGO_CLUSTER_DEV")
            self.OPENAI_KEY = os.getenv("OPENAI_KEY_DEV")
            self.DATABASE_NAME = os.getenv("DATABASE_NAME_DEV")

        if self.MONGO_USERNAME is None or self.MONGO_PASSWORD is None or self.MONGO_CLUSTER is None \
                or self.OPENAI_KEY is None:
            raise EnvironmentError(f"Environment variable  not found")


try:
    parser = argparse.ArgumentParser(description="Configuration")
    parser.add_argument('--env', default='dev', choices=['dev', 'prod'], help="Specify the environment (dev or prod)")
    args = parser.parse_args()
    config = Config(args.env)

except FileNotFoundError as e:
    print(e)
    exit(1)

except EnvironmentError as e:
    print(e)
    exit(1)