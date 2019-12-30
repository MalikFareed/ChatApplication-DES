########################################'-------Bismillah Al Rahman Al Raheem-------'###################################################
import binascii

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> KEYS GENERATION METHODS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#it will convert 8-characters user key into 64-bits binary string.
def Chars_to_Bits(_userKey):
    bitsString = 'X'
    bits_list = []
    bits_list.append('X')

    for char in _userKey:    #converting and adding into list every character of key into 8 bits binary.
        bits_list.append(f'{ord(char):08b}')
        bitsString += f'{ord(char):08b}'

    return bitsString

#it converts 64-bits user key into left-28 and right-28 bits.
def PC1(_initialBitsString):
    left_bits = ''
    right_bits = ''
    
    #initializing standard table of PC-1.
    pc1LeftStandardTable = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36]
    pc1RightStandardTable = [63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]

    for index in pc1LeftStandardTable:  #adding 28 bits in left table as per indexing of PC1 left table.
        left_bits += _initialBitsString[index]

    for index in pc1RightStandardTable:  #adding 28 bits in right table as per indexing of PC1 right table.
        right_bits += _initialBitsString[index]

    return left_bits,right_bits


#it give bit(s) shift to 28-bits string as per rounds requirement.
def Left_Shift(_round,_bitsString):
    leftShiftSchedule = {'1':1,'2':1,'3':2,'4':2,'5':2,'6':2,'7':2,'8':2,'9':1,'10':2,'11':2,'12':2,'13':2,'14':2,'15':2,'16':1}

    shiftValue = leftShiftSchedule.get(_round)
   
    leftShiftBits = [bit for bit in _bitsString]

    for num in range(1,shiftValue+1):        
        leftShiftBits.append(leftShiftBits.pop(0))

    leftShiftedBitsString = ''
    for bit in leftShiftBits:
        leftShiftedBitsString += bit
        
    return leftShiftedBitsString


#it will take 56-bits and generate a key.
def PC2(_56bitsString):
    key = ''
    
    pc2StanderdTable = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
    
    for index in pc2StanderdTable:
        key += _56bitsString[index]

    return key


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MAIN FLOW's METHODS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#it take chunk of 8-characters and convert that to 64-bits string.
def Char_to_Bits(_pt):
    pt64BitsString = 'X' #it will hold all 64 bits that will be converting from each character(8-bits) of Plain Text.
    
    for char in _pt:
        pt64BitsString += f'{ord(char):08b}'

    return pt64BitsString


#it will 64-bits of PT and convert that to Left32Bits and Right32Bits after swaping values according to IP table.
def IP(_64BitsString):    
    ipIndexedBits = 'X'  #it will hold 64 bits after swaping bits according to IP standard table.
    left32Bits = 'X' #it will hold first 32 bits of ipIndexedBits.
    right32Bits = 'X'    #it will hold last 32 bits of ipIndexedBits.
    IPStandardTable = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
                       57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]    

    for index in IPStandardTable:
        ipIndexedBits += _64BitsString[index]

    for index in range(1,33):
        left32Bits += ipIndexedBits[index]

    for index in range(33,65):
        right32Bits += ipIndexedBits[index]

    return left32Bits,right32Bits

#it will 32-bits shift to 64-bits string.
def Swap_32_Bits(_64Bits):
    first32Bits = _64Bits[0:32]
    last32Bits = _64Bits[32:]

    _64Bits = last32Bits + first32Bits
    return _64Bits

#it will swap values of 64-bits string and retirn CT(64-bits).
def IP_Inverse(_64Bits):
    IPInverseStandardTable = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,
                              22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,
                              43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

    CT64Bits = ''

    for index in IPInverseStandardTable:
        CT64Bits += _64Bits[index]

    return CT64Bits

#converts int to bytes.
def Int_to_Bytes(_int):
    hexString = '%x' % _int
    n = len(hexString)    
    return binascii.unhexlify(hexString.zfill(n+ (n & 1)))
    
#converts bits to text.
def Bits_to_Text(_bits, encoding = 'utf-8', errors = 'surrogatepass'):
    n = int(_bits,2)
    return Int_to_Bytes(n).decode(encoding,errors)

#######################>>>>>>>>>>>>>>>>>>>>>>> METHODS FOR SINGLE ROUND EXECUTION <<<<<<<<<<<<<<<<<<<<<<<<<############################

#it take 32-bits and expand them to 48-bits usein Expansion table.
def Expension_Table(_right32Bits):
    expensionStandardTable = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,
                              18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
    expanded48Bits = 'X'
    
    for index in expensionStandardTable:
        expanded48Bits += _right32Bits[index]

    return expanded48Bits

#it will XOR Key-48 and Expanded-48 bits and return result.    
def XOR_48_Bits(_expanded48Bits, _48BitsKey):
    expandedInt = int(_expanded48Bits[1:],2)
    keyInt = int(_48BitsKey,2)

    result = expandedInt ^ keyInt
    result = '{0:048b}'.format(result)

    return result

#it will XOR Left-32 and PermutationTable-32 bits and return resulr as next round Right-32 bits.
def XOR_32_Bits(_prem32Bits,_left32Bits):
    permInt = int(_prem32Bits,2)
    leftBitsInt = int(_left32Bits[1:],2)

    result = permInt ^ leftBitsInt
    result = '{0:032b}'.format(result)
    
    return result
    
#it will fetch row and column number(int) for fetching values from S-Box tables.
def Fetch_Row_Col(_8Bits):
    row = _8Bits[0] + _8Bits[-1]
    row = int(row,2)

    col = _8Bits[1:5]
    col = int(col,2)

    return row,col

#it take 48-bits and contract them to 32-bits by fetching values from S-Box tables.
def S_Boxes_Values(_48BitsString):
        S1 = [ [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
               [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13] ]
        S2 = [ [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
               [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9] ]
        S3 = [ [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
               [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12] ]
        S4 = [ [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
               [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14] ]
        S5 = [ [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
               [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3] ]
        S6 = [ [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
               [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13] ]
        S7 = [ [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
               [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12] ]
        S8 = [ [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
               [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11] ]

        SBoxStandardTablesList = [[],S1,S2,S3,S4,S5,S6,S7,S8]
        SBoxes6BitsHolders = [] #it will hold 8 bits holder each contains 6 bits after breaking _48BitsString.
        rowsColsIndexesList = []   #it will hold int value of row,col to fetch SBox value.
        SBoxesValuesList = ['X']

        _48BitsString = list(_48BitsString)
        _48BitsString.reverse()

        for num in range(0,8):
            hold6Bits = ''
            for num in range(0,6):
                hold6Bits += _48BitsString.pop()
                
            SBoxes6BitsHolders.append(hold6Bits)
        
        for item in SBoxes6BitsHolders:
            row,col = Fetch_Row_Col(item)
            rc = row,col
            rowsColsIndexesList.append(rc)
        
        listNo = 1   
        for row,col in rowsColsIndexesList:
            SBoxesValuesList.append(SBoxStandardTablesList[listNo][row][col])
            listNo += 1

        return SBoxesValuesList

        
#it take 32 bits and swap those bits according to P-table and return also 32-bits.
def Permutation(_32Bits):
    permutationStandardTable = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
                                2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
    perm32Bits = ''
    
    for index in permutationStandardTable:
        perm32Bits += _32Bits[index]

    return perm32Bits
    














