
class NumBloom :
    '''A bloom filter for numeric or numeric-like strings'''

    def __init__(self, length, funcs) :
        '''Initiation'''
        # A sequence such as 
        # 123456 654321
        #|--pri-|-sec--|
        # lastCheck = pri + sec
        self.primary = bytearray(1024 * 128)
        self.secondary = bytearray(1024 * 128)
        self.lastCheck = bytearray(1024 * 128)
        
        self.pri = 0x01
        self.sec = 0x02
        self.last = 0x03

    def filtration(self, sequence) :
        ''' Filter '''
        num = int(sequence)
        sec = int(num % 1000000)
        pri = int(num / 1000000 % 1000000)
        num = sec + pri
        state1 = self.checkAndSet(self.pri, pri, True)
        state2 = self.checkAndSet(self.sec, sec, True)
        state3 = self.checkAndSet(self.last, num, True)
        if state1 is not True :
            self.checkAndSet(self.pri, pri, False)
        if state2 is not True :
            self.checkAndSet(self.sec, sec, False)
        if state3 is not True :
            self.checkAndSet(self.last, num, False)

        if state1 and state2 and state3 :
            print('element exists...')
        else :
            print('new element...')

    def checkAndSet(self, which, index, isCheck) :
        '''index :positon of the candidate
        isCheck  :True to check or False to set 1 at the position'''

        byteAt = int(index / 8)
        bitAt = index % 8
        mask = 0x01 << bitAt
        if which == self.pri : 
            if isCheck is True :
                return mask == (self.primary[byteAt] & mask)
            else :
                self.primary[byteAt] |= mask

        elif which == self.sec : 
            if isCheck is True :
                return mask == (self.secondary[byteAt] & mask)
            else :
                self.secondary[byteAt] |= mask
        elif which == self.last : 
            if isCheck is True :
                return mask == (self.lastCheck[byteAt] & mask)
            else :
                self.lastCheck[byteAt] |= mask

