#필요한 기능,파일 불러오기
import os
import sys
import asyncio
import discord
from discord.ext import commands
import random
import datetime
import emoji
from datetime import datetime, date, time
from urllib import parse, request
import re

from read0928 import *


client = commands.Bot(command_prefix='~')

# 1-6에서 생성된 토큰을 이곳에 입력해주세요.
token = "token"

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
    print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    print(client.user.id)
    print("===========")
    # 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
    # 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
    while True:
        game2 = discord.Game("리드만 생각")
        await client.change_presence(status=discord.Status.online, activity=game2)
        await asyncio.sleep(10)
        game3 = discord.Game("리드랑 디스코드")
        await client.change_presence(status=discord.Status.online, activity=game3)
        await asyncio.sleep(10)
        game4 = discord.Game("도움말은 ~도움")
        await client.change_presence(status=discord.Status.online, activity=game4)
        await asyncio.sleep(10)
# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.



@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
        return None #동작하지 않고 무시합니다.

    id = message.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.

    def check3(m):
        return lambda m: m.author == message.author and m.channel == message.channel
    
    async def get_input_of_type4(func,message):
        while True:
            try:
                msg = await client.wait_for('message', timeout=20 ,check=check3(message))
                if msg.content == "가위" or msg.content == "바위" or msg.content == "보" or msg.content == "그만":
                    return func(msg.content)
                else:
                    continue
            except ValueError:
                continue
            
    member = message.author
    member = str(member)
    member = member[:-5]
            
    cho_quiz = ChoQuiz.find(channel)
    if cho_quiz is not None:
        if re.sub(' ','',message.content) == re.sub(' ','', cho_quiz.answer):
            await channel.send(f'**{message.author.mention}**님의 [**{cho_quiz.answer}**] 정답! :white_check_mark:')
            result = cho_quiz.correct(channel)
            await channel.send(result)
    
    if message.content.startswith('~도움'):
        embed = discord.Embed(
            title='**리드봇 등장!**',
            description='커맨드 리스트',
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name='~골라줘,~뭐먹지,~명언,~아재개그,~로또', value='랜덤으로 하나 골라줌.')
        embed.add_field(name='~한영, ~영한, ~한일, ~일한', value='번역함. 네이버 파파고 제공')
        embed.add_field(name='~말해', value='똑같이 말해준다.')
        embed.add_field(name='~주사위 number' , value='1부터 number까지 랜덤으로 값줌.')
        embed.add_field(name='~야구노말,~야구이지,~야구하드', value='야구게임 할수 있음 그만할려면 0입력')
        embed.add_field(name='~가위바위보,~갈바', value='연승 가위바위보 그만할려면 "그만" 입력')
        embed.add_field(name='~알람켜기,~알람켜,~알람끄기,~알람꺼', value='알람켜기 명령한다음 초 숫자입력')
        embed.add_field(name='~초퀴', value='~초퀴 입력후 ~초퀴 장르 문제수 입력 ex. ~초퀴 영화 3 입력, 패스하고 싶으면 ~초퀴 패스 끝내고 싶으면 ~초퀴 끝')
        embed.set_footer(text='문의사항 디스코드 갠챗& 카톡 read0928')
        await channel.send(embed=embed)
        

    elif message.content.startswith('~리드 바보'):
        msg = await channel.send('```아니야!! 리드는 이 봇을 만든 사람이야```')
        await asyncio.sleep(1.0)
        await msg.edit(content=f"{member} 바보") #메시지 수정기능
    
    elif message.content.startswith('~말해'):
        mes = message.content
        mes = mes[4:]
        await channel.send(mes)
    elif message.content.startswith('~야구 룰'):
        await channel.send('1. 1000~9999사이 숫자 중 중복되는 숫자가 없는 숫자를 입력한다. ex) 9981 x, 1235 o\n\n2.정해져 있는 숫자에서 숫자가 포함만 되있으면 볼, 숫자위치가 같으면 스트라이크. 단,스트라이크 볼 중복카운트아님\n3.4스트라이크 => 게임 승리.\n4.처음에는 0이 올 수 없고, 이지모드에는 0이없다.\n5.0을 치면 다시 시작')
    elif message.content.startswith('~어그로'):
        dirctory = os.path.dirname(__file__)
        file = discord.File(dirctory + "\나루토사스케2.gif",spoiler=True)
        await channel.send('미안하다 이거 보여주려고 어그로끌었다.. 나루토 사스케 싸움수준 ㄹㅇ실화냐? 진짜 세계관최강자들의 싸움이다.. 그찐따같던 나루토가 맞나? 진짜 나루토는 전설이다..진짜옛날에 맨날나루토봘는데 왕같은존재인 호카게 되서 세계최강 전설적인 영웅이된나루토보면 진짜내가다 감격스럽고 나루토 노래부터 명장면까지 가슴울리는장면들이 뇌리에 스치면서 가슴이 웅장해진다.. 그리고 극장판 에 카카시앞에 운석날라오는 거대한 걸 사스케가 갑자기 순식간에 나타나서 부숴버리곤 개간지나게 나루토가 없다면 마을을 지킬 자는 나밖에 없다 라며 바람처럼 사라진장면은 진짜 나루토처음부터 본사람이면 안울수가없더라 진짜 너무 감격스럽고 보루토를 최근에 알았는데 미안하다.. 지금20화보는데 진짜 나루토세대나와서 너무 감격스럽고 모두어엿하게 큰거보니 내가 다 뭔가 알수없는 추억이라해야되나 그런감정이 이상하게 얽혀있다.. 시노는 말이많아진거같다 좋은선생이고..그리고 보루토왜욕하냐 귀여운데 나루토를보는것같다 성격도 닮았어 그리고버루토에 나루토사스케 둘이싸워도 이기는 신같은존재 나온다는게 사실임?? 그리고인터닛에 쳐봣는디 이거 ㄹㅇㄹㅇ 진짜팩트냐?? 저적이 보루토에 나오는 신급괴물임?ㅡ 나루토사스케 합체한거봐라 진짜 ㅆㅂ 이거보고 개충격먹어가지고 와 소리 저절로 나오더라 ;; 진짜 저건 개오지는데.. 저게 ㄹㅇ이면 진짜 꼭봐야돼 진짜 세계도 파괴시키는거아니야 .. 와 진짜 나루토사스케가 저렇게 되다니 진짜 눈물나려고했다.. 버루토그라서 계속보는중인데 저거 ㄹㅇ이냐..? 하.. ㅆㅂ 사스케 보고싶다.. 진짜언제 이렇게 신급 최강들이 되었을까 옛날생각나고 나 중딩때생각나고 뭔가 슬프기도하고 좋기도하고 감격도하고 여러가지감정이 복잡하네.. 아무튼 나루토는 진짜 애니중최거명작임..',file=file) 
    elif message.content.startswith('~한일'):
        mes = message.content.replace('~한일', '').strip()
        transText = translate('ko', 'ja', mes)
        embed = discord.Embed(
            title=transText,
            description=mes,
            colour=discord.Colour.purple()
        )
        embed.set_footer(text='Translated by.네이버 파파고')
        await channel.send(embed=embed)
    
    elif message.content.startswith('~일한'):
        mes = message.content.replace('~일한', '').strip()
        transText = translate('ja', 'ko', mes)
        embed = discord.Embed(
            title=transText,
            description=mes,
            colour=discord.Colour.purple()
        )   
        embed.set_footer(text='Translated by.네이버 파파고')
        await channel.send(embed=embed)

    elif message.content.startswith('~한영'):
        mes = message.content.replace('~한영', '').strip()
        transText = translate('ko', 'en', mes)
        embed = discord.Embed(
            title=transText,
            description=mes,
            colour=discord.Colour.purple()
        )   
        embed.set_footer(text='Translated by.네이버 파파고')
        await channel.send(embed=embed)

    elif message.content.startswith('~영한'):
        mes = message.content.replace('~영한', '').strip()
        transText = translate('en', 'ko', mes)
        embed = discord.Embed(
            title=transText,
            description=mes,
            colour=discord.Colour.purple()
        )   
        embed.set_footer(text='Translated by.네이버 파파고')
        await channel.send(embed=embed)
        
    
    
    elif message.content.startswith("~가위바위보") or message.content.startswith("~갈바"):
        await channel.send(f"{member}, 가위바위보 시작!! 제한시간은 20초! 가위, 바위, 보중 하나를 말해주세요")
        tal=True
        k=0
        while (tal==True):
            try:
                rcp = await get_input_of_type4(str,message)
                if rcp == "그만":
                    tal=False
                    await channel.send(f'{member} 게임을 중단합니다. {k}연승에서 마무리')
                    break
            except asyncio.TimeoutError:
                await channel.send(f'{member}, 시간 초과 ㅠㅠ.. ')
                tal=False
                break
            except ValueError:
                continue      
            bot_response = random.randint(1, 3)
            if bot_response == 1: # 봇이 가위를 낸 경우,
                if rcp == "가위": # 가위 vs 가위이기 때문에 비겼습니다.
                    await channel.send(f"✌ {member}, 비겼어~ 계속 하자!")
                    continue
                elif rcp == "바위": # 바위 vs 가위이기 때문에 유저가 이겼습니다.
                    k=k+1
                    await channel.send(f"✌ {member} {k}연승 중, 내가 졌어..")                        
                    continue
                elif rcp == "보":
                    await channel.send(f"✌ {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                else:
                    continue
            if bot_response == 2: # 봇이 바위를 낸 경우,
                if rcp == "가위": # 가위 vs 바위
                    await channel.send(f"✊ {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                elif rcp == "바위": # 바위 vs 바위
                    await channel.send(f"✊ {member}, 비겼어~ 계속 하자!")
                    continue
                elif rcp == "보": # 보자기 vs 바위
                    k=k+1
                    await channel.send(f"✊ {member} {k}연승 중, 내가 졌어..")
                    continue
                else:
                    continue
            if bot_response == 3:
                if rcp == "가위": # 가위 vs 보자기
                    k=k+1
                    await channel.send(f"🖐 {member} {k}연승 중, 내가 졌어..")
                    continue
                elif rcp == "바위": # 바위 vs 보자기                        
                    await channel.send(f"🖐 {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                elif rcp == "보": # 보자기 vs 보자기
                    await channel.send(f"🖐 {member}, 비겼어~ 계속 하자!")
                    continue
                else:
                    continue
    
    else: #위의 if에 해당되지 않는 경우
        return None #동작하지 않고 무시한다.




@client.command(pass_context=True)
async def 주사위(ctx, num1):
    picked = random.randint(1, int(num1))
    if picked%2==0: #주사위 짝수일 경우
        if picked > int(num1)//2:
            if picked==int(num1):
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n와 대박🎰!!, 제일 높은 숫자네요")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n오늘 운이 좀 괜찮은데요??!")
        if picked <= int(num1)//2:
            if picked==1:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n헐😱.. 제일 낮은 숫자네요..")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"오늘 운이 좀 별로네요 ㅠㅠ")
    if picked%2==1: #주사위 홀수일 경우
        if picked >= int(num1)//2+1:
            if picked==int(num1):
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n와 대박🎰!!, 제일 높은 숫자네요")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n오늘 운이 좀 괜찮은데요??!")
        if picked <= int(num1)//2:
            if picked==1:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n헐😱.. 제일 낮은 숫자네요..")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"오늘 운이 좀 별로네요 ㅠㅠ")



@client.command(pass_context=True) #채널에 언제왔는지 알려줌
async def 언제가입했니(ctx, *, member: discord.Member):
    await ctx.send('{0}님은 {0.joined_at}에 이 채널에 가입하셨습니다.'.format(member))

@client.command(pass_context=True) #랜덤으로 선택지 골라줌
async def 골라줘(ctx, *args):
    choice=random.choice(args)
    await ctx.send(f"난 {choice}")
    
@client.command(pass_context=True) #로또 랜덤생성
async def 로또(ctx, *, member: discord.Member):
    list=[]
    ran_num = random.randint(1,45)
    for i in range(6):
        while ran_num in list:
            ran_num = random.randint(1,45)
        list.append(ran_num)
    list.sort()
    await ctx.send('{0}의 로또번호!! :ticket:'.format(member)+f'{list}')


#텍스트 파일 필요 요구
@client.command(pass_context=True) #랜덤으로 음식골라줌
async def 뭐먹지(ctx):
    food = open("C:/Users/chk/Desktop/음식메뉴.txt",'r',encoding="UTF8")
    foodchoice = random.choice(food.readlines()).rstrip()
    await ctx.send(f"{foodchoice}를 먹어보는 건 어때?")


@client.command(pass_context=True)
async def 명언(ctx):
    f= open("C:/Users/chk/Desktop/명언 모음.txt",'r',encoding="UTF8")
    fsay=random.choice(f.readlines())
    await ctx.send(f'```{fsay}```')

@client.command(pass_context=True)
async def 아재개그(ctx):
    g= open("C:/Users/chk/Desktop/아재개그.txt",'r',encoding="UTF8")
    humor=random.choice(g.readlines())
    await ctx.send(humor)
    
    
    
#--------input 요구 함수    

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await client.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue
            
async def get_input_of_type2(func,ctx):
        while True:
            try:
                msg = await client.wait_for('message', timeout=20 ,check=check(ctx))
                return func(msg.content)
            except ValueError:
                continue
#실험용
@client.command()
async def 더하기(ctx):
    await ctx.send("첫번째 숫자는 뭘로?")
    firstnum = await get_input_of_type(int, ctx)
    await ctx.send("두번째 숫자는 뭘로?")
    secondnum = await get_input_of_type(int, ctx)
    await ctx.send(f"{firstnum} + {secondnum} = {firstnum+secondnum}")
    
#야구 난이도별 코드
@client.command()
async def 야구이지(ctx):
    a=[]
    for i in range(100,999):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        if (b1=="0" or b2=="0" or b0==b1 or b0==b2 or b1==b2):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 이지모드 시작! 0은 포함되지않아. 100~999사이 숫자만 입력해줘")
    while(k<7):
        await ctx.send(f"{member}, 숫자를 입력해~ 기회는 {7-k}번 남았어!")
        num2 = await get_input_of_type(int,ctx)
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
                break
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,3):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,3):
            for j in range(0,3):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count
        if(num==num2):
            if k==1:
                await ctx.send(f"{member}, 당신은 1/648 확률을 뚫어낸 찍신??! 대박! 정답이야!!")
                break
            else:
                await ctx.send(f"{member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==7:
                await ctx.send(f"{member}, 7번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"{member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"{member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼!")
                    continue

@client.command(aliases=["야구노말","야구노멀"])
async def 야구게임(ctx):
    a=[]
    for i in range(1000,10000):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        b3=p[3]
        if (b0==b1 or b0==b2 or b0==b3 or b1==b2 or b1==b3 or b2==b3):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 시작!")
    while(k<10):
        await ctx.send(f"{member}, 숫자를 입력해~ 기회는 {10-k}번 남았어!")
        num2 = await get_input_of_type(int,ctx)
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,4):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,4):
            for j in range(0,4):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count
        if(num==num2):
            if k==1:
                await ctx.send(f"{member}, 당신은 찍신??! 한번 만에 바로 맞췄어 대박!")
                break
            else:
                await ctx.send(f"{member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==10:
                await ctx.send(f"{member}, 10번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"{member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"{member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼!")
                    continue

@client.command()
async def 야구하드(ctx):
    a=[]
    for i in range(1000,10000):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        b3=p[3]
        if (b0==b1 or b0==b2 or b0==b3 or b1==b2 or b1==b3 or b2==b3):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 하드모드 시작!")
    tal=True
    while(k<8 and tal==True):
        await ctx.send(f"{member}, 숫자를 입력해~ 기회는 {8-k}번, 제한시간은 20초 남았어!")
        try:
            num2 = await get_input_of_type2(int,ctx)
        except asyncio.TimeoutError:
            await ctx.send(f'시간 초과 ㅠㅠ.. 다시 시작해 주세요! 정답은 {num}')
            tal=False
            break
        except ValueError:
            continue
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
                tal=False
                break
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,4):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,4):
            for j in range(0,4):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count            
        if(num==num2):
            if k==1:
                await ctx.send(f"{member}, 당신은 1/4536 확률을 뚫어낸 찍신??! 대박! 정답이야!!")
                break
            else:
                await ctx.send(f"{member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==8:
                await ctx.send(f"{member}, 8번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"{member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"{member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼!")
                    continue



@client.command()
async def 애교(ctx):
    a= emoji.emojize(":arrow_upper_right:")
    b= emoji.emojize(":arrow_lower_right:")
    c= emoji.emojize(":arrow_right:")
    msg = await ctx.send("으으응"+str(a)+str(b)+str(c))
    await msg.add_reaction("↗")
    await msg.add_reaction("↘")
    await msg.add_reaction("➡")
        
#알람 관련. ffmpeg 설치필요 응용하면 노래봇 만들기 가능
@client.command(aliases=["알람켜"])
async def 알람켜기(ctx):
    member = ctx.author
    member = str(member)
    member = member[:-5]
    voice_state=ctx.author.voice
    if (not voice_state) or (not voice_state.channel):
        await ctx.send(f"{member}보이스 채널에 들어와서 알람을 켜줘")
        return
    else:
        await ctx.send(f"{member}, 몇 초 알람으로 할래? 양의 숫자만 입력해줘")
    num2 = await get_input_of_type(int,ctx)
    if num2<=0:
        await ctx.send("잘못 입력했어..다시 알람설정해~")
    else:
        channel = voice_state.channel
        vc=await channel.connect()
        await ctx.send(f"{num2}초 알람이 설정되었어!")
        await asyncio.sleep(num2)
        vc.play(discord.FFmpegPCMAudio(executable="C:/Users/chk/Desktop/ffmpeg-20200724-21442a8-win64-static/bin/ffmpeg.exe",source='alert.mp3'))
        await ctx.send(f"{ctx.author.mention}, 일어나~ 일어나~! 일어나~~!! 일어나!!!")
        
                       
    
@client.command(aliases=["ㅋㅋ"])
async def 크크루삥뽕(ctx):
    member = ctx.author
    member = str(member)
    member = member[:-5]
    voice_state=ctx.author.voice
    if (not voice_state) or (not voice_state.channel):
        await ctx.send(f"{member}, 보이스 채널에 들어와서 알람을 켜줘")
        return
    else:
        channel = voice_state.channel
        vc=await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Users/chk/Desktop/ffmpeg-20200724-21442a8-win64-static/bin/ffmpeg.exe",source='zzfQQ.mp3'), after=lambda e: print('ㅋㅋㄹㅃㅃ~', e))
        
                       
@client.command(aliases=["알람꺼","꺼"])
async def 알람끄기(ctx):
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("이미 들어와있지않아")
        return

    await voice_client.disconnect()
    await ctx.send("알람 껐어")

#마피아42 관련 뽑기시뮬레이션    
@client.command()
async def 실버깡(ctx):
    slist = ["서핑 마니아 마피아","해변의 스파이","인어공주 마담","잠수부 도굴꾼","바캉스 마녀","찬란한 아쿠아마린","여름 테두리","오리 튜브 테두리","개구리 지갑","휴양지의 해커","라이프가드 간호사","미공개 테두리1","미공개 테두리2","미공개 명패1","미공개 명패2","미공개 지갑","피서지에서 생긴 일","신비한 합창","루블","루나","스포이드","마법의 염색약","신분증","사망 광고판","부고기사","고대의 제작서","요정의 연마제","명장의 망치","큐피트의 화살","고급 엽서","징벌의 엽서","깜짝 엽서","3티어 카드","해변가 확성기","유리병 편지","해변의 엽서","대양의 보배","바다색 염색약"]
    silv = random.choices(slist,weights=[0.5]*15+[0.4,0.5,0.1,0.5,0.5]+[5]*13+[5.1]*5)
    silv = silv[0]
    if silv == "루블":
        rlist = random.choices(range(500000,750001))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "루나":
        rlist = random.choices(range(1000,1501))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "마법의 염색약":
        rlist = random.choices(range(7,11))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "사망 광고판":
        rlist = random.choices(range(45,61))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "부고기사":
        rlist = random.choices(range(45,61))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "고대의 제작서":
        rlist = random.choices(range(3,5))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "요정의 연마제":
        rlist = random.choices(range(3,5))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "명장의 망치":
        rlist = random.choices(range(3,5))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "고급 엽서":
        rlist = random.choices(range(25,31))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "징벌의 엽서":
        rlist = random.choices(range(5,8))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "깜짝 엽서":
        rlist = random.choices(range(3,7))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "3티어 카드":
        rlist = random.choices(range(1,3))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "해변가 확성기":
        rlist = random.choices(range(7,11))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "유리병 편지":
        rlist = random.choices(range(20,31))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "해변의 엽서":
        rlist = random.choices(range(10,16))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "대양의 보배":
        rlist = random.choices(range(2,4))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    elif silv == "바다색 염색약":
        rlist = random.choices(range(4,6))
        await ctx.send(silv+" "+str(rlist[0])+"개")
    else:
        await ctx.send(silv+" 1개")
        
@client.command()
async def 골드깡(ctx):
    glist = ["서핑 마니아 마피아","해변의 스파이","인어공주 마담","잠수부 도굴꾼","바캉스 마녀","찬란한 아쿠아마린","여름 테두리","오리 튜브 테두리","개구리 지갑","휴양지의 해커","라이프가드 간호사","미공개 테두리1","미공개 테두리2","미공개 명패1","미공개 명패2","미공개 지갑","피서지에서 생긴 일","신비한 합창","루블","루나","황금 큐피트의 화살","징벌의 엽서","깜짝 엽서","4티어 카드","해변가 확성기","유리병 편지","해변의 엽서","대양의 보배","바다색 염색약"]
    gold = random.choices(glist,weights=[2.7]*15+[2,2.7,1,1,1]+[5.2]*4+[6.2]*5)
    gold = gold[0]
    if gold == "루블":
        rlist = random.choices(range(500000,750001))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "루나":
        rlist = random.choices(range(1000,1501))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "징벌의 엽서":
        rlist = random.choices(range(17,21))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "깜짝 엽서":
        rlist = random.choices(range(10,14))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "해변가 확성기":
        rlist = random.choices(range(30,41))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "유리병 편지":
        rlist = random.choices(range(80,91))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "해변의 엽서":
        rlist = random.choices(range(40,51))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "대양의 보배":
        rlist = random.choices(range(8,11))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    elif gold == "바다색 염색약":
        rlist = random.choices(range(17,21))
        await ctx.send(gold+" "+str(rlist[0])+"개")
    else:
        await ctx.send(gold+" 1개")
        
@client.command(aliases=["임티"])    
async def 이모티콘(ctx):

    emoji = [" ꒰⑅ᵕ༚ᵕ꒱ ", " ꒰◍ˊ◡ˋ꒱ ", " ⁽⁽◝꒰ ˙ ꒳ ˙ ꒱◜⁾⁾ ", " ༼ つ ◕_◕ ༽つ ", " ⋌༼ •̀ ⌂ •́ ༽⋋ ",
             " ( ･ิᴥ･ิ) ", " •ө• ", " ค^•ﻌ•^ค ", " つ╹㉦╹)つ ", " ◕ܫ◕ ", " ᶘ ͡°ᴥ͡°ᶅ ", " ( ؕؔʘ̥̥̥̥ ه ؔؕʘ̥̥̥̥ ) ", " ( •́ ̯•̀ ) ",
             " •̀.̫•́✧ ", " '͡•_'͡• ", " (΄◞ิ౪◟ิ‵) ", " ˵¯͒ བ¯͒˵ ", " ͡° ͜ʖ ͡° ", " ͡~ ͜ʖ ͡° ", " (づ｡◕‿‿◕｡)づ ",
             " ´_ゝ` ", " ٩(͡◕_͡◕ ", " ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ ", " ٩(͡ï_͡ï☂ ", " ௐ ", " (´･ʖ̫･`) ", " ε⌯(ง ˙ω˙)ว ",
             " (っ˘ڡ˘ς) ", "●▅▇█▇▆▅▄▇", "╋╋◀", "︻╦̵̵̿╤──", "ー═┻┳︻▄", "︻╦̵̵͇̿̿̿̿══╤─",
             " ጿ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ጿ ", "∑◙█▇▆▅▄▃▂", " ♋♉♋ ", " (๑╹ω╹๑) ", " (╯°□°）╯︵ ┻━┻ ",
             " (///▽///) ", " σ(oдolll) ", " 【o´ﾟ□ﾟ`o】 ", " ＼(^o^)／ ", " (◕‿‿◕｡) ", " ･ᴥ･ ", " ꈍ﹃ꈍ ",
             " ˃̣̣̣̣̣̣︿˂̣̣̣̣̣̣ ", " ( ◍•㉦•◍ ) ", " (｡ì_í｡) ", " (╭•̀ﮧ •́╮) ", " ଘ(੭*ˊᵕˋ)੭ ", " ´_ゝ` ", " (~˘▾˘)~ "] # 이모티콘 배열입니다.
        
    randomNum = random.randrange(0, len(emoji)) # 0 ~ 이모티콘 배열 크기 중 랜덤숫자를 지정합니다.
    await ctx.send(emoji[randomNum]) # 랜덤 이모티콘을 메시지로 출력합니다.

        
        
@client.command(pass_context=True, aliases=["초성퀴즈"])
async def 초퀴(ctx, *args):
    """초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)"""
    channel = ctx.message.channel
    cho_quiz = ChoQuiz.find(channel)
    if len(args) == 1 and args[0] == '끝':
        result = ChoQuiz.end(channel)
    elif len(args) == 1 and args[0] == '패스':
        if cho_quiz is not None:
            result = '정답은 [**' + cho_quiz.answer + '**]였어요. :hugging:'
            result += '\n' + cho_quiz.correct(channel)
        else:
            result = '진행중인 초성퀴즈가 없어요.'
    else:
        if cho_quiz is not None:
            result = '이미 진행중인 초성퀴즈가 있어요.'
        else:
            genre = args[0] if len(args) > 0 else None
            count = int(args[1]) if len(args) > 1 else 10
            answer = jaum_quiz(genre)  # 정답 생성
            if answer is not None:
                cho_quiz = ChoQuiz.start(channel, genre, count, answer)
                result = cho(answer)  # 초성 공개
            else:
                result = '장르는 `영화`, `음악`, `동식물`, `사전`, `게임`, `인물`, `책`이 있어요.'
    await ctx.send(result)
        

#관리 명령어. 권한관련 명령어 추가필요
@client.command()
async def 몰래하는청소실험3258238359323857938124(ctx, amount : int):
    if amount>99:
        await ctx.channel.purge(limit=1)
    else:
        await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
async def 닉네임변경19328794817948121982453(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

        
client.run(token)

#더 잘 만들어진 봇들이 많음
