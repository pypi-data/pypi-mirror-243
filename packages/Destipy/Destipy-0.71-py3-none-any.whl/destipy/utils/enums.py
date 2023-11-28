from enum import IntEnum


class ApplicationScopes(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Applications-ApplicationScopes.html#schema_Applications-ApplicationScopes
	"""
	READ_BASIC_USER_PROFILE = 1
	READ_GROUPS = 2
	WRITE_GROUPS = 4
	ADMIN_GROUPS = 8
	BNET_WRITE = 16
	MOVE_EQUIP_DESTINY_ITEMS = 32
	READ_DESTINY_INVENTORY_AND_VAULT = 64
	READ_USER_DATA = 128
	EDIT_USER_DATA = 256
	READ_DESTINY_VENDORS_AND_ADVISORS = 512
	READ_AND_APPLY_TOKENS = 1024
	ADVANCED_WRITE_ACTIONS = 2048
	PARTNER_OFFER_GRANT = 4096
	DESTINY_UNLOCK_VALUE_QUERY = 8192
	USER_PII_READ = 16384


class ApplicationStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Applications-ApplicationStatus.html#schema_Applications-ApplicationStatus
	"""
	NONE = 0
	PRIVATE = 1
	PUBLIC = 2
	DISABLED = 3
	BLOCKED = 4


class DeveloperRole(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Applications-DeveloperRole.html#schema_Applications-DeveloperRole
	"""
	NONE = 0
	OWNER = 1
	TEAM_MEMBER = 2


class BungieMembershipType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_BungieMembershipType.html#schema_BungieMembershipType
	"""
	NONE = 0
	TIGER_XBOX = 1
	TIGER_PSN = 2
	TIGER_STEAM = 3
	TIGER_BLIZZARD = 4
	TIGER_STADIA = 5
	TIGER_EGS = 6
	TIGER_DEMON = 10
	BUNGIE_NEXT = 254
	ALL = -1


class IgnoreStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Ignores-IgnoreStatus.html#schema_Ignores-IgnoreStatus
	"""
	NOT_IGNORED = 0
	IGNORED_USER = 1
	IGNORED_GROUP = 2
	IGNORED_BY_GROUP = 4
	IGNORED_POST = 8
	IGNORED_TAG = 16
	IGNORED_GLOBAL = 32


class BungieCredentialType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_BungieCredentialType.html#schema_BungieCredentialType
	"""
	NONE = 0
	XUID = 1
	PSNID = 2
	WLID = 3
	FAKE = 4
	FACEBOOK = 5
	GOOGLE = 8
	WINDOWS = 9
	DEMON_ID = 10
	STEAM_ID = 12
	BATTLE_NET_ID = 14
	STADIA_ID = 16
	TWITCH_ID = 18
	EGS_ID = 20


class ContentPropertyDataTypeEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Content-Models-ContentPropertyDataTypeEnum.html#schema_Content-Models-ContentPropertyDataTypeEnum
	"""
	NONE = 0
	PLAINTEXT = 1
	HTML = 2
	DROPDOWN = 3
	LIST = 4
	JSON = 5
	CONTENT = 6
	REPRESENTATION = 7
	SET = 8
	FILE = 9
	FOLDER_SET = 10
	DATE = 11
	MULTILINE_PLAINTEXT = 12
	DESTINY_CONTENT = 13
	COLOR = 14


class ForumTopicsCategoryFiltersEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumTopicsCategoryFiltersEnum.html#schema_Forum-ForumTopicsCategoryFiltersEnum
	"""
	NONE = 0
	LINKS = 1
	QUESTIONS = 2
	ANSWERED_QUESTIONS = 4
	MEDIA = 8
	TEXT_ONLY = 16
	ANNOUNCEMENT = 32
	BUNGIE_OFFICIAL = 64
	POLLS = 128


class ForumTopicsQuickDateEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumTopicsQuickDateEnum.html#schema_Forum-ForumTopicsQuickDateEnum
	"""
	ALL = 0
	LAST_YEAR = 1
	LAST_MONTH = 2
	LAST_WEEK = 3
	LAST_DAY = 4


class ForumTopicsSortEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumTopicsSortEnum.html#schema_Forum-ForumTopicsSortEnum
	"""
	DEFAULT = 0
	LAST_REPLIED = 1
	MOST_REPLIED = 2
	POPULARITY = 3
	CONTROVERSIALITY = 4
	LIKED = 5
	HIGHEST_RATED = 6
	MOST_UPVOTED = 7


class ForumMediaType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumMediaType.html#schema_Forum-ForumMediaType
	"""
	NONE = 0
	IMAGE = 1
	VIDEO = 2
	YOUTUBE = 3


class ForumPostPopularity(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumPostPopularity.html#schema_Forum-ForumPostPopularity
	"""
	EMPTY = 0
	DEFAULT = 1
	DISCUSSED = 2
	COOL_STORY = 3
	HEATING_UP = 4
	HOT = 5


class ForumPostCategoryEnums(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forums-ForumPostCategoryEnums.html#schema_Forums-ForumPostCategoryEnums
	"""
	NONE = 0
	TEXT_ONLY = 1
	MEDIA = 2
	LINK = 4
	POLL = 8
	QUESTION = 16
	ANSWERED = 32
	ANNOUNCEMENT = 64
	CONTENT_COMMENT = 128
	BUNGIE_OFFICIAL = 256
	NINJA_OFFICIAL = 512
	RECRUITMENT = 1024


class ForumFlagsEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forums-ForumFlagsEnum.html#schema_Forums-ForumFlagsEnum
	"""
	NONE = 0
	BUNGIE_STAFF_POST = 1
	FORUM_NINJA_POST = 2
	FORUM_MENTOR_POST = 4
	TOPIC_BUNGIE_STAFF_POSTED = 8
	TOPIC_BUNGIE_VOLUNTEER_POSTED = 16
	QUESTION_ANSWERED_BY_BUNGIE = 32
	QUESTION_ANSWERED_BY_NINJA = 64
	COMMUNITY_CONTENT = 128


class GroupType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupType.html#schema_GroupsV2-GroupType
	"""
	GENERAL = 0
	CLAN = 1


class ChatSecuritySetting(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-ChatSecuritySetting.html#schema_GroupsV2-ChatSecuritySetting
	"""
	GROUP = 0
	ADMINS = 1


class GroupHomepage(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupHomepage.html#schema_GroupsV2-GroupHomepage
	"""
	WALL = 0
	FORUM = 1
	ALLIANCE_FORUM = 2


class MembershipOption(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-MembershipOption.html#schema_GroupsV2-MembershipOption
	"""
	REVIEWED = 0
	OPEN = 1
	CLOSED = 2


class GroupPostPublicity(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupPostPublicity.html#schema_GroupsV2-GroupPostPublicity
	"""
	PUBLIC = 0
	ALLIANCE = 1
	PRIVATE = 2


class Capabilities(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-Capabilities.html#schema_GroupsV2-Capabilities
	"""
	NONE = 0
	LEADERBOARDS = 1
	CALLSIGN = 2
	OPTIONAL_CONVERSATIONS = 4
	CLAN_BANNER = 8
	D2_INVESTMENT_DATA = 16
	TAGS = 32
	ALLIANCES = 64


class HostGuidedGamesPermissionLevel(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-HostGuidedGamesPermissionLevel.html#schema_GroupsV2-HostGuidedGamesPermissionLevel
	"""
	NONE = 0
	BEGINNER = 1
	MEMBER = 2


class RuntimeGroupMemberType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-RuntimeGroupMemberType.html#schema_GroupsV2-RuntimeGroupMemberType
	"""
	NONE = 0
	BEGINNER = 1
	MEMBER = 2
	ADMIN = 3
	ACTING_FOUNDER = 4
	FOUNDER = 5


class DestinyProgressionRewardItemState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyProgressionRewardItemState.html#schema_Destiny-DestinyProgressionRewardItemState
	"""
	NONE = 0
	INVISIBLE = 1
	EARNED = 2
	CLAIMED = 4
	CLAIM_ALLOWED = 8


class DestinyProgressionScope(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyProgressionScope.html#schema_Destiny-DestinyProgressionScope
	"""
	ACCOUNT = 0
	CHARACTER = 1
	CLAN = 2
	ITEM = 3
	IMPLICIT_FROM_EQUIPMENT = 4
	MAPPED = 5
	MAPPED_AGGREGATE = 6
	MAPPED_STAT = 7
	MAPPED_UNLOCK_VALUE = 8


class DestinyProgressionStepDisplayEffect(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyProgressionStepDisplayEffect.html#schema_Destiny-DestinyProgressionStepDisplayEffect
	"""
	NONE = 0
	CHARACTER = 1
	ITEM = 2


class SocketTypeActionType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-SocketTypeActionType.html#schema_Destiny-SocketTypeActionType
	"""
	INSERT_PLUG = 0
	INFUSE_ITEM = 1
	REINITIALIZE_SOCKET = 2


class DestinySocketVisibility(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinySocketVisibility.html#schema_Destiny-DestinySocketVisibility
	"""
	VISIBLE = 0
	HIDDEN = 1
	HIDDEN_WHEN_EMPTY = 2
	HIDDEN_IF_NO_PLUGS_AVAILABLE = 3


class DestinySocketCategoryStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinySocketCategoryStyle.html#schema_Destiny-DestinySocketCategoryStyle
	"""
	UNKNOWN = 0
	REUSABLE = 1
	CONSUMABLE = 2
	UNLOCKABLE = 3
	INTRINSIC = 4
	ENERGY_METER = 5
	LARGE_PERK = 6
	ABILITIES = 7
	SUPERS = 8


class TierType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-TierType.html#schema_Destiny-TierType
	"""
	UNKNOWN = 0
	CURRENCY = 1
	BASIC = 2
	COMMON = 3
	RARE = 4
	SUPERIOR = 5
	EXOTIC = 6


class BucketScope(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-BucketScope.html#schema_Destiny-BucketScope
	"""
	CHARACTER = 0
	ACCOUNT = 1


class BucketCategory(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-BucketCategory.html#schema_Destiny-BucketCategory
	"""
	INVISIBLE = 0
	ITEM = 1
	CURRENCY = 2
	EQUIPPABLE = 3
	IGNORED = 4


class ItemLocation(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-ItemLocation.html#schema_Destiny-ItemLocation
	"""
	UNKNOWN = 0
	INVENTORY = 1
	VAULT = 2
	VENDOR = 3
	POSTMASTER = 4


class DestinyStatAggregationType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyStatAggregationType.html#schema_Destiny-DestinyStatAggregationType
	"""
	CHARACTER_AVERAGE = 0
	CHARACTER = 1
	ITEM = 2


class DestinyStatCategory(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyStatCategory.html#schema_Destiny-DestinyStatCategory
	"""
	GAMEPLAY = 0
	WEAPON = 1
	DEFENSE = 2
	PRIMARY = 3


class EquippingItemBlockAttributes(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-EquippingItemBlockAttributes.html#schema_Destiny-EquippingItemBlockAttributes
	"""
	NONE = 0
	EQUIP_ON_ACQUIRE = 1


class DestinyAmmunitionType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyAmmunitionType.html#schema_Destiny-DestinyAmmunitionType
	"""
	NONE = 0
	PRIMARY = 1
	SPECIAL = 2
	HEAVY = 3
	UNKNOWN = 4


class DestinyClass(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyClass.html#schema_Destiny-DestinyClass
	"""
	TITAN = 0
	HUNTER = 1
	WARLOCK = 2
	UNKNOWN = 3


class DestinyGender(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyGender.html#schema_Destiny-DestinyGender
	"""
	MALE = 0
	FEMALE = 1
	UNKNOWN = 2


class DestinyVendorProgressionType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorProgressionType.html#schema_Destiny-DestinyVendorProgressionType
	"""
	DEFAULT = 0
	RITUAL = 1
	NO_SEASONAL_REFRESH = 2


class VendorDisplayCategorySortOrder(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-VendorDisplayCategorySortOrder.html#schema_Destiny-VendorDisplayCategorySortOrder
	"""
	DEFAULT = 0
	SORT_BY_TIER = 1


class DestinyVendorInteractionRewardSelection(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorInteractionRewardSelection.html#schema_Destiny-DestinyVendorInteractionRewardSelection
	"""
	NONE = 0
	ONE = 1
	ALL = 2


class DestinyVendorReplyType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorReplyType.html#schema_Destiny-DestinyVendorReplyType
	"""
	ACCEPT = 0
	DECLINE = 1
	COMPLETE = 2


class VendorInteractionType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-VendorInteractionType.html#schema_Destiny-VendorInteractionType
	"""
	UNKNOWN = 0
	UNDEFINED = 1
	QUEST_COMPLETE = 2
	QUEST_CONTINUE = 3
	REPUTATION_PREVIEW = 4
	RANK_UP_REWARD = 5
	TOKEN_TURN_IN = 6
	QUEST_ACCEPT = 7
	PROGRESS_TAB = 8
	END = 9
	START = 10


class DestinyItemSortType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyItemSortType.html#schema_Destiny-DestinyItemSortType
	"""
	ITEM_ID = 0
	TIMESTAMP = 1
	STACK_SIZE = 2


class DestinyVendorItemRefundPolicy(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorItemRefundPolicy.html#schema_Destiny-DestinyVendorItemRefundPolicy
	"""
	NOT_REFUNDABLE = 0
	DELETES_ITEM = 1
	REVOKES_LICENSE = 2


class DestinyGatingScope(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyGatingScope.html#schema_Destiny-DestinyGatingScope
	"""
	NONE = 0
	GLOBAL = 1
	CLAN = 2
	PROFILE = 3
	CHARACTER = 4
	ITEM = 5
	ASSUMED_WORST_CASE = 6


class ActivityGraphNodeHighlightType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-ActivityGraphNodeHighlightType.html#schema_Destiny-ActivityGraphNodeHighlightType
	"""
	NONE = 0
	NORMAL = 1
	HYPER = 2
	COMET = 3
	RISE_OF_IRON = 4


class DestinyUnlockValueUIStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyUnlockValueUIStyle.html#schema_Destiny-DestinyUnlockValueUIStyle
	"""
	AUTOMATIC = 0
	FRACTION = 1
	CHECKBOX = 2
	PERCENTAGE = 3
	DATE_TIME = 4
	FRACTION_FLOAT = 5
	INTEGER = 6
	TIME_DURATION = 7
	HIDDEN = 8
	MULTIPLIER = 9
	GREEN_PIPS = 10
	RED_PIPS = 11
	EXPLICIT_PERCENTAGE = 12
	RAW_FLOAT = 13
	LEVEL_AND_REWARD = 14


class DestinyObjectiveGrantStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyObjectiveGrantStyle.html#schema_Destiny-DestinyObjectiveGrantStyle
	"""
	WHEN_INCOMPLETE = 0
	WHEN_COMPLETE = 1
	ALWAYS = 2


class DamageType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DamageType.html#schema_Destiny-DamageType
	"""
	NONE = 0
	KINETIC = 1
	ARC = 2
	THERMAL = 3
	VOID = 4
	RAID = 5
	STASIS = 6
	STRAND = 7


class DestinyTalentNodeStepWeaponPerformances(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyTalentNodeStepWeaponPerformances.html#schema_Destiny-Definitions-DestinyTalentNodeStepWeaponPerformances
	"""
	NONE = 0
	RATE_OF_FIRE = 1
	DAMAGE = 2
	ACCURACY = 4
	RANGE = 8
	ZOOM = 16
	RECOIL = 32
	READY = 64
	RELOAD = 128
	HAIR_TRIGGER = 256
	AMMO_AND_MAGAZINE = 512
	TRACKING_AND_DETONATION = 1024
	SHOTGUN_SPREAD = 2048
	CHARGE_TIME = 4096
	ALL = 8191


class DestinyTalentNodeStepImpactEffects(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyTalentNodeStepImpactEffects.html#schema_Destiny-Definitions-DestinyTalentNodeStepImpactEffects
	"""
	NONE = 0
	ARMOR_PIERCING = 1
	RICOCHET = 2
	FLINCH = 4
	COLLATERAL_DAMAGE = 8
	DISORIENT = 16
	HIGHLIGHT_TARGET = 32
	ALL = 63


class DestinyTalentNodeStepGuardianAttributes(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyTalentNodeStepGuardianAttributes.html#schema_Destiny-Definitions-DestinyTalentNodeStepGuardianAttributes
	"""
	NONE = 0
	STATS = 1
	SHIELDS = 2
	HEALTH = 4
	REVIVE = 8
	AIM_UNDER_FIRE = 16
	RADAR = 32
	INVISIBILITY = 64
	REPUTATIONS = 128
	ALL = 255


class DestinyTalentNodeStepLightAbilities(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyTalentNodeStepLightAbilities.html#schema_Destiny-Definitions-DestinyTalentNodeStepLightAbilities
	"""
	NONE = 0
	GRENADES = 1
	MELEE = 2
	MOVEMENT_MODES = 4
	ORBS = 8
	SUPER_ENERGY = 16
	SUPER_MODS = 32
	ALL = 63


class DestinyTalentNodeStepDamageTypes(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyTalentNodeStepDamageTypes.html#schema_Destiny-Definitions-DestinyTalentNodeStepDamageTypes
	"""
	NONE = 0
	KINETIC = 1
	ARC = 2
	SOLAR = 4
	VOID = 8
	ALL = 15


class DestinyObjectiveUiStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyObjectiveUiStyle.html#schema_Destiny-DestinyObjectiveUiStyle
	"""
	NONE = 0
	HIGHLIGHTED = 1
	CRAFTING_WEAPON_LEVEL = 2
	CRAFTING_WEAPON_LEVEL_PROGRESS = 3
	CRAFTING_WEAPON_TIMESTAMP = 4
	CRAFTING_MEMENTOS = 5
	CRAFTING_MEMENTO_TITLE = 6


class DestinyActivityNavPointType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyActivityNavPointType.html#schema_Destiny-DestinyActivityNavPointType
	"""
	INACTIVE = 0
	PRIMARY_OBJECTIVE = 1
	SECONDARY_OBJECTIVE = 2
	TRAVEL_OBJECTIVE = 3
	PUBLIC_EVENT_OBJECTIVE = 4
	AMMO_CACHE = 5
	POINT_TYPE_FLAG = 6
	CAPTURE_POINT = 7
	DEFENSIVE_ENCOUNTER = 8
	GHOST_INTERACTION = 9
	KILL_AI = 10
	QUEST_ITEM = 11
	PATROL_MISSION = 12
	INCOMING = 13
	ARENA_OBJECTIVE = 14
	AUTOMATION_HINT = 15
	TRACKED_QUEST = 16


class DestinyActivityModeType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-DestinyActivityModeType.html#schema_Destiny-HistoricalStats-Definitions-DestinyActivityModeType
	"""
	NONE = 0
	STORY = 2
	STRIKE = 3
	RAID = 4
	ALL_PV_P = 5
	PATROL = 6
	ALL_PV_E = 7
	RESERVED9 = 9
	CONTROL = 10
	RESERVED11 = 11
	CLASH = 12
	RESERVED13 = 13
	CRIMSON_DOUBLES = 15
	NIGHTFALL = 16
	HEROIC_NIGHTFALL = 17
	ALL_STRIKES = 18
	IRON_BANNER = 19
	RESERVED20 = 20
	RESERVED21 = 21
	RESERVED22 = 22
	RESERVED24 = 24
	ALL_MAYHEM = 25
	RESERVED26 = 26
	RESERVED27 = 27
	RESERVED28 = 28
	RESERVED29 = 29
	RESERVED30 = 30
	SUPREMACY = 31
	PRIVATE_MATCHES_ALL = 32
	SURVIVAL = 37
	COUNTDOWN = 38
	TRIALS_OF_THE_NINE = 39
	SOCIAL = 40
	TRIALS_COUNTDOWN = 41
	TRIALS_SURVIVAL = 42
	IRON_BANNER_CONTROL = 43
	IRON_BANNER_CLASH = 44
	IRON_BANNER_SUPREMACY = 45
	SCORED_NIGHTFALL = 46
	SCORED_HEROIC_NIGHTFALL = 47
	RUMBLE = 48
	ALL_DOUBLES = 49
	DOUBLES = 50
	PRIVATE_MATCHES_CLASH = 51
	PRIVATE_MATCHES_CONTROL = 52
	PRIVATE_MATCHES_SUPREMACY = 53
	PRIVATE_MATCHES_COUNTDOWN = 54
	PRIVATE_MATCHES_SURVIVAL = 55
	PRIVATE_MATCHES_MAYHEM = 56
	PRIVATE_MATCHES_RUMBLE = 57
	HEROIC_ADVENTURE = 58
	SHOWDOWN = 59
	LOCKDOWN = 60
	SCORCHED = 61
	SCORCHED_TEAM = 62
	GAMBIT = 63
	ALL_PV_E_COMPETITIVE = 64
	BREAKTHROUGH = 65
	BLACK_ARMORY_RUN = 66
	SALVAGE = 67
	IRON_BANNER_SALVAGE = 68
	PV_P_COMPETITIVE = 69
	PV_P_QUICKPLAY = 70
	CLASH_QUICKPLAY = 71
	CLASH_COMPETITIVE = 72
	CONTROL_QUICKPLAY = 73
	CONTROL_COMPETITIVE = 74
	GAMBIT_PRIME = 75
	RECKONING = 76
	MENAGERIE = 77
	VEX_OFFENSIVE = 78
	NIGHTMARE_HUNT = 79
	ELIMINATION = 80
	MOMENTUM = 81
	DUNGEON = 82
	SUNDIAL = 83
	TRIALS_OF_OSIRIS = 84
	DARES = 85
	OFFENSIVE = 86
	LOST_SECTOR = 87
	RIFT = 88
	ZONE_CONTROL = 89
	IRON_BANNER_RIFT = 90
	IRON_BANNER_ZONE_CONTROL = 91


class DestinyActivityModeCategory(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyActivityModeCategory.html#schema_Destiny-DestinyActivityModeCategory
	"""
	NONE = 0
	PV_E = 1
	PV_P = 2
	PV_E_COMPETITIVE = 3


class DestinyItemSubType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyItemSubType.html#schema_Destiny-DestinyItemSubType
	"""
	NONE = 0
	CRUCIBLE = 1
	VANGUARD = 2
	EXOTIC = 5
	AUTO_RIFLE = 6
	SHOTGUN = 7
	MACHINEGUN = 8
	HAND_CANNON = 9
	ROCKET_LAUNCHER = 10
	FUSION_RIFLE = 11
	SNIPER_RIFLE = 12
	PULSE_RIFLE = 13
	SCOUT_RIFLE = 14
	CRM = 16
	SIDEARM = 17
	SWORD = 18
	MASK = 19
	SHADER = 20
	ORNAMENT = 21
	FUSION_RIFLE_LINE = 22
	GRENADE_LAUNCHER = 23
	SUBMACHINE_GUN = 24
	TRACE_RIFLE = 25
	HELMET_ARMOR = 26
	GAUNTLETS_ARMOR = 27
	CHEST_ARMOR = 28
	LEG_ARMOR = 29
	CLASS_ARMOR = 30
	BOW = 31
	DUMMY_REPEATABLE_BOUNTY = 32
	GLAIVE = 33


class DestinyGraphNodeState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyGraphNodeState.html#schema_Destiny-DestinyGraphNodeState
	"""
	HIDDEN = 0
	VISIBLE = 1
	TEASER = 2
	INCOMPLETE = 3
	COMPLETED = 4


class DestinyRewardSourceCategory(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-DestinyRewardSourceCategory.html#schema_Destiny-Definitions-DestinyRewardSourceCategory
	"""
	NONE = 0
	ACTIVITY = 1
	VENDOR = 2
	AGGREGATE = 3


class DestinyPresentationNodeType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyPresentationNodeType.html#schema_Destiny-DestinyPresentationNodeType
	"""
	DEFAULT = 0
	CATEGORY = 1
	COLLECTIBLES = 2
	RECORDS = 3
	METRIC = 4
	CRAFTABLE = 5


class DestinyScope(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyScope.html#schema_Destiny-DestinyScope
	"""
	PROFILE = 0
	CHARACTER = 1


class DestinyPresentationDisplayStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyPresentationDisplayStyle.html#schema_Destiny-DestinyPresentationDisplayStyle
	"""
	CATEGORY = 0
	BADGE = 1
	MEDALS = 2
	COLLECTIBLE = 3
	RECORD = 4
	SEASONAL_TRIUMPH = 5
	GUARDIAN_RANK = 6


class DestinyRecordValueStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyRecordValueStyle.html#schema_Destiny-DestinyRecordValueStyle
	"""
	INTEGER = 0
	PERCENTAGE = 1
	MILLISECONDS = 2
	BOOLEAN = 3
	DECIMAL = 4


class DestinyRecordToastStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyRecordToastStyle.html#schema_Destiny-DestinyRecordToastStyle
	"""
	NONE = 0
	RECORD = 1
	LORE = 2
	BADGE = 3
	META_RECORD = 4
	MEDAL_COMPLETE = 5
	SEASON_CHALLENGE_COMPLETE = 6
	GILDED_TITLE_COMPLETE = 7
	CRAFTING_RECIPE_UNLOCKED = 8
	TOAST_GUARDIAN_RANK_DETAILS = 9


class DestinyPresentationScreenStyle(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyPresentationScreenStyle.html#schema_Destiny-DestinyPresentationScreenStyle
	"""
	DEFAULT = 0
	CATEGORY_SETS = 1
	BADGE = 2


class PlugUiStyles(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-PlugUiStyles.html#schema_Destiny-PlugUiStyles
	"""
	NONE = 0
	MASTERWORK = 1


class PlugAvailabilityMode(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-PlugAvailabilityMode.html#schema_Destiny-PlugAvailabilityMode
	"""
	NORMAL = 0
	UNAVAILABLE_IF_SOCKET_CONTAINS_MATCHING_PLUG_CATEGORY = 1
	AVAILABLE_IF_SOCKET_CONTAINS_MATCHING_PLUG_CATEGORY = 2


class DestinyEnergyType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyEnergyType.html#schema_Destiny-DestinyEnergyType
	"""
	ANY = 0
	ARC = 1
	THERMAL = 2
	VOID = 3
	GHOST = 4
	SUBCLASS = 5
	STASIS = 6


class SocketPlugSources(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-SocketPlugSources.html#schema_Destiny-SocketPlugSources
	"""
	NONE = 0
	INVENTORY_SOURCED = 1
	REUSABLE_PLUG_ITEMS = 2
	PROFILE_PLUG_SET = 4
	CHARACTER_PLUG_SET = 8


class ItemPerkVisibility(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-ItemPerkVisibility.html#schema_Destiny-ItemPerkVisibility
	"""
	VISIBLE = 0
	DISABLED = 1
	HIDDEN = 2


class SpecialItemType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-SpecialItemType.html#schema_Destiny-SpecialItemType
	"""
	NONE = 0
	SPECIAL_CURRENCY = 1
	ARMOR = 8
	WEAPON = 9
	ENGRAM = 23
	CONSUMABLE = 24
	EXCHANGE_MATERIAL = 25
	MISSION_REWARD = 27
	CURRENCY = 29


class DestinyItemType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyItemType.html#schema_Destiny-DestinyItemType
	"""
	NONE = 0
	CURRENCY = 1
	ARMOR = 2
	WEAPON = 3
	MESSAGE = 7
	ENGRAM = 8
	CONSUMABLE = 9
	EXCHANGE_MATERIAL = 10
	MISSION_REWARD = 11
	QUEST_STEP = 12
	QUEST_STEP_COMPLETE = 13
	EMBLEM = 14
	QUEST = 15
	SUBCLASS = 16
	CLAN_BANNER = 17
	AURA = 18
	MOD = 19
	DUMMY = 20
	SHIP = 21
	VEHICLE = 22
	EMOTE = 23
	GHOST = 24
	PACKAGE = 25
	BOUNTY = 26
	WRAPPER = 27
	SEASONAL_ARTIFACT = 28
	FINISHER = 29
	PATTERN = 30


class DestinyBreakerType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyBreakerType.html#schema_Destiny-DestinyBreakerType
	"""
	NONE = 0
	SHIELD_PIERCING = 1
	DISRUPTION = 2
	STAGGER = 3


class DestinyProgressionRewardItemAcquisitionBehavior(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyProgressionRewardItemAcquisitionBehavior.html#schema_Destiny-DestinyProgressionRewardItemAcquisitionBehavior
	"""
	INSTANT = 0
	PLAYER_CLAIM_REQUIRED = 1


class GroupAllianceStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupAllianceStatus.html#schema_GroupsV2-GroupAllianceStatus
	"""
	UNALLIED = 0
	PARENT = 1
	CHILD = 2


class GroupPotentialMemberStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupPotentialMemberStatus.html#schema_GroupsV2-GroupPotentialMemberStatus
	"""
	NONE = 0
	APPLICANT = 1
	INVITEE = 2


class ForumRecruitmentIntensityLabel(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumRecruitmentIntensityLabel.html#schema_Forum-ForumRecruitmentIntensityLabel
	"""
	NONE = 0
	CASUAL = 1
	PROFESSIONAL = 2


class ForumRecruitmentToneLabel(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumRecruitmentToneLabel.html#schema_Forum-ForumRecruitmentToneLabel
	"""
	NONE = 0
	FAMILY_FRIENDLY = 1
	ROWDY = 2


class ForumPostSortEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-ForumPostSortEnum.html#schema_Forum-ForumPostSortEnum
	"""
	DEFAULT = 0
	OLDEST_FIRST = 1


class GroupDateRange(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupDateRange.html#schema_GroupsV2-GroupDateRange
	"""
	ALL = 0
	PAST_DAY = 1
	PAST_WEEK = 2
	PAST_MONTH = 3
	PAST_YEAR = 4


class GroupSortBy(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupSortBy.html#schema_GroupsV2-GroupSortBy
	"""
	NAME = 0
	DATE = 1
	POPULARITY = 2
	ID = 3


class GroupMemberCountFilter(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupMemberCountFilter.html#schema_GroupsV2-GroupMemberCountFilter
	"""
	ALL = 0
	ONE_TO_TEN = 1
	ELEVEN_TO_ONE_HUNDRED = 2
	GREATER_THAN_ONE_HUNDRED = 3


class IgnoreLength(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Ignores-IgnoreLength.html#schema_Ignores-IgnoreLength
	"""
	NONE = 0
	WEEK = 1
	TWO_WEEKS = 2
	THREE_WEEKS = 3
	MONTH = 4
	THREE_MONTHS = 5
	SIX_MONTHS = 6
	YEAR = 7
	FOREVER = 8
	THREE_MINUTES = 9
	HOUR = 10
	THIRTY_DAYS = 11


class GroupApplicationResolveState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupApplicationResolveState.html#schema_GroupsV2-GroupApplicationResolveState
	"""
	UNRESOLVED = 0
	ACCEPTED = 1
	DENIED = 2
	RESCINDED = 3


class PlatformErrorCodes(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Exceptions-PlatformErrorCodes.html#schema_Exceptions-PlatformErrorCodes
	"""
	NONE = 0
	SUCCESS = 1
	TRANSPORT_EXCEPTION = 2
	UNHANDLED_EXCEPTION = 3
	NOT_IMPLEMENTED = 4
	SYSTEM_DISABLED = 5
	FAILED_TO_LOAD_AVAILABLE_LOCALES_CONFIGURATION = 6
	PARAMETER_PARSE_FAILURE = 7
	PARAMETER_INVALID_RANGE = 8
	BAD_REQUEST = 9
	AUTHENTICATION_INVALID = 10
	DATA_NOT_FOUND = 11
	INSUFFICIENT_PRIVILEGES = 12
	DUPLICATE = 13
	UNKNOWN_SQL_RESULT = 14
	VALIDATION_ERROR = 15
	VALIDATION_MISSING_FIELD_ERROR = 16
	VALIDATION_INVALID_INPUT_ERROR = 17
	INVALID_PARAMETERS = 18
	PARAMETER_NOT_FOUND = 19
	UNHANDLED_HTTP_EXCEPTION = 20
	NOT_FOUND = 21
	WEB_AUTH_MODULE_ASYNC_FAILED = 22
	INVALID_RETURN_VALUE = 23
	USER_BANNED = 24
	INVALID_POST_BODY = 25
	MISSING_POST_BODY = 26
	EXTERNAL_SERVICE_TIMEOUT = 27
	VALIDATION_LENGTH_ERROR = 28
	VALIDATION_RANGE_ERROR = 29
	JSON_DESERIALIZATION_ERROR = 30
	THROTTLE_LIMIT_EXCEEDED = 31
	VALIDATION_TAG_ERROR = 32
	VALIDATION_PROFANITY_ERROR = 33
	VALIDATION_URL_FORMAT_ERROR = 34
	THROTTLE_LIMIT_EXCEEDED_MINUTES = 35
	THROTTLE_LIMIT_EXCEEDED_MOMENTARILY = 36
	THROTTLE_LIMIT_EXCEEDED_SECONDS = 37
	EXTERNAL_SERVICE_UNKNOWN = 38
	VALIDATION_WORD_LENGTH_ERROR = 39
	VALIDATION_INVISIBLE_UNICODE = 40
	VALIDATION_BAD_NAMES = 41
	EXTERNAL_SERVICE_FAILED = 42
	SERVICE_RETIRED = 43
	UNKNOWN_SQL_EXCEPTION = 44
	UNSUPPORTED_LOCALE = 45
	INVALID_PAGE_NUMBER = 46
	MAXIMUM_PAGE_SIZE_EXCEEDED = 47
	SERVICE_UNSUPPORTED = 48
	VALIDATION_MAXIMUM_UNICODE_COMBINING_CHARACTERS = 49
	VALIDATION_MAXIMUM_SEQUENTIAL_CARRIAGE_RETURNS = 50
	PER_ENDPOINT_REQUEST_THROTTLE_EXCEEDED = 51
	AUTH_CONTEXT_CACHE_ASSERTION = 52
	EX_PLATFORM_STRING_VALIDATION_ERROR = 53
	PER_APPLICATION_THROTTLE_EXCEEDED = 54
	PER_APPLICATION_ANONYMOUS_THROTTLE_EXCEEDED = 55
	PER_APPLICATION_AUTHENTICATED_THROTTLE_EXCEEDED = 56
	PER_USER_THROTTLE_EXCEEDED = 57
	PAYLOAD_SIGNATURE_VERIFICATION_FAILURE = 58
	INVALID_SERVICE_AUTH_CONTEXT = 59
	OBSOLETE_CREDENTIAL_TYPE = 89
	UNABLE_TO_UN_PAIR_MOBILE_APP = 90
	UNABLE_TO_PAIR_MOBILE_APP = 91
	CANNOT_USE_MOBILE_AUTH_WITH_NON_MOBILE_PROVIDER = 92
	MISSING_DEVICE_COOKIE = 93
	FACEBOOK_TOKEN_EXPIRED = 94
	AUTH_TICKET_REQUIRED = 95
	COOKIE_CONTEXT_REQUIRED = 96
	UNKNOWN_AUTHENTICATION_ERROR = 97
	BUNGIE_NET_ACCOUNT_CREATION_REQUIRED = 98
	WEB_AUTH_REQUIRED = 99
	CONTENT_UNKNOWN_SQL_RESULT = 100
	CONTENT_NEED_UNIQUE_PATH = 101
	CONTENT_SQL_EXCEPTION = 102
	CONTENT_NOT_FOUND = 103
	CONTENT_SUCCESS_WITH_TAG_ADD_FAIL = 104
	CONTENT_SEARCH_MISSING_PARAMETERS = 105
	CONTENT_INVALID_ID = 106
	CONTENT_PHYSICAL_FILE_DELETION_ERROR = 107
	CONTENT_PHYSICAL_FILE_CREATION_ERROR = 108
	CONTENT_PERFORCE_SUBMISSION_ERROR = 109
	CONTENT_PERFORCE_INITIALIZATION_ERROR = 110
	CONTENT_DEPLOYMENT_PACKAGE_NOT_READY_ERROR = 111
	CONTENT_UPLOAD_FAILED = 112
	CONTENT_TOO_MANY_RESULTS = 113
	CONTENT_INVALID_STATE = 115
	CONTENT_NAVIGATION_PARENT_NOT_FOUND = 116
	CONTENT_NAVIGATION_PARENT_UPDATE_ERROR = 117
	DEPLOYMENT_PACKAGE_NOT_EDITABLE = 118
	CONTENT_VALIDATION_ERROR = 119
	CONTENT_PROPERTIES_VALIDATION_ERROR = 120
	CONTENT_TYPE_NOT_FOUND = 121
	DEPLOYMENT_PACKAGE_NOT_FOUND = 122
	CONTENT_SEARCH_INVALID_PARAMETERS = 123
	CONTENT_ITEM_PROPERTY_AGGREGATION_ERROR = 124
	DEPLOYMENT_PACKAGE_FILE_NOT_FOUND = 125
	CONTENT_PERFORCE_FILE_HISTORY_NOT_FOUND = 126
	CONTENT_ASSET_ZIP_CREATION_FAILURE = 127
	CONTENT_ASSET_ZIP_CREATION_BUSY = 128
	CONTENT_PROJECT_NOT_FOUND = 129
	CONTENT_FOLDER_NOT_FOUND = 130
	CONTENT_PACKAGES_INCONSISTENT = 131
	CONTENT_PACKAGES_INVALID_STATE = 132
	CONTENT_PACKAGES_INCONSISTENT_TYPE = 133
	CONTENT_CANNOT_DELETE_PACKAGE = 134
	CONTENT_LOCKED_FOR_CHANGES = 135
	CONTENT_FILE_UPLOAD_FAILED = 136
	CONTENT_NOT_REVIEWED = 137
	CONTENT_PERMISSION_DENIED = 138
	CONTENT_INVALID_EXTERNAL_URL = 139
	CONTENT_EXTERNAL_FILE_CANNOT_BE_IMPORTED_LOCALLY = 140
	CONTENT_TAG_SAVE_FAILURE = 141
	CONTENT_PERFORCE_UNMATCHED_FILE_ERROR = 142
	CONTENT_PERFORCE_CHANGELIST_RESULT_NOT_FOUND = 143
	CONTENT_PERFORCE_CHANGELIST_FILE_ITEMS_NOT_FOUND = 144
	CONTENT_PERFORCE_INVALID_REVISION_ERROR = 145
	CONTENT_UNLOADED_SAVE_RESULT = 146
	CONTENT_PROPERTY_INVALID_NUMBER = 147
	CONTENT_PROPERTY_INVALID_URL = 148
	CONTENT_PROPERTY_INVALID_DATE = 149
	CONTENT_PROPERTY_INVALID_SET = 150
	CONTENT_PROPERTY_CANNOT_DESERIALIZE = 151
	CONTENT_REGEX_VALIDATION_FAIL_ON_PROPERTY = 152
	CONTENT_MAX_LENGTH_FAIL_ON_PROPERTY = 153
	CONTENT_PROPERTY_UNEXPECTED_DESERIALIZATION_ERROR = 154
	CONTENT_PROPERTY_REQUIRED = 155
	CONTENT_CANNOT_CREATE_FILE = 156
	CONTENT_INVALID_MIGRATION_FILE = 157
	CONTENT_MIGRATION_ALTERING_PROCESSED_ITEM = 158
	CONTENT_PROPERTY_DEFINITION_NOT_FOUND = 159
	CONTENT_REVIEW_DATA_CHANGED = 160
	CONTENT_ROLLBACK_REVISION_NOT_IN_PACKAGE = 161
	CONTENT_ITEM_NOT_BASED_ON_LATEST_REVISION = 162
	CONTENT_UNAUTHORIZED = 163
	CONTENT_CANNOT_CREATE_DEPLOYMENT_PACKAGE = 164
	CONTENT_USER_NOT_FOUND = 165
	CONTENT_LOCALE_PERMISSION_DENIED = 166
	CONTENT_INVALID_LINK_TO_INTERNAL_ENVIRONMENT = 167
	CONTENT_INVALID_BLACKLISTED_CONTENT = 168
	CONTENT_MACRO_MALFORMED_NO_CONTENT_ID = 169
	CONTENT_MACRO_MALFORMED_NO_TEMPLATE_TYPE = 170
	CONTENT_ILLEGAL_B_NET_MEMBERSHIP_ID = 171
	CONTENT_LOCALE_DID_NOT_MATCH_EXPECTED = 172
	CONTENT_BABEL_CALL_FAILED = 173
	CONTENT_ENGLISH_POST_LIVE_FORBIDDEN = 174
	CONTENT_LOCALE_EDIT_PERMISSION_DENIED = 175
	CONTENT_STACK_UNKNOWN_ERROR = 176
	CONTENT_STACK_NOT_FOUND = 177
	CONTENT_STACK_RATE_LIMITED = 178
	CONTENT_STACK_TIMEOUT = 179
	CONTENT_STACK_SERVICE_ERROR = 180
	CONTENT_STACK_DESERIALIZATION_FAILURE = 181
	USER_NON_UNIQUE_NAME = 200
	USER_MANUAL_LINKING_STEP_REQUIRED = 201
	USER_CREATE_UNKNOWN_SQL_RESULT = 202
	USER_CREATE_UNKNOWN_SQL_EXCEPTION = 203
	USER_MALFORMED_MEMBERSHIP_ID = 204
	USER_CANNOT_FIND_REQUESTED_USER = 205
	USER_CANNOT_LOAD_ACCOUNT_CREDENTIAL_LINK_INFO = 206
	USER_INVALID_MOBILE_APP_TYPE = 207
	USER_MISSING_MOBILE_PAIRING_INFO = 208
	USER_CANNOT_GENERATE_MOBILE_KEY_WHILE_USING_MOBILE_CREDENTIAL = 209
	USER_GENERATE_MOBILE_KEY_EXISTING_SLOT_COLLISION = 210
	USER_DISPLAY_NAME_MISSING_OR_INVALID = 211
	USER_CANNOT_LOAD_ACCOUNT_PROFILE_DATA = 212
	USER_CANNOT_SAVE_USER_PROFILE_DATA = 213
	USER_EMAIL_MISSING_OR_INVALID = 214
	USER_TERMS_OF_USE_REQUIRED = 215
	USER_CANNOT_CREATE_NEW_ACCOUNT_WHILE_LOGGED_IN = 216
	USER_CANNOT_RESOLVE_CENTRAL_ACCOUNT = 217
	USER_INVALID_AVATAR = 218
	USER_MISSING_CREATED_USER_RESULT = 219
	USER_CANNOT_CHANGE_UNIQUE_NAME_YET = 220
	USER_CANNOT_CHANGE_DISPLAY_NAME_YET = 221
	USER_CANNOT_CHANGE_EMAIL = 222
	USER_UNIQUE_NAME_MUST_START_WITH_LETTER = 223
	USER_NO_LINKED_ACCOUNTS_SUPPORT_FRIEND_LISTINGS = 224
	USER_ACKNOWLEDGMENT_TABLE_FULL = 225
	USER_CREATION_DESTINY_MEMBERSHIP_REQUIRED = 226
	USER_FRIENDS_TOKEN_NEEDS_REFRESH = 227
	USER_EMAIL_VALIDATION_UNKNOWN = 228
	USER_EMAIL_VALIDATION_LIMIT = 229
	TRANSACTION_EMAIL_SEND_FAILURE = 230
	MAIL_HOOK_PERMISSION_FAILURE = 231
	MAIL_SERVICE_RATE_LIMIT = 232
	USER_EMAIL_MUST_BE_VERIFIED = 233
	USER_MUST_ALLOW_CUSTOMER_SERVICE_EMAILS = 234
	NON_TRANSACTIONAL_EMAIL_SEND_FAILURE = 235
	UNKNOWN_ERROR_SETTING_GLOBAL_DISPLAY_NAME = 236
	DUPLICATE_GLOBAL_DISPLAY_NAME = 237
	ERROR_RUNNING_NAME_VALIDATION_CHECKS = 238
	ERROR_DATABASE_GLOBAL_NAME = 239
	ERROR_NO_AVAILABLE_NAME_CHANGES = 240
	ERROR_NAME_ALREADY_SET_TO_INPUT = 241
	USER_DISPLAY_NAME_LESS_THAN_MIN_LENGTH = 242
	USER_DISPLAY_NAME_GREATER_THAN_MAX_LENGTH = 243
	USER_DISPLAY_NAME_CONTAINS_UNACCEPTABLE_OR_INVALID_CONTENT = 244
	MESSAGING_UNKNOWN_ERROR = 300
	MESSAGING_SELF_ERROR = 301
	MESSAGING_SEND_THROTTLE = 302
	MESSAGING_NO_BODY = 303
	MESSAGING_TOO_MANY_USERS = 304
	MESSAGING_CAN_NOT_LEAVE_CONVERSATION = 305
	MESSAGING_UNABLE_TO_SEND = 306
	MESSAGING_DELETED_USER_FORBIDDEN = 307
	MESSAGING_CANNOT_DELETE_EXTERNAL_CONVERSATION = 308
	MESSAGING_GROUP_CHAT_DISABLED = 309
	MESSAGING_MUST_INCLUDE_SELF_IN_PRIVATE_MESSAGE = 310
	MESSAGING_SENDER_IS_BANNED = 311
	MESSAGING_GROUP_OPTIONAL_CHAT_EXCEEDED_MAXIMUM = 312
	PRIVATE_MESSAGING_REQUIRES_DESTINY_MEMBERSHIP = 313
	MESSAGING_SEND_DAILY_THROTTLE = 314
	ADD_SURVEY_ANSWERS_UNKNOWN_SQL_EXCEPTION = 400
	FORUM_BODY_CANNOT_BE_EMPTY = 500
	FORUM_SUBJECT_CANNOT_BE_EMPTY_ON_TOPIC_POST = 501
	FORUM_CANNOT_LOCATE_PARENT_POST = 502
	FORUM_THREAD_LOCKED_FOR_REPLIES = 503
	FORUM_UNKNOWN_SQL_RESULT_DURING_CREATE_POST = 504
	FORUM_UNKNOWN_TAG_CREATION_ERROR = 505
	FORUM_UNKNOWN_SQL_RESULT_DURING_TAG_ITEM = 506
	FORUM_UNKNOWN_EXCEPTION_CREATE_POST = 507
	FORUM_QUESTION_MUST_BE_TOPIC_POST = 508
	FORUM_EXCEPTION_DURING_TAG_SEARCH = 509
	FORUM_EXCEPTION_DURING_TOPIC_RETRIEVAL = 510
	FORUM_ALIASED_TAG_ERROR = 511
	FORUM_CANNOT_LOCATE_THREAD = 512
	FORUM_UNKNOWN_EXCEPTION_EDIT_POST = 513
	FORUM_CANNOT_LOCATE_POST = 514
	FORUM_UNKNOWN_EXCEPTION_GET_OR_CREATE_TAGS = 515
	FORUM_EDIT_PERMISSION_DENIED = 516
	FORUM_UNKNOWN_SQL_RESULT_DURING_TAG_ID_RETRIEVAL = 517
	FORUM_CANNOT_GET_RATING = 518
	FORUM_UNKNOWN_EXCEPTION_GET_RATING = 519
	FORUM_RATINGS_ACCESS_ERROR = 520
	FORUM_RELATED_POST_ACCESS_ERROR = 521
	FORUM_LATEST_REPLY_ACCESS_ERROR = 522
	FORUM_USER_STATUS_ACCESS_ERROR = 523
	FORUM_AUTHOR_ACCESS_ERROR = 524
	FORUM_GROUP_ACCESS_ERROR = 525
	FORUM_URL_EXPECTED_BUT_MISSING = 526
	FORUM_REPLIES_CANNOT_BE_EMPTY = 527
	FORUM_REPLIES_CANNOT_BE_IN_DIFFERENT_GROUPS = 528
	FORUM_SUB_TOPIC_CANNOT_BE_CREATED_AT_THIS_THREAD_LEVEL = 529
	FORUM_CANNOT_CREATE_CONTENT_TOPIC = 530
	FORUM_TOPIC_DOES_NOT_EXIST = 531
	FORUM_CONTENT_COMMENTS_NOT_ALLOWED = 532
	FORUM_UNKNOWN_SQL_RESULT_DURING_EDIT_POST = 533
	FORUM_UNKNOWN_SQL_RESULT_DURING_GET_POST = 534
	FORUM_POST_VALIDATION_BAD_URL = 535
	FORUM_BODY_TOO_LONG = 536
	FORUM_SUBJECT_TOO_LONG = 537
	FORUM_ANNOUNCEMENT_NOT_ALLOWED = 538
	FORUM_CANNOT_SHARE_OWN_POST = 539
	FORUM_EDIT_NO_OP = 540
	FORUM_UNKNOWN_DATABASE_ERROR_DURING_GET_POST = 541
	FORUM_EXCEEED_MAXIMUM_ROW_LIMIT = 542
	FORUM_CANNOT_SHARE_PRIVATE_POST = 543
	FORUM_CANNOT_CROSS_POST_BETWEEN_GROUPS = 544
	FORUM_INCOMPATIBLE_CATEGORIES = 555
	FORUM_CANNOT_USE_THESE_CATEGORIES_ON_NON_TOPIC_POST = 556
	FORUM_CAN_ONLY_DELETE_TOPICS = 557
	FORUM_DELETE_SQL_EXCEPTION = 558
	FORUM_DELETE_SQL_UNKNOWN_RESULT = 559
	FORUM_TOO_MANY_TAGS = 560
	FORUM_CAN_ONLY_RATE_TOPICS = 561
	FORUM_BANNED_POSTS_CANNOT_BE_EDITED = 562
	FORUM_THREAD_ROOT_IS_BANNED = 563
	FORUM_CANNOT_USE_OFFICIAL_TAG_CATEGORY_AS_TAG = 564
	FORUM_ANSWER_CANNOT_BE_MADE_ON_CREATE_POST = 565
	FORUM_ANSWER_CANNOT_BE_MADE_ON_EDIT_POST = 566
	FORUM_ANSWER_POST_ID_IS_NOT_A_DIRECT_REPLY_OF_QUESTION = 567
	FORUM_ANSWER_TOPIC_ID_IS_NOT_A_QUESTION = 568
	FORUM_UNKNOWN_EXCEPTION_DURING_MARK_ANSWER = 569
	FORUM_UNKNOWN_SQL_RESULT_DURING_MARK_ANSWER = 570
	FORUM_CANNOT_RATE_YOUR_OWN_POSTS = 571
	FORUM_POLLS_MUST_BE_THE_FIRST_POST_IN_TOPIC = 572
	FORUM_INVALID_POLL_INPUT = 573
	FORUM_GROUP_ADMIN_EDIT_NON_MEMBER = 574
	FORUM_CANNOT_EDIT_MODERATOR_EDITED_POST = 575
	FORUM_REQUIRES_DESTINY_MEMBERSHIP = 576
	FORUM_UNEXPECTED_ERROR = 577
	FORUM_AGE_LOCK = 578
	FORUM_MAX_PAGES = 579
	FORUM_MAX_PAGES_OLDEST_FIRST = 580
	FORUM_CANNOT_APPLY_FORUM_ID_WITHOUT_TAGS = 581
	FORUM_CANNOT_APPLY_FORUM_ID_TO_NON_TOPICS = 582
	FORUM_CANNOT_DOWNVOTE_COMMUNITY_CREATIONS = 583
	FORUM_TOPICS_MUST_HAVE_OFFICIAL_CATEGORY = 584
	FORUM_RECRUITMENT_TOPIC_MALFORMED = 585
	FORUM_RECRUITMENT_TOPIC_NOT_FOUND = 586
	FORUM_RECRUITMENT_TOPIC_NO_SLOTS_REMAINING = 587
	FORUM_RECRUITMENT_TOPIC_KICK_BAN = 588
	FORUM_RECRUITMENT_TOPIC_REQUIREMENTS_NOT_MET = 589
	FORUM_RECRUITMENT_TOPIC_NO_PLAYERS = 590
	FORUM_RECRUITMENT_APPROVE_FAIL_MESSAGE_BAN = 591
	FORUM_RECRUITMENT_GLOBAL_BAN = 592
	FORUM_USER_BANNED_FROM_THIS_TOPIC = 593
	FORUM_RECRUITMENT_FIRETEAM_MEMBERS_ONLY = 594
	FORUM_REQUIRES_DESTINY2_PROGRESS = 595
	FORUM_REQUIRES_DESTINY2_ENTITLEMENT_PURCHASE = 596
	GROUP_MEMBERSHIP_APPLICATION_ALREADY_RESOLVED = 601
	GROUP_MEMBERSHIP_ALREADY_APPLIED = 602
	GROUP_MEMBERSHIP_INSUFFICIENT_PRIVILEGES = 603
	GROUP_ID_NOT_RETURNED_FROM_CREATION = 604
	GROUP_SEARCH_INVALID_PARAMETERS = 605
	GROUP_MEMBERSHIP_PENDING_APPLICATION_NOT_FOUND = 606
	GROUP_INVALID_ID = 607
	GROUP_INVALID_MEMBERSHIP_ID = 608
	GROUP_INVALID_MEMBERSHIP_TYPE = 609
	GROUP_MISSING_TAGS = 610
	GROUP_MEMBERSHIP_NOT_FOUND = 611
	GROUP_INVALID_RATING = 612
	GROUP_USER_FOLLOWING_ACCESS_ERROR = 613
	GROUP_USER_MEMBERSHIP_ACCESS_ERROR = 614
	GROUP_CREATOR_ACCESS_ERROR = 615
	GROUP_ADMIN_ACCESS_ERROR = 616
	GROUP_PRIVATE_POST_NOT_VIEWABLE = 617
	GROUP_MEMBERSHIP_NOT_LOGGED_IN = 618
	GROUP_NOT_DELETED = 619
	GROUP_UNKNOWN_ERROR_UNDELETING_GROUP = 620
	GROUP_DELETED = 621
	GROUP_NOT_FOUND = 622
	GROUP_MEMBER_BANNED = 623
	GROUP_MEMBERSHIP_CLOSED = 624
	GROUP_PRIVATE_POST_OVERRIDE_ERROR = 625
	GROUP_NAME_TAKEN = 626
	GROUP_DELETION_GRACE_PERIOD_EXPIRED = 627
	GROUP_CANNOT_CHECK_BAN_STATUS = 628
	GROUP_MAXIMUM_MEMBERSHIP_COUNT_REACHED = 629
	NO_DESTINY_ACCOUNT_FOR_CLAN_PLATFORM = 630
	ALREADY_REQUESTING_MEMBERSHIP_FOR_CLAN_PLATFORM = 631
	ALREADY_CLAN_MEMBER_ON_PLATFORM = 632
	GROUP_JOINED_CANNOT_SET_CLAN_NAME = 633
	GROUP_LEFT_CANNOT_CLEAR_CLAN_NAME = 634
	GROUP_RELATIONSHIP_REQUEST_PENDING = 635
	GROUP_RELATIONSHIP_REQUEST_BLOCKED = 636
	GROUP_RELATIONSHIP_REQUEST_NOT_FOUND = 637
	GROUP_RELATIONSHIP_BLOCK_NOT_FOUND = 638
	GROUP_RELATIONSHIP_NOT_FOUND = 639
	GROUP_ALREADY_ALLIED = 641
	GROUP_ALREADY_MEMBER = 642
	GROUP_RELATIONSHIP_ALREADY_EXISTS = 643
	INVALID_GROUP_TYPES_FOR_RELATIONSHIP_REQUEST = 644
	GROUP_AT_MAXIMUM_ALLIANCES = 646
	GROUP_CANNOT_SET_CLAN_ONLY_SETTINGS = 647
	CLAN_CANNOT_SET_TWO_DEFAULT_POST_TYPES = 648
	GROUP_MEMBER_INVALID_MEMBER_TYPE = 649
	GROUP_INVALID_PLATFORM_TYPE = 650
	GROUP_MEMBER_INVALID_SORT = 651
	GROUP_INVALID_RESOLVE_STATE = 652
	CLAN_ALREADY_ENABLED_FOR_PLATFORM = 653
	CLAN_NOT_ENABLED_FOR_PLATFORM = 654
	CLAN_ENABLED_BUT_COULD_NOT_JOIN_NO_ACCOUNT = 655
	CLAN_ENABLED_BUT_COULD_NOT_JOIN_ALREADY_MEMBER = 656
	CLAN_CANNOT_JOIN_NO_CREDENTIAL = 657
	NO_CLAN_MEMBERSHIP_FOR_PLATFORM = 658
	GROUP_TO_GROUP_FOLLOW_LIMIT_REACHED = 659
	CHILD_GROUP_ALREADY_IN_ALLIANCE = 660
	OWNER_GROUP_ALREADY_IN_ALLIANCE = 661
	ALLIANCE_OWNER_CANNOT_JOIN_ALLIANCE = 662
	GROUP_NOT_IN_ALLIANCE = 663
	CHILD_GROUP_CANNOT_INVITE_TO_ALLIANCE = 664
	GROUP_TO_GROUP_ALREADY_FOLLOWED = 665
	GROUP_TO_GROUP_NOT_FOLLOWING = 666
	CLAN_MAXIMUM_MEMBERSHIP_REACHED = 667
	CLAN_NAME_NOT_VALID = 668
	CLAN_NAME_NOT_VALID_ERROR = 669
	ALLIANCE_OWNER_NOT_DEFINED = 670
	ALLIANCE_CHILD_NOT_DEFINED = 671
	CLAN_CULTURE_ILLEGAL_CHARACTERS = 672
	CLAN_TAG_ILLEGAL_CHARACTERS = 673
	CLAN_REQUIRES_INVITATION = 674
	CLAN_MEMBERSHIP_CLOSED = 675
	CLAN_INVITE_ALREADY_MEMBER = 676
	GROUP_INVITE_ALREADY_MEMBER = 677
	GROUP_JOIN_APPROVAL_REQUIRED = 678
	CLAN_TAG_REQUIRED = 679
	GROUP_NAME_CANNOT_START_OR_END_WITH_WHITE_SPACE = 680
	CLAN_CALLSIGN_CANNOT_START_OR_END_WITH_WHITE_SPACE = 681
	CLAN_MIGRATION_FAILED = 682
	CLAN_NOT_ENABLED_ALREADY_MEMBER_OF_ANOTHER_CLAN = 683
	GROUP_MODERATION_NOT_PERMITTED_ON_NON_MEMBERS = 684
	CLAN_CREATION_IN_WORLD_SERVER_FAILED = 685
	CLAN_NOT_FOUND = 686
	CLAN_MEMBERSHIP_LEVEL_DOES_NOT_PERMIT_THAT_ACTION = 687
	CLAN_MEMBER_NOT_FOUND = 688
	CLAN_MISSING_MEMBERSHIP_APPROVERS = 689
	CLAN_IN_WRONG_STATE_FOR_REQUESTED_ACTION = 690
	CLAN_NAME_ALREADY_USED = 691
	CLAN_TOO_FEW_MEMBERS = 692
	CLAN_INFO_CANNOT_BE_WHITESPACE = 693
	GROUP_CULTURE_THROTTLE = 694
	CLAN_TARGET_DISALLOWS_INVITES = 695
	CLAN_INVALID_OPERATION = 696
	CLAN_FOUNDER_CANNOT_LEAVE_WITHOUT_ABDICATION = 697
	CLAN_NAME_RESERVED = 698
	CLAN_APPLICANT_IN_CLAN_SO_NOW_INVITED = 699
	ACTIVITIES_UNKNOWN_EXCEPTION = 701
	ACTIVITIES_PARAMETER_NULL = 702
	ACTIVITY_COUNTS_DIABLED = 703
	ACTIVITY_SEARCH_INVALID_PARAMETERS = 704
	ACTIVITY_PERMISSION_DENIED = 705
	SHARE_ALREADY_SHARED = 706
	ACTIVITY_LOGGING_DISABLED = 707
	CLAN_REQUIRES_EXISTING_DESTINY_ACCOUNT = 750
	CLAN_NAME_RESTRICTED = 751
	CLAN_CREATION_BAN = 752
	CLAN_CREATION_TENURE_REQUIREMENTS_NOT_MET = 753
	CLAN_FIELD_CONTAINS_RESERVED_TERMS = 754
	CLAN_FIELD_CONTAINS_INAPPROPRIATE_CONTENT = 755
	ITEM_ALREADY_FOLLOWED = 801
	ITEM_NOT_FOLLOWED = 802
	CANNOT_FOLLOW_SELF = 803
	GROUP_FOLLOW_LIMIT_EXCEEDED = 804
	TAG_FOLLOW_LIMIT_EXCEEDED = 805
	USER_FOLLOW_LIMIT_EXCEEDED = 806
	FOLLOW_UNSUPPORTED_ENTITY_TYPE = 807
	NO_VALID_TAGS_IN_LIST = 900
	BELOW_MINIMUM_SUGGESTION_LENGTH = 901
	CANNOT_GET_SUGGESTIONS_ON_MULTIPLE_TAGS_SIMULTANEOUSLY = 902
	NOT_A_VALID_PARTIAL_TAG = 903
	TAG_SUGGESTIONS_UNKNOWN_SQL_RESULT = 904
	TAGS_UNABLE_TO_LOAD_POPULAR_TAGS_FROM_DATABASE = 905
	TAG_INVALID = 906
	TAG_NOT_FOUND = 907
	SINGLE_TAG_EXPECTED = 908
	TAGS_EXCEEDED_MAXIMUM_PER_ITEM = 909
	IGNORE_INVALID_PARAMETERS = 1000
	IGNORE_SQL_EXCEPTION = 1001
	IGNORE_ERROR_RETRIEVING_GROUP_PERMISSIONS = 1002
	IGNORE_ERROR_INSUFFICIENT_PERMISSION = 1003
	IGNORE_ERROR_RETRIEVING_ITEM = 1004
	IGNORE_CANNOT_IGNORE_SELF = 1005
	IGNORE_ILLEGAL_TYPE = 1006
	IGNORE_NOT_FOUND = 1007
	IGNORE_USER_GLOBALLY_IGNORED = 1008
	IGNORE_USER_IGNORED = 1009
	TARGET_USER_IGNORED = 1010
	NOTIFICATION_SETTING_INVALID = 1100
	PSN_API_EXPIRED_ACCESS_TOKEN = 1204
	P_S_N_EX_FORBIDDEN = 1205
	P_S_N_EX_SYSTEM_DISABLED = 1218
	PSN_API_ERROR_CODE_UNKNOWN = 1223
	PSN_API_ERROR_WEB_EXCEPTION = 1224
	PSN_API_BAD_REQUEST = 1225
	PSN_API_ACCESS_TOKEN_REQUIRED = 1226
	PSN_API_INVALID_ACCESS_TOKEN = 1227
	PSN_API_BANNED_USER = 1229
	PSN_API_ACCOUNT_UPGRADE_REQUIRED = 1230
	PSN_API_SERVICE_TEMPORARILY_UNAVAILABLE = 1231
	PSN_API_SERVER_BUSY = 1232
	PSN_API_UNDER_MAINTENANCE = 1233
	PSN_API_PROFILE_USER_NOT_FOUND = 1234
	PSN_API_PROFILE_PRIVACY_RESTRICTION = 1235
	PSN_API_PROFILE_UNDER_MAINTENANCE = 1236
	PSN_API_ACCOUNT_ATTRIBUTE_MISSING = 1237
	PSN_API_NO_PERMISSION = 1238
	PSN_API_TARGET_USER_BLOCKED = 1239
	PSN_API_JWKS_MISSING = 1240
	PSN_API_JWT_MALFORMED_HEADER = 1241
	PSN_API_JWT_MALFORMED_PAYLOAD = 1242
	XBL_EX_SYSTEM_DISABLED = 1300
	XBL_EX_UNKNOWN_ERROR = 1301
	XBL_API_ERROR_WEB_EXCEPTION = 1302
	XBL_STS_TOKEN_INVALID = 1303
	XBL_STS_MISSING_TOKEN = 1304
	XBL_STS_EXPIRED_TOKEN = 1305
	XBL_ACCESS_TO_THE_SANDBOX_DENIED = 1306
	XBL_MSA_RESPONSE_MISSING = 1307
	XBL_MSA_ACCESS_TOKEN_EXPIRED = 1308
	XBL_MSA_INVALID_REQUEST = 1309
	XBL_MSA_FRIENDS_REQUIRE_SIGN_IN = 1310
	XBL_USER_ACTION_REQUIRED = 1311
	XBL_PARENTAL_CONTROLS = 1312
	XBL_DEVELOPER_ACCOUNT = 1313
	XBL_USER_TOKEN_EXPIRED = 1314
	XBL_USER_TOKEN_INVALID = 1315
	XBL_OFFLINE = 1316
	XBL_UNKNOWN_ERROR_CODE = 1317
	XBL_MSA_INVALID_GRANT = 1318
	REPORT_NOT_YET_RESOLVED = 1400
	REPORT_OVERTURN_DOES_NOT_CHANGE_DECISION = 1401
	REPORT_NOT_FOUND = 1402
	REPORT_ALREADY_REPORTED = 1403
	REPORT_INVALID_RESOLUTION = 1404
	REPORT_NOT_ASSIGNED_TO_YOU = 1405
	LEGACY_GAME_STATS_SYSTEM_DISABLED = 1500
	LEGACY_GAME_STATS_UNKNOWN_ERROR = 1501
	LEGACY_GAME_STATS_MALFORMED_SNEAKER_NET_CODE = 1502
	DESTINY_ACCOUNT_ACQUISITION_FAILURE = 1600
	DESTINY_ACCOUNT_NOT_FOUND = 1601
	DESTINY_BUILD_STATS_DATABASE_ERROR = 1602
	DESTINY_CHARACTER_STATS_DATABASE_ERROR = 1603
	DESTINY_PV_P_STATS_DATABASE_ERROR = 1604
	DESTINY_PV_E_STATS_DATABASE_ERROR = 1605
	DESTINY_GRIMOIRE_STATS_DATABASE_ERROR = 1606
	DESTINY_STATS_PARAMETER_MEMBERSHIP_TYPE_PARSE_ERROR = 1607
	DESTINY_STATS_PARAMETER_MEMBERSHIP_ID_PARSE_ERROR = 1608
	DESTINY_STATS_PARAMETER_RANGE_PARSE_ERROR = 1609
	DESTINY_STRING_ITEM_HASH_NOT_FOUND = 1610
	DESTINY_STRING_SET_NOT_FOUND = 1611
	DESTINY_CONTENT_LOOKUP_NOT_FOUND_FOR_KEY = 1612
	DESTINY_CONTENT_ITEM_NOT_FOUND = 1613
	DESTINY_CONTENT_SECTION_NOT_FOUND = 1614
	DESTINY_CONTENT_PROPERTY_NOT_FOUND = 1615
	DESTINY_CONTENT_CONFIG_NOT_FOUND = 1616
	DESTINY_CONTENT_PROPERTY_BUCKET_VALUE_NOT_FOUND = 1617
	DESTINY_UNEXPECTED_ERROR = 1618
	DESTINY_INVALID_ACTION = 1619
	DESTINY_CHARACTER_NOT_FOUND = 1620
	DESTINY_INVALID_FLAG = 1621
	DESTINY_INVALID_REQUEST = 1622
	DESTINY_ITEM_NOT_FOUND = 1623
	DESTINY_INVALID_CUSTOMIZATION_CHOICES = 1624
	DESTINY_VENDOR_ITEM_NOT_FOUND = 1625
	DESTINY_INTERNAL_ERROR = 1626
	DESTINY_VENDOR_NOT_FOUND = 1627
	DESTINY_RECENT_ACTIVITIES_DATABASE_ERROR = 1628
	DESTINY_ITEM_BUCKET_NOT_FOUND = 1629
	DESTINY_INVALID_MEMBERSHIP_TYPE = 1630
	DESTINY_VERSION_INCOMPATIBILITY = 1631
	DESTINY_ITEM_ALREADY_IN_INVENTORY = 1632
	DESTINY_BUCKET_NOT_FOUND = 1633
	DESTINY_CHARACTER_NOT_IN_TOWER = 1634
	DESTINY_CHARACTER_NOT_LOGGED_IN = 1635
	DESTINY_DEFINITIONS_NOT_LOADED = 1636
	DESTINY_INVENTORY_FULL = 1637
	DESTINY_ITEM_FAILED_LEVEL_CHECK = 1638
	DESTINY_ITEM_FAILED_UNLOCK_CHECK = 1639
	DESTINY_ITEM_UNEQUIPPABLE = 1640
	DESTINY_ITEM_UNIQUE_EQUIP_RESTRICTED = 1641
	DESTINY_NO_ROOM_IN_DESTINATION = 1642
	DESTINY_SERVICE_FAILURE = 1643
	DESTINY_SERVICE_RETIRED = 1644
	DESTINY_TRANSFER_FAILED = 1645
	DESTINY_TRANSFER_NOT_FOUND_FOR_SOURCE_BUCKET = 1646
	DESTINY_UNEXPECTED_RESULT_IN_VENDOR_TRANSFER_CHECK = 1647
	DESTINY_UNIQUENESS_VIOLATION = 1648
	DESTINY_ERROR_DESERIALIZATION_FAILURE = 1649
	DESTINY_VALID_ACCOUNT_TICKET_REQUIRED = 1650
	DESTINY_SHARD_RELAY_CLIENT_TIMEOUT = 1651
	DESTINY_SHARD_RELAY_PROXY_TIMEOUT = 1652
	DESTINY_P_G_C_R_NOT_FOUND = 1653
	DESTINY_ACCOUNT_MUST_BE_OFFLINE = 1654
	DESTINY_CAN_ONLY_EQUIP_IN_GAME = 1655
	DESTINY_CANNOT_PERFORM_ACTION_ON_EQUIPPED_ITEM = 1656
	DESTINY_QUEST_ALREADY_COMPLETED = 1657
	DESTINY_QUEST_ALREADY_TRACKED = 1658
	DESTINY_TRACKABLE_QUESTS_FULL = 1659
	DESTINY_ITEM_NOT_TRANSFERRABLE = 1660
	DESTINY_VENDOR_PURCHASE_NOT_ALLOWED = 1661
	DESTINY_CONTENT_VERSION_MISMATCH = 1662
	DESTINY_ITEM_ACTION_FORBIDDEN = 1663
	DESTINY_REFUND_INVALID = 1664
	DESTINY_PRIVACY_RESTRICTION = 1665
	DESTINY_ACTION_INSUFFICIENT_PRIVILEGES = 1666
	DESTINY_INVALID_CLAIM_EXCEPTION = 1667
	DESTINY_LEGACY_PLATFORM_RESTRICTED = 1668
	DESTINY_LEGACY_PLATFORM_IN_USE = 1669
	DESTINY_LEGACY_PLATFORM_INACCESSIBLE = 1670
	DESTINY_CANNOT_PERFORM_ACTION_AT_THIS_LOCATION = 1671
	DESTINY_THROTTLED_BY_GAME_SERVER = 1672
	DESTINY_ITEM_NOT_TRANSFERRABLE_HAS_SIDE_EFFECTS = 1673
	DESTINY_ITEM_LOCKED = 1674
	DESTINY_CANNOT_AFFORD_MATERIAL_REQUIREMENTS = 1675
	DESTINY_FAILED_PLUG_INSERTION_RULES = 1676
	DESTINY_SOCKET_NOT_FOUND = 1677
	DESTINY_SOCKET_ACTION_NOT_ALLOWED = 1678
	DESTINY_SOCKET_ALREADY_HAS_PLUG = 1679
	DESTINY_PLUG_ITEM_NOT_AVAILABLE = 1680
	DESTINY_CHARACTER_LOGGED_IN_NOT_ALLOWED = 1681
	DESTINY_PUBLIC_ACCOUNT_NOT_ACCESSIBLE = 1682
	DESTINY_CLAIMS_ITEM_ALREADY_CLAIMED = 1683
	DESTINY_CLAIMS_NO_INVENTORY_SPACE = 1684
	DESTINY_CLAIMS_REQUIRED_LEVEL_NOT_MET = 1685
	DESTINY_CLAIMS_INVALID_STATE = 1686
	DESTINY_NOT_ENOUGH_ROOM_FOR_MULTIPLE_REWARDS = 1687
	DESTINY_DIRECT_BABEL_CLIENT_TIMEOUT = 1688
	FB_INVALID_REQUEST = 1800
	FB_REDIRECT_MISMATCH = 1801
	FB_ACCESS_DENIED = 1802
	FB_UNSUPPORTED_RESPONSE_TYPE = 1803
	FB_INVALID_SCOPE = 1804
	FB_UNSUPPORTED_GRANT_TYPE = 1805
	FB_INVALID_GRANT = 1806
	INVITATION_EXPIRED = 1900
	INVITATION_UNKNOWN_TYPE = 1901
	INVITATION_INVALID_RESPONSE_STATUS = 1902
	INVITATION_INVALID_TYPE = 1903
	INVITATION_ALREADY_PENDING = 1904
	INVITATION_INSUFFICIENT_PERMISSION = 1905
	INVITATION_INVALID_CODE = 1906
	INVITATION_INVALID_TARGET_STATE = 1907
	INVITATION_CANNOT_BE_REACTIVATED = 1908
	INVITATION_NO_RECIPIENTS = 1910
	INVITATION_GROUP_CANNOT_SEND_TO_SELF = 1911
	INVITATION_TOO_MANY_RECIPIENTS = 1912
	INVITATION_INVALID = 1913
	INVITATION_NOT_FOUND = 1914
	TOKEN_INVALID = 2000
	TOKEN_BAD_FORMAT = 2001
	TOKEN_ALREADY_CLAIMED = 2002
	TOKEN_ALREADY_CLAIMED_SELF = 2003
	TOKEN_THROTTLING = 2004
	TOKEN_UNKNOWN_REDEMPTION_FAILURE = 2005
	TOKEN_PURCHASE_CLAIM_FAILED_AFTER_TOKEN_CLAIMED = 2006
	TOKEN_USER_ALREADY_OWNS_OFFER = 2007
	TOKEN_INVALID_OFFER_KEY = 2008
	TOKEN_EMAIL_NOT_VALIDATED = 2009
	TOKEN_PROVISIONING_BAD_VENDOR_OR_OFFER = 2010
	TOKEN_PURCHASE_HISTORY_UNKNOWN_ERROR = 2011
	TOKEN_THROTTLE_STATE_UNKNOWN_ERROR = 2012
	TOKEN_USER_AGE_NOT_VERIFIED = 2013
	TOKEN_EXCEEDED_OFFER_MAXIMUM = 2014
	TOKEN_NO_AVAILABLE_UNLOCKS = 2015
	TOKEN_MARKETPLACE_INVALID_PLATFORM = 2016
	TOKEN_NO_MARKETPLACE_CODES_FOUND = 2017
	TOKEN_OFFER_NOT_AVAILABLE_FOR_REDEMPTION = 2018
	TOKEN_UNLOCK_PARTIAL_FAILURE = 2019
	TOKEN_MARKETPLACE_INVALID_REGION = 2020
	TOKEN_OFFER_EXPIRED = 2021
	R_A_F_EXCEEDED_MAXIMUM_REFERRALS = 2022
	R_A_F_DUPLICATE_BOND = 2023
	R_A_F_NO_VALID_VETERAN_DESTINY_MEMBERSHIPS_FOUND = 2024
	R_A_F_NOT_A_VALID_VETERAN_USER = 2025
	R_A_F_CODE_ALREADY_CLAIMED_OR_NOT_FOUND = 2026
	R_A_F_MISMATCHED_DESTINY_MEMBERSHIP_TYPE = 2027
	R_A_F_UNABLE_TO_ACCESS_PURCHASE_HISTORY = 2028
	R_A_F_UNABLE_TO_CREATE_BOND = 2029
	R_A_F_UNABLE_TO_FIND_BOND = 2030
	R_A_F_UNABLE_TO_REMOVE_BOND = 2031
	R_A_F_CANNOT_BOND_TO_SELF = 2032
	R_A_F_INVALID_PLATFORM = 2033
	R_A_F_GENERATE_THROTTLED = 2034
	R_A_F_UNABLE_TO_CREATE_BOND_VERSION_MISMATCH = 2035
	R_A_F_UNABLE_TO_REMOVE_BOND_VERSION_MISMATCH = 2036
	R_A_F_REDEEM_THROTTLED = 2037
	NO_AVAILABLE_DISCOUNT_CODE = 2038
	DISCOUNT_ALREADY_CLAIMED = 2039
	DISCOUNT_CLAIM_FAILURE = 2040
	DISCOUNT_CONFIGURATION_FAILURE = 2041
	DISCOUNT_GENERATION_FAILURE = 2042
	DISCOUNT_ALREADY_EXISTS = 2043
	TOKEN_REQUIRES_CREDENTIAL_XUID = 2044
	TOKEN_REQUIRES_CREDENTIAL_PSNID = 2045
	OFFER_REQUIRED = 2046
	UNKNOWN_EVERVERSE_HISTORY_ERROR = 2047
	MISSING_EVERVERSE_HISTORY_ERROR = 2048
	BUNGIE_REWARD_EMAIL_STATE_INVALID = 2049
	BUNGIE_REWARD_NOT_YET_CLAIMABLE = 2050
	MISSING_OFFER_CONFIG = 2051
	R_A_F_QUEST_ENTITLEMENT_REQUIRES_BNET = 2052
	R_A_F_QUEST_ENTITLEMENT_TRANSPORT_FAILURE = 2053
	R_A_F_QUEST_ENTITLEMENT_UNKNOWN_FAILURE = 2054
	R_A_F_VETERAN_REWARD_UNKNOWN_FAILURE = 2055
	R_A_F_TOO_EARLY_TO_CANCEL_BOND = 2056
	LOYALTY_REWARD_ALREADY_REDEEMED = 2057
	UNCLAIMED_LOYALTY_REWARD_ENTRY_NOT_FOUND = 2058
	PARTNER_OFFER_PARTIAL_FAILURE = 2059
	PARTNER_OFFER_ALREADY_CLAIMED = 2060
	PARTNER_OFFER_SKU_NOT_FOUND = 2061
	PARTNER_OFFER_SKU_EXPIRED = 2062
	PARTNER_OFFER_PERMISSION_FAILURE = 2063
	PARTNER_OFFER_NO_DESTINY_ACCOUNT = 2064
	PARTNER_OFFER_APPLY_DATA_NOT_FOUND = 2065
	API_EXCEEDED_MAX_KEYS = 2100
	API_INVALID_OR_EXPIRED_KEY = 2101
	API_KEY_MISSING_FROM_REQUEST = 2102
	APPLICATION_DISABLED = 2103
	APPLICATION_EXCEEDED_MAX = 2104
	APPLICATION_DISALLOWED_BY_SCOPE = 2105
	AUTHORIZATION_CODE_INVALID = 2106
	ORIGIN_HEADER_DOES_NOT_MATCH_KEY = 2107
	ACCESS_NOT_PERMITTED_BY_APPLICATION_SCOPE = 2108
	APPLICATION_NAME_IS_TAKEN = 2109
	REFRESH_TOKEN_NOT_YET_VALID = 2110
	ACCESS_TOKEN_HAS_EXPIRED = 2111
	APPLICATION_TOKEN_FORMAT_NOT_VALID = 2112
	APPLICATION_NOT_CONFIGURED_FOR_BUNGIE_AUTH = 2113
	APPLICATION_NOT_CONFIGURED_FOR_O_AUTH = 2114
	O_AUTH_ACCESS_TOKEN_EXPIRED = 2115
	APPLICATION_TOKEN_KEY_ID_DOES_NOT_EXIST = 2116
	PROVIDED_TOKEN_NOT_VALID_REFRESH_TOKEN = 2117
	REFRESH_TOKEN_EXPIRED = 2118
	AUTHORIZATION_RECORD_INVALID = 2119
	TOKEN_PREVIOUSLY_REVOKED = 2120
	TOKEN_INVALID_MEMBERSHIP = 2121
	AUTHORIZATION_CODE_STALE = 2122
	AUTHORIZATION_RECORD_EXPIRED = 2123
	AUTHORIZATION_RECORD_REVOKED = 2124
	AUTHORIZATION_RECORD_INACTIVE_API_KEY = 2125
	AUTHORIZATION_RECORD_API_KEY_MATCHING = 2126
	PARTNERSHIP_INVALID_TYPE = 2200
	PARTNERSHIP_VALIDATION_ERROR = 2201
	PARTNERSHIP_VALIDATION_TIMEOUT = 2202
	PARTNERSHIP_ACCESS_FAILURE = 2203
	PARTNERSHIP_ACCOUNT_INVALID = 2204
	PARTNERSHIP_GET_ACCOUNT_INFO_FAILURE = 2205
	PARTNERSHIP_DISABLED = 2206
	PARTNERSHIP_ALREADY_EXISTS = 2207
	COMMUNITY_STREAMING_UNAVAILABLE = 2300
	TWITCH_NOT_LINKED = 2500
	TWITCH_ACCOUNT_NOT_FOUND = 2501
	TWITCH_COULD_NOT_LOAD_DESTINY_INFO = 2502
	TWITCH_COULD_NOT_REGISTER_USER = 2503
	TWITCH_COULD_NOT_UNREGISTER_USER = 2504
	TWITCH_REQUIRES_RELINKING = 2505
	TWITCH_NO_PLATFORM_CHOSEN = 2506
	TWITCH_DROP_HISTORY_PERMISSION_FAILURE = 2507
	TWITCH_DROPS_REPAIR_PARTIAL_FAILURE = 2508
	TWITCH_NOT_AUTHORIZED = 2509
	TWITCH_UNKNOWN_AUTHORIZATION_FAILURE = 2510
	TRENDING_CATEGORY_NOT_FOUND = 2600
	TRENDING_ENTRY_TYPE_NOT_SUPPORTED = 2601
	REPORT_OFFENDER_NOT_IN_PGCR = 2700
	REPORT_REQUESTOR_NOT_IN_PGCR = 2701
	REPORT_SUBMISSION_FAILED = 2702
	REPORT_CANNOT_REPORT_SELF = 2703
	AWA_TYPE_DISABLED = 2800
	AWA_TOO_MANY_PENDING_REQUESTS = 2801
	AWA_THE_FEATURE_REQUIRES_A_REGISTERED_DEVICE = 2802
	AWA_REQUEST_WAS_UNANSWERED_FOR_TOO_LONG = 2803
	AWA_WRITE_REQUEST_MISSING_OR_INVALID_TOKEN = 2804
	AWA_WRITE_REQUEST_TOKEN_EXPIRED = 2805
	AWA_WRITE_REQUEST_TOKEN_USAGE_LIMIT_REACHED = 2806
	STEAM_WEB_API_ERROR = 2900
	STEAM_WEB_NULL_RESPONSE_ERROR = 2901
	STEAM_ACCOUNT_REQUIRED = 2902
	STEAM_NOT_AUTHORIZED = 2903
	CLAN_FIRETEAM_NOT_FOUND = 3000
	CLAN_FIRETEAM_ADD_NO_ALTERNATES_FOR_IMMEDIATE = 3001
	CLAN_FIRETEAM_FULL = 3002
	CLAN_FIRETEAM_ALT_FULL = 3003
	CLAN_FIRETEAM_BLOCKED = 3004
	CLAN_FIRETEAM_PLAYER_ENTRY_NOT_FOUND = 3005
	CLAN_FIRETEAM_PERMISSIONS = 3006
	CLAN_FIRETEAM_INVALID_PLATFORM = 3007
	CLAN_FIRETEAM_CANNOT_ADJUST_SLOT_COUNT = 3008
	CLAN_FIRETEAM_INVALID_PLAYER_PLATFORM = 3009
	CLAN_FIRETEAM_NOT_READY_FOR_INVITES_NOT_ENOUGH_PLAYERS = 3010
	CLAN_FIRETEAM_GAME_INVITES_NOT_SUPPORT_FOR_PLATFORM = 3011
	CLAN_FIRETEAM_PLATFORM_INVITE_PREQ_FAILURE = 3012
	CLAN_FIRETEAM_INVALID_AUTH_CONTEXT = 3013
	CLAN_FIRETEAM_INVALID_AUTH_PROVIDER_PSN = 3014
	CLAN_FIRETEAM_PS4_SESSION_FULL = 3015
	CLAN_FIRETEAM_INVALID_AUTH_TOKEN = 3016
	CLAN_FIRETEAM_SCHEDULED_FIRETEAMS_DISABLED = 3017
	CLAN_FIRETEAM_NOT_READY_FOR_INVITES_NOT_SCHEDULED_YET = 3018
	CLAN_FIRETEAM_NOT_READY_FOR_INVITES_CLOSED = 3019
	CLAN_FIRETEAM_SCHEDULED_FIRETEAMS_REQUIRE_ADMIN_PERMISSIONS = 3020
	CLAN_FIRETEAM_NON_PUBLIC_MUST_HAVE_CLAN = 3021
	CLAN_FIRETEAM_PUBLIC_CREATION_RESTRICTION = 3022
	CLAN_FIRETEAM_ALREADY_JOINED = 3023
	CLAN_FIRETEAM_SCHEDULED_FIRETEAMS_RANGE = 3024
	CLAN_FIRETEAM_PUBLIC_CREATION_RESTRICTION_EXTENDED = 3025
	CLAN_FIRETEAM_EXPIRED = 3026
	CLAN_FIRETEAM_INVALID_AUTH_PROVIDER = 3027
	CLAN_FIRETEAM_INVALID_AUTH_PROVIDER_XUID = 3028
	CLAN_FIRETEAM_THROTTLE = 3029
	CLAN_FIRETEAM_TOO_MANY_OPEN_SCHEDULED_FIRETEAMS = 3030
	CLAN_FIRETEAM_CANNOT_REOPEN_SCHEDULED_FIRETEAMS = 3031
	CLAN_FIRETEAM_JOIN_NO_ACCOUNT_SPECIFIED = 3032
	CLAN_FIRETEAM_MIN_DESTINY2_PROGRESS_FOR_CREATION = 3033
	CLAN_FIRETEAM_MIN_DESTINY2_PROGRESS_FOR_JOIN = 3034
	CLAN_FIRETEAM_S_M_S_OR_PURCHASE_REQUIRED_CREATE = 3035
	CLAN_FIRETEAM_PURCHASE_REQUIRED_CREATE = 3036
	CLAN_FIRETEAM_S_M_S_OR_PURCHASE_REQUIRED_JOIN = 3037
	CLAN_FIRETEAM_PURCHASE_REQUIRED_JOIN = 3038
	CROSS_SAVE_OVERRIDDEN_ACCOUNT_NOT_FOUND = 3200
	CROSS_SAVE_TOO_MANY_OVERRIDDEN_PLATFORMS = 3201
	CROSS_SAVE_NO_OVERRIDDEN_PLATFORMS = 3202
	CROSS_SAVE_PRIMARY_ACCOUNT_NOT_FOUND = 3203
	CROSS_SAVE_REQUEST_INVALID = 3204
	CROSS_SAVE_BUNGIE_ACCOUNT_VALIDATION_FAILURE = 3206
	CROSS_SAVE_OVERRIDDEN_PLATFORM_NOT_ALLOWED = 3207
	CROSS_SAVE_THRESHOLD_EXCEEDED = 3208
	CROSS_SAVE_INCOMPATIBLE_MEMBERSHIP_TYPE = 3209
	CROSS_SAVE_COULD_NOT_FIND_LINKED_ACCOUNT_FOR_MEMBERSHIP_TYPE = 3210
	CROSS_SAVE_COULD_NOT_CREATE_DESTINY_PROFILE_FOR_MEMBERSHIP_TYPE = 3211
	CROSS_SAVE_ERROR_CREATING_DESTINY_PROFILE_FOR_MEMBERSHIP_TYPE = 3212
	CROSS_SAVE_CANNOT_OVERRIDE_SELF = 3213
	CROSS_SAVE_RECENT_SILVER_PURCHASE = 3214
	CROSS_SAVE_SILVER_BALANCE_NEGATIVE = 3215
	CROSS_SAVE_ACCOUNT_NOT_AUTHENTICATED = 3216
	ERROR_ONE_ACCOUNT_ALREADY_ACTIVE = 3217
	ERROR_ONE_ACCOUNT_DESTINY_RESTRICTION = 3218
	CROSS_SAVE_MUST_MIGRATE_TO_STEAM = 3219
	CROSS_SAVE_STEAM_ALREADY_PAIRED = 3220
	CROSS_SAVE_CANNOT_PAIR_JUST_STEAM_AND_BLIZZARD = 3221
	CROSS_SAVE_CANNOT_PAIR_STEAM_ALONE_BEFORE_SHADOWKEEP = 3222
	AUTH_VERIFICATION_NOT_LINKED_TO_ACCOUNT = 3300
	P_C_MIGRATION_MISSING_BLIZZARD = 3400
	P_C_MIGRATION_MISSING_STEAM = 3401
	P_C_MIGRATION_INVALID_BLIZZARD = 3402
	P_C_MIGRATION_INVALID_STEAM = 3403
	P_C_MIGRATION_UNKNOWN_FAILURE = 3404
	P_C_MIGRATION_UNKNOWN_EXCEPTION = 3405
	P_C_MIGRATION_NOT_LINKED = 3406
	P_C_MIGRATION_ACCOUNTS_ALREADY_USED = 3407
	P_C_MIGRATION_STEP_FAILED = 3408
	P_C_MIGRATION_INVALID_BLIZZARD_CROSS_SAVE_STATE = 3409
	P_C_MIGRATION_DESTINATION_BANNED = 3410
	P_C_MIGRATION_DESTINY_FAILURE = 3411
	P_C_MIGRATION_SILVER_TRANSFER_FAILED = 3412
	P_C_MIGRATION_ENTITLEMENT_TRANSFER_FAILED = 3413
	P_C_MIGRATION_CANNOT_STOMP_CLAN_FOUNDER = 3414
	UNSUPPORTED_BROWSER = 3500
	STADIA_ACCOUNT_REQUIRED = 3600
	ERROR_PHONE_VALIDATION_TOO_MANY_USES = 3702
	ERROR_PHONE_VALIDATION_NO_ASSOCIATED_PHONE = 3703
	ERROR_PHONE_VALIDATION_CODE_INVALID = 3705
	ERROR_PHONE_VALIDATION_BANNED = 3706
	ERROR_PHONE_VALIDATION_CODE_TOO_RECENTLY_SENT = 3707
	ERROR_PHONE_VALIDATION_CODE_EXPIRED = 3708
	ERROR_PHONE_VALIDATION_INVALID_NUMBER_TYPE = 3709
	ERROR_PHONE_VALIDATION_CODE_TOO_RECENTLY_CHECKED = 3710
	APPLE_PUSH_ERROR_UNKNOWN = 3800
	APPLE_PUSH_ERROR_NULL = 3801
	APPLE_PUSH_ERROR_TIMEOUT = 3802
	APPLE_PUSH_BAD_REQUEST = 3803
	APPLE_PUSH_FAILED_AUTH = 3804
	APPLE_PUSH_THROTTLED = 3805
	APPLE_PUSH_SERVICE_UNAVAILABLE = 3806
	NOT_AN_IMAGE_OR_VIDEO = 3807
	ERROR_BUNGIE_FRIENDS_BLOCK_FAILED = 3900
	ERROR_BUNGIE_FRIENDS_AUTO_REJECT = 3901
	ERROR_BUNGIE_FRIENDS_NO_REQUEST_FOUND = 3902
	ERROR_BUNGIE_FRIENDS_ALREADY_FRIENDS = 3903
	ERROR_BUNGIE_FRIENDS_UNABLE_TO_REMOVE_REQUEST = 3904
	ERROR_BUNGIE_FRIENDS_UNABLE_TO_REMOVE = 3905
	ERROR_BUNGIE_FRIENDS_IDENTICAL_SOURCE_TARGET = 3906
	ERROR_BUNGIE_FRIENDS_SELF = 3907
	ERROR_BUNGIE_BLOCK_SELF = 3908
	ERROR_BUNGIE_FRIENDS_LIST_FULL = 3910
	ERROR_BUNGIE_BLOCK_LIST_FULL = 3911
	ERROR_EGS_UNKNOWN = 4000
	ERROR_EGS_BAD_REQUEST = 4001
	ERROR_EGS_NOT_AUTHORIZED = 4002
	ERROR_EGS_FORBIDDEN = 4003
	ERROR_EGS_ACCOUNT_NOT_FOUND = 4004
	ERROR_EGS_WEB_EXCEPTION = 4005
	ERROR_EGS_UNAVAILABLE = 4006
	ERROR_EGS_JWKS_MISSING = 4007
	ERROR_EGS_JWT_MALFORMED_HEADER = 4008
	ERROR_EGS_JWT_MALFORMED_PAYLOAD = 4009


class GroupsForMemberFilter(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GroupsV2-GroupsForMemberFilter.html#schema_GroupsV2-GroupsForMemberFilter
	"""
	ALL = 0
	FOUNDED = 1
	NON_FOUNDED = 2


class DropStateEnum(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Streaming-DropStateEnum.html#schema_Streaming-DropStateEnum
	"""
	CLAIMED = 0
	APPLIED = 1
	FULFILLED = 2


class ItemBindStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-ItemBindStatus.html#schema_Destiny-ItemBindStatus
	"""
	NOT_BOUND = 0
	BOUND_TO_CHARACTER = 1
	BOUND_TO_ACCOUNT = 2
	BOUND_TO_GUILD = 3


class TransferStatuses(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-TransferStatuses.html#schema_Destiny-TransferStatuses
	"""
	CAN_TRANSFER = 0
	ITEM_IS_EQUIPPED = 1
	NOT_TRANSFERRABLE = 2
	NO_ROOM_IN_DESTINATION = 4


class ItemState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-ItemState.html#schema_Destiny-ItemState
	"""
	NONE = 0
	LOCKED = 1
	TRACKED = 2
	MASTERWORK = 4
	CRAFTED = 8
	HIGHLIGHTED_OBJECTIVE = 16


class DestinyGameVersions(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyGameVersions.html#schema_Destiny-DestinyGameVersions
	"""
	NONE = 0
	DESTINY2 = 1
	DLC1 = 2
	DLC2 = 4
	FORSAKEN = 8
	YEAR_TWO_ANNUAL_PASS = 16
	SHADOWKEEP = 32
	BEYOND_LIGHT = 64
	ANNIVERSARY30TH = 128
	THE_WITCH_QUEEN = 256
	LIGHTFALL = 512


class DestinyComponentType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html#schema_Destiny-DestinyComponentType
	"""
	NONE = 0
	PROFILES = 100
	VENDOR_RECEIPTS = 101
	PROFILE_INVENTORIES = 102
	PROFILE_CURRENCIES = 103
	PROFILE_PROGRESSION = 104
	PLATFORM_SILVER = 105
	CHARACTERS = 200
	CHARACTER_INVENTORIES = 201
	CHARACTER_PROGRESSIONS = 202
	CHARACTER_RENDER_DATA = 203
	CHARACTER_ACTIVITIES = 204
	CHARACTER_EQUIPMENT = 205
	CHARACTER_LOADOUTS = 206
	ITEM_INSTANCES = 300
	ITEM_OBJECTIVES = 301
	ITEM_PERKS = 302
	ITEM_RENDER_DATA = 303
	ITEM_STATS = 304
	ITEM_SOCKETS = 305
	ITEM_TALENT_GRIDS = 306
	ITEM_COMMON_DATA = 307
	ITEM_PLUG_STATES = 308
	ITEM_PLUG_OBJECTIVES = 309
	ITEM_REUSABLE_PLUGS = 310
	VENDORS = 400
	VENDOR_CATEGORIES = 401
	VENDOR_SALES = 402
	KIOSKS = 500
	CURRENCY_LOOKUPS = 600
	PRESENTATION_NODES = 700
	COLLECTIBLES = 800
	RECORDS = 900
	TRANSITORY = 1000
	METRICS = 1100
	STRING_VARIABLES = 1200
	CRAFTABLES = 1300
	SOCIAL_COMMENDATIONS = 1400


class ComponentPrivacySetting(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Components-ComponentPrivacySetting.html#schema_Components-ComponentPrivacySetting
	"""
	NONE = 0
	PUBLIC = 1
	PRIVATE = 2


class DestinyPresentationNodeState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyPresentationNodeState.html#schema_Destiny-DestinyPresentationNodeState
	"""
	NONE = 0
	INVISIBLE = 1
	OBSCURED = 2


class DestinyRecordState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyRecordState.html#schema_Destiny-DestinyRecordState
	"""
	NONE = 0
	RECORD_REDEEMED = 1
	REWARD_UNAVAILABLE = 2
	OBJECTIVE_NOT_COMPLETED = 4
	OBSCURED = 8
	INVISIBLE = 16
	ENTITLEMENT_UNOWNED = 32
	CAN_EQUIP_TITLE = 64


class DestinyCollectibleState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyCollectibleState.html#schema_Destiny-DestinyCollectibleState
	"""
	NONE = 0
	NOT_ACQUIRED = 1
	OBSCURED = 2
	INVISIBLE = 4
	CANNOT_AFFORD_MATERIAL_REQUIREMENTS = 8
	INVENTORY_SPACE_UNAVAILABLE = 16
	UNIQUENESS_VIOLATION = 32
	PURCHASE_DISABLED = 64


class DestinyPartyMemberStates(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyPartyMemberStates.html#schema_Destiny-DestinyPartyMemberStates
	"""
	NONE = 0
	FIRETEAM_MEMBER = 1
	POSSE_MEMBER = 2
	GROUP_MEMBER = 4
	PARTY_LEADER = 8


class DestinyGamePrivacySetting(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyGamePrivacySetting.html#schema_Destiny-DestinyGamePrivacySetting
	"""
	OPEN = 0
	CLAN_AND_FRIENDS_ONLY = 1
	FRIENDS_ONLY = 2
	INVITATION_ONLY = 3
	CLOSED = 4


class DestinyJoinClosedReasons(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyJoinClosedReasons.html#schema_Destiny-DestinyJoinClosedReasons
	"""
	NONE = 0
	IN_MATCHMAKING = 1
	LOADING = 2
	SOLO_MODE = 4
	INTERNAL_REASONS = 8
	DISALLOWED_BY_GAME_STATE = 16
	OFFLINE = 32768


class DestinyRace(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyRace.html#schema_Destiny-DestinyRace
	"""
	HUMAN = 0
	AWOKEN = 1
	EXO = 2
	UNKNOWN = 3


class DestinyMilestoneDisplayPreference(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-Milestones-DestinyMilestoneDisplayPreference.html#schema_Destiny-Definitions-Milestones-DestinyMilestoneDisplayPreference
	"""
	MILESTONE_DEFINITION = 0
	CURRENT_QUEST_STEPS = 1
	CURRENT_ACTIVITY_CHALLENGES = 2


class DestinyMilestoneType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Definitions-Milestones-DestinyMilestoneType.html#schema_Destiny-Definitions-Milestones-DestinyMilestoneType
	"""
	UNKNOWN = 0
	TUTORIAL = 1
	ONE_TIME = 2
	WEEKLY = 3
	DAILY = 4
	SPECIAL = 5


class DestinyActivityDifficultyTier(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyActivityDifficultyTier.html#schema_Destiny-DestinyActivityDifficultyTier
	"""
	TRIVIAL = 0
	EASY = 1
	NORMAL = 2
	CHALLENGING = 3
	HARD = 4
	BRAVE = 5
	ALMOST_IMPOSSIBLE = 6
	IMPOSSIBLE = 7


class EquipFailureReason(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-EquipFailureReason.html#schema_Destiny-EquipFailureReason
	"""
	NONE = 0
	ITEM_UNEQUIPPABLE = 1
	ITEM_UNIQUE_EQUIP_RESTRICTED = 2
	ITEM_FAILED_UNLOCK_CHECK = 4
	ITEM_FAILED_LEVEL_CHECK = 8
	ITEM_WRAPPED = 16
	ITEM_NOT_LOADED = 32
	ITEM_EQUIP_BLOCKLISTED = 64
	ITEM_LOADOUT_REQUIREMENT_NOT_MET = 128


class DestinyTalentNodeState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyTalentNodeState.html#schema_Destiny-DestinyTalentNodeState
	"""
	INVALID = 0
	CAN_UPGRADE = 1
	NO_POINTS = 2
	NO_PREREQUISITES = 3
	NO_STEPS = 4
	NO_UNLOCK = 5
	NO_MATERIAL = 6
	NO_GRID_LEVEL = 7
	SWAPPING_LOCKED = 8
	MUST_SWAP = 9
	COMPLETE = 10
	UNKNOWN = 11
	CREATION_ONLY = 12
	HIDDEN = 13


class DestinyVendorFilter(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorFilter.html#schema_Destiny-DestinyVendorFilter
	"""
	NONE = 0
	API_PURCHASABLE = 1


class VendorItemStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-VendorItemStatus.html#schema_Destiny-VendorItemStatus
	"""
	SUCCESS = 0
	NO_INVENTORY_SPACE = 1
	NO_FUNDS = 2
	NO_PROGRESSION = 4
	NO_UNLOCK = 8
	NO_QUANTITY = 16
	OUTSIDE_PURCHASE_WINDOW = 32
	NOT_AVAILABLE = 64
	UNIQUENESS_VIOLATION = 128
	UNKNOWN_ERROR = 256
	ALREADY_SELLING = 512
	UNSELLABLE = 1024
	SELLING_INHIBITED = 2048
	ALREADY_OWNED = 4096
	DISPLAY_ONLY = 8192


class DestinyVendorItemState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-DestinyVendorItemState.html#schema_Destiny-DestinyVendorItemState
	"""
	NONE = 0
	INCOMPLETE = 1
	REWARD_AVAILABLE = 2
	COMPLETE = 4
	NEW = 8
	FEATURED = 16
	ENDING = 32
	ON_SALE = 64
	OWNED = 128
	WIDE_VIEW = 256
	NEXUS_ATTENTION = 512
	SET_DISCOUNT = 1024
	PRICE_DROP = 2048
	DAILY_OFFER = 4096
	CHARITY = 8192
	SEASONAL_REWARD_EXPIRATION = 16384
	BEST_DEAL = 32768
	POPULAR = 65536
	FREE = 131072
	LOCKED = 262144
	PARACAUSAL = 524288
	CRYPTARCH = 1048576


class DestinySocketArrayType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Requests-Actions-DestinySocketArrayType.html#schema_Destiny-Requests-Actions-DestinySocketArrayType
	"""
	DEFAULT = 0
	INTRINSIC = 1


class DestinyStatsGroupType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-DestinyStatsGroupType.html#schema_Destiny-HistoricalStats-Definitions-DestinyStatsGroupType
	"""
	NONE = 0
	GENERAL = 1
	WEAPONS = 2
	MEDALS = 3
	RESERVED_GROUPS = 100
	LEADERBOARD = 101
	ACTIVITY = 102
	UNIQUE_WEAPON = 103
	INTERNAL = 104


class DestinyStatsCategoryType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-DestinyStatsCategoryType.html#schema_Destiny-HistoricalStats-Definitions-DestinyStatsCategoryType
	"""
	NONE = 0
	KILLS = 1
	ASSISTS = 2
	DEATHS = 3
	CRITICALS = 4
	K_DA = 5
	KD = 6
	SCORE = 7
	ENTERED = 8
	TIME_PLAYED = 9
	MEDAL_WINS = 10
	MEDAL_GAME = 11
	MEDAL_SPECIAL_KILLS = 12
	MEDAL_SPREES = 13
	MEDAL_MULTI_KILLS = 14
	MEDAL_ABILITIES = 15


class UnitType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-UnitType.html#schema_Destiny-HistoricalStats-Definitions-UnitType
	"""
	NONE = 0
	COUNT = 1
	PER_GAME = 2
	SECONDS = 3
	POINTS = 4
	TEAM = 5
	DISTANCE = 6
	PERCENT = 7
	RATIO = 8
	BOOLEAN = 9
	WEAPON_TYPE = 10
	STANDING = 11
	MILLISECONDS = 12
	COMPLETION_REASON = 13


class DestinyStatsMergeMethod(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-DestinyStatsMergeMethod.html#schema_Destiny-HistoricalStats-Definitions-DestinyStatsMergeMethod
	"""
	ADD = 0
	MIN = 1
	MAX = 2


class PeriodType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-HistoricalStats-Definitions-PeriodType.html#schema_Destiny-HistoricalStats-Definitions-PeriodType
	"""
	NONE = 0
	DAILY = 1
	ALL_TIME = 2
	ACTIVITY = 3


class AwaType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Advanced-AwaType.html#schema_Destiny-Advanced-AwaType
	"""
	NONE = 0
	INSERT_PLUGS = 1


class AwaUserSelection(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Advanced-AwaUserSelection.html#schema_Destiny-Advanced-AwaUserSelection
	"""
	NONE = 0
	REJECTED = 1
	APPROVED = 2


class AwaResponseReason(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Destiny-Advanced-AwaResponseReason.html#schema_Destiny-Advanced-AwaResponseReason
	"""
	NONE = 0
	ANSWERED = 1
	TIMED_OUT = 2
	REPLACED = 3


class CommunityContentSortMode(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Forum-CommunityContentSortMode.html#schema_Forum-CommunityContentSortMode
	"""
	TRENDING = 0
	LATEST = 1
	HIGHEST_RATED = 2


class TrendingEntryType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Trending-TrendingEntryType.html#schema_Trending-TrendingEntryType
	"""
	NEWS = 0
	DESTINY_ITEM = 1
	DESTINY_ACTIVITY = 2
	DESTINY_RITUAL = 3
	SUPPORT_ARTICLE = 4
	CREATION = 5
	STREAM = 6
	UPDATE = 7
	LINK = 8
	FORUM_TAG = 9
	CONTAINER = 10
	RELEASE = 11


class FireteamDateRange(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Fireteam-FireteamDateRange.html#schema_Fireteam-FireteamDateRange
	"""
	ALL = 0
	NOW = 1
	TWENTY_FOUR_HOURS = 2
	FORTY_EIGHT_HOURS = 3
	THIS_WEEK = 4


class FireteamPlatform(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Fireteam-FireteamPlatform.html#schema_Fireteam-FireteamPlatform
	"""
	ANY = 0
	PLAYSTATION4 = 1
	XBOX_ONE = 2
	BLIZZARD = 3
	STEAM = 4
	STADIA = 5
	EGS = 6


class FireteamPublicSearchOption(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Fireteam-FireteamPublicSearchOption.html#schema_Fireteam-FireteamPublicSearchOption
	"""
	PUBLIC_AND_PRIVATE = 0
	PUBLIC_ONLY = 1
	PRIVATE_ONLY = 2


class FireteamSlotSearch(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Fireteam-FireteamSlotSearch.html#schema_Fireteam-FireteamSlotSearch
	"""
	NO_SLOT_RESTRICTION = 0
	HAS_OPEN_PLAYER_SLOTS = 1
	HAS_OPEN_PLAYER_OR_ALT_SLOTS = 2


class FireteamPlatformInviteResult(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Fireteam-FireteamPlatformInviteResult.html#schema_Fireteam-FireteamPlatformInviteResult
	"""
	NONE = 0
	SUCCESS = 1
	ALREADY_IN_FIRETEAM = 2
	THROTTLED = 3
	SERVICE_ERROR = 4


class PresenceStatus(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Social-Friends-PresenceStatus.html#schema_Social-Friends-PresenceStatus
	"""
	OFFLINE_OR_UNKNOWN = 0
	ONLINE = 1


class PresenceOnlineStateFlags(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Social-Friends-PresenceOnlineStateFlags.html#schema_Social-Friends-PresenceOnlineStateFlags
	"""
	NONE = 0
	DESTINY1 = 1
	DESTINY2 = 2


class FriendRelationshipState(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Social-Friends-FriendRelationshipState.html#schema_Social-Friends-FriendRelationshipState
	"""
	UNKNOWN = 0
	FRIEND = 1
	INCOMING_REQUEST = 2
	OUTGOING_REQUEST = 3


class PlatformFriendType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_Social-Friends-PlatformFriendType.html#schema_Social-Friends-PlatformFriendType
	"""
	UNKNOWN = 0
	XBOX = 1
	PSN = 2
	STEAM = 3
	EGS = 4


class OptInFlags(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_User-OptInFlags.html#schema_User-OptInFlags
	"""
	NONE = 0
	NEWSLETTER = 1
	SYSTEM = 2
	MARKETING = 4
	USER_RESEARCH = 8
	CUSTOMER_SERVICE = 16
	SOCIAL = 32
	PLAY_TESTS = 64
	PLAY_TESTS_LOCAL = 128
	CAREERS = 256


class GlobalAlertLevel(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GlobalAlertLevel.html#schema_GlobalAlertLevel
	"""
	UNKNOWN = 0
	BLUE = 1
	YELLOW = 2
	RED = 3


class GlobalAlertType(IntEnum):
	"""
	Reference: https://bungie-net.github.io/multi/schema_GlobalAlertType.html#schema_GlobalAlertType
	"""
	GLOBAL_ALERT = 0
	STREAMING_ALERT = 1
