

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there"
    
    if p_message == "errado":
        return "Chão"
    
    if p_message == "!help":
        return "`This is a help message that you can modify.`"
    
    return "Wtf did you just said?"