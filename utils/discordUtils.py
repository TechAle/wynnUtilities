from discord_webhook import DiscordWebhook, DiscordEmbed


def sendMessageWebhook(title, description, url, color='F70D1A'):
    webhook = DiscordWebhook(url=url, username="WynnStalker",
                             avatar_url="https://cdn.discordapp.com/app-icons/973942027563712632/3043f3b6d99b2b737ef7216e8c14c106.png?size=256")

    embed = DiscordEmbed(
        title=title, description=description, color=color, rate_limit_retry=True
    )

    webhook.add_embed(embed)
    webhook.execute()

