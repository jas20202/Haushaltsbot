'''
- Help message aus helpmessage.txt
- Task help
'''

def get_help_message():
    f = open("helpmessage.txt", "r")
    message = f.read()
    return message