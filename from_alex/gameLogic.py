throw_sequence = ["p","r","s","s","r","p","r","p","r","s","p","s","s","s","s","p","p","p","s","s","s","s","r","p","s","r","s","r","p","s","s","p","s","r","s","s","p","s","p","p"]

def validated(choice):
    if choice.lower() not in "rps": return False
    return True

def naoWon(nao_choice, human_choice):
    """Returns a string that nao "win", "lose" or 
    that it was a "draw".

    If there was an input error, returns "error"
    
    nao_choice is assumed to be "r", "p", or "s"
    
    human_choice is assumed to be "r", "p", or "s"
    """
    nc = nao_choice.lower()
    hc = human_choice.lower()

    if (nc==hc): return "draw"
    if (nc=="r" and hc=="p"): return "lose"
    if (nc=="r" and hc=="s"): return "win"
    if (nc=="p" and hc=="s"): return "lose"
    if (nc=="p" and hc=="r"): return "win"
    if (nc=="s" and hc=="r"): return "lose"
    if (nc=="s" and hc=="p"): return "win"

def choiceThatBeats(choice):
    if choice=="r": return "p"
    if choice=="p": return "s"
    if choice=="s": return "r"

def choiceThatLosesTo(choice):
    if choice=="r": return "s"
    if choice=="p": return "r"
    if choice=="s": return "p"

def choiceThatDraws(choice):
    return choice
