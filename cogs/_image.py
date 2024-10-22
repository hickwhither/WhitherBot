import discord
from discord.ext import commands

from PIL import ImageDraw, ImageFont, Image
import io, re, textwrap

from options import HAVE_PILLOW

async def setup(bot) -> None:
    if not HAVE_PILLOW: return
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
    async def deptrai(self, ctx, *, msg: str):
        """Tạo giấy chứng nhận cho bạn =)"""
        await ctx.typing()
        msg.split()
        
        img = Image.open('./assets/images/deptraibg.png')
        msg = no_accent_vietnamese(msg)
        para = list(textwrap.wrap(msg, width = 35)[:6])

        MAX_W, MAX_H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/fonts/HappySwirly-KVB7l.ttf', 60, encoding='utf-8')

        current_h, pad = 420, 50
        for line in para:
            w = draw.textlength(line, font = font)
            draw.text(((MAX_W - w) / 2, current_h), line, fill = 'black', font = font)
        del draw


        # ko hiểu thì nhớ 1 cách máy móc cx đc :L dù sau cx chỉ có cách này
        buffer = io.BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)

        await ctx.reply(file=discord.File(fp=buffer, filename = 'image.png'))
    