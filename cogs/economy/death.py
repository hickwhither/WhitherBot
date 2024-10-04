import discord
from discord import Embed, Colour
from discord.ext import commands

from models.economy.user import UserModel

import asyncio
import random

from . import credit_icon, bt

color_fired = ['#360808', '#7F0808', '#B30808', '#CA0808', '#FF0808', '#F77B7A']

COMMENT_STOP = [
    [
        "Bạn đã dừng lại mà không cần bắn một viên nào, thật là thận trọng!",
        "Không bắn mà đã dừng, có vẻ bạn muốn an toàn tuyệt đối!",
        "Chưa bắn đã dừng, bạn là người biết cách tránh rủi ro!",
        "Bạn quá an toàn khi dừng lại mà chưa bắn viên nào!",
        "Không thử vận may mà đã dừng, có lẽ bạn biết điều gì đó!",
        "Một quyết định dừng lại đầy cẩn trọng trước khi bắn!",
        "Dừng mà chưa bắn viên nào, bạn chắc chắn là người cẩn thận!",
        "Chưa thử mà đã dừng, bạn không thích mạo hiểm nhỉ!",
        "Không dám thử vận may hôm nay sao? Bạn dừng lại mà chưa bắn!",
        "Dừng trước khi bắn một viên, an toàn nhưng bỏ lỡ thử thách!",
    ],
    [
        "Bạn đã dừng lại ở viên đầu tiên, khá an toàn!",
        "Sau viên đầu tiên, bạn đã quyết định dừng lại, một bước đi thông minh!",
        "Dừng ở viên thứ nhất, không quá mạo hiểm nhưng cũng không nhút nhát!",
        "Viên đầu tiên không có đạn, bạn thật may mắn khi dừng lại!",
        "Dừng lại ở viên thứ nhất là một quyết định khôn ngoan!",
        "Bạn đã rất cẩn trọng khi dừng lại ở viên đầu tiên!",
        "Một lựa chọn an toàn khi không thử vận may với viên đầu tiên!",
        "Dừng ở viên đầu tiên, bạn chọn an toàn hơn mạo hiểm!",
        "Không cần thử, bạn đã dừng lại ở viên đầu tiên!",
        "Dừng lại sau viên đầu tiên, hãy xem điều gì xảy ra tiếp theo!"
    ],
    [
        "Dừng lại ở viên thứ hai, khá thận trọng!",
        "Viên thứ hai đã không có đạn, bạn thật may mắn khi dừng lại!",
        "Một quyết định thông minh khi dừng lại ở viên thứ hai!",
        "Bạn đã không tiếp tục và dừng lại ở viên thứ hai, tốt lắm!",
        "Sau viên thứ hai, bạn đã quyết định an toàn hơn là tiếp tục!",
        "Dừng lại sau viên thứ hai là một lựa chọn thông minh!",
        "Rất khôn ngoan khi dừng lại ở viên thứ hai, bạn đã thoát hiểm!",
        "Viên thứ hai an toàn, bạn đã dừng lại đúng lúc!",
        "Dừng lại ở viên thứ hai, bạn đã có một quyết định đúng đắn!",
        "Viên thứ hai an toàn, bạn đã có lựa chọn sáng suốt khi dừng lại!"
    ],
    [
        "Dừng lại ở viên thứ ba, một quyết định tốt!",
        "Viên thứ ba không có đạn, bạn đã dừng lại đúng lúc!",
        "Một lựa chọn sáng suốt khi dừng lại ở viên thứ ba!",
        "Bạn đã có một bước đi an toàn khi dừng lại ở viên thứ ba!",
        "Dừng lại ở viên thứ ba, và bạn vẫn còn an toàn!",
        "Viên thứ ba an toàn, dừng lại là lựa chọn khôn ngoan!",
        "Thật tốt khi dừng lại ở viên thứ ba, bạn đã tránh được rủi ro!",
        "Dừng lại ở viên thứ ba, một quyết định thông minh!",
        "Sau viên thứ ba, bạn đã chọn dừng lại, rất khôn ngoan!",
        "Viên thứ ba an toàn, bạn đã quyết định dừng lại đúng lúc!"
    ],
    [
        "Dừng lại ở viên thứ tư, một quyết định thông minh!",
        "Viên thứ tư an toàn, bạn đã dừng lại rất đúng lúc!",
        "Bạn đã dừng lại ở viên thứ tư, rất khôn ngoan!",
        "Sau viên thứ tư, bạn chọn dừng lại, thật sáng suốt!",
        "Dừng lại ở viên thứ tư, bạn đã thoát hiểm!",
        "Viên thứ tư an toàn, bạn đã quyết định dừng lại tốt!",
        "Dừng lại ở viên thứ tư, bạn đã lựa chọn khôn ngoan!",
        "Một quyết định an toàn khi dừng lại ở viên thứ tư!",
        "Viên thứ tư không có đạn, dừng lại là lựa chọn thông minh!",
        "Dừng lại sau viên thứ tư, một quyết định sáng suốt!"
    ],
    [
        "Bạn đã bắn hết 5 viên, thật dũng cảm và táo bạo!",
        "Một quyết định mạo hiểm khi bắn hết 5 viên, bạn thật tuyệt vời!",
        "Bắn hết 5 viên, bạn đã thể hiện tinh thần quả cảm!",
        "Chúc mừng bạn đã dám bắn hết 5 viên, một cú sốc lớn!",
        "Bắn hết 5 viên là một lựa chọn táo bạo, bạn rất kiên cường!",
        "Bạn thật can đảm khi bắn hết 5 viên, điều này thật đáng khen!",
        "Một quyết định mạnh mẽ khi bắn hết 5 viên, không ai có thể làm điều đó dễ dàng!",
        "Bắn hết 5 viên, bạn đã chấp nhận mọi rủi ro với tinh thần dũng cảm!",
        "Bạn thật sự xuất sắc khi quyết định bắn hết 5 viên!",
        "Kết quả bắn hết 5 viên không như mong đợi, nhưng bạn đã thể hiện sự mạnh mẽ!"
    ]
]

COMMENT_DIE = [
    [
        "Chết ngay ở viên đầu tiên, thật không may mắn!",
        "Viên đầu tiên đã mang đến sự kết thúc, bạn thật không may!",
        "Một khởi đầu tồi tệ, viên đầu tiên đã hạ gục bạn!",
        "Chỉ vừa bắt đầu mà bạn đã chết ở viên đầu tiên!",
        "Viên đầu tiên đã lấy đi tất cả, thật đáng tiếc!",
        "Chết ngay ở viên thứ nhất, một cú sốc không thể tin được!",
        "Viên đầu tiên không cho bạn cơ hội nào, thật tệ!",
        "Chết ngay ở viên đầu tiên, bạn đã không kịp tránh!",
        "Một khởi đầu xui xẻo, viên đầu tiên đã khiến bạn thất bại!",
        "Chết ở viên đầu tiên, không ai muốn bắt đầu như vậy!"
    ],
    [
        "Chết ngay ở viên thứ hai, thật không may mắn!",
        "Viên thứ hai đã hạ gục bạn, một quyết định sai lầm!",
        "Thật đáng tiếc khi bạn chết ở viên thứ hai!",
        "Chết ngay ở viên thứ hai, một cú sốc cho tất cả!",
        "Chỉ vừa bắt đầu mà đã chết ở viên thứ hai, không ai muốn thế!",
        "Viên thứ hai đã mang đến thất bại, bạn đã không may!",
        "Chết ở viên thứ hai, không ai có thể đoán trước được!",
        "Viên thứ hai đã cướp đi cơ hội của bạn!",
        "Chết ngay ở viên thứ hai, thật đáng buồn!",
        "Viên thứ hai đã khiến bạn ra đi, không ai mong chờ điều này!"
    ],
    [
        "Chết ngay ở viên thứ ba, thật không may mắn!",
        "Viên thứ ba đã kết thúc trò chơi của bạn!",
        "Thật bất ngờ khi chết ở viên thứ ba!",
        "Chết ở viên thứ ba, không ai có thể tưởng tượng được!",
        "Chỉ cần một viên nữa, nhưng bạn đã chết ở viên thứ ba!",
        "Viên thứ ba đã mang lại sự thất vọng!",
        "Chết ngay ở viên thứ ba, bạn đã không may!",
        "Viên thứ ba không cho bạn cơ hội nào!",
        "Chết ở viên thứ ba, bạn có thể đã dừng lại sớm hơn!",
        "Một cú sốc khi chết ở viên thứ ba!"
    ],
    [
        "Chết ngay ở viên thứ tư, thật không may mắn!",
        "Viên thứ tư đã kết thúc mọi thứ!",
        "Chết ở viên thứ tư, thật đáng tiếc!",
        "Chỉ còn một viên nữa, nhưng bạn đã chết ở viên thứ tư!",
        "Viên thứ tư đã cướp đi mọi hy vọng của bạn!",
        "Chết ở viên thứ tư, không ai mong chờ điều này!",
        "Viên thứ tư khiến bạn không còn cơ hội!",
        "Chết ngay ở viên thứ tư, không ai có thể tin được!",
        "Thật không may khi chết ở viên thứ tư!",
        "Viên thứ tư đã mang đến sự thất bại cuối cùng!"
    ],
    [
        "Rất tiếc, bạn đã chết ở viên thứ 5, nhưng bạn đã dám thử sức!",
        "Thật đáng tiếc khi bạn không thể sống sót qua viên thứ 5!",
        "Bạn đã dũng cảm đến viên thứ 5, nhưng đáng tiếc rằng điều đó không đủ!",
        "Chết ở viên thứ 5, nhưng bạn đã cho thấy sự kiên cường!",
        "Một cú sốc lớn khi bạn chết ở viên thứ 5, nhưng bạn đã dám chơi!",
        "Thật không may, viên thứ 5 đã là kết thúc cho bạn!",
        "Bạn đã đến gần, nhưng chết ở viên thứ 5 thật sự đáng tiếc!",
        "Chết ở viên thứ 5, nhưng tinh thần chiến đấu của bạn thật đáng khen!",
        "Đến viên thứ 5 rồi mà vẫn không thoát, bạn thật dũng cảm!",
        "Một kết thúc không mong đợi ở viên thứ 5, nhưng bạn đã làm tốt!"
    ]
]

class RouletteGame:
    message: discord.Message
    bullet_position:int = 0
    shots_fired: int = 0
    dead: bool = False
    is_playing: bool = False

    def __init__(self, ctx:commands.Context, bet: int, user_data: UserModel, db, bot: discord.Client):
        self.ctx = ctx
        self.author = ctx.author
        self.bot = bot

        self.bet = bet
        self.prize = [round(self.bet*0.25)*i for i in range(1, 6)]
        self.total_prize = bet
        self.bullet_position = random.randint(0, 5)

        self.user_data = user_data
        self.user_data.credit -= bet
        self.db = db
        self.db.commit()

        self.bot=bot

    async def start_game(self):
        self.message = await self.ctx.send(embed = self.embed_status())
        await self.message.add_reaction("🔫")
        await self.message.add_reaction("🛑")
        self.is_playing = True

        while self.is_playing:
            def check(reaction:discord.Reaction, user):
                return user == self.ctx.author and reaction.message.id == self.message.id

            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == "🔫":
                await self.on_shoot()
            if str(reaction.emoji) == "🛑":
                await self.on_stop()
            await self.message.edit(embed=self.embed_status())
            
        embed = self.embed_status()
        embed.set_footer(text=f"🔫 ~ {self.comment_congrats()}")
        await self.message.edit(embed=embed)
        if not self.dead: await self.winning()
                
    
    def comment_congrats(self):
        if self.dead: return random.choice(COMMENT_DIE[self.shots_fired])
        return random.choice(COMMENT_STOP[self.shots_fired])

    def embed_status(self):
        embed = Embed(color=Colour.from_str(color_fired[self.shots_fired]), title=f"{self.author.display_name} đã cược {self.bet} để chơi Roulette game")
        
        magazine = []
        for i in range(6):
            if i == self.shots_fired:
                magazine.append(f'{"🔴" if self.dead else "❓"} <- current pos')
            else:
                magazine.append('⚫' if i<self.shots_fired else '❓')
        embed.add_field(name='Magazine', value='\n'.join(magazine))

        prize_dis = []
        for i in range(5):
            if i < self.shots_fired:
                prize_dis.append(f'Prize #{i+1}: **{bt(self.prize[i])}** ✅')
            else:
                prize_dis.append(f'Prize #{i+1}: {bt(self.prize[i])}')
        embed.add_field(name='Prize', value='\n'.join(prize_dis))

        if self.dead:
            embed.add_field(value='', name=f"Và đã mất tất {bt(self.total_prize)} =))", inline=False)
        else:
            embed.add_field(value='', name=f"Tổng tiền nhận lại: {bt(self.total_prize)}", inline=False)

        return embed

    async def on_shoot(self):
        if self.shots_fired == self.bullet_position: # Die
            self.is_playing = False
            self.dead = True
        else:
            self.total_prize += self.prize[self.shots_fired]
            self.shots_fired += 1
            
            if self.shots_fired==5: self.is_playing = False
    
    async def on_stop(self):
        self.is_playing = False
    
    async def winning(self):
        self.user_data.credit += self.total_prize
        self.db.commit()



class Death(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user: return user
        user = UserModel(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user

    @commands.command(help="Should never try")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roulette(self, ctx: commands.Context, amount: int|str=100):
        user = self.get_user(ctx.author.id)
        if amount == "all":
            amount = user.credit
        if amount < 100:
            return await ctx.reply(f"Số tiền phải ít nhất là {bt(100)}")
        game = RouletteGame(ctx, amount, user, self.db, self.bot)
        await game.start_game()

