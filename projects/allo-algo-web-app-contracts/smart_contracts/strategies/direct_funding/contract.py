import algopy
from algopy import arc4, ARC4Contract, Box, BoxMap, Txn, Account, Contract
from algopy.arc4 import DynamicArray, Address, Struct, String

class proposalData(arc4.Struct):
    proposalId : arc4.UInt64
    proposalTitle : arc4.String
    proposalOwner : arc4.Address
    proposalAmount : arc4.UInt64
    proposalDescription : arc4.String

class DirectDonations(ARC4Contract):

    def __init__(self) -> None:
        self.totalFunds : algopy.UInt64 = algopy.UInt64(0)
        self.totalRewards : algopy.UInt64 = algopy.UInt64(0)
        self.proposer = Account()
        self.platformAdmin = Account()
        self.funder = Account()
        self.funders = BoxMap(algopy.UInt64, DynamicArray[Account])
        self.proposals = BoxMap(algopy.UInt64, proposalData)
        self.proposalFunders = BoxMap(algopy.UInt64, DynamicArray[Account])
        self.funderAmount = BoxMap(Account, algopy.UInt64, key_prefix=b"funder_amount")
        self.isActive : bool = False
        self.isFunder = BoxMap(Account, bool, key_prefix=b"is_funder")
        self.isProposer = BoxMap(Account, bool, key_prefix=b"is_proposer")
        self.isPlatformAdmin = BoxMap(Account, bool, key_prefix=b"is_platform_admin")
        self.proposal_id_incrementer : algopy.UInt64 = algopy.UInt64(0)

    @arc4.abimethod()
    def initialize(self, _proposer: Account, _platformAdmin: Account) -> None:
        self.proposer = _proposer
        self.platformAdmin = _platformAdmin
        self.isProposer[self.proposer] = True
        self.isPlatformAdmin[self.platformAdmin] = True
        self.isActive = True

    @arc4.abimethod()
    def createProposal(self, _proposalTitle: String, _proposalDescription: String) -> None :
        self.__isActive()
        self.proposal_id_incrementer += algopy.UInt64(1)
        new_proposal = proposalData(
            proposalId = arc4.UInt64.from_bytes(algopy.op.itob(self.proposal_id_incrementer)),
            # proposalId = self.proposal_id_incrementer,
            proposalTitle = _proposalTitle,
            proposalOwner = arc4.Address.from_bytes(algopy.op.(Txn.sender)),
            proposalAmount = arc4.UInt64.from_bytes(algopy.op.itob(algopy.UInt64(0))),
            proposalDescription= _proposalDescription
        )
        self.proposals[self.proposal_id_incrementer] = new_proposal


    @arc4.abimethod()
    def donateToProposal(self, _proposalId: algopy.UInt64, _amount: algopy.UInt64) -> None:
        self.__isActive()
        assert (_proposalId > 0 and _proposalId <= self.proposal_id_incrementer), "Invalid proposal id"
        assert _amount > 0, "Invalid amount"
        proposal = self.proposals[_proposalId]
        proposal_amount = proposal.proposalAmount
        proposal.proposalAmount = arc4.UInt64.from_bytes(algopy.op.itob(proposal_amount.native + _amount))
        # proposal.proposalAmount = arc4.UInt64.from_bytes((proposal_amount + arc4.UInt64.from_bytes(algopy.op.itob(int(_amount)))))
        self.totalFunds += algopy.UInt64(int(_amount))
        self.funderAmount[Txn.sender] += algopy.UInt64(int(_amount))
        self.proposalFunders[_proposalId].append(Txn.sender)
        # self.funders.append(DynamicArray[algopy.op.Txn.sender])
        self.funders[_proposalId].append(Txn.sender)
        self.isFunder[Txn.sender] = True

    @algopy.subroutine
    def __isActive(self) -> None :
        assert self.isActive == True, "Contract is not active"