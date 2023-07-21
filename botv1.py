import discord
from discord.ext import commands
import random
import re
import sqlite3
import os
import sys
import TOKEN as key

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=None)
native_thumbnail = 'https://img.freepik.com/free-vector/glitch-error-404-page_23-2148105404.jpg?w=2000'

def restart_bot(): 
    os.execv(sys.executable, ['python'] + sys.argv)
    
def run_discord_bot():
    TOKEN = key.key()

    # Connect to the database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('character_database.db')
    cursor = conn.cursor()

    # Create the character table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            character_id INTEGER PRIMARY KEY,
            character_name TEXT,
            thumbnail TEXT,
            class TEXT,
            race TEXT,
            level INTEGER,
            xp INTEGER,
            player_name TEXT,
            alignment TEXT,
            backstory TEXT,
            armor_class INTEGER,
            initiative INTEGER,
            speed INTEGER,
            inspiration INTEGER,
            max_hp INTEGER,
            current_hp INTEGER,
            death_saves TEXT,
            strength INTEGER,
            dexterity INTEGER,
            constitution INTEGER,
            intelligence INTEGER,
            wisdom INTEGER,
            charisma INTEGER,
            strength_mod INTEGER,
            dexterity_mod INTEGER,
            constitution_mod INTEGER,
            intelligence_mod INTEGER,
            wisdom_mod INTEGER,
            charisma_mod INTEGER,
            copper INTEGER,
            silver INTEGER,
            electrum INTEGER,
            gold INTEGER,
            platinum INTEGER,
            temp_hp INTEGER,
            hit_dice TEXT,
            prof_bonus INTEGER  
                   
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()




    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('Fixing my Life'))
        print(f'{bot.user} has connected to Discord!')

    # @bot.event
    # async def on_message(message):

    #     if message.content == "Hello".lower():
    #         await message.channel.send("Hi!")

    #     #if message.content.startswith('!r'):

    #     await bot.process_commands(message)

    @bot.command(aliases=['roll', 'r'])
    async def rollDice(ctx,*, message):
        #print(message)
        try:
            #_, command = message.split(' ', 1)
            command = message.replace(' ', '')  # Remove any spaces in the command

            match = re.match(r"(\d*)d(\d+)([+-]\d+)?", command)
            if match:
                rolls = int(match.group(1)) if match.group(1) else 1
                limit = int(match.group(2))
                modifier = int(match.group(3)) if match.group(3) else 0

                results = [random.randint(1, limit) for _ in range(rolls)]
                total = sum(results) + modifier

                await ctx.send(f"Rolling {rolls}d{limit} + {modifier}: {results}\nTotal: {total}")
                
            else:
                raise ValueError
        except (ValueError, ZeroDivisionError):
            await ctx.send('Invalid command. Please use the format `!r NdM +/- X` or a valid mathematical expression.')

    @bot.command()
    async def ping(ctx):
        await ctx.reply(f"Pong! {round(bot.latency * 1000)}ms")

    @bot.command(aliases=['8ball', 'test'])
    async def eightball(ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Detter not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                     "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "my reply is no.", "ny sources say no.",
                    "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "signs point to yes.", "very doubtful.", "Without a doubt.",
                    "yes.", "yes - definitely.", "You may rely on it."]
        try:
            await ctx.send(f"**Question: ** {question}\n**Answers:** {random.choice(responses)}")
        except:
            await ctx.send("No question has been asked")

    @bot.command()
    async def userinfo(ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        roles = [role.name for role in user.roles[1:]]  # Exclude @everyone role

        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No Roles", inline=False)
        #embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Created Account", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member:discord.Member, *, reason=None):
        if reason == None:
            reason = "no reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f"User {member.mention} has been kicked for {reason}")

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member:discord.Member, *, reason=None):
        if reason == None:
            reason = "no reason provided"
        await ctx.guild.ban(member)
        await ctx.send(f"User {member.mention} has been banned for {reason}")

    @bot.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,15, commands.BucketType.user)
    async def unban(ctx, member:discord.User, *, reason=None):
        if reason == None:
            reason = f"No Reason Provided"
        try:
            await ctx.guild.unban(member, reason=reason)
        except:
            await ctx.send("An error occured while unbanning the user")
            return
        await ctx.send(f"{member.mention} has been **unbanned**", delete_after=15)
        
        # await ctx.message.delete()
        print(f"Sucsessfully unbanned {member.name}")

    @bot.command(invoke_without_command=True)
    async def help(ctx, member:discord.Member = None):
        if member == None:
            member = ctx. author
        

        embed = discord.Embed(title="These are the commands you can use:", description="These are the commands you may use (global/private):", colour=discord.Colour.pink())
        embed.set_author(name="StakBuuh", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="`![roll|r] NdM +/- X`", value="roll a NdM dice plus modifier (global)", inline=False)
        embed.add_field(name="`!ping`", value="to ping an user (global)",inline=False)
        embed.add_field(name=" `[!8bball|test]`", value="yes or no question (global)",inline=False)
        embed.add_field(name="`!userinfo <user>`", value="get information about an user (global)",inline=False)
        embed.add_field(name="`!userinfo`", value="get information about yourself (global)",inline=False)
        embed.add_field(name="`!ping`", value="to ping an user (global)",inline=False)
        embed.add_field(name="`!help`", value="get help with the commands (global)", inline=False)
        embed.add_field(name="`!kick <user> <reason>`", value="kick an user (private)", inline=False)
        embed.add_field(name="`!ban <user> <reason>`", value="ban an user (private)", inline=False)
        embed.add_field(name="`!unban <user> <reason>`", value="unban an user (private)", inline=False)
        embed.add_field(name="`!character <name/id>`", value="view character information (global)", inline=False)
        embed.add_field(name="`!character new <name>`", value="create a new character (global)", inline=False)
        embed.add_field(name="`!character set <name/id> <target=new_value>`", value="update character information (global)", inline=False)
        embed.add_field(name="`!abilities <character_id>`", value="view character abilities (global)", inline=False)
        embed.add_field(name="`!abilities <character_id> <target=new_value>`", value="update character abilities (global)", inline=False)
        embed.add_field(name="`!health <character_id>`", value="view character health (global)", inline=False)
        embed.add_field(name="`!health <character_id> <(-)amount>[m/t]`", value="update character health [max HP/temp HP] (global)", inline=False)
        embed.add_field(name="`!health <character_id> <(-)amount>`", value="update character current health (global)", inline=False)
        await ctx.send(embed=embed)

    # character build up

    @bot.command()
    async def character(ctx, action: str = None, name: str = None, *, data_list: str = None):
        # Connect to the database
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()

        if action != "new" and action != "set" and action != "view":
            data_list = name
            name = action
            action = None
        print(f"action: {action}, name: {name}, data_list: {data_list}")
        if action != None:
            if name == None:
                await ctx.send("Please specify a character name!")
                return
            
            if (action.lower() == 'new'):
                # Insert the new character into the database
                cursor.execute('''
                    INSERT INTO characters (
                        character_name,
                        thumbnail,
                        class,
                        race,
                        level,
                        xp,
                        player_name,
                        alignment,
                        backstory,
                        armor_class,
                        initiative,
                        speed,
                        inspiration,
                        max_hp,
                        current_hp,
                        death_saves,
                        strength,
                        dexterity,
                        constitution,
                        intelligence,
                        wisdom,
                        charisma,
                        strength_mod,
                        dexterity_mod,
                        constitution_mod,
                        intelligence_mod,
                        wisdom_mod,
                        charisma_mod,
                        copper,
                        silver,
                        electrum,
                        gold,
                        platinum,
                        temp_hp,
                        hit_dice

                    )
                    VALUES (?, '', '', '', 0, 0, '', '', '', 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0, 0)
                ''', (name,))

                # Get the ID of the newly inserted character
                character_id = cursor.lastrowid

                # Commit the changes
                conn.commit()

                await ctx.send(f"New character table created for {name}.  `({character_id})`")
            # Update character information
            elif action.lower() == 'set' and data_list != None:
                # Connect to the database
                conn = sqlite3.connect('character_database.db')
                cursor = conn.cursor()
                character_id = name.lower()
                temp_name = name.lower()
                # Parse the data_list into a dictionary
                data_dict = {}
                try:
                    data_pairs = data_list.split(',')
                    for pair in data_pairs:
                        name, value = pair.strip().split('=')
                        data_dict[name.strip()] = value.strip()
                except Exception as e:
                    await ctx.send(f"Invalid data format: {e}")
                    return

                # Update character information in the database
                update_query = 'UPDATE characters SET '
                update_params = []
                for name, value in data_dict.items():
                    update_query += f"{name} = ?, "
                    update_params.append(value)

                #check if id is in the database
                cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
                character_data = cursor.fetchone()
                if character_data:
                    update_query = update_query[:-2] + f" WHERE character_id = ?"
                    update_params.append(character_id)
                    cursor.execute(update_query, update_params)
                    conn.commit()
                    await ctx.send(f"Character ID {character_id} updated successfully.")
                else:
                    cursor.execute('SELECT * FROM characters WHERE character_name = ?', (temp_name,))
                    character_data = cursor.fetchone()
                    if character_data:
                        update_query = update_query[:-2] + f" WHERE character_name = ?"
                        update_params.append(temp_name)
                        cursor.execute(update_query, update_params)
                        conn.commit()
                        await ctx.send(f"Character ID {character_id} updated successfully.")
                    else:
                        await ctx.send(f"Unable to set Character.")

        # View character information
        elif action == None and name != None:
            character_id = name.lower()
            
            # Fetch character information from the database
            cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
            character_data = cursor.fetchone()

            # check if name is character_name and not character_id
            cursor.execute('SELECT * FROM characters WHERE character_name = ?', (character_id,))
            character_data2 = cursor.fetchone()

            if character_data == None and character_data2 != None:
                character_data = character_data2

            if character_data:
                # Extract the relevant character information
                character_name = character_data[1]
                character_thumbnail = character_data[2]
                character_class = character_data[3]
                character_race = character_data[4]
                character_level = character_data[5]
                character_xp = character_data[6]
                character_player_name = character_data[7]
                character_alignment = character_data[8]
                character_backstory = character_data[9]
                character_armor_class = character_data[10]
                character_initiative = character_data[11]
                character_speed = character_data[12]
                character_inspiration = character_data[13]
                character_death_saves = character_data[16]
                character_hit_dice = character_data[35]

                # Extract other character information accordingly

                # Create an embedded message
                embed = discord.Embed(title="Character Info", color=discord.Color.blue())
                if character_thumbnail == '':
                    embed.set_thumbnail(url=native_thumbnail)
                else:
                    embed.set_thumbnail(url=character_thumbnail)
                embed.set_author(name=character_name)
                embed.add_field(name="Class", value=character_class, inline=True)
                embed.add_field(name="Race", value=character_race, inline=True)
                embed.add_field(name="Level", value=character_level, inline=True)
                embed.add_field(name="XP", value=character_xp, inline=True)
                embed.add_field(name="Player Name", value=character_player_name, inline=True)
                embed.add_field(name="Alignment", value=character_alignment, inline=True)
                embed.add_field(name="Backstory", value=character_backstory, inline=True)
                embed.add_field(name="Armor Class", value=character_armor_class, inline=True)
                embed.add_field(name="Initiative", value=character_initiative, inline=True)
                embed.add_field(name="Speed", value=character_speed, inline=True)
                embed.add_field(name="Inspiration", value=character_inspiration, inline=True)
                embed.add_field(name="Death Saves", value=character_death_saves, inline=True)
                embed.add_field(name="Hit Dice", value=character_hit_dice, inline=True)
                embed.add_field(name="Profiency Bonus", value=character_data[36], inline=True)

                # Add other fields accordingly
                conn.commit()
                await ctx.send(embed=embed)
            else:
                conn.commit()
                await ctx.send("Character not found.")
            conn.close()
        
        

        else:
            await ctx.send("Invalid argument!")
            conn.close()


    @bot.command()
    async def abilities(ctx, character_id: str):
       
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()

        # Fetch character information from the database
        cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
        character_data = cursor.fetchone()
            # check if name is character_name and not character_id
        cursor.execute('SELECT * FROM characters WHERE character_name = ?', (character_id,))
        character_data2 = cursor.fetchone()

        if character_data == None and character_data2 != None:
            character_data = character_data2

        # view character information
        if character_data:
            # Extract the relevant character information
            character_name = character_data[1]
            character_thumbnail = character_data[2]
            character_strength = character_data[17]
            character_dexterity = character_data[18]
            character_constitution = character_data[19]
            character_intelligence = character_data[20]
            character_wisdom = character_data[21]
            character_charisma = character_data[22]
            character_strength_mod = character_data[23]
            character_dexterity_mod = character_data[24]
            character_constitution_mod = character_data[25]
            character_intelligence_mod = character_data[26]
            character_wisdom_mod = character_data[27]
            character_charisma_mod = character_data[28]

            # Create an embedded message
            embed = discord.Embed(title="Character Abilities", color=discord.Color.pink())
            embed.set_author(name=character_name)
            
            if character_thumbnail == '':
                embed.set_thumbnail(url=native_thumbnail)
            else:
                embed.set_thumbnail(url=character_thumbnail)
            embed.add_field(name="Strength", value=f"{character_strength} ({character_strength_mod})", inline=True)
            embed.add_field(name="Dexterity", value=f"{character_dexterity} ({character_dexterity_mod})", inline=True)
            embed.add_field(name="Constitution", value=f"{character_constitution} ({character_constitution_mod})", inline=True)
            embed.add_field(name="Intelligence", value=f"{character_intelligence} ({character_intelligence_mod})", inline=True)
            embed.add_field(name="Wisdom", value=f"{character_wisdom} ({character_wisdom_mod})", inline=True)
            embed.add_field(name="Charisma", value=f"{character_charisma} ({character_charisma_mod})", inline=True)

            conn.commit()
            await ctx.send(embed=embed)
        else:
            conn.commit()
            await ctx.send("Character not found.")
        
        conn.close()


    @bot.command()
    async def health(ctx, character_id: str, modifier: str = None):
        # Connect to the database
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        print(f"character_id: {character_id}, modifier: {modifier}")
        # Fetch character information from the database
        cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
        character_data = cursor.fetchone()
        # check if name is character_name and not character_id
        cursor.execute('SELECT * FROM characters WHERE character_name = ?', (character_id,))
        character_data2 = cursor.fetchone()

        if character_data == None and character_data2 != None:
            character_data = character_data2

        if character_data:
            # Extract the relevant character information
            character_name = character_data[1]
            character_thumbnail = character_data[2]
            character_max_hp = character_data[14]
            character_current_hp = character_data[15]
            character_temp_hp = character_data[34]

            if modifier is not None:
                
                modifier_type = modifier[-1]

                if modifier_type == 'm':
                    modifier_value = int(modifier[:-1])
                    character_max_hp += modifier_value
                elif modifier_type == 't':
                    modifier_value = int(modifier[:-1])
                    character_temp_hp += modifier_value
                else:
                    character_current_hp += int(modifier)

                # Update the character's health information in the database
                cursor.execute('UPDATE characters SET max_hp = ?, current_hp = ?, temp_hp = ? WHERE character_id = ?',
                            (character_max_hp, character_current_hp, character_temp_hp, character_id))
                conn.commit()

            # Create an embedded message
            embed = discord.Embed(title="Character Health", color=discord.Color.red())
            embed.set_author(name=character_name)
            if character_thumbnail == '':
                embed.set_thumbnail(url=native_thumbnail)
            else:
                embed.set_thumbnail(url=character_thumbnail)
            embed.add_field(name="Max HP", value=character_max_hp, inline=True)
            embed.add_field(name="Current HP", value=character_current_hp, inline=True)
            embed.add_field(name="Temporary HP", value=character_temp_hp, inline=True)

            # Add other fields accordingly

            await ctx.send(embed=embed)
        else:
            await ctx.send("Character not found.")

        # Close the database connection
        conn.close()

    @bot.command()
    async def hp(ctx, character_id: str, modifier: int = 0):
        print(f"character_id: {character_id}, modifier: {modifier}")
        # Connect to the database
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()

        # Fetch character information from the database
        cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
        character_data = cursor.fetchone()
        # check if name is character_name and not character_id
        cursor.execute('SELECT * FROM characters WHERE character_name = ?', (character_id,))
        character_data2 = cursor.fetchone()

        if character_data == None and character_data2 != None:
            character_data = character_data2
            

        if character_data:
            character_id = character_data[0] # ID
            character_level = character_data[5] # Level
            character_xp = character_data[6] + modifier # XP + modifier
            print(f"character_level: {character_level}, character_xp: {character_xp}")
            character_hit_dice = character_data[35] # Hit dice
            character_constitution = character_data[25] # Constitution modifier
            if character_hit_dice == '':
                await ctx.send("Character has no hit dice.")
                return
            mult, dice = character_hit_dice.split('d')
            hit_dice = int(mult) * int(dice)

            if character_level < 1:
                await ctx.send("Character level must be at least 1.")
            else:
                # Check if XP reaches the threshold to increment level and upgrade HP
                xp_thresholds = [0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000, 100000, 120000,
                                140000, 165000, 195000, 225000, 265000, 305000, 355000]

                if character_level < 20 and character_xp >= xp_thresholds[character_level]:
                    while character_level < 20 and character_xp >= xp_thresholds[character_level]:
                        character_level += 1

                    # Calculate the new max HP based on level and hit dice
                    if character_level == 1:
                        max_hp = 20 + character_constitution
                    else:
                        max_hp = character_level * hit_dice + 20 + character_constitution

                    # Update character level and max HP in the database
                    cursor.execute('UPDATE characters SET level = ?, xp = ?, max_hp = ? WHERE character_id = ?',
                                (character_level, character_xp, max_hp, character_id))
                    conn.commit()

                    await ctx.send(f"Character level increased to {character_level}. Max HP upgraded to {max_hp}.")
                else:
                    cursor.execute('UPDATE characters SET xp = ? WHERE character_id = ?', (character_xp, character_id))
                    conn.commit()
                    await ctx.send(f"Character XP is not sufficient to level up. Updated to {character_xp}.")
        else:
            await ctx.send("Character not found.")

        # Close the database connection
        conn.close()

    @commands.has_permissions(administrator=True)
    @bot.command()
    async def server(ctx, action: str = None):
        if action == None:
           
            guild = ctx.guild

            # Get general server information
            server_name = guild.name
            server_id = guild.id
            server_owner = guild.owner.name
            server_roles = guild.roles
            server_member_count = guild.member_count

            roles = [role.name for role in guild.roles[1:]]  # Exclude @everyone role

            # Create an embedded message
            embed = discord.Embed(title="Server Information", color=discord.Color.green())
            embed.add_field(name="Server Name", value=server_name, inline=True)
            embed.add_field(name="Server ID", value=server_id, inline=True)
            embed.add_field(name="Server Owner", value=server_owner, inline=True)
            embed.add_field(name="Server Roles", value=", ".join(roles) if roles else "No Roles", inline=True)
            embed.add_field(name="Member Count", value=server_member_count, inline=True)

            await ctx.send(embed=embed)
        elif action.lower() == 'members':
            guild = ctx.guild
            members = guild.members
            member_list = []
            for member in members:
                member_list.append(member.name)
            await ctx.send(f"{member_list}")

        elif action.lower() == 'restart':
            await ctx.send("Restarting bot")
            restart_bot()

    @commands.has_permissions(administrator=True)
    @bot.command()
    async def add_field(ctx, field_name: str, default_value: str = ''):
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        # Add a new field to the character table with a default value
        cursor.execute(f'ALTER TABLE characters ADD COLUMN {field_name} TEXT DEFAULT {default_value}')
        conn.commit()
        await ctx.send(f"Field '{field_name}' added successfully with default value '{default_value}'.")





























    bot.run(TOKEN)