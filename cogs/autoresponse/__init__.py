from .cog import AutoResponse

def setup(bot):
    bot.add_cog(AutoResponse(bot))