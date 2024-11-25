import algopy
from algopy import arc4, ARC4Contract, Box, BoxMap, Txn, Account, Contract
from algopy.arc4 import DynamicArray, Address, Struct, String

class proposalData(arc4.Struct):
    proposalId: arc4.UInt64
    proposalTitle: arc4.String
    proposalOwner: arc4.Address
    proposalVotes: arc4.UInt64
    proposalDescription: arc4.String


class QuadraticVoting(algopy.ARC4Contract):

    def __init__(self) -> None:
        self.totalFunds = algopy.UInt64(0)
        self.proposals = BoxMap(algopy.UInt64, proposalData)
        self.voters = DynamicArray[arc4.Address]()
        self.voterCredits = BoxMap(arc4.Address, algopy.UInt64, key_prefix=b"voter_credits")
        self.proposalVoters = BoxMap(algopy.UInt64, DynamicArray[arc4.Address], key_prefix=b"proposal_votes")
        self.proposal_id_incrementer = algopy.UInt64(0)
        self.isActive = False

    @arc4.abimethod()
    def initialize(self) -> None:
        # self.__assertNonEmpty(_voters) 
        self.isActive = True
        # for voter in _voters:
        #     self.voters.append(voter)
        #     self.voterCredits[voter] = algopy.UInt64(100)

    @arc4.abimethod()
    def createProposal(self, _proposalTitle: String, _proposalDescription: String) -> None:
        self.__isActive()
        self.proposal_id_incrementer += algopy.UInt64(1)
        new_proposal = proposalData(
            proposalId = arc4.UInt64.from_bytes(algopy.op.itob(self.proposal_id_incrementer)),
            proposalTitle = _proposalTitle,
            proposalOwner = arc4.Address(algopy.op.Txn.sender),
            proposalVotes = arc4.UInt64(0),
            proposalDescription = _proposalDescription
        )
        self.proposals[self.proposal_id_incrementer] = new_proposal.copy()

    @arc4.abimethod()
    def allocateCredits(self, _voters: DynamicArray[arc4.Address]) -> None:
        self.__assertNonEmpty(_voters)
        for voter in _voters:
            self.voters.append(voter)
            self.voterCredits[voter] = algopy.UInt64(100)

    @arc4.abimethod()
    def vote(self, _proposalId: algopy.UInt64, _credits: algopy.UInt64) -> None:
        self.__isActive()
        assert (_proposalId > 0 and _proposalId <= self.proposal_id_incrementer), "Invalid proposal id"
        voter_credits = self.voterCredits[arc4.Address(algopy.op.Txn.sender)]
        assert voter_credits >= _credits, "Insufficient credits"
        assert _credits > 0, "Credits must be greater than zero"

        self.voterCredits[arc4.Address(algopy.op.Txn.sender)] -= _credits
        proposal = self.proposals[_proposalId].copy()
        proposal.proposalVotes = arc4.UInt64.from_bytes(algopy.op.itob(proposal.proposalVotes.native + _credits))
        self.proposalVoters[_proposalId].append(arc4.Address(algopy.op.Txn.sender))

    @arc4.abimethod()
    def getProposalVotes(self, _proposalId: algopy.UInt64) -> arc4.UInt64:
        self.__isActive()
        assert (_proposalId > 0 and _proposalId <= self.proposal_id_incrementer), "Invalid proposal id"
        proposal = self.proposals[_proposalId].copy()
        return proposal.proposalVotes

    @algopy.subroutine
    def __isActive(self) -> None:
        assert self.isActive == True, "Contract is not active"

    @algopy.subroutine
    def __assertNonEmpty(self, _array: DynamicArray[arc4.Address]) -> None:
        assert _array.length > 0, "voters array cannot be empty"
