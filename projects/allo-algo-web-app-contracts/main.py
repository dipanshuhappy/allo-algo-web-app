from typing import List


class ProposalData:
    def __init__(self, payout_address: str):
        self.payout_address = payout_address
        self.unique_donations = 0
        self.direct_donations = 0
        self.donators = []
        self.final_allocation = 0


class QuadraticFunding:
    def __init__(self):
        self.total_funds = 0
        self.index = 0
        self.proposals = {}

    def get_final_allocation(self, proposal_id: int) -> int:
        return self.proposals[proposal_id].final_allocation

    def get_direct_donations(self, proposal_id: int) -> int:
        return self.proposals[proposal_id].direct_donations

    def get_unique_donations(self, proposal_id: int) -> int:
        return self.proposals[proposal_id].unique_donations

    def get_donators(self, proposal_id: int) -> List[str]:
        return self.proposals[proposal_id].donators

    def create_proposal(self, payout_address: str):
        new_proposal = ProposalData(payout_address)
        self.proposals[self.index] = new_proposal
        self.index += 1

    def distribute(self):
        for i in range(self.index):
            proposal = self.proposals[i]
            final_payout = proposal.final_allocation
            final_recipient = proposal.payout_address
            print(f"Payment of {final_payout} to {final_recipient}")
            # self.submit_payment(final_payout, final_recipient)

    def allocate(self):
        total_votes = 0
        for proposal_id in range(self.index):
            proposal = self.proposals[proposal_id]
            sqrt_votes = int(proposal.direct_donations ** 0.5)
            total_votes += sqrt_votes

        for proposal_id in range(self.index):
            proposal = self.proposals[proposal_id]
            sqrt_votes = int(proposal.direct_donations ** 0.5)
            share = int((sqrt_votes * self.total_funds) / total_votes)
            proposal.final_allocation = share
            self.proposals[proposal_id] = proposal

        self.total_funds = 0

    def donate(self, proposal_id: int, amount_micro_algo: int, sender_address: str):
        proposal = self.proposals[proposal_id]

        if value_exists(proposal.donators, sender_address):
            proposal.unique_donations += 1
            proposal.donators.append(sender_address)

        proposal.direct_donations += amount_micro_algo
        self.total_funds += amount_micro_algo
        self.proposals[proposal_id] = proposal

    def submit_payment(self, amount: int, receiver: str):
        # Implement payment submission logic here (e.g., interacting with an external API or contract)
        print(f"Payment of {amount} to {receiver}")


def value_exists(array: List[str], value: str) -> bool:
    return value in array


# Example usage:
quadratic_funding = QuadraticFunding()
quadratic_funding.create_proposal("payout_address_1")
quadratic_funding.create_proposal("payout_address_2")
quadratic_funding.create_proposal("payout_address_3")
print(quadratic_funding.index)
# Get sender address input
sender_address = input("Enter your address: ")
sender_address2 = input("Enter your address: ")
sender_address3 = input("Enter your address: ") 
# Make a donation
quadratic_funding.donate(0, 1, sender_address)
quadratic_funding.donate(0, 2, sender_address2)
quadratic_funding.donate(0, 3, sender_address3)
quadratic_funding.donate(0, 3, sender_address3)
quadratic_funding.donate(0, 3, sender_address3)
quadratic_funding.donate(0, 3, sender_address3)
quadratic_funding.donate(0, 3, sender_address3)
quadratic_funding.donate(1, 1000, sender_address2)
quadratic_funding.donate(2, 1000, sender_address3)
quadratic_funding.allocate()

quadratic_funding.distribute()
