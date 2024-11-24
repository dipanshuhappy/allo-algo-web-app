import algopy
from algopy import arc4 
class Pool(arc4.Struct):
    profileId: arc4.DynamicBytes
    strategy: arc4.UInt64
    metadata: arc4.String
    managerRole: arc4.DynamicBytes
    adminRole: arc4.DynamicBytes

class Allo(algopy.ARC4Contract):
    def __init__(self):
        self.percentageFee = algopy.UInt64(5)
        self.poolFee = algopy.UInt64(1000000)
        self.poolIndex = algopy.UInt64(0)
        self.treasury = algopy.Account("6FW6U2CDSXTGMIJRADU53MOCFAZ7AQCV7NDXEDSB2EOT4NAFE6TF2LRH2A")
        self.registryId = algopy.UInt64(0)
        self.pools = algopy.BoxMap(algopy.UInt64, algopy.UInt64)
    @arc4.abimethod()
    def initialize(
        self,
        owner: algopy.Account,
        registry: algopy.UInt64,
        treasury: algopy.Account,
    ) -> None:
        assert self.owner == algopy.Account(), "Contract has already been initialized"
        assert owner != algopy.Account(), "Owner cannot be zero address"
        self.owner = owner
        self.registryId = registry.app_id
        self.treasury = treasury
    @algopy.subroutine
    def _onlyOwner(self) -> None:
        assert self.owner == algopy.Txn.sender, "Ownable: caller is not the owner"
    @arc4.abimethod()
    def createPoolWithCustomStrategy(
        self,
        profileId: arc4.DynamicBytes,
        strategy: algopy.Application,
        initStrategyData: arc4.DynamicBytes,
        amount: algopy.UInt64,
        metadata: arc4.String,
        managers: arc4.DynamicArray[arc4.Address]  # Changed from algopy.Address to algopy.Account
    ) -> algopy.UInt64:
        pass
    
   
    @algopy.subroutine
    def _createPool(
        self,
        profileId: arc4.DynamicBytes,
        strategy: algopy.UInt64,
        initStrategyData: arc4.DynamicBytes,
        amount: algopy.UInt64,
        metadata: arc4.String,
        managers: arc4.DynamicArray[arc4.Address] # Changed from algopy.Address to algopy.Account
    ) -> algopy.UInt64:

        poolId = self.poolIndex + 1
        
        POOL_MANAGER_ROLE = algopy.op.itob(poolId)
        POOL_ADMIN_ROLE = algopy.op.sha256(algopy.op.concat(algopy.op.itob(poolId), algopy.Bytes(b"admin")))

        pool = Pool(
            profileId=profileId.copy(),
            strategy=arc4.UInt64(strategy),
            metadata=metadata,
            managerRole=arc4.DynamicBytes.from_bytes(POOL_MANAGER_ROLE),
            adminRole=arc4.DynamicBytes.from_bytes(POOL_ADMIN_ROLE)
        )

        self.pools[poolId] = arc4.DynamicBytes.from_bytes(pool.bytes)

        self._grantRole(arc4.DynamicBytes.from_bytes(POOL_ADMIN_ROLE), algopy.Txn.sender)
        self._setRoleAdmin(arc4.DynamicBytes.from_bytes(POOL_MANAGER_ROLE), arc4.DynamicBytes.from_bytes(POOL_ADMIN_ROLE))

        # Initialize strategy
        # Need to perform inner transaction to call strategy.initialize(poolId, initStrategyData)
        # For simplicity, we skip the inner transaction code

        # Grant pool manager roles
        for manager in managers:
            assert manager.bytes != algopy.Account().bytes, "ZERO_ADDRESS"
            self._grantRole(arc4.DynamicBytes.from_bytes(POOL_MANAGER_ROLE), algopy.Account.from_bytes(manager.bytes))
        self.poolIndex = poolId
        # Handle baseFee and amount
        # For simplicity, we skip the fund transfer code

        return poolId

    
        


