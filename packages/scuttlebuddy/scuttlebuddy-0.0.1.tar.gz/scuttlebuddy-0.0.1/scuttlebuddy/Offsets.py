
# BaseOffsets

GameTime = 0x21FA3A8
LocalPlayer = 0x220C7D8
HeroList = 0x21EFD20
MinionList = 0x21F2C80
MissileList = 0x220C8C0
TurretList = 0x21F9620
InhibitorList = 0x220CAB8
UnderMouseObject = 0x0


# GameCameraOffsets

ViewProjMatrix = 0x2255C90
Renderer = 0x225E740
RendererWidth = 0xC
RendererHeight = 0x10


# GameObjectOffsets

NetworkId = 0x10
Name = 0x60
Team = 0x3C
IsVisible = 0x340
Expiry = 0x298
XPosition = 0x220
YPosition = 0x228
ZPosition = 0x224
ObjectName = 0x38a8


# AttackableUnitOffsets

IsDead = 0x274
Mana = 0x370
MaxMana = 0x388
Health = 0x1088
MaxHealth = 0x10A0
Armor = 0x16DC
BonusArmor = 0x16e0
MagicResistance = 0x16E4
BonusMagicResistance = 0x16E8
Targetable = 0xEE0
IsAlive = 0x12C
IsDead2 = 0x278
IsDead3 = 0x338


# AiBaseUnitOffsets

CurrentTargetIndex = 0x0
AttackRange = 0x16FC
BaseAttackDamage = 0x16B4
BonusAttackDamage = 0x1620
AbilityPower = 0x15E8
MagicPenetration = 0x158C
Lethality = 0x15E0
BonusAttackSpeed = 0x164C
AttackSpeedMultiplier = 0x1668
Level = 0x4028
CriticalChance = 0x16A0


# MissileOffsets

NetworkId = 0x10
Name = 0x60
Speed = 0x88
Position = 0x104
SourceIndex = 0x370
DestinationIndex = 0x3C8
StartPosition = 0x38C
EndPosition = 0x398
SpellInfo = 0x2E8
SpellInfoSpellName = 0x28
SpellInfoMissileName = 0x118


# BuffOffsets

BuffEntryBuffStartTime = 0x18
BuffEntryBuffEndTime = 0x1C
BuffEntryBuffCount = 0x38
BuffEntryBuffCountAlt = 0x3C
BuffInfo = 0x10
BuffInfoName = 0x8
BuffType = 0x8


# HeroOffsets

SpawnCount = 0x358
BuffManager = 0x2810
BuffManagerEntryStart = 0x18
BuffManagerEntryEnd = 0x20
SpellBook = 0x3108
AiManager = 0x3740
ActiveSpell = 0x2A70


# SpellOffsets

SpellSlotLevel = 0x28
SpellSlotReadyAt = 0x30
SpellSlotSmiteReadyAt = 0x68
SpellSlotDamage = 0x90
SpellSlotSmiteCharges = 0x5C
SpellSlotSpellInput = 0x128
SpellInputStartPosition = 0x18
SpellInputEndPosition = 0x24
SpellInputTargetId = 0x14
SpellSlotSpellInfo = 0x130
SpellInfoSpellData = 0x60
SpellDataSpellName = 0x80


# AiManagerOffsets

IsMoving = 0x2BC
PathStart = 0x2D0
PathEnd = 0x2DC
CurrentPathSegment = 0x2C0
PathSegments = 0x2E8
PathSegmentsCount = 0x2F0
CurrentPosition = 0x414
IsDashing = 0x324
DashSpeed = 0x300
MovementSpeed = 0x2B8
TargetPosition = 0x14


# ActiveCastSpellOffsets

Type = 0x10
SourceId = 0x90
TargetId = 0xE8
StartPosition = 0xAC
EndPosition = 0xB8
StartTime = 0x188
EndTime = 0x170
SpellInfo = 0x8
SpellInfoName = 0x18


# InhibitorOffsets

IsAlive = 0x11C0


