#Can be further improved later will need access to the order.py file to import total from

from order import Total;

def validateCard(cardNumber, expiryDate, cvv):
    
    if(cardNumber.length==16 and expiryDate.length==4 and cvv.length==3):
        return True
    else:
        return False  
    
def pay(user, Total):
    
    if(user.card==null){
        print("No card on file, please enter card")
        userAddCard();
    }

    if