import datetime
from discord_webhooks import DiscordWebhooks
import json

def app_ready():
    webhook = DiscordWebhooks("https://discordapp.com/api/webhooks/674845969871011840/3L76-2iyIfY5D84sg4aTsXUyWCiofE_jEngesU_fItRw4BXH1W8T-v9I12j4FdCkqd9G")
    webhook.set_content(content="<@&674846334322212865>", title="참치봇 서비스를 복구 했습니다!", description="이제 참치봇의 기능들을 다시 사용하실 수 있습니다", color=0x5b50fa, timestamp=str(datetime.datetime.utcnow().isoformat()))
    webhook.set_author(name='참치봇 SERVER', icon_url="https://cdn.discordapp.com/attachments/626434906829881364/653550951092846612/fe545f435ed0fbfc.png")
    webhook.set_footer(text="버그 발견 / 문의는 @COiN#7338로 DM를 남겨주세요")
    webhook.send()
    return