import os

from dotenv import load_dotenv

load_dotenv()


class Credentials:

    @classmethod
    def openai_api_key(cls) -> str:
        return os.getenv("OPENAI_API_KEY")

    @classmethod
    def retell_api_key(cls) -> str:
        return os.getenv("RETELL_API_KEY")

    @classmethod
    def retell_agent_id(cls) -> str:
        return os.getenv('RETELL_AGENT_ID')

    @classmethod
    def calendly_api_key(cls) -> str:
        return os.getenv("CALENDLY_API_KEY")

    @classmethod
    def google_token(cls) -> str:
        return os.getenv("GOOGLE_TOKEN")
    

class EnvVariables:
    @classmethod
    def chat_model(cls) -> str:
        return os.getenv("CHAT_MODEL", "gpt-4o")

    @classmethod
    def database_url(cls) -> str:
        return os.getenv("DATABASE_URL", "postgresql://myuser:mysecretpassword@localhost:5432/food-beverage-db")
