import discord
from discord.ext import commands

from PIL import ImageDraw, ImageFont, Image
import io, re, textwrap

async def setup(bot) -> None:
    await bot.add_cog(ImageCog(bot))

PATTERNS = {
        r'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        r'[đ]': 'd',
        r'[èéẻẽẹêềếểễệ]': 'e',
        r'[ìíỉĩị]': 'i',
        r'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        r'[ùúủũụưừứửữự]': 'u',
        r'[ỳýỷỹỵ]': 'y'
    }
def no_accent_vietnamese(s):
        for pattern, replace in PATTERNS.items():
            s = re.sub(pattern, replace, s)
            s = re.sub(pattern.upper(), replace.upper(), s)
        return s

class ImageCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(10, 60, commands.BucketType.user)
    async def deptrai(self, ctx: commands.Context):
        """Tạo giấy chứng nhận cho bạn =)"""
        await ctx.typing()
        
        img = Image.open('./assets/images/chungnhan.png')
        msg = no_accent_vietnamese(ctx.author.display_name)
        para = list(textwrap.wrap(msg, width = 35)[:6])

        MAX_W, MAX_H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/fonts/Happy Swirly.ttf', 150, encoding='utf-8')

        current_h, current_x = 619, 180
        pad = 50
        for line in para:
            w = draw.textlength(line, font = font)
            draw.text((current_x, current_h), line, fill = 'pink', font = font)
        del draw

        img_url = ctx.author.display_avatar.url
        avatar_data = await ctx.author.display_avatar.read()
        avatar = Image.open(io.BytesIO(avatar_data)).convert("RGBA")
        avatar = avatar.resize((500, 500))

        avatar_x = 1550 - avatar.width // 2
        avatar_y = 558 - avatar.height // 2
        img.paste(avatar, (avatar_x, avatar_y), avatar)


        buffer = io.BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)

        await ctx.reply(file=discord.File(fp=buffer, filename = 'image.png'))
    