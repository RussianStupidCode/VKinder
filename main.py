from app.frontend.vk_bot.bot import VkBot
from app.core.config import DEBUG

token = '1fe6f70f19c0912143b4fd86cbe730c33253ab07749b92c5422ffaf4f3184d174868cfe40c0d6df8254b8'
if __name__ == "__main__":
    bot = VkBot()
    bot.set_group_token()
    bot.listen()