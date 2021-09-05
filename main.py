from app.frontend.console.command_handler import CommandHandler
from app.core.config import DEBUG

if __name__ == "__main__":
    handler = CommandHandler()
    handler.set_vk_token()
    handler.get_criteria_list()
    handler.main_loop()