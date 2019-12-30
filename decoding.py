########################################## -------Bismillah Al Rahman Al Raheem------- ################################################
import socket
import sys
import time
from functions import Chars_to_Bits, PC1, Left_Shift, PC2, IP, Expension_Table, XOR_48_Bits, S_Boxes_Values, Permutation, XOR_32_Bits, Swap_32_Bits, IP_Inverse, Char_to_Bits, Bits_to_Text 
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> KEYS GENERATION CODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def MAIN():
    s = socket.socket()
    host = socket.gethostname()     
    port = 8080
    s.connect((host,port))
    print('Successfullly connect with Server: ',socket.gethostname())

    while 1:
        receiveMessage = s.recv(2048)
        receiveMessage = receiveMessage.decode()
        #print(receiveMessage)        
      
        userKey = '12345678'
            
        initialBitsString = ''  #holds user key PT converted to 64 bits string.
        keyLeftBits = ''    #holds first 32 bits of initialBitsString.
        keyRightBits = ''   #holds last 32 bits of initialBitsString.
        roundsKeysList = ['X']  #>>hold keys for all 16 rounds.
        
        initial64BitsString = Chars_to_Bits(userKey)
        keyLeftBits,keyRightBits = PC1(initial64BitsString)

        for roundNo in range(1,17):
            combineLeftShiftBits = 'X'
            keyLeftBits = Left_Shift(str(roundNo),keyLeftBits)    
            keyRightBits = Left_Shift(str(roundNo),keyRightBits)    
            combineLeftShiftBits += keyLeftBits + keyRightBits    
            roundsKeysList.append(PC2(combineLeftShiftBits))

        roundsKeysList.reverse() #reversing the keys to use from Key-16 for decoding.
            
        CT64BitsList = []    #every item hold 8 characters from PT.
        roundLeft32Bits = ''    #hold left 32 bits for each round.
        roundRight32Bits = ''   #hold right 32 bits for each round.
        roundRight32BitsBackup = '' #hold right 32 bits for each round to assign value to roundLeft32Bits after completion of each round.
        final64Bits = ''    #hold 64 bits after completion of all 16 rounds.
        CT = 'X' #hold Cipher Text of 64 bits.
        CTList = [] #it will hold CT bits of group of 8 characters.
        decodedPTList = [] 
        
        #print(receiveMessage)
        #print(len(receiveMessage))
        CT64BitsList.append(receiveMessage)
        #CT64BitsList = [rm.strip() for rm in receiveMessage]
        
        for CT64Bits in CT64BitsList:   
            pt64BitsString = 'X'+ CT64Bits 
            roundLeft32Bits,roundRight32Bits = IP(pt64BitsString)    

            #<<<<<< Rounds Loop >>>>>>
            for key in roundsKeysList:
                if key == 'X':
                    continue    
            
                expanded48Bits = ''     #hold 48 bits after expanded roundRight32Bits from expansion table.
                expAndKeyXor48Bits = '' #hold result after XOR of expanded48Bits and Key of individual round.
                SBoxContract32Bits = 'X' #hold value from SBoxes eight tables and converted them(int values) to 32 bits binary.
            
                expanded48Bits = Expension_Table(roundRight32Bits)
                expAndKeyXor48Bits = XOR_48_Bits(expanded48Bits,key)    

                SBoxValuesList = S_Boxes_Values(expAndKeyXor48Bits)
                for num in SBoxValuesList:
                    if num == 'X':
                        continue    
                    SBoxContract32Bits += '{0:04b}'.format(num)
            
            
                perm32Bits = Permutation(SBoxContract32Bits)    
                roundRight32BitsBackup = roundRight32Bits
                roundRight32Bits = 'X' + XOR_32_Bits(perm32Bits,roundLeft32Bits)   
                roundLeft32Bits = roundRight32BitsBackup  
           

            final64Bits = roundLeft32Bits[1:] + roundRight32Bits[1:]
            final64Bits = Swap_32_Bits(final64Bits)
            final64Bits = 'X' + final64Bits
            CT = IP_Inverse(final64Bits)
            CTList.append(CT)
            

        for CT in CTList:
            decodedPTList.append(Bits_to_Text(CT))

        print('server# ',''.join(decodedPTList))

        sendMessage = input(str('YOU>> '))
        sendMessage = sendMessage.encode()
        s.send(sendMessage)
        
       
try:
    MAIN()
except Exception as ex:
    print(ex)



