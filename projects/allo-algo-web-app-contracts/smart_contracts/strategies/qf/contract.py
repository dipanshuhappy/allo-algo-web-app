import algopy
from algopy import arc4, ARC4Contract, Box, BoxMap, Txn, Account, Contract
from algopy.arc4 import DynamicArray, Address, Struct, String

class proposalData(arc4.Struct):
    proposalId: arc4.UInt64
    proposalTitle: arc4.String
    proposalOwner: arc4.Address
    proposalVotes: arc4.UInt64
    proposalDescription: arc4.String


class QuadraticVoting(ARC4Contract):
    def __init__(self) -> None:
        self.totalFunds: algopy.UInt64 = algopy.UInt64(0)
        self.proposals = BoxMap(algopy.UInt64, proposalData)
        self.voterCredits = BoxMap(Account, algopy.UInt64, key_prefix=b"voter_credits")
        self.proposalVotes = BoxMap(algopy.UInt64, DynamicArray[Address], key_prefix=b"proposal_votes")
        self.proposal_id_incrementer: algopy.UInt64 = algopy.UInt64(0)
        self.isActive: bool = False

    @arc4.abimethod()
    def initialize(self) -> None:
        self.isActive = True

    @arc4.abimethod()
    def createProposal(self, _proposalTitle: String, _proposalDescription: String) -> None:
        self.__isActive()
        self.proposal_id_incrementer += algopy.UInt64(1)
        new_proposal = proposalData(
            proposalId=self.proposal_id_incrementer,
            proposalTitle=_proposalTitle,
            proposalOwner=arc4.Address.from_bytes(algopy.op.Txn.sender),
            proposalVotes=arc4.UInt64(0),
            proposalDescription=_proposalDescription
        )
        self.proposals[self.proposal_id_incrementer] = new_proposal

    @arc4.abimethod()
    def allocateCredits(self, _amount: algopy.UInt64) -> None:
        assert _amount > 0, "Invalid credit amount"
        self.voterCredits[Txn.sender] += _amount
        self.totalFunds += _amount

    @arc4.abimethod()
    def vote(self, _proposalId: algopy.UInt64, _credits: algopy.UInt64) -> None:
        self.__isActive()
        assert (_proposalId > 0 and _proposalId <= self.proposal_id_incrementer), "Invalid proposal id"
        voter_credits = self.voterCredits[Txn.sender]
        assert voter_credits >= _credits, "Insufficient credits"
        assert _credits > 0, "Credits must be greater than zero"

        quadratic_cost = _credits
        assert voter_credits >= quadratic_cost, "Insufficient credits for quadratic voting"

        self.voterCredits[Txn.sender] -= quadratic_cost
        proposal = self.proposals[_proposalId]
        proposal.proposalVotes += _credits
        self.proposalVotes[_proposalId].append(Txn.sender)

    @arc4.abimethod()
    def getProposalVotes(self, _proposalId: algopy.UInt64) -> algopy.UInt64:
        self.__isActive()
        assert (_proposalId > 0 and _proposalId <= self.proposal_id_incrementer), "Invalid proposal id"
        proposal = self.proposals[_proposalId]
        return proposal.proposalVotes

    @algopy.subroutine
    def __isActive(self) -> None:
        assert self.isActive == True, "Contract is not active"
