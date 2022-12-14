# bot.py
from dataclasses import dataclass
from lib2to3 import refactor
import os
from pickle import FALSE
import random
import json
from re import S
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
from numpy import datetime_data, datetime64
from datetime import datetime


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = discord.Client()
client = commands.Bot()

avalon = "ssssssss"
avalon_checkroles = [0,0,0]
avalon_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
avalon_strings = ["основной танк","танк терпила","аркана 'таймфриз'","аркана 'сало'","основной хилл","групповой хилл",
"авалонский друид","курса","авалонский топор","меч резни","охотник за душами","пылающий посох","песнь рассвета","фрост", "арбалет","перчатки", "горелка"]
avalon_quantity = [1,1,1,1,1,1,2,1,1,1,1,1,1,8,8,1,1]
avalon_roles = ["","","","","","","","","","","","","","","",""]
emoji_strings = ["MAIN_TANK", "TANK_TERPEL", "STOP_STRAY228", "MAZAIKA_POD_SALOM", "HOLY_MAIN", "NEED_HEAL",
"IRON_ROOT", "ZXCURSED", "AVALON_TOPOR", "ME4_REZNI", "SPIRIT_HUNTER", "BLEIZA", "FIRE_RINGPAIR", "FROST_DEFOLT", "SOLEVOI_ARBALET", "ZABIVNOI_PER4I", "DEMON_FUNG"]
avalon_reactions = []
avapasta = """
----------------------
f_jav 3 - Занять роль
f_unjav 3 - Сойти с роли
f_cljav 3 - Очистить роль для рла
----------------------
"""

@dataclass
class AvalonDetails:
    date: datetime64
    rl : str
    created: datetime64
    description: str = ""

@dataclass
class AvalonMember:
    role_name: str
    nickname: list
    quantity: int
    type: str
    number: int
    emoji: discord.Emoji = '🏃'

    def empty(self):
        self.nickname = ""

types_members = [0,0,0]
Group_messages = []

def CreateEmptyAvalon(avalon_strings, avalon_quantity):
    raid_members = []
    for i in range(1, 5):
        new_member = AvalonMember(number = i, role_name = avalon_strings[i-1], nickname = [], quantity = avalon_quantity[i-1], type="Main")
        raid_members.append(new_member)
    for i in range(5, 8):
        new_member = AvalonMember(number = i, role_name = avalon_strings[i-1], nickname = [], quantity = avalon_quantity[i-1], type="Heal")
        raid_members.append(new_member)
    for i in range(8, 12):
        new_member = AvalonMember(number = i, role_name = avalon_strings[i-1], nickname = [], quantity = avalon_quantity[i-1], type="Cutting")
        raid_members.append(new_member)
    for i in range(12, 18):
        new_member = AvalonMember(number = i, role_name = avalon_strings[i-1], nickname = [], quantity = avalon_quantity[i-1], type="DPS")
        raid_members.append(new_member)
    return raid_members




def RolesPrint(raid_members, avadetails):
    s = ""


    embed = discord.Embed(
            title="**Дата: {}  **\n".format(avadetails.date.strftime("%D %H:%M")),
            description="Создано: {}  \n \n**Raid Leader - {} ** \n".format(avadetails.created.strftime("%D %H:%M"), avadetails.rl),
            color=discord.Colour.gold(), # Pycord provides a class with default colors you can choose from
        )

    #output, types = RolesPrint(members, details, embed)


    #embed.add_field(name="A Normal Field", value="A really nice field with some information. **The description as well as the fields support markdown!**")

    #embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
    #embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
    #embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)

    #embed.set_footer(text="Footer! No markdown here.") # footers can have icons too
    #embed.set_author(name="Avalons Masters", icon_url="https://media.discordapp.net/attachments/1003262931993104404/1003726707200622593/123123123-1.png?width=640&height=640")
    #embed.set_thumbnail(url="https://ao2d.fra1.digitaloceanspaces.com/images/AVALONBOWMAN1.png")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1003262931993104404/1003726707200622593/123123123-1.png?width=640&height=640")
    #embed.set_image(url="https://ao2d.fra1.digitaloceanspaces.com/images/AVALONBOWMAN1.png")




    types_members = [0,0,0]
    print("s")
    for i in range(17):
        if len(raid_members[i].nickname) != 0:
            if raid_members[i].type == "Main":
                types_members[0] += len(raid_members[i].nickname)
            if raid_members[i].type == "Heal":  
                types_members[0] += len(raid_members[i].nickname)
            if raid_members[i].type == "Cutting":
                types_members[1] += len(raid_members[i].nickname)
            if raid_members[i].type == "DPS":  
                types_members[2] += len(raid_members[i].nickname)

    ava_name = ""
    ava_value = ""

    for i in range(0, 7):
        ava_name = "\n                   **Основные роли: [{}/8].**".format(types_members[0])
        nickstring = ""
        for one in  raid_members[i].nickname:
            nickstring += one
        ava_value += "\n{} - {} | {} шт | - {}".format(raid_members[i].emoji, raid_members[i].role_name, raid_members[i].quantity ,nickstring)
    embed.add_field(name=ava_name, value=ava_value, inline=False)
    ava_value = ""
    for i in range(7, 11):
        ava_name = "\n                   **Роли порезки: [{}/4]**".format(types_members[1])
        nickstring = ""
        for one in  raid_members[i].nickname:
            nickstring += one
        ava_value += "\n{} - {} | {} шт | - {}".format(raid_members[i].emoji, raid_members[i].role_name, raid_members[i].quantity ,nickstring)
    embed.add_field(name=ava_name, value=ava_value, inline=False)
    ava_value = ""
    for i in range(11, 17):
        ava_name = "\n                    **ДПС: [{}/8]**".format(types_members[2])
        nickstring = ""
        for one in  raid_members[i].nickname:
            nickstring += one
        ava_value += "\n{} - {} | {} шт | - {}".format(raid_members[i].emoji, raid_members[i].role_name, raid_members[i].quantity ,nickstring)
    embed.add_field(name=ava_name, value=ava_value, inline=False)
    ava_value = ""



    s = ""
    for i in range(16):
        if i == 0:
            s += "\n    **Основные роли: [{}/7]**".format(types_members[0])
        if i == 7:
            s += "\n    **Роли порезки: [{}/4]**".format(types_members[1])
        if i == 11:
            s += "\n    **ДПС: [{}/8]**".format(types_members[2])

        nickstring = ""
        for one in  raid_members[i].nickname:
            nickstring += one 
        s += "\n{} - {} | {} шт | - {}".format(raid_members[i].number, raid_members[i].role_name, raid_members[i].quantity ,nickstring)
    return (s, types_members, embed)

bot = commands.Bot(command_prefix='f_')



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    print("hello")
    await ctx.respond("Hey!")

welcome_channel = bot.get_channel('992506822487445547')
Main_guild = bot.get_guild('992506822487445544')
"""
@bot.event
async def on_member_join(member):
    await welcome_channel.send(Welcome_embed)
"""

class View(discord.ui.View): # Create a class called View that subclasses discord.ui.View
    @discord.ui.button(label="Подать заявку", style=discord.ButtonStyle.primary) 
    async def button_callback(self, button, interaction):
        
        Main_guild = interaction.guild
        category = discord.utils.get(Main_guild.categories, id=1005856727830384769)
        recruiter = discord.utils.get(Main_guild.roles, id=1001500694177656862)
        exists = False
        for existing in category.channels:
            if (existing.name == 'Тикет - {} '.format(interaction.user.name)):
                exists = True
        if (exists):
            interaction_msg = await interaction.response.send_message("Заявка уже лежит!") # Send a message when the button is clicked
            await interaction_msg.delete()
        else:
            overwrites = {
            Main_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            recruiter: discord.PermissionOverwrite(read_messages=True)
            }

            print(category) 
            ticket_channel = await Main_guild.create_text_channel('Тикет - {} '.format(interaction.user.name), category=category, overwrites=overwrites)

            Join_embed = discord.Embed(
                title="Зявка для вступления",
                description=f" {interaction.user.mention} , заполняй заявку!",
                color=discord.Colour.gold(), # Pycord provides a class with default colors you can choose from
                )
            Join_embed.add_field(name="Ниже необходимо ввести следующее:", value="\n Игровое имя персонажа:\nНаиболее выкачанные классы\nПеречень гильдий в которых вы были:\nПричина ухода из последней гильдии:\nКакие цели преследуете в игре:\nСкриншот экрана выбора персонажа:\nСкриншот параметров персонажа:\nКак к вам обращаться:\nВаш возраст:", inline=False)
            Join_embed.add_field(name="Заполнил?", value=f"Пингани {recruiter.mention} и жди ответа!", inline=False)
            Join_embed.set_thumbnail(url="https://i.imgur.com/JFMkwBH.png%22")        
            await ticket_channel.send('', embed=Join_embed)
            interaction_msg = await interaction.response.send_message("Канал создан!") # Send a message when the button is clicked
            await interaction_msg.delete()


class Close(discord.ui.View): # Create a class called View that subclasses discord.ui.View
    @discord.ui.button(label="Закрыть заявку", style=discord.ButtonStyle.primary) 
    async def button_callback(self, button, interaction):
        Main_guild = interaction.guild
        category = discord.utils.get(Main_guild.categories, id=1005856727830384769)
        close_category = discord.utils.get(Main_guild.categories, id=1005864153451348008)
        recruiter = discord.utils.get(Main_guild.roles, id=1001500694177656862)
        if (recruiter in interaction.user.roles):
            await interaction.channel.edit(category=close_category)
            await interaction.channel.send(f'Закрыл - {interaction.user.mention }')
        else:
            await interaction.channel.send(f'Это кнопка для {recruiter.mention}')


        

        print(category) 
        ticket_channel = await Main_guild.create_text_channel('Тикет - {} '.format(interaction.user.name), category=category, overwrites=overwrites)

        Join_embed = discord.Embed(
            title="Зявка для вступления",
            description=f" {interaction.user.mention} , заполняй заявку!",
            color=discord.Colour.gold(), # Pycord provides a class with default colors you can choose from
            )
        Join_embed.add_field(name="Ниже необходимо ввести следующее:", value="\n Игровое имя персонажа:\nНаиболее выкачанные классы\nПеречень гильдий в которых вы были:\nПричина ухода из последней гильдии:\nКакие цели преследуете в игре:\nСкриншот экрана выбора персонажа:\nСкриншот параметров персонажа:\nКак к вам обращаться:\nВаш возраст:", inline=False)
        Join_embed.add_field(name="Заполнил?", value=f"Пингани {recruiter.mention} и жди ответа!", inline=False)
        Join_embed.set_thumbnail(url="https://i.imgur.com/JFMkwBH.png%22")        
        await ticket_channel.send('', embed=Join_embed)
        await interaction.response.send_message("Канал создан!") # Send a message when the button is clicked



@bot.slash_command(name= "welcome_default", description = "Say hello")
async def welcome_default(ctx):
    print('msg printed')
    Welcome_embed = discord.Embed(
            title="Avalons Masters",
            description="**Добро пожаловать!**",
            color=discord.Colour.gold(), # Pycord provides a class with default colors you can choose from
        )
    Welcome_embed.add_field(name="Основная информация:", value="\nОсновное время игры (prime time) - 13:30 - 23:00 МСК;\nОсновной город - Fort Sterling;", inline=False)
    Welcome_embed.add_field(name="Основные цели:", value="\nАктивное развитие начинающих игроков в PVE и PVP аспектах игры;\nСоздание комфортной атмосферы при нахождения в гильдии;", inline=False)
    Welcome_embed.add_field(name="Преимущества нахождения в гильдии:", value="\nОтсутствие налога с поднятого серебра, 0%;\nНаличие убежищ в чёрной локации;\nОбширный выбор PVE-аспектов игры;\nСкидки на станках в городах;", inline=False)
    Welcome_embed.add_field(name="Требование для вступления:", value="\nот 2 млн общей славы;\n от 15 полных лет;\n игра с компьютера;\nисправный микрофон;", inline=False)
    Welcome_embed.add_field(name="Чтобы вступить тыкай на кнопку ниже", value="_", inline=False)
    Welcome_embed.set_thumbnail(url="https://i.imgur.com/JFMkwBH.png%22")
    await ctx.send("", embed=Welcome_embed, view=View())


""""
 @bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
"""





bot.run(TOKEN)