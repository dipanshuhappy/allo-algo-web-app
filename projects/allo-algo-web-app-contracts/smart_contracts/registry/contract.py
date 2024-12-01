import algopy
import algopy.arc4 as arc4
from ..anchor.contract import Anchor
VERSION = 1



# class Registry(algopy.ARC4Contract):
#     def __init__(self) -> None:
#         self.version = algopy.BigUInt(VERSION)
#         self.index = algopy.BigUInt(0)
#         self.profilesById = algopy.BoxMap(algopy.BigUInt,Profile)
#         # self.anchorToProfileId = algopy.BoxMap(algopy.UInt64,algopy.Bytes)
#         # self.nonce = algopy.BoxMap(algopy.Account,algopy.UInt64)
#         # self.profilesById = algopy.BoxMap(algopy.Bytes,algopy.Bytes)
#         # self.profileApplicationIdToPendingAnchor = algopy.BoxMap(algopy.BigUInt,algopy.Account,key_prefix="")
    
#     @arc4.abimethod()
#     def getAccountNonce(self,account:algopy.Account) -> algopy.UInt64:
#         value = self.nonce[account]
#         return value
#     @arc4.abimethod()
#     def getMembers(self,profileId:algopy.Bytes) -> arc4.DynamicArray[arc4.Address]:
#         profile = Profile.from_bytes(self.profilesById[profileId])
#         return profile.members.copy()
    
#     @arc4.abimethod()
#     def incrementAccountNonce(self,account:algopy.Account) -> None:
#         value,valid = self.nonce.maybe(account)
#         if valid:
#             self.nonce[account] = value + 1
#         else:
#             self.nonce[account] = algopy.UInt64(1)
#     @arc4.abimethod()
#     def getProfileById(self, id: algopy.Bytes) -> Profile:
#         return Profile.from_bytes(self.profilesById[id])
#     @arc4.abimethod()
#     def getProfileByAnchor(self, anchor: algopy.UInt64) -> Profile:
#         return Profile.from_bytes(self.profilesById[self.anchorToProfileId[anchor]])
#     @arc4.abimethod()
#     def getProfileId(self, nonce: arc4.UInt256,name:algopy.String,metadata:algopy.String) -> algopy.Bytes:
#         id = algopy.op.sha256(algopy.op.concat(nonce.bytes,algopy.Txn.sender.bytes))
#         return id
#     @arc4.abimethod()
#     def addAnchorToProfileId(self,anchor:algopy.UInt64,profileId:algopy.Bytes) -> None:
#         profileBytes = self.profilesById[profileId]
#         profile = Profile.from_bytes(profileBytes)
#         assert profile.anchor == anchor, "Profile has a different anchor"
#         self.anchorToProfileId[anchor] = profileId
#     @arc4.abimethod()
#     def createProfile(self,id:algopy.Bytes,name:algopy.String,metadata:algopy.String) -> algopy.UInt64:
#          nonce = self.getAccountNonce(algopy.Txn.sender)
#          anchor_app = arc4.arc4_create(Anchor,fee=2000).created_app
#          profile = Profile(
#              id=arc4.DynamicBytes.from_bytes(id),
#              nonce=algopy.arc4.UInt64(nonce),
#              name=algopy.arc4.String.from_bytes(name.bytes),
#              metadata=algopy.arc4.String.from_bytes(metadata.bytes),
#              owner=arc4.Address.from_bytes(algopy.Txn.sender.bytes),
#              anchor=arc4.UInt64.from_bytes(algopy.op.itob(anchor_app.id)),
#              members= arc4.DynamicArray(arc4.Address())
#             )
        
#          self.profilesById[id] = profile.copy().bytes
#         #  self.anchorToProfileId[anchor_app.id] = id
#          return anchor_app.id
    
#     @arc4.abimethod()
#     def addMember(self,profileId:algopy.Bytes,member:arc4.Address) -> None:
#         profile : Profile = Profile.from_bytes(self.profilesById[profileId])
#         profile.members.append(member)
#         self.profilesById[profileId] = profile.copy().bytes
    
#     @arc4.abimethod()
#     def updateProfileName(self,profileId:algopy.Bytes,name:arc4.String) -> None:
#         self._onlyProfileOwner(profileId)
#         profile = Profile.from_bytes(self.profilesById[profileId])
#         profile.name = name
#         self.profilesById[profileId] = profile.copy().bytes
#     @arc4.abimethod()
#     def updateProfileMetadata(self,profileId:algopy.Bytes,metadata:arc4.String) -> None:
#         self._onlyProfileOwner(profileId)
#         profile = Profile.from_bytes(self.profilesById[profileId])
#         profile.metadata = metadata
#         self.profilesById[profileId] = profile.copy().bytes
#     @arc4.abimethod()
#     def isOwnerOrMemberOfProfile(self,profileId:algopy.Bytes,address:arc4.Address) -> bool:
#         profile : Profile = Profile.from_bytes(self.profilesById[profileId])
#         members = profile.members.copy()
#         isMember = False
#         for member in members:
#             if member == address:
#                 isMember = True
#                 break
        
#         return profile.owner == address or isMember
#     @algopy.subroutine
#     def _onlyProfileOwner(self,profileId:algopy.Bytes) -> None:
#         profile = Profile.from_bytes(self.profilesById[profileId]).copy()
#         assert profile.owner == algopy.Txn.sender, "Only the owner of the profile can call this function"

class Profile(arc4.Struct):
    id: arc4.UInt256
    name: arc4.String
    metadata: arc4.String
    owner: arc4.Address
    anchors: arc4.DynamicArray[arc4.UInt64]
    members: arc4.DynamicArray[arc4.Address]
class Registry(algopy.ARC4Contract):
    def __init__(self) -> None:
        self.version = algopy.BigUInt(VERSION)
        self.index = algopy.BigUInt(0)
        self.profilesById = algopy.BoxMap(algopy.BigUInt,Profile)
    @arc4.abimethod()
    def getProfileById(self, id: algopy.BigUInt) -> Profile:
        return self.profilesById[id]
    @arc4.abimethod()
    def getAnchors(self,profileId:algopy.BigUInt) -> arc4.DynamicArray[arc4.UInt64]:
        profile = self.profilesById[profileId].copy()
        return profile.anchors.copy()
    @arc4.abimethod()
    def getMembers(self,profileId:algopy.BigUInt) -> arc4.DynamicArray[arc4.Address]:
        profile = self.profilesById[profileId].copy()
        return profile.members.copy()
    @arc4.abimethod()
    def getProfileName(self, profileId:algopy.BigUInt) -> algopy.String:
        profile = self.getProfileById(profileId)
        return profile.name.native
    @arc4.abimethod()
    def getProfileMetadata(self, profileId:algopy.BigUInt) -> algopy.String:
        profile = self.getProfileById(profileId)
        return profile.metadata.native
    @arc4.abimethod()
    def addMember(self,profileId:algopy.BigUInt,member:arc4.Address) -> None:
        profile : Profile = Profile.from_bytes(self.profilesById[profileId].bytes)
        profile.members.append(member)
        self.profilesById[profileId] = Profile.from_bytes(profile.copy().bytes)
    @arc4.abimethod()
    def createProfile(self,name:algopy.String,metadata:algopy.String) -> algopy.UInt64:
         profileId = self.index
         anchor_app = arc4.arc4_create(Anchor,fee=2000).created_app
         anchors = arc4.DynamicArray[arc4.UInt64]()
         anchors.append(arc4.UInt64(anchor_app.id))
         profile = Profile(
             id=arc4.UInt256.from_bytes(profileId.bytes),
             name=arc4.String.from_bytes(name.bytes),
             metadata=arc4.String.from_bytes(metadata.bytes),
             owner=arc4.Address.from_bytes(algopy.Txn.sender.bytes),
             anchors=anchors.copy(),
             members= arc4.DynamicArray(arc4.Address())
            )
        
         self.profilesById[profileId] = Profile.from_bytes(profile.bytes)
         return anchor_app.id 