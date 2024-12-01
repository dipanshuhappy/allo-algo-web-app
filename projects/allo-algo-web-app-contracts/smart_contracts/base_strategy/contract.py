import algopy
from algopy import Contract, ARC4Contract, String, Account, UInt64, arc4, Bytes
from algopy.arc4 import DynamicArray, Address, Struct


class PayoutSummary(arc4.Struct):
    recipientAddress: arc4.Address
    amount: arc4.UInt64

class BaseStrategy(ARC4Contract):
    def __init__(self) -> None:
        self.alloContractId = Address()
        self.strategyId = String()
        self.poolActive: bool = False
        self.poolId = UInt64(0)
        self.poolAmount = UInt64(0)

    @arc4.abimethod()
    def initializeVariables(self, _alloContractId: Address, _strategyId: String) -> None:
        self.__OnlyAllo()
        self.alloContractId = _alloContractId
        self.strategyId = _strategyId

    @algopy.subroutine
    def __OnlyAllo(self) -> None :
        assert algopy.Txn.sender == self.alloContractId, "only allo contract can call this function"

    @algopy.subroutine
    def __OnlyInitialized(self) -> None :
        assert self.poolId !=0, "pool is not initialized"

    @arc4.abimethod()
    def getAlloContractId(self) -> Address :
        return self.alloContractId

    @arc4.abimethod()
    def getPoolId(self) -> UInt64 :
        return self.poolId

    @arc4.abimethod()
    def getStrategyId(self) -> String :
        return self.strategyId

    @arc4.abimethod()
    def getPoolAmount(self) -> UInt64 :
        return self.poolAmount

    @arc4.abimethod()
    def isPoolActive(self) -> bool :
        return self.poolActive

    @arc4.abimethod()
    def baseStrategy_init(self, _poolId: UInt64) -> None :
        self.__OnlyAllo()
        assert self.poolId == 0, "pool already initialized"
        assert _poolId != 0, "invalid pool id" 
        self.poolId = _poolId

    @arc4.abimethod()
    def increasePoolAmount(self, _amount: UInt64) -> None :
        self.__OnlyAllo()
        self.poolAmount += _amount

        # receipient register
    @arc4.abimethod()   
    def registerRecipient(self, _data: Bytes, _sender: Account) -> None:
        pass

    @arc4.abimethod()
    def beforeRegisterRecipient(self, data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def afterRegisterRecipient(self, data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def register_Recipient(self, _data: Bytes, _sender: Account) -> None :
        self.__OnlyAllo()
        self.__OnlyInitialized()
        self.beforeRegisterRecipient(_data, _sender)
        self.registerRecipient(_data, _sender)
        self.afterRegisterRecipient(_data, _sender)

    # allocate
    @arc4.abimethod()
    def allocate(self, _data: Bytes, _sender: Account) -> None:
        pass

    @arc4.abimethod()
    def beforeAllocate(self, data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def afterAllocate(self, data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def Allocate(self, _data: Bytes, _sender: Account) -> None:
        self.__OnlyAllo()
        self.beforeAllocate(_data, _sender)
        self.allocate(_data, _sender)
        self.afterAllocate(_data, _sender)

    # distribute
    @arc4.abimethod()   
    def distribute(self, _recipientIds: DynamicArray[Address], _data: Bytes, _sender: Account) -> None:
        pass

    @arc4.abimethod()
    def beforeDistribute(self, _recipientIds: DynamicArray[Address], _data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def afterDistribute(self, _recipientIds: DynamicArray[Address], _data: Bytes, sender: Account) -> None:
        pass

    @arc4.abimethod()
    def Distribute(self, _recipientIds: DynamicArray[Address], _data: Bytes, _sender: Account) -> None:
        self.__OnlyAllo()
        self.__OnlyInitialized()
        self.beforeDistribute(_recipientIds, _data, _sender)
        self.distribute(_recipientIds, _data, _sender)
        self.afterDistribute(_recipientIds,_data, _sender)

    # payouts
    @arc4.abimethod()   
    def getPayOut(self, _recipientIds: Address, _data: Bytes) -> None:
        pass

    # @arc4.abimethod()
    # def GetPayout(self, _recipientIds: DynamicArray[Address], _data: DynamicArray[Bytes]) -> None:
    #     recipientLength = _recipientIds.length
    #     assert recipientLength == _data.length, "recipient and data length mismatch"
    #     for i in range(recipientLength):
    #         self.getPayOut(_recipientIds[i], _data[i])