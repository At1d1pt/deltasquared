from .cog import Moderation

def setup(bot):
    bot.add_cog(Moderation(bot))