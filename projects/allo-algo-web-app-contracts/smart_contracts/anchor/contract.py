import algopy
class Anchor(algopy.ARC4Contract):
    def __init__(self) -> None:
        self.owner = algopy.Account()
    @algopy.arc4.abimethod()
    def create(self, owner: algopy.Account) -> None:
        assert (
            self.owner == algopy.Account()
        ), "Contract has already been initialized"
        self.owner = owner
    @algopy.arc4.abimethod()
    def createAndOptIn(self, owner: algopy.Account,appId: algopy.Application) -> None:
        assert (
            self.owner == algopy.Account()
        ), "Contract has already been initialized"
        self.owner = owner
        algopy.itxn.ApplicationCall(app_id=appId, on_completion=algopy.OnCompleteAction.OptIn,fee=algopy.Global.min_txn_fee).submit()

    @algopy.subroutine
    def _onlyOwner(self) -> None:
        assert (
            self.owner == algopy.Txn.sender
        ), "Only the account set in global_state.owner may call this method"
    @algopy.arc4.abimethod()
    def transferAlgo(self,receiver:algopy.Account,amount:algopy.UInt64)-> None:
        self._onlyOwner()
        algopy.itxn.Payment(receiver=receiver, amount=amount,fee=1000).submit()
    @algopy.arc4.abimethod()
    def transferAsset(self,receiver:algopy.Account,asset:algopy.Asset,amount:algopy.UInt64)-> None:
        self._onlyOwner()
        algopy.itxn.AssetTransfer(asset_receiver=receiver, xfer_asset=asset, fee=1000,asset_amount=amount).submit()
    @algopy.arc4.abimethod()
    def opt_into_asset(self,asset:algopy.Asset)-> None:
        self._onlyOwner()
        algopy.itxn.AssetTransfer(asset_receiver=algopy.Txn.sender, fee=1000,xfer_asset=asset,asset_amount=algopy.UInt64(0)).submit()
    
