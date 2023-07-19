import random

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hi' or p_message == 'hello':
        return 'Hello! there I am a bot'
    
    if p_message[0] == 'r':
        arr = []
        total = 0
        result = ''
        rolls = int(p_message[1])
        if p_message[2] == 'd':
            dice = int(p_message[3:])
            for i in range(0,rolls):
                num = random.randint(1, dice)
                total = total + num
                arr.append(num)
            result = f'{arr} sum: {total}'
            return result
        elif p_message[3] == 'd':
            rolls = int(p_message[1:3])
            
            dice = int(p_message[4:])
            for i in range(0,rolls):
                num = random.randint(1, dice)
                total = total + num
                arr.append(num)
            result = f'{arr} sum: {total}'
            return result
        else:
            return "wrong input - use up to 99d"

    
    if p_message == 'help':
        return "`To use this bot, type ! followed by the command. \n\nCommands: \n!hi or !hello - To greet the bot \n!1d6 - To roll a 6 sided dice \n!help - To get this message`"
    
    #return 'I don\'t understand you. Please type !help to get a list of commands'