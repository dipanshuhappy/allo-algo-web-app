import algopy
import algopy.arc4 as arc4
from ..anchor.contract import Anchor
VERSION = 1


class Profile(arc4.Struct):
    id: arc4.DynamicBytes
    nonce: arc4.UInt256
    name: arc4.String
    metadata: arc4.String
    owner: arc4.Address
    anchor: arc4.UInt64
    members: arc4.DynamicArray[arc4.Address]

class Registry(algopy.ARC4Contract):
    def __init__(self) -> None:
        self.version = algopy.BigUInt(VERSION)
        self.anchorToProfileId = algopy.BoxMap(algopy.UInt64,algopy.Bytes)
        self.profilesById = algopy.BoxMap(algopy.Bytes,algopy.Bytes)
        self.profileApplicationIdToPendingAnchor = algopy.BoxMap(algopy.BigUInt,algopy.Account,key_prefix="")
    
    @arc4.abimethod()
    def getProfileById(self, id: algopy.Bytes) -> Profile:
        return Profile.from_bytes(self.profilesById[id])
    @arc4.abimethod()
    def getProfileByAnchor(self, anchor: algopy.UInt64) -> Profile:
        return Profile.from_bytes(self.profilesById[self.anchorToProfileId[anchor]])
    @arc4.abimethod()
    def createProfile(self, nonce: arc4.UInt256,name:algopy.String,metadata:algopy.String) -> algopy.Bytes:
         id = algopy.op.sha256(algopy.op.concat(nonce.bytes,algopy.Txn.sender.bytes))
         anchor_app = arc4.arc4_create(Anchor,fee=2000).created_app
         profile = Profile(
             id=arc4.DynamicBytes.from_bytes(id),
             nonce=nonce,
             name=algopy.arc4.String.from_bytes(name.bytes),
             metadata=algopy.arc4.String.from_bytes(metadata.bytes),
             owner=arc4.Address.from_bytes(algopy.Txn.sender.bytes),
             anchor=arc4.UInt64.from_bytes(algopy.op.itob(anchor_app.id)),
             members= arc4.DynamicArray(arc4.Address())
            )
        
         self.profilesById[id] = profile.copy().bytes
         self.anchorToProfileId[anchor_app.id] = id

         return id
    
    @arc4.abimethod()
    def addMember(self,profileId:algopy.Bytes,member:arc4.Address) -> None:
        profile : Profile = Profile.from_bytes(self.profilesById[profileId])
        profile.members.append(member)
        self.profilesById[profileId] = profile.copy().bytes
    
    @arc4.abimethod()
    def updateProfileName(self,profileId:algopy.Bytes,name:arc4.String) -> None:
        self._onlyProfileOwner(profileId)
        profile = Profile.from_bytes(self.profilesById[profileId])
        profile.name = name
        self.profilesById[profileId] = profile.copy().bytes
    @arc4.abimethod()
    def updateProfileMetadata(self,profileId:algopy.Bytes,metadata:arc4.String) -> None:
        self._onlyProfileOwner(profileId)
        profile = Profile.from_bytes(self.profilesById[profileId])
        profile.metadata = metadata
        self.profilesById[profileId] = profile.copy().bytes
    @arc4.abimethod()
    def isOwnerOrMemberOfProfile(self,profileId:algopy.Bytes,address:arc4.Address) -> bool:
        profile : Profile = Profile.from_bytes(self.profilesById[profileId])
        members = profile.members.copy()
        isMember = False
        for member in members:
            if member == address:
                isMember = True
                break
        
        return profile.owner == address or isMember
    @algopy.subroutine
    def _onlyProfileOwner(self,profileId:algopy.Bytes) -> None:
        profile = Profile.from_bytes(self.profilesById[profileId]).copy()
        assert profile.owner == algopy.Txn.sender, "Only the owner of the profile can call this function"