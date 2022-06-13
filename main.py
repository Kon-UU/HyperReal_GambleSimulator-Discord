from discord.ext import commands
import discord
import hashlib
import random
import statistics
import json

bot = commands.Bot(command_prefix=".")
USERTAKE = 0.98 # 유저가 가져가는 비율
ANNOUNCE_SERVER = 
LOG_SERVER = 
STRING_POOL = "1234567890abcdef"
seed = ""
session = ""

with open("data.json", "r") as f:
        data = json.load(f)

for i in range(64):
    seed += random.choice(STRING_POOL) #실제로는 이렇게 하는거보다는 10만개 정도 미리 계산 해놓은 다음에 역순으로 줘서 해시값 풀로 준 다음에 이전 결과값 알 수 있게 해주는게 좋음.
for i in range(6):
    session += random.choice(STRING_POOL)
root_seed = seed
numberlist = []
gc = 0

token = ""

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=".h"))
    print("inited.")
    if not ANNOUNCE_SERVER == 0:
        em = rst_announce()
        await bot.get_channel(ANNOUNCE_SERVER).send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def r(ctx):
    if not ANNOUNCE_SERVER == 0:
        em = rst_announce()
        await bot.get_channel(ANNOUNCE_SERVER).send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def c(ctx): #현재 시드 값
    await ctx.send(root_seed)

@bot.command()
async def p(ctx, c, m):
    global data
    try:
        qq = data[ctx.author.id]
    except:
        await ctx.send(".g를 먼저 입력 해주세요.")
        return
    global numberlist
    global seed

    c = int(c)
    m = float(m)
    if data[ctx.author.id] < c:
        await ctx.send("유효하지 않은 베팅")
        return

    if not 1 < m:
        await ctx.send("유효하지 않은 배율")
        return

    if not 1 < c:
        await ctx.send("유효하지 않은 베팅")
        return
    seed = hashlib.sha256(seed.encode()).hexdigest()
    cc = int(hashlib.sha256(f'{seed}'.encode('utf-8')).hexdigest()[0: int(52 / 4)], base=16) / (2 ** 52)
    result = round(((1 / cc) - 1) * USERTAKE + 1, 2)
    print(seed)

    if float(m) <= result:
        pf = c * m - c
    else:
        pf = -1 * c

    numberlist.append(result)
    em = discord.Embed(title = f"게임 결과 #{len(numberlist)}", description = f"시드 : {seed[0:5]}...{seed[59:64]}",color=0x242133)
    em.set_author(name="HyperReal 100% 공정한 게임")
    em.add_field(name = "게임 배율",value = f"{result}x")
    em.add_field(name = "선택 배율",value = f"{m}x")
    em.add_field(name = "배팅 금액",value = f"{c}원")
    em.add_field(name = "수익 금액",value = f"{'{:+}'.format(pf)}원")
    
    data[ctx.author.id] = round(data[ctx.author.id] + pf)
    save_data(data)

    await ctx.send(embed = em)
    await bot.get_channel(LOG_SERVER).send(f"#{len(numberlist)} : {result}x")

@bot.command()
async def h(ctx):
    em = discord.Embed(title = f"플레이 방법", description = f".p (배팅 금액) (선택 배율)\n.g - 1만원 설정\n.m - 잔액 확인",color=0x242133)
    em.set_author(name="HyperReal 100% 공정한 게임")
    
    await ctx.send(embed = em)

@bot.command()
async def m(ctx):
    global data
    em = discord.Embed(title = f"잔액 현황", description = f"{data[ctx.author.id]}",color=0x242133)
    em.set_author(name="HyperReal 100% 공정한 게임")
    
    await ctx.send(embed = em)

@bot.command()
async def g(ctx): # 돈 뽑기
    global data
    data[ctx.author.id] = 10000
    save_data(data)
    await ctx.send("잔액이 10000원으로 설정 되었습니다.")

def rst_announce():
    global root_seed
    global seed
    global numberlist
    
    if not len(numberlist) == 0:
        em = discord.Embed(title = f"시드가 재생성되었습니다.", description = f"게임 정보를 공개합니다.",color=0x242133)
        em.add_field(name = "플레이 된 게임",value = f"{len(numberlist)}")
        em.add_field(name = "중앙 배율",value = f"{round(statistics.median(numberlist), 2)}x")
        em.add_field(name = "이전 시드",value = f"{root_seed}")
        em.add_field(name = "서버 수수료",value = f"{round((1 - USERTAKE) * 100)}%")
    else:
        em = discord.Embed(title = f"HPRL이 재시작되었습니다.",color=0x242133)
    em.set_author(name="HyperReal 100% 공정한 게임")
    em.set_footer(text=f"HPRL session({session})")

    seed = ""
    numberlist = []
    for i in range(64):
        seed += random.choice(STRING_POOL)
    root_seed = seed
    return em

def save_data(dt):
    global data
    with open("data.json", "w") as f:
        json.dump(dt,f)

bot.run(token)
