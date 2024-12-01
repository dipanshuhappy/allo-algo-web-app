import algopy
from algopy import arc4, ARC4Contract, Box, BoxMap, Txn, Account, Contract
from algopy.arc4 import DynamicArray, Address, Struct, String

class proposalData(arc4.Struct):
   payoutAddress: arc4.Address 
   uniqueDonations: arc4.UInt64
   directDonations: arc4.UInt64
   donators: DynamicArray[arc4.Address]
   finalAllocation: arc4.UInt64


class QuadraticFunding(algopy.ARC4Contract):
    def __init__(self) -> None:
        self.totalFunds = algopy.UInt64(0)
        self.index = algopy.UInt64(0)
        self.proposals = BoxMap(algopy.UInt64, proposalData)
    @arc4.abimethod()
    def getFinalAllocation(self,proposalId:algopy.UInt64) -> algopy.UInt64:
        return self.proposals[proposalId].finalAllocation.native

    @arc4.abimethod()
    def getDirectDonations(self,proposalId:algopy.UInt64) -> algopy.UInt64:
        return self.proposals[proposalId].directDonations.native
    @arc4.abimethod()
    def getUniqueDonations(self,proposalId:algopy.UInt64) -> algopy.UInt64:
        return self.proposals[proposalId].uniqueDonations.native
    
    @arc4.abimethod()
    def getDonators(self,proposalId:algopy.UInt64) -> DynamicArray[arc4.Address]:
        return self.proposals[proposalId].donators.copy()
    
    @arc4.abimethod()
    def createProposal(self,payoutAddress: algopy.Account) -> None:
        new_proposal = proposalData(
           directDonations=arc4.UInt64(0),
           payoutAddress=arc4.Address.from_bytes(payoutAddress.bytes),
           uniqueDonations=arc4.UInt64(0),
           finalAllocation=arc4.UInt64(0),
           donators=DynamicArray[arc4.Address]()
        )
        self.proposals[self.index] = new_proposal.copy()
        self.index = self.index + algopy.UInt64(1)

    @arc4.abimethod()
    def distribute(self) -> None:
        
        for i in algopy.urange(0, self.index):
            proposal = self.proposals[i].copy()
            finalPayout = proposal.finalAllocation.native
            finalRecipient = proposal.payoutAddress
            algopy.itxn.Payment(
                amount=finalPayout,
                fee=1000,
                receiver=finalRecipient.native
            ).submit()

    @arc4.abimethod()
    def allocate(self) -> None:
        totalVotes = algopy.UInt64(0)
        for proposal_id in algopy.urange(0, self.index):
            proposal = self.proposals[proposal_id].copy()
            sqrtVotes : algopy.UInt64 = algopy.op.sqrt(proposal.directDonations.native)
            totalVotes += sqrtVotes
        for proposal_id in algopy.urange(0, self.index):
            proposal = self.proposals[proposal_id].copy()
            sqrt_votes : algopy.UInt64 =  algopy.op.sqrt(proposal.directDonations.native)
            share = algopy.op.btoi(algopy.op.itob((sqrt_votes) * self.totalFunds // totalVotes ))
            proposal.finalAllocation = arc4.UInt64.from_bytes(algopy.op.itob(share))
            self.proposals[proposal_id] = proposal.copy()
        self.totalFunds = algopy.UInt64(0)

    @arc4.abimethod()
    def donate(self,proposalId:algopy.UInt64,amountMicroAlgo:algopy.UInt64 ) -> None:
        proposal = self.proposals[proposalId].copy()
        senderBytesAddress = arc4.Address.from_bytes(algopy.Txn.sender.bytes)
      
        
        if value_exists(proposal.donators.copy(),senderBytesAddress):
           proposal.uniqueDonations = arc4.UInt64.from_bytes(algopy.op.itob(proposal.uniqueDonations.native +  algopy.UInt64(1)))
           proposal.donators.append(senderBytesAddress)
        proposal.directDonations = arc4.UInt64.from_bytes(algopy.op.itob(proposal.directDonations.native + amountMicroAlgo))
        self.totalFunds = self.totalFunds + amountMicroAlgo
        self.proposals[proposalId] = proposal.copy()

@algopy.subroutine
def value_exists(array:arc4.DynamicArray[arc4.Address], value:arc4.Address) -> bool:
    for item in array:
        if item == value:
            return True
    return False

