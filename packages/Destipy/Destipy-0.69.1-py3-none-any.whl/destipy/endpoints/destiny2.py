from datetime import datetime
from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Destiny2:
    """Destiny2 endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetDestinyManifest(
        self,
    ) -> dict:
        """Returns the current version of the manifest as a json object.

            Args:


            Returns:
        {
            "version": {
                "Name": "version",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "mobileAssetContentPath": {
                "Name": "mobileAssetContentPath",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "mobileGearAssetDataBases": {
                "Name": "mobileGearAssetDataBases",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "version": {
                            "Name": "version",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "path": {
                            "Name": "path",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "mobileWorldContentPaths": {
                "Name": "mobileWorldContentPaths",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "jsonWorldContentPaths": {
                "Name": "jsonWorldContentPaths",
                "Type": "object",
                "Description": "This points to the generated JSON that contains all the Definitions. Each key is a locale. The value is a path to the aggregated world definitions (warning: large file!)",
                "Attributes": []
            },
            "jsonWorldComponentContentPaths": {
                "Name": "jsonWorldComponentContentPaths",
                "Type": "object",
                "Description": "This points to the generated JSON that contains all the Definitions. Each key is a locale. The value is a dictionary, where the key is a definition type by name, and the value is the path to the file for that definition. WARNING: This is unsafe and subject to change - do not depend on data in these files staying around long-term.",
                "Attributes": []
            },
            "mobileClanBannerDatabasePath": {
                "Name": "mobileClanBannerDatabasePath",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "mobileGearCDN": {
                "Name": "mobileGearCDN",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "iconImagePyramidInfo": {
                "Name": "iconImagePyramidInfo",
                "Type": "array",
                "Description": "Information about the \"Image Pyramid\" for Destiny icons. Where possible, we create smaller versions of Destiny icons. These are found as subfolders under the location of the \"original/full size\" Destiny images, with the same file name and extension as the original image itself. (this lets us avoid sending largely redundant path info with every entity, at the expense of the smaller versions of the image being less discoverable)",
                "Attributes": [],
                "Array Contents": [
                    {
                        "name": {
                            "Name": "name",
                            "Type": "string",
                            "Description": "The name of the subfolder where these images are located.",
                            "Attributes": []
                        }
                    },
                    {
                        "factor": {
                            "Name": "factor",
                            "Type": "float",
                            "Description": "The factor by which the original image size has been reduced.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetDestinyManifest.html#operation_get_Destiny2-GetDestinyManifest"""

        try:
            self.logger.info("Executing GetDestinyManifest...")
            url = self.base_url + "/Destiny2/Manifest/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetDestinyEntityDefinition(
        self,
        entityType: str,
        hashIdentifier: int,
    ) -> dict:
        """Returns the static definition of an entity of the given Type and hash identifier. Examine the API Documentation for the Type Names of entities that have their own definitions. Note that the return type will always *inherit from* DestinyDefinition, but the specific type returned will be the requested entity type if it can be found. Please don't use this as a chatty alternative to the Manifest database if you require large sets of data, but for simple and one-off accesses this should be handy.

            Args:
                entityType (str): The type of entity for whom you would like results. These correspond to the entity's definition contract name. For instance, if you are looking for items, this property should be 'DestinyInventoryItemDefinition'. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is tentatively in final form, but there may be bugs that prevent desirable operation.
                hashIdentifier (int): The hash identifier for the specific Entity you want returned.

            Returns:
        {
            "hash": {
                "Name": "hash",
                "Type": "uint32",
                "Description": "The unique identifier for this entity. Guaranteed to be unique for the type of entity, but not globally.When entities refer to each other in Destiny content, it is this hash that they are referring to.",
                "Attributes": []
            },
            "index": {
                "Name": "index",
                "Type": "int32",
                "Description": "The index of the entity as it was found in the investment tables.",
                "Attributes": []
            },
            "redacted": {
                "Name": "redacted",
                "Type": "boolean",
                "Description": "If this is true, then there is an entity with this identifier/type combination, but BNet is not yet allowed to show it. Sorry!",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetDestinyEntityDefinition.html#operation_get_Destiny2-GetDestinyEntityDefinition"""

        try:
            self.logger.info("Executing GetDestinyEntityDefinition...")
            url = (
                self.base_url
                + f"/Destiny2/Manifest/{entityType}/{hashIdentifier}/".format(
                    entityType=entityType, hashIdentifier=hashIdentifier
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchDestinyPlayerByBungieName(
        self, membershipType: int, displayName: str, displayNameCode: int
    ) -> dict:
        """Returns a list of Destiny memberships given a global Bungie Display Name. This method will hide overridden memberships due to cross save.

            Args:
                membershipType (int): A valid non-BungieNet membership type, or All. Indicates which memberships to return. You probably want this set to All.

            Returns:
        {
            "supplementalDisplayName": {
                "Name": "supplementalDisplayName",
                "Type": "string",
                "Description": "A platform specific additional display name - ex: psn Real Name, bnet Unique Name, etc.",
                "Attributes": []
            },
            "iconPath": {
                "Name": "iconPath",
                "Type": "string",
                "Description": "URL the Icon if available.",
                "Attributes": []
            },
            "crossSaveOverride": {
                "Name": "crossSaveOverride",
                "Type": "int32",
                "Description": "If there is a cross save override in effect, this value will tell you the type that is overridding this one.",
                "Attributes": []
            },
            "applicableMembershipTypes": {
                "Name": "applicableMembershipTypes",
                "Type": "array",
                "Description": "The list of Membership Types indicating the platforms on which this Membership can be used. Not in Cross Save = its original membership type. Cross Save Primary = Any membership types it is overridding, and its original membership type Cross Save Overridden = Empty list",
                "Attributes": [],
                "Array Contents": "int32"
            },
            "isPublic": {
                "Name": "isPublic",
                "Type": "boolean",
                "Description": "If True, this is a public user membership.",
                "Attributes": []
            },
            "membershipType": {
                "Name": "membershipType",
                "Type": "int32",
                "Description": "Type of the membership. Not necessarily the native type.",
                "Attributes": []
            },
            "membershipId": {
                "Name": "membershipId",
                "Type": "int64",
                "Description": "Membership ID as they user is known in the Accounts service",
                "Attributes": []
            },
            "displayName": {
                "Name": "displayName",
                "Type": "string",
                "Description": "Display Name the player has chosen for themselves. The display name is optional when the data type is used as input to a platform API.",
                "Attributes": []
            },
            "bungieGlobalDisplayName": {
                "Name": "bungieGlobalDisplayName",
                "Type": "string",
                "Description": "The bungie global display name, if set.",
                "Attributes": []
            },
            "bungieGlobalDisplayNameCode": {
                "Name": "bungieGlobalDisplayNameCode",
                "Type": "int16",
                "Description": "The bungie global display name code, if set.",
                "Attributes": [
                    "Nullable"
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-SearchDestinyPlayerByBungieName.html#operation_post_Destiny2-SearchDestinyPlayerByBungieName"""

        request_body = {"displayName": displayName, "displayNameCode": displayNameCode}

        try:
            self.logger.info("Executing SearchDestinyPlayerByBungieName...")
            url = (
                self.base_url
                + f"/Destiny2/SearchDestinyPlayerByBungieName/{membershipType}/".format(
                    membershipType=membershipType
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLinkedProfiles(
        self,
        membershipId: int,
        membershipType: int,
        getAllMemberships: bool,
    ) -> dict:
        """Returns a summary information about all profiles linked to the requesting membership type/membership ID that have valid Destiny information. The passed-in Membership Type/Membership ID may be a Bungie.Net membership or a Destiny membership. It only returns the minimal amount of data to begin making more substantive requests, but will hopefully serve as a useful alternative to UserServices for people who just care about Destiny data. Note that it will only return linked accounts whose linkages you are allowed to view.

            Args:
                membershipId (int): The ID of the membership whose linked Destiny accounts you want returned. Make sure your membership ID matches its Membership Type: don't pass us a PSN membership ID and the XBox membership type, it's not going to work!
                membershipType (int): The type for the membership whose linked Destiny accounts you want returned.
                getAllMemberships (bool): (optional) if set to 'true', all memberships regardless of whether they're obscured by overrides will be returned. Normal privacy restrictions on account linking will still apply no matter what.

            Returns:
        {
            "profiles": {
                "Name": "profiles",
                "Type": "array",
                "Description": "Any Destiny account for whom we could successfully pull characters will be returned here, as the Platform-level summary of user data. (no character data, no Destiny account data other than the Membership ID and Type so you can make further queries)",
                "Attributes": [],
                "Array Contents": [
                    {
                        "dateLastPlayed": {
                            "Name": "dateLastPlayed",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isOverridden": {
                            "Name": "isOverridden",
                            "Type": "boolean",
                            "Description": "If this profile is being overridden/obscured by Cross Save, this will be set to true. We will still return the profile for display purposes where users need to know the info: it is up to any given area of the app/site to determine if this profile should still be shown.",
                            "Attributes": []
                        }
                    },
                    {
                        "isCrossSavePrimary": {
                            "Name": "isCrossSavePrimary",
                            "Type": "boolean",
                            "Description": "If true, this account is hooked up as the \"Primary\" cross save account for one or more platforms.",
                            "Attributes": []
                        }
                    },
                    {
                        "platformSilver": {
                            "Name": "platformSilver",
                            "Type": "object",
                            "Description": "This is the silver available on this Profile across any platforms on which they have purchased silver. This is only available if you are requesting yourself.",
                            "Attributes": []
                        }
                    },
                    {
                        "unpairedGameVersions": {
                            "Name": "unpairedGameVersions",
                            "Type": "int32",
                            "Description": "If this profile is not in a cross save pairing, this will return the game versions that we believe this profile has access to. For the time being, we will not return this information for any membership that is in a cross save pairing. The gist is that, once the pairing occurs, we do not currently have a consistent way to get that information for the profile's original Platform, and thus gameVersions would be too inconsistent (based on the last platform they happened to play on) for the info to be useful. If we ever can get this data, this field will be deprecated and replaced with data on the DestinyLinkedProfileResponse itself, with game versions per linked Platform. But since we can't get that, we have this as a stop-gap measure for getting the data in the only situation that we currently need it.",
                            "Attributes": [
                                "Nullable",
                                "Enumeration"
                            ]
                        }
                    },
                    {
                        "supplementalDisplayName": {
                            "Name": "supplementalDisplayName",
                            "Type": "string",
                            "Description": "A platform specific additional display name - ex: psn Real Name, bnet Unique Name, etc.",
                            "Attributes": []
                        }
                    },
                    {
                        "iconPath": {
                            "Name": "iconPath",
                            "Type": "string",
                            "Description": "URL the Icon if available.",
                            "Attributes": []
                        }
                    },
                    {
                        "crossSaveOverride": {
                            "Name": "crossSaveOverride",
                            "Type": "int32",
                            "Description": "If there is a cross save override in effect, this value will tell you the type that is overridding this one.",
                            "Attributes": []
                        }
                    },
                    {
                        "applicableMembershipTypes": {
                            "Name": "applicableMembershipTypes",
                            "Type": "array",
                            "Description": "The list of Membership Types indicating the platforms on which this Membership can be used. Not in Cross Save = its original membership type. Cross Save Primary = Any membership types it is overridding, and its original membership type Cross Save Overridden = Empty list",
                            "Attributes": []
                        }
                    },
                    {
                        "isPublic": {
                            "Name": "isPublic",
                            "Type": "boolean",
                            "Description": "If True, this is a public user membership.",
                            "Attributes": []
                        }
                    },
                    {
                        "membershipType": {
                            "Name": "membershipType",
                            "Type": "int32",
                            "Description": "Type of the membership. Not necessarily the native type.",
                            "Attributes": []
                        }
                    },
                    {
                        "membershipId": {
                            "Name": "membershipId",
                            "Type": "int64",
                            "Description": "Membership ID as they user is known in the Accounts service",
                            "Attributes": []
                        }
                    },
                    {
                        "displayName": {
                            "Name": "displayName",
                            "Type": "string",
                            "Description": "Display Name the player has chosen for themselves. The display name is optional when the data type is used as input to a platform API.",
                            "Attributes": []
                        }
                    },
                    {
                        "bungieGlobalDisplayName": {
                            "Name": "bungieGlobalDisplayName",
                            "Type": "string",
                            "Description": "The bungie global display name, if set.",
                            "Attributes": []
                        }
                    },
                    {
                        "bungieGlobalDisplayNameCode": {
                            "Name": "bungieGlobalDisplayNameCode",
                            "Type": "int16",
                            "Description": "The bungie global display name code, if set.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    }
                ]
            },
            "bnetMembership": {
                "Name": "bnetMembership",
                "Type": "object",
                "Description": "If the requested membership had a linked Bungie.Net membership ID, this is the basic information about that BNet account.I know, Tetron; I know this is mixing UserServices concerns with DestinyServices concerns. But it's so damn convenient! https://www.youtube.com/watch?v=X5R-bB-gKVI",
                "Attributes": []
            },
            "profilesWithErrors": {
                "Name": "profilesWithErrors",
                "Type": "array",
                "Description": "This is brief summary info for profiles that we believe have valid Destiny info, but who failed to return data for some other reason and thus we know that subsequent calls for their info will also fail.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "errorCode": {
                            "Name": "errorCode",
                            "Type": "int32",
                            "Description": "The error that we encountered. You should be able to look up localized text to show to the user for these failures.",
                            "Attributes": []
                        }
                    },
                    {
                        "infoCard": {
                            "Name": "infoCard",
                            "Type": "object",
                            "Description": "Basic info about the account that failed. Don't expect anything other than membership ID, Membership Type, and displayName to be populated.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetLinkedProfiles.html#operation_get_Destiny2-GetLinkedProfiles"""

        try:
            self.logger.info("Executing GetLinkedProfiles...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{membershipId}/LinkedProfiles/".format(
                    membershipId=membershipId,
                    membershipType=membershipType,
                    getAllMemberships=getAllMemberships,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetProfile(
        self,
        destinyMembershipId: int,
        membershipType: int,
        components: list,
    ) -> dict:
        """Returns Destiny Profile information for the supplied membership.

            Args:
                destinyMembershipId (int): Destiny membership ID.
                membershipType (int): A valid non-BungieNet membership type.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "responseMintedTimestamp": {
                "Name": "responseMintedTimestamp",
                "Type": "date-time",
                "Description": "Records the timestamp of when most components were last generated from the world server source. Unless the component type is specified in the documentation for secondaryComponentsMintedTimestamp, this value is sufficient to do data freshness.",
                "Attributes": []
            },
            "secondaryComponentsMintedTimestamp": {
                "Name": "secondaryComponentsMintedTimestamp",
                "Type": "date-time",
                "Description": "Some secondary components are not tracked in the primary response timestamp and have their timestamp tracked here. If your component is any of the following, this field is where you will find your timestamp value: PresentationNodes, Records, Collectibles, Metrics, StringVariables, Craftables, Transitory All other component types may use the primary timestamp property.",
                "Attributes": []
            },
            "vendorReceipts": {
                "Name": "vendorReceipts",
                "Type": "object",
                "Description": "Recent, refundable purchases you have made from vendors. When will you use it? Couldn't say...COMPONENT TYPE: VendorReceipts",
                "Attributes": [
                    "Depends on Component \"VendorReceipts\""
                ]
            },
            "profileInventory": {
                "Name": "profileInventory",
                "Type": "object",
                "Description": "The profile-level inventory of the Destiny Profile.COMPONENT TYPE: ProfileInventories",
                "Attributes": [
                    "Depends on Component \"ProfileInventories\""
                ]
            },
            "profileCurrencies": {
                "Name": "profileCurrencies",
                "Type": "object",
                "Description": "The profile-level currencies owned by the Destiny Profile.COMPONENT TYPE: ProfileCurrencies",
                "Attributes": [
                    "Depends on Component \"ProfileCurrencies\""
                ]
            },
            "profile": {
                "Name": "profile",
                "Type": "object",
                "Description": "The basic information about the Destiny Profile (formerly \"Account\").COMPONENT TYPE: Profiles",
                "Attributes": [
                    "Depends on Component \"Profiles\""
                ]
            },
            "platformSilver": {
                "Name": "platformSilver",
                "Type": "object",
                "Description": "Silver quantities for any platform on which this Profile plays destiny. COMPONENT TYPE: PlatformSilver",
                "Attributes": [
                    "Depends on Component \"PlatformSilver\""
                ]
            },
            "profileKiosks": {
                "Name": "profileKiosks",
                "Type": "object",
                "Description": "Items available from Kiosks that are available Profile-wide (i.e. across all characters)This component returns information about what Kiosk items are available to you on a *Profile* level. It is theoretically possible for Kiosks to have items gated by specific Character as well. If you ever have those, you will find them on the characterKiosks property.COMPONENT TYPE: Kiosks",
                "Attributes": [
                    "Depends on Component \"Kiosks\""
                ]
            },
            "profilePlugSets": {
                "Name": "profilePlugSets",
                "Type": "object",
                "Description": "When sockets refer to reusable Plug Sets (see DestinyPlugSetDefinition for more info), this is the set of plugs and their states that are profile-scoped.This comes back with ItemSockets, as it is needed for a complete picture of the sockets on requested items.COMPONENT TYPE: ItemSockets",
                "Attributes": [
                    "Depends on Component \"ItemSockets\""
                ]
            },
            "profileProgression": {
                "Name": "profileProgression",
                "Type": "object",
                "Description": "When we have progression information - such as Checklists - that may apply profile-wide, it will be returned here rather than in the per-character progression data.COMPONENT TYPE: ProfileProgression",
                "Attributes": [
                    "Depends on Component \"ProfileProgression\""
                ]
            },
            "profilePresentationNodes": {
                "Name": "profilePresentationNodes",
                "Type": "object",
                "Description": "COMPONENT TYPE: PresentationNodes",
                "Attributes": [
                    "Depends on Component \"PresentationNodes\""
                ]
            },
            "profileRecords": {
                "Name": "profileRecords",
                "Type": "object",
                "Description": "COMPONENT TYPE: Records",
                "Attributes": [
                    "Depends on Component \"Records\""
                ]
            },
            "profileCollectibles": {
                "Name": "profileCollectibles",
                "Type": "object",
                "Description": "COMPONENT TYPE: Collectibles",
                "Attributes": [
                    "Depends on Component \"Collectibles\""
                ]
            },
            "profileTransitoryData": {
                "Name": "profileTransitoryData",
                "Type": "object",
                "Description": "COMPONENT TYPE: Transitory",
                "Attributes": [
                    "Depends on Component \"Transitory\""
                ]
            },
            "metrics": {
                "Name": "metrics",
                "Type": "object",
                "Description": "COMPONENT TYPE: Metrics",
                "Attributes": [
                    "Depends on Component \"Metrics\""
                ]
            },
            "profileStringVariables": {
                "Name": "profileStringVariables",
                "Type": "object",
                "Description": "COMPONENT TYPE: StringVariables",
                "Attributes": [
                    "Depends on Component \"StringVariables\""
                ]
            },
            "profileCommendations": {
                "Name": "profileCommendations",
                "Type": "object",
                "Description": "COMPONENT TYPE: SocialCommendations",
                "Attributes": [
                    "Depends on Component \"SocialCommendations\""
                ]
            },
            "characters": {
                "Name": "characters",
                "Type": "object",
                "Description": "Basic information about each character, keyed by the CharacterId.COMPONENT TYPE: Characters",
                "Attributes": [
                    "Depends on Component \"Characters\""
                ]
            },
            "characterInventories": {
                "Name": "characterInventories",
                "Type": "object",
                "Description": "The character-level non-equipped inventory items, keyed by the Character's Id.COMPONENT TYPE: CharacterInventories",
                "Attributes": [
                    "Depends on Component \"CharacterInventories\""
                ]
            },
            "characterLoadouts": {
                "Name": "characterLoadouts",
                "Type": "object",
                "Description": "The character loadouts, keyed by the Character's Id.COMPONENT TYPE: CharacterLoadouts",
                "Attributes": [
                    "Depends on Component \"CharacterLoadouts\""
                ]
            },
            "characterProgressions": {
                "Name": "characterProgressions",
                "Type": "object",
                "Description": "Character-level progression data, keyed by the Character's Id.COMPONENT TYPE: CharacterProgressions",
                "Attributes": [
                    "Depends on Component \"CharacterProgressions\""
                ]
            },
            "characterRenderData": {
                "Name": "characterRenderData",
                "Type": "object",
                "Description": "Character rendering data - a minimal set of info needed to render a character in 3D - keyed by the Character's Id.COMPONENT TYPE: CharacterRenderData",
                "Attributes": [
                    "Depends on Component \"CharacterRenderData\""
                ]
            },
            "characterActivities": {
                "Name": "characterActivities",
                "Type": "object",
                "Description": "Character activity data - the activities available to this character and its status, keyed by the Character's Id.COMPONENT TYPE: CharacterActivities",
                "Attributes": [
                    "Depends on Component \"CharacterActivities\""
                ]
            },
            "characterEquipment": {
                "Name": "characterEquipment",
                "Type": "object",
                "Description": "The character's equipped items, keyed by the Character's Id.COMPONENT TYPE: CharacterEquipment",
                "Attributes": [
                    "Depends on Component \"CharacterEquipment\""
                ]
            },
            "characterKiosks": {
                "Name": "characterKiosks",
                "Type": "object",
                "Description": "Items available from Kiosks that are available to a specific character as opposed to the account as a whole. It must be combined with data from the profileKiosks property to get a full picture of the character's available items to check out of a kiosk.This component returns information about what Kiosk items are available to you on a *Character* level. Usually, kiosk items will be earned for the entire Profile (all characters) at once. To find those, look in the profileKiosks property.COMPONENT TYPE: Kiosks",
                "Attributes": [
                    "Depends on Component \"Kiosks\""
                ]
            },
            "characterPlugSets": {
                "Name": "characterPlugSets",
                "Type": "object",
                "Description": "When sockets refer to reusable Plug Sets (see DestinyPlugSetDefinition for more info), this is the set of plugs and their states, per character, that are character-scoped.This comes back with ItemSockets, as it is needed for a complete picture of the sockets on requested items.COMPONENT TYPE: ItemSockets",
                "Attributes": [
                    "Depends on Component \"ItemSockets\""
                ]
            },
            "characterUninstancedItemComponents": {
                "Name": "characterUninstancedItemComponents",
                "Type": "object",
                "Description": "Do you ever get the feeling that a system was designed *too* flexibly? That it can be used in so many different ways that you end up being unable to provide an easy to use abstraction for the mess that's happening under the surface?Let's talk about character-specific data that might be related to items without instances. These two statements are totally unrelated, I promise.At some point during D2, it was decided that items - such as Bounties - could be given to characters and *not* have instance data, but that *could* display and even use relevant state information on your account and character.Up to now, any item that had meaningful dependencies on character or account state had to be instanced, and thus \"itemComponents\" was all that you needed: it was keyed by item's instance IDs and provided the stateful information you needed inside.Unfortunately, we don't live in such a magical world anymore. This is information held on a per-character basis about non-instanced items that the characters have in their inventory - or that reference character-specific state information even if it's in Account-level inventory - and the values related to that item's state in relation to the given character.To give a concrete example, look at a Moments of Triumph bounty. They exist in a character's inventory, and show/care about a character's progression toward completing the bounty. But the bounty itself is a non-instanced item, like a mod or a currency. This returns that data for the characters who have the bounty in their inventory.I'm not crying, you're crying Okay we're both crying but it's going to be okay I promise Actually I shouldn't promise that, I don't know if it's going to be okay",
                "Attributes": []
            },
            "characterPresentationNodes": {
                "Name": "characterPresentationNodes",
                "Type": "object",
                "Description": "COMPONENT TYPE: PresentationNodes",
                "Attributes": [
                    "Depends on Component \"PresentationNodes\""
                ]
            },
            "characterRecords": {
                "Name": "characterRecords",
                "Type": "object",
                "Description": "COMPONENT TYPE: Records",
                "Attributes": [
                    "Depends on Component \"Records\""
                ]
            },
            "characterCollectibles": {
                "Name": "characterCollectibles",
                "Type": "object",
                "Description": "COMPONENT TYPE: Collectibles",
                "Attributes": [
                    "Depends on Component \"Collectibles\""
                ]
            },
            "characterStringVariables": {
                "Name": "characterStringVariables",
                "Type": "object",
                "Description": "COMPONENT TYPE: StringVariables",
                "Attributes": [
                    "Depends on Component \"StringVariables\""
                ]
            },
            "characterCraftables": {
                "Name": "characterCraftables",
                "Type": "object",
                "Description": "COMPONENT TYPE: Craftables",
                "Attributes": [
                    "Depends on Component \"Craftables\""
                ]
            },
            "itemComponents": {
                "Name": "itemComponents",
                "Type": "object",
                "Description": "Information about instanced items across all returned characters, keyed by the item's instance ID.COMPONENT TYPE: [See inside the DestinyItemComponentSet contract for component types.]",
                "Attributes": []
            },
            "characterCurrencyLookups": {
                "Name": "characterCurrencyLookups",
                "Type": "object",
                "Description": "A \"lookup\" convenience component that can be used to quickly check if the character has access to items that can be used for purchasing.COMPONENT TYPE: CurrencyLookups",
                "Attributes": [
                    "Depends on Component \"CurrencyLookups\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetProfile.html#operation_get_Destiny2-GetProfile"""

        try:
            self.logger.info("Executing GetProfile...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/".format(
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    components=components,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCharacter(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        components: list,
    ) -> dict:
        """Returns character information for the supplied character.

            Args:
                characterId (int): ID of the character.
                destinyMembershipId (int): Destiny membership ID.
                membershipType (int): A valid non-BungieNet membership type.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "inventory": {
                "Name": "inventory",
                "Type": "object",
                "Description": "The character-level non-equipped inventory items.COMPONENT TYPE: CharacterInventories",
                "Attributes": [
                    "Depends on Component \"CharacterInventories\""
                ]
            },
            "character": {
                "Name": "character",
                "Type": "object",
                "Description": "Base information about the character in question.COMPONENT TYPE: Characters",
                "Attributes": [
                    "Depends on Component \"Characters\""
                ]
            },
            "progressions": {
                "Name": "progressions",
                "Type": "object",
                "Description": "Character progression data, including Milestones.COMPONENT TYPE: CharacterProgressions",
                "Attributes": [
                    "Depends on Component \"CharacterProgressions\""
                ]
            },
            "renderData": {
                "Name": "renderData",
                "Type": "object",
                "Description": "Character rendering data - a minimal set of information about equipment and dyes used for rendering.COMPONENT TYPE: CharacterRenderData",
                "Attributes": [
                    "Depends on Component \"CharacterRenderData\""
                ]
            },
            "activities": {
                "Name": "activities",
                "Type": "object",
                "Description": "Activity data - info about current activities available to the player.COMPONENT TYPE: CharacterActivities",
                "Attributes": [
                    "Depends on Component \"CharacterActivities\""
                ]
            },
            "equipment": {
                "Name": "equipment",
                "Type": "object",
                "Description": "Equipped items on the character.COMPONENT TYPE: CharacterEquipment",
                "Attributes": [
                    "Depends on Component \"CharacterEquipment\""
                ]
            },
            "loadouts": {
                "Name": "loadouts",
                "Type": "object",
                "Description": "The loadouts available to the character.COMPONENT TYPE: CharacterLoadouts",
                "Attributes": [
                    "Depends on Component \"CharacterLoadouts\""
                ]
            },
            "kiosks": {
                "Name": "kiosks",
                "Type": "object",
                "Description": "Items available from Kiosks that are available to this specific character. COMPONENT TYPE: Kiosks",
                "Attributes": [
                    "Depends on Component \"Kiosks\""
                ]
            },
            "plugSets": {
                "Name": "plugSets",
                "Type": "object",
                "Description": "When sockets refer to reusable Plug Sets (see DestinyPlugSetDefinition for more info), this is the set of plugs and their states that are scoped to this character.This comes back with ItemSockets, as it is needed for a complete picture of the sockets on requested items.COMPONENT TYPE: ItemSockets",
                "Attributes": [
                    "Depends on Component \"ItemSockets\""
                ]
            },
            "presentationNodes": {
                "Name": "presentationNodes",
                "Type": "object",
                "Description": "COMPONENT TYPE: PresentationNodes",
                "Attributes": [
                    "Depends on Component \"PresentationNodes\""
                ]
            },
            "records": {
                "Name": "records",
                "Type": "object",
                "Description": "COMPONENT TYPE: Records",
                "Attributes": [
                    "Depends on Component \"Records\""
                ]
            },
            "collectibles": {
                "Name": "collectibles",
                "Type": "object",
                "Description": "COMPONENT TYPE: Collectibles",
                "Attributes": [
                    "Depends on Component \"Collectibles\""
                ]
            },
            "itemComponents": {
                "Name": "itemComponents",
                "Type": "object",
                "Description": "The set of components belonging to the player's instanced items.COMPONENT TYPE: [See inside the DestinyItemComponentSet contract for component types.]",
                "Attributes": []
            },
            "uninstancedItemComponents": {
                "Name": "uninstancedItemComponents",
                "Type": "object",
                "Description": "The set of components belonging to the player's UNinstanced items. Because apparently now those too can have information relevant to the character's state.COMPONENT TYPE: [See inside the DestinyItemComponentSet contract for component types.]",
                "Attributes": []
            },
            "currencyLookups": {
                "Name": "currencyLookups",
                "Type": "object",
                "Description": "A \"lookup\" convenience component that can be used to quickly check if the character has access to items that can be used for purchasing.COMPONENT TYPE: CurrencyLookups",
                "Attributes": [
                    "Depends on Component \"CurrencyLookups\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetCharacter.html#operation_get_Destiny2-GetCharacter"""

        try:
            self.logger.info("Executing GetCharacter...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    components=components,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanWeeklyRewardState(
        self,
        groupId: int,
    ) -> dict:
        """Returns information on the weekly clan rewards and if the clan has earned them or not. Note that this will always report rewards as not redeemed.

            Args:
                groupId (int): A valid group id of clan.

            Returns:
        {
            "milestoneHash": {
                "Name": "milestoneHash",
                "Type": "uint32",
                "Description": "The unique identifier for the Milestone. Use it to look up the DestinyMilestoneDefinition, so you can combine the other data in this contract with static definition data.",
                "Attributes": [
                    "Mapped to Definition"
                ]
            },
            "availableQuests": {
                "Name": "availableQuests",
                "Type": "array",
                "Description": "Indicates what quests are available for this Milestone. Usually this will be only a single Quest, but some quests have multiple available that you can choose from at any given time. All possible quests for a milestone can be found in the DestinyMilestoneDefinition, but they must be combined with this Live data to determine which one(s) are actually active right now. It is possible for Milestones to not have any quests.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "questItemHash": {
                            "Name": "questItemHash",
                            "Type": "uint32",
                            "Description": "Quests are defined as Items in content. As such, this is the hash identifier of the DestinyInventoryItemDefinition that represents this quest. It will have pointers to all of the steps in the quest, and display information for the quest (title, description, icon etc) Individual steps will be referred to in the Quest item's DestinyInventoryItemDefinition.setData property, and themselves are Items with their own renderable data.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "status": {
                            "Name": "status",
                            "Type": "object",
                            "Description": "The current status of the quest for the character making the request.",
                            "Attributes": []
                        }
                    },
                    {
                        "activity": {
                            "Name": "activity",
                            "Type": "object",
                            "Description": "*IF* the Milestone has an active Activity that can give you greater details about what you need to do, it will be returned here. Remember to associate this with the DestinyMilestoneDefinition's activities to get details about the activity, including what specific quest it is related to if you have multiple quests to choose from.",
                            "Attributes": []
                        }
                    },
                    {
                        "challenges": {
                            "Name": "challenges",
                            "Type": "array",
                            "Description": "The activities referred to by this quest can have many associated challenges. They are all contained here, with activityHashes so that you can associate them with the specific activity variants in which they can be found. In retrospect, I probably should have put these under the specific Activity Variants, but it's too late to change it now. Theoretically, a quest without Activities can still have Challenges, which is why this is on a higher level than activity/variants, but it probably should have been in both places. That may come as a later revision.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "activities": {
                "Name": "activities",
                "Type": "array",
                "Description": "The currently active Activities in this milestone, when the Milestone is driven by Challenges.Not all Milestones have Challenges, but when they do this will indicate the Activities and Challenges under those Activities related to this Milestone.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "activityHash": {
                            "Name": "activityHash",
                            "Type": "uint32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "challenges": {
                            "Name": "challenges",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "modifierHashes": {
                            "Name": "modifierHashes",
                            "Type": "array",
                            "Description": "If the activity has modifiers, this will be the list of modifiers that all variants have in common. Perform lookups against DestinyActivityModifierDefinition which defines the modifier being applied to get at the modifier data.Note that, in the DestiyActivityDefinition, you will see many more modifiers than this being referred to: those are all *possible* modifiers for the activity, not the active ones. Use only the active ones to match what's really live.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "booleanActivityOptions": {
                            "Name": "booleanActivityOptions",
                            "Type": "object",
                            "Description": "The set of activity options for this activity, keyed by an identifier that's unique for this activity (not guaranteed to be unique between or across all activities, though should be unique for every *variant* of a given *conceptual* activity: for instance, the original D2 Raid has many variant DestinyActivityDefinitions. While other activities could potentially have the same option hashes, for any given D2 base Raid variant the hash will be unique).As a concrete example of this data, the hashes you get for Raids will correspond to the currently active \"Challenge Mode\".We don't have any human readable information for these, but saavy 3rd party app users could manually associate the key (a hash identifier for the \"option\" that is enabled/disabled) and the value (whether it's enabled or disabled presently)On our side, we don't necessarily even know what these are used for (the game designers know, but we don't), and we have no human readable data for them. In order to use them, you will have to do some experimentation.",
                            "Attributes": []
                        }
                    },
                    {
                        "loadoutRequirementIndex": {
                            "Name": "loadoutRequirementIndex",
                            "Type": "int32",
                            "Description": "If returned, this is the index into the DestinyActivityDefinition's \"loadouts\" property, indicating the currently active loadout requirements.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "phases": {
                            "Name": "phases",
                            "Type": "array",
                            "Description": "If the Activity has discrete \"phases\" that we can track, that info will be here. Otherwise, this value will be NULL. Note that this is a list and not a dictionary: the order implies the ascending order of phases or progression in this activity.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "values": {
                "Name": "values",
                "Type": "object",
                "Description": "Milestones may have arbitrary key/value pairs associated with them, for data that users will want to know about but that doesn't fit neatly into any of the common components such as Quests. A good example of this would be - if this existed in Destiny 1 - the number of wins you currently have on your Trials of Osiris ticket. Looking in the DestinyMilestoneDefinition, you can use the string identifier of this dictionary to look up more info about the value, including localized string content for displaying the value. The value in the dictionary is the floating point number. The definition will tell you how to format this number.",
                "Attributes": []
            },
            "vendorHashes": {
                "Name": "vendorHashes",
                "Type": "array",
                "Description": "A milestone may have one or more active vendors that are \"related\" to it (that provide rewards, or that are the initiators of the Milestone). I already regret this, even as I'm typing it. [I told you I'd regret this] You see, sometimes a milestone may be directly correlated with a set of vendors that provide varying tiers of rewards. The player may not be able to interact with one or more of those vendors. This will return the hashes of the Vendors that the player *can* interact with, allowing you to show their current inventory as rewards or related items to the Milestone or its activities.Before we even use it, it's already deprecated! How much of a bummer is that? We need more data.",
                "Attributes": [
                    "Mapped to Definition"
                ],
                "Array Contents": "uint32"
            },
            "vendors": {
                "Name": "vendors",
                "Type": "array",
                "Description": "Replaces vendorHashes, which I knew was going to be trouble the day it walked in the door. This will return not only what Vendors are active and relevant to the activity (in an implied order that you can choose to ignore), but also other data - for example, if the Vendor is featuring a specific item relevant to this event that you should show with them.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "vendorHash": {
                            "Name": "vendorHash",
                            "Type": "uint32",
                            "Description": "The hash identifier of the Vendor related to this Milestone. You can show useful things from this, such as thier Faction icon or whatever you might care about.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "previewItemHash": {
                            "Name": "previewItemHash",
                            "Type": "uint32",
                            "Description": "If this vendor is featuring a specific item for this event, this will be the hash identifier of that item. I'm taking bets now on how long we go before this needs to be a list or some other, more complex representation instead and I deprecate this too. I'm going to go with 5 months. Calling it now, 2017-09-14 at 9:46pm PST.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    }
                ]
            },
            "rewards": {
                "Name": "rewards",
                "Type": "array",
                "Description": "If the entity to which this component is attached has known active Rewards for the player, this will detail information about those rewards, keyed by the RewardEntry Hash. (See DestinyMilestoneDefinition for more information about Reward Entries) Note that these rewards are not for the Quests related to the Milestone. Think of these as \"overview/checklist\" rewards that may be provided for Milestones that may provide rewards for performing a variety of tasks that aren't under a specific Quest.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "rewardCategoryHash": {
                            "Name": "rewardCategoryHash",
                            "Type": "uint32",
                            "Description": "Look up the relevant DestinyMilestoneDefinition, and then use rewardCategoryHash to look up the category info in DestinyMilestoneDefinition.rewards.",
                            "Attributes": []
                        }
                    },
                    {
                        "entries": {
                            "Name": "entries",
                            "Type": "array",
                            "Description": "The individual reward entries for this category, and their status.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "startDate": {
                "Name": "startDate",
                "Type": "date-time",
                "Description": "If known, this is the date when the event last began or refreshed. It will only be populated for events with fixed and repeating start and end dates.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "endDate": {
                "Name": "endDate",
                "Type": "date-time",
                "Description": "If known, this is the date when the event will next end or repeat. It will only be populated for events with fixed and repeating start and end dates.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "order": {
                "Name": "order",
                "Type": "int32",
                "Description": "Used for ordering milestones in a display to match how we order them in BNet. May pull from static data, or possibly in the future from dynamic information.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetClanWeeklyRewardState.html#operation_get_Destiny2-GetClanWeeklyRewardState"""

        try:
            self.logger.info("Executing GetClanWeeklyRewardState...")
            url = self.base_url + f"/Destiny2/Clan/{groupId}/WeeklyRewardState/".format(
                groupId=groupId
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanBannerSource(
        self,
    ) -> dict:
        """Returns the dictionary of values for the Clan Banner

            Args:


            Returns:
        {}


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetClanBannerSource.html#operation_get_Destiny2-GetClanBannerSource"""

        try:
            self.logger.info("Executing GetClanBannerSource...")
            url = self.base_url + "/Destiny2/Clan/ClanBannerDictionary/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetItem(
        self,
        destinyMembershipId: int,
        itemInstanceId: int,
        membershipType: int,
        components: list,
    ) -> dict:
        """Retrieve the details of an instanced Destiny Item. An instanced Destiny item is one with an ItemInstanceId. Non-instanced items, such as materials, have no useful instance-specific details and thus are not queryable here.

            Args:
                destinyMembershipId (int): The membership ID of the destiny profile.
                itemInstanceId (int): The Instance ID of the destiny item.
                membershipType (int): A valid non-BungieNet membership type.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "characterId": {
                "Name": "characterId",
                "Type": "int64",
                "Description": "If the item is on a character, this will return the ID of the character that is holding the item.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "item": {
                "Name": "item",
                "Type": "object",
                "Description": "Common data for the item relevant to its non-instanced properties.COMPONENT TYPE: ItemCommonData",
                "Attributes": [
                    "Depends on Component \"ItemCommonData\""
                ]
            },
            "instance": {
                "Name": "instance",
                "Type": "object",
                "Description": "Basic instance data for the item.COMPONENT TYPE: ItemInstances",
                "Attributes": [
                    "Depends on Component \"ItemInstances\""
                ]
            },
            "objectives": {
                "Name": "objectives",
                "Type": "object",
                "Description": "Information specifically about the item's objectives.COMPONENT TYPE: ItemObjectives",
                "Attributes": [
                    "Depends on Component \"ItemObjectives\""
                ]
            },
            "perks": {
                "Name": "perks",
                "Type": "object",
                "Description": "Information specifically about the perks currently active on the item.COMPONENT TYPE: ItemPerks",
                "Attributes": [
                    "Depends on Component \"ItemPerks\""
                ]
            },
            "renderData": {
                "Name": "renderData",
                "Type": "object",
                "Description": "Information about how to render the item in 3D.COMPONENT TYPE: ItemRenderData",
                "Attributes": [
                    "Depends on Component \"ItemRenderData\""
                ]
            },
            "stats": {
                "Name": "stats",
                "Type": "object",
                "Description": "Information about the computed stats of the item: power, defense, etc...COMPONENT TYPE: ItemStats",
                "Attributes": [
                    "Depends on Component \"ItemStats\""
                ]
            },
            "talentGrid": {
                "Name": "talentGrid",
                "Type": "object",
                "Description": "Information about the talent grid attached to the item. Talent nodes can provide a variety of benefits and abilities, and in Destiny 2 are used almost exclusively for the character's \"Builds\".COMPONENT TYPE: ItemTalentGrids",
                "Attributes": [
                    "Depends on Component \"ItemTalentGrids\""
                ]
            },
            "sockets": {
                "Name": "sockets",
                "Type": "object",
                "Description": "Information about the sockets of the item: which are currently active, what potential sockets you could have and the stats/abilities/perks you can gain from them.COMPONENT TYPE: ItemSockets",
                "Attributes": [
                    "Depends on Component \"ItemSockets\""
                ]
            },
            "reusablePlugs": {
                "Name": "reusablePlugs",
                "Type": "object",
                "Description": "Information about the Reusable Plugs for sockets on an item. These are plugs that you can insert into the given socket regardless of if you actually own an instance of that plug: they are logic-driven plugs rather than inventory-driven. These may need to be combined with Plug Set component data to get a full picture of available plugs on a given socket. COMPONENT TYPE: ItemReusablePlugs",
                "Attributes": [
                    "Depends on Component \"ItemReusablePlugs\""
                ]
            },
            "plugObjectives": {
                "Name": "plugObjectives",
                "Type": "object",
                "Description": "Information about objectives on Plugs for a given item. See the component's documentation for more info.COMPONENT TYPE: ItemPlugObjectives",
                "Attributes": [
                    "Depends on Component \"ItemPlugObjectives\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetItem.html#operation_get_Destiny2-GetItem"""

        try:
            self.logger.info("Executing GetItem...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Item/{itemInstanceId}/".format(
                    destinyMembershipId=destinyMembershipId,
                    itemInstanceId=itemInstanceId,
                    membershipType=membershipType,
                    components=components,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetVendors(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        components: list,
        filter: int,
    ) -> dict:
        """Get currently available vendors from the list of vendors that can possibly have rotating inventory. Note that this does not include things like preview vendors and vendors-as-kiosks, neither of whom have rotating/dynamic inventories. Use their definitions as-is for those.

            Args:
                characterId (int): The Destiny Character ID of the character for whom we're getting vendor info.
                destinyMembershipId (int): Destiny membership ID of another user. You may be denied.
                membershipType (int): A valid non-BungieNet membership type.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.
                filter (int): The filter of what vendors and items to return, if any.

            Returns:
        {
            "vendorGroups": {
                "Name": "vendorGroups",
                "Type": "object",
                "Description": "For Vendors being returned, this will give you the information you need to group them and order them in the same way that the Bungie Companion app performs grouping. It will automatically be returned if you request the Vendors component.COMPONENT TYPE: Vendors",
                "Attributes": [
                    "Depends on Component \"Vendors\""
                ]
            },
            "vendors": {
                "Name": "vendors",
                "Type": "object",
                "Description": "The base properties of the vendor. These are keyed by the Vendor Hash, so you will get one Vendor Component per vendor returned.COMPONENT TYPE: Vendors",
                "Attributes": [
                    "Depends on Component \"Vendors\""
                ]
            },
            "categories": {
                "Name": "categories",
                "Type": "object",
                "Description": "Categories that the vendor has available, and references to the sales therein. These are keyed by the Vendor Hash, so you will get one Categories Component per vendor returned.COMPONENT TYPE: VendorCategories",
                "Attributes": [
                    "Depends on Component \"VendorCategories\""
                ]
            },
            "sales": {
                "Name": "sales",
                "Type": "object",
                "Description": "Sales, keyed by the vendorItemIndex of the item being sold. These are keyed by the Vendor Hash, so you will get one Sale Item Set Component per vendor returned.Note that within the Sale Item Set component, the sales are themselves keyed by the vendorSaleIndex, so you can relate it to the corrent sale item definition within the Vendor's definition.COMPONENT TYPE: VendorSales",
                "Attributes": [
                    "Depends on Component \"VendorSales\""
                ]
            },
            "itemComponents": {
                "Name": "itemComponents",
                "Type": "object",
                "Description": "The set of item detail components, one set of item components per Vendor. These are keyed by the Vendor Hash, so you will get one Item Component Set per vendor returned.The components contained inside are themselves keyed by the vendorSaleIndex, and will have whatever item-level components you requested (Sockets, Stats, Instance data etc...) per item being sold by the vendor.",
                "Attributes": []
            },
            "currencyLookups": {
                "Name": "currencyLookups",
                "Type": "object",
                "Description": "A \"lookup\" convenience component that can be used to quickly check if the character has access to items that can be used for purchasing.COMPONENT TYPE: CurrencyLookups",
                "Attributes": [
                    "Depends on Component \"CurrencyLookups\""
                ]
            },
            "stringVariables": {
                "Name": "stringVariables",
                "Type": "object",
                "Description": "A map of string variable values by hash for this character context.COMPONENT TYPE: StringVariables",
                "Attributes": [
                    "Depends on Component \"StringVariables\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetVendors.html#operation_get_Destiny2-GetVendors"""

        try:
            self.logger.info("Executing GetVendors...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    components=components,
                    filter=filter,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetVendor(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        vendorHash: int,
        components: list,
    ) -> dict:
        """Get the details of a specific Vendor.

            Args:
                characterId (int): The Destiny Character ID of the character for whom we're getting vendor info.
                destinyMembershipId (int): Destiny membership ID of another user. You may be denied.
                membershipType (int): A valid non-BungieNet membership type.
                vendorHash (int): The Hash identifier of the Vendor to be returned.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "vendor": {
                "Name": "vendor",
                "Type": "object",
                "Description": "The base properties of the vendor.COMPONENT TYPE: Vendors",
                "Attributes": [
                    "Depends on Component \"Vendors\""
                ]
            },
            "categories": {
                "Name": "categories",
                "Type": "object",
                "Description": "Categories that the vendor has available, and references to the sales therein.COMPONENT TYPE: VendorCategories",
                "Attributes": [
                    "Depends on Component \"VendorCategories\""
                ]
            },
            "sales": {
                "Name": "sales",
                "Type": "object",
                "Description": "Sales, keyed by the vendorItemIndex of the item being sold.COMPONENT TYPE: VendorSales",
                "Attributes": [
                    "Depends on Component \"VendorSales\""
                ]
            },
            "itemComponents": {
                "Name": "itemComponents",
                "Type": "object",
                "Description": "Item components, keyed by the vendorItemIndex of the active sale items.COMPONENT TYPE: [See inside the DestinyItemComponentSet contract for component types.]",
                "Attributes": []
            },
            "currencyLookups": {
                "Name": "currencyLookups",
                "Type": "object",
                "Description": "A \"lookup\" convenience component that can be used to quickly check if the character has access to items that can be used for purchasing.COMPONENT TYPE: CurrencyLookups",
                "Attributes": [
                    "Depends on Component \"CurrencyLookups\""
                ]
            },
            "stringVariables": {
                "Name": "stringVariables",
                "Type": "object",
                "Description": "A map of string variable values by hash for this character context.COMPONENT TYPE: StringVariables",
                "Attributes": [
                    "Depends on Component \"StringVariables\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetVendor.html#operation_get_Destiny2-GetVendor"""

        try:
            self.logger.info("Executing GetVendor...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    vendorHash=vendorHash,
                    components=components,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicVendors(
        self,
        components: list,
    ) -> dict:
        """Get items available from vendors where the vendors have items for sale that are common for everyone. If any portion of the Vendor's available inventory is character or account specific, we will be unable to return their data from this endpoint due to the way that available inventory is computed. As I am often guilty of saying: 'It's a long story...'

            Args:
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "vendorGroups": {
                "Name": "vendorGroups",
                "Type": "object",
                "Description": "For Vendors being returned, this will give you the information you need to group them and order them in the same way that the Bungie Companion app performs grouping. It will automatically be returned if you request the Vendors component.COMPONENT TYPE: Vendors",
                "Attributes": [
                    "Depends on Component \"Vendors\""
                ]
            },
            "vendors": {
                "Name": "vendors",
                "Type": "object",
                "Description": "The base properties of the vendor. These are keyed by the Vendor Hash, so you will get one Vendor Component per vendor returned.COMPONENT TYPE: Vendors",
                "Attributes": [
                    "Depends on Component \"Vendors\""
                ]
            },
            "categories": {
                "Name": "categories",
                "Type": "object",
                "Description": "Categories that the vendor has available, and references to the sales therein. These are keyed by the Vendor Hash, so you will get one Categories Component per vendor returned.COMPONENT TYPE: VendorCategories",
                "Attributes": [
                    "Depends on Component \"VendorCategories\""
                ]
            },
            "sales": {
                "Name": "sales",
                "Type": "object",
                "Description": "Sales, keyed by the vendorItemIndex of the item being sold. These are keyed by the Vendor Hash, so you will get one Sale Item Set Component per vendor returned.Note that within the Sale Item Set component, the sales are themselves keyed by the vendorSaleIndex, so you can relate it to the corrent sale item definition within the Vendor's definition.COMPONENT TYPE: VendorSales",
                "Attributes": [
                    "Depends on Component \"VendorSales\""
                ]
            },
            "stringVariables": {
                "Name": "stringVariables",
                "Type": "object",
                "Description": "A set of string variable values by hash for a public vendors context.COMPONENT TYPE: StringVariables",
                "Attributes": [
                    "Depends on Component \"StringVariables\""
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetPublicVendors.html#operation_get_Destiny2-GetPublicVendors"""

        try:
            self.logger.info("Executing GetPublicVendors...")
            url = self.base_url + "/Destiny2/Vendors/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCollectibleNodeDetails(
        self,
        characterId: int,
        collectiblePresentationNodeHash: int,
        destinyMembershipId: int,
        membershipType: int,
        components: list,
    ) -> dict:
        """Given a Presentation Node that has Collectibles as direct descendants, this will return item details about those descendants in the context of the requesting character.

            Args:
                characterId (int): The Destiny Character ID of the character for whom we're getting collectible detail info.
                collectiblePresentationNodeHash (int): The hash identifier of the Presentation Node for whom we should return collectible details. Details will only be returned for collectibles that are direct descendants of this node.
                destinyMembershipId (int): Destiny membership ID of another user. You may be denied.
                membershipType (int): A valid non-BungieNet membership type.
                components (list): A comma separated list of components to return (as strings or numeric values). See the DestinyComponentType enum for valid components to request. You must request at least one component to receive results.

            Returns:
        {
            "collectibles": {
                "Name": "collectibles",
                "Type": "object",
                "Description": "COMPONENT TYPE: Collectibles",
                "Attributes": [
                    "Depends on Component \"Collectibles\""
                ]
            },
            "collectibleItemComponents": {
                "Name": "collectibleItemComponents",
                "Type": "object",
                "Description": "Item components, keyed by the item hash of the items pointed at collectibles found under the requested Presentation Node.NOTE: I had a lot of hemming and hawing about whether these should be keyed by collectible hash or item hash... but ultimately having it be keyed by item hash meant that UI that already uses DestinyItemComponentSet data wouldn't have to have a special override to do the collectible -> item lookup once you delve into an item's details, and it also meant that you didn't have to remember that the Hash being used as the key for plugSets was different from the Hash being used for the other Dictionaries. As a result, using the Item Hash felt like the least crappy solution.We may all come to regret this decision. We will see.COMPONENT TYPE: [See inside the DestinyItemComponentSet contract for component types.]",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetCollectibleNodeDetails.html#operation_get_Destiny2-GetCollectibleNodeDetails"""

        try:
            self.logger.info("Executing GetCollectibleNodeDetails...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Collectibles/{collectiblePresentationNodeHash}/".format(
                    characterId=characterId,
                    collectiblePresentationNodeHash=collectiblePresentationNodeHash,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    components=components,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def TransferItem(
        self,
        itemReferenceHash: int,
        stackSize: int,
        transferToVault: bool,
        itemId: int,
        characterId: int,
        membershipType: int,
    ) -> dict:
        """Transfer an item to/from your vault. You must have a valid Destiny account. You must also pass BOTH a reference AND an instance ID if it's an instanced item. itshappening.gif

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-TransferItem.html#operation_post_Destiny2-TransferItem"""

        request_body = {
            "itemReferenceHash": itemReferenceHash,
            "stackSize": stackSize,
            "transferToVault": transferToVault,
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing TransferItem...")
            url = self.base_url + "/Destiny2/Actions/Items/TransferItem/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def PullFromPostmaster(
        self,
        itemReferenceHash: int,
        stackSize: int,
        itemId: int,
        characterId: int,
        membershipType: int,
    ) -> dict:
        """Extract an item from the Postmaster, with whatever implications that may entail. You must have a valid Destiny account. You must also pass BOTH a reference AND an instance ID if it's an instanced item.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-PullFromPostmaster.html#operation_post_Destiny2-PullFromPostmaster"""

        request_body = {
            "itemReferenceHash": itemReferenceHash,
            "stackSize": stackSize,
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing PullFromPostmaster...")
            url = self.base_url + "/Destiny2/Actions/Items/PullFromPostmaster/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EquipItem(
        self, itemId: int, characterId: int, membershipType: int
    ) -> dict:
        """Equip an item. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-EquipItem.html#operation_post_Destiny2-EquipItem"""

        request_body = {
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing EquipItem...")
            url = self.base_url + "/Destiny2/Actions/Items/EquipItem/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EquipItems(
        self, itemIds: list, characterId: int, membershipType: int
    ) -> dict:
        """Equip a list of items by itemInstanceIds. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. Any items not found on your character will be ignored.

            Args:


            Returns:
        {
            "equipResults": {
                "Name": "equipResults",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "itemInstanceId": {
                            "Name": "itemInstanceId",
                            "Type": "int64",
                            "Description": "The instance ID of the item in question (all items that can be equipped must, but definition, be Instanced and thus have an Instance ID that you can use to refer to them)",
                            "Attributes": []
                        }
                    },
                    {
                        "equipStatus": {
                            "Name": "equipStatus",
                            "Type": "int32",
                            "Description": "A PlatformErrorCodes enum indicating whether it succeeded, and if it failed why.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-EquipItems.html#operation_post_Destiny2-EquipItems"""

        request_body = {
            "itemIds": itemIds,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing EquipItems...")
            url = self.base_url + "/Destiny2/Actions/Items/EquipItems/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EquipLoadout(
        self, loadoutIndex: int, characterId: int, membershipType: int
    ) -> dict:
        """Equip a loadout. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-EquipLoadout.html#operation_post_Destiny2-EquipLoadout"""

        request_body = {
            "loadoutIndex": loadoutIndex,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing EquipLoadout...")
            url = self.base_url + "/Destiny2/Actions/Loadouts/EquipLoadout/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def SnapshotLoadout(
        self,
        colorHash: int,
        iconHash: int,
        nameHash: int,
        loadoutIndex: int,
        characterId: int,
        membershipType: int,
    ) -> dict:
        """Snapshot a loadout with the currently equipped items.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-SnapshotLoadout.html#operation_post_Destiny2-SnapshotLoadout"""

        request_body = {
            "colorHash": colorHash,
            "iconHash": iconHash,
            "nameHash": nameHash,
            "loadoutIndex": loadoutIndex,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing SnapshotLoadout...")
            url = self.base_url + "/Destiny2/Actions/Loadouts/SnapshotLoadout/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def UpdateLoadoutIdentifiers(
        self,
        colorHash: int,
        iconHash: int,
        nameHash: int,
        loadoutIndex: int,
        characterId: int,
        membershipType: int,
    ) -> dict:
        """Update the color, icon, and name of a loadout.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-UpdateLoadoutIdentifiers.html#operation_post_Destiny2-UpdateLoadoutIdentifiers"""

        request_body = {
            "colorHash": colorHash,
            "iconHash": iconHash,
            "nameHash": nameHash,
            "loadoutIndex": loadoutIndex,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing UpdateLoadoutIdentifiers...")
            url = (
                self.base_url
                + "/Destiny2/Actions/Loadouts/UpdateLoadoutIdentifiers/".format()
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ClearLoadout(
        self, loadoutIndex: int, characterId: int, membershipType: int
    ) -> dict:
        """Clear the identifiers and items of a loadout.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-ClearLoadout.html#operation_post_Destiny2-ClearLoadout"""

        request_body = {
            "loadoutIndex": loadoutIndex,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing ClearLoadout...")
            url = self.base_url + "/Destiny2/Actions/Loadouts/ClearLoadout/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def SetItemLockState(
        self, state: bool, itemId: int, characterId: int, membershipType: int
    ) -> dict:
        """Set the Lock State for an instanced item. You must have a valid Destiny Account.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-SetItemLockState.html#operation_post_Destiny2-SetItemLockState"""

        request_body = {
            "state": state,
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing SetItemLockState...")
            url = self.base_url + "/Destiny2/Actions/Items/SetLockState/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def SetQuestTrackedState(
        self, state: bool, itemId: int, characterId: int, membershipType: int
    ) -> dict:
        """Set the Tracking State for an instanced item, if that item is a Quest or Bounty. You must have a valid Destiny Account. Yeah, it's an item.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-SetQuestTrackedState.html#operation_post_Destiny2-SetQuestTrackedState"""

        request_body = {
            "state": state,
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing SetQuestTrackedState...")
            url = self.base_url + "/Destiny2/Actions/Items/SetTrackedState/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def InsertSocketPlug(
        self,
        actionToken: str,
        itemInstanceId: int,
        plug: dict,
        characterId: int,
        membershipType: int,
    ) -> dict:
        """Insert a plug into a socketed item. I know how it sounds, but I assure you it's much more G-rated than you might be guessing. We haven't decided yet whether this will be able to insert plugs that have side effects, but if we do it will require special scope permission for an application attempting to do so. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. Request must include proof of permission for 'InsertPlugs' from the account owner.

            Args:


            Returns:
        {
            "item": {
                "characterId": {
                    "Name": "characterId",
                    "Type": "int64",
                    "Description": "If the item is on a character, this will return the ID of the character that is holding the item.",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "item": {
                    "Name": "item",
                    "Type": "object",
                    "Description": "Common data for the item relevant to its non-instanced properties.COMPONENT TYPE: ItemCommonData",
                    "Attributes": [
                        "Depends on Component \"ItemCommonData\""
                    ]
                },
                "instance": {
                    "Name": "instance",
                    "Type": "object",
                    "Description": "Basic instance data for the item.COMPONENT TYPE: ItemInstances",
                    "Attributes": [
                        "Depends on Component \"ItemInstances\""
                    ]
                },
                "objectives": {
                    "Name": "objectives",
                    "Type": "object",
                    "Description": "Information specifically about the item's objectives.COMPONENT TYPE: ItemObjectives",
                    "Attributes": [
                        "Depends on Component \"ItemObjectives\""
                    ]
                },
                "perks": {
                    "Name": "perks",
                    "Type": "object",
                    "Description": "Information specifically about the perks currently active on the item.COMPONENT TYPE: ItemPerks",
                    "Attributes": [
                        "Depends on Component \"ItemPerks\""
                    ]
                },
                "renderData": {
                    "Name": "renderData",
                    "Type": "object",
                    "Description": "Information about how to render the item in 3D.COMPONENT TYPE: ItemRenderData",
                    "Attributes": [
                        "Depends on Component \"ItemRenderData\""
                    ]
                },
                "stats": {
                    "Name": "stats",
                    "Type": "object",
                    "Description": "Information about the computed stats of the item: power, defense, etc...COMPONENT TYPE: ItemStats",
                    "Attributes": [
                        "Depends on Component \"ItemStats\""
                    ]
                },
                "talentGrid": {
                    "Name": "talentGrid",
                    "Type": "object",
                    "Description": "Information about the talent grid attached to the item. Talent nodes can provide a variety of benefits and abilities, and in Destiny 2 are used almost exclusively for the character's \"Builds\".COMPONENT TYPE: ItemTalentGrids",
                    "Attributes": [
                        "Depends on Component \"ItemTalentGrids\""
                    ]
                },
                "sockets": {
                    "Name": "sockets",
                    "Type": "object",
                    "Description": "Information about the sockets of the item: which are currently active, what potential sockets you could have and the stats/abilities/perks you can gain from them.COMPONENT TYPE: ItemSockets",
                    "Attributes": [
                        "Depends on Component \"ItemSockets\""
                    ]
                },
                "reusablePlugs": {
                    "Name": "reusablePlugs",
                    "Type": "object",
                    "Description": "Information about the Reusable Plugs for sockets on an item. These are plugs that you can insert into the given socket regardless of if you actually own an instance of that plug: they are logic-driven plugs rather than inventory-driven. These may need to be combined with Plug Set component data to get a full picture of available plugs on a given socket. COMPONENT TYPE: ItemReusablePlugs",
                    "Attributes": [
                        "Depends on Component \"ItemReusablePlugs\""
                    ]
                },
                "plugObjectives": {
                    "Name": "plugObjectives",
                    "Type": "object",
                    "Description": "Information about objectives on Plugs for a given item. See the component's documentation for more info.COMPONENT TYPE: ItemPlugObjectives",
                    "Attributes": [
                        "Depends on Component \"ItemPlugObjectives\""
                    ]
                }
            },
            "addedInventoryItems": {
                "Name": "addedInventoryItems",
                "Type": "array",
                "Description": "Items that appeared in the inventory possibly as a result of an action.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "itemHash": {
                            "Name": "itemHash",
                            "Type": "uint32",
                            "Description": "The identifier for the item's definition, which is where most of the useful static information for the item can be found.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "itemInstanceId": {
                            "Name": "itemInstanceId",
                            "Type": "int64",
                            "Description": "If the item is instanced, it will have an instance ID. Lack of an instance ID implies that the item has no distinct local qualities aside from stack size.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "quantity": {
                            "Name": "quantity",
                            "Type": "int32",
                            "Description": "The quantity of the item in this stack. Note that Instanced items cannot stack. If an instanced item, this value will always be 1 (as the stack has exactly one item in it)",
                            "Attributes": []
                        }
                    },
                    {
                        "bindStatus": {
                            "Name": "bindStatus",
                            "Type": "int32",
                            "Description": "If the item is bound to a location, it will be specified in this enum.",
                            "Attributes": []
                        }
                    },
                    {
                        "location": {
                            "Name": "location",
                            "Type": "int32",
                            "Description": "An easy reference for where the item is located. Redundant if you got the item from an Inventory, but useful when making detail calls on specific items.",
                            "Attributes": []
                        }
                    },
                    {
                        "bucketHash": {
                            "Name": "bucketHash",
                            "Type": "uint32",
                            "Description": "The hash identifier for the specific inventory bucket in which the item is located.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "transferStatus": {
                            "Name": "transferStatus",
                            "Type": "int32",
                            "Description": "If there is a known error state that would cause this item to not be transferable, this Flags enum will indicate all of those error states. Otherwise, it will be 0 (CanTransfer).",
                            "Attributes": []
                        }
                    },
                    {
                        "lockable": {
                            "Name": "lockable",
                            "Type": "boolean",
                            "Description": "If the item can be locked, this will indicate that state.",
                            "Attributes": []
                        }
                    },
                    {
                        "state": {
                            "Name": "state",
                            "Type": "int32",
                            "Description": "A flags enumeration indicating the transient/custom states of the item that affect how it is rendered: whether it's tracked or locked for example, or whether it has a masterwork plug inserted.",
                            "Attributes": []
                        }
                    },
                    {
                        "overrideStyleItemHash": {
                            "Name": "overrideStyleItemHash",
                            "Type": "uint32",
                            "Description": "If populated, this is the hash of the item whose icon (and other secondary styles, but *not* the human readable strings) should override whatever icons/styles are on the item being sold.If you don't do this, certain items whose styles are being overridden by socketed items - such as the \"Recycle Shader\" item - would show whatever their default icon/style is, and it wouldn't be pretty or look accurate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "expirationDate": {
                            "Name": "expirationDate",
                            "Type": "date-time",
                            "Description": "If the item can expire, this is the date at which it will/did expire.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isWrapper": {
                            "Name": "isWrapper",
                            "Type": "boolean",
                            "Description": "If this is true, the object is actually a \"wrapper\" of the object it's representing. This means that it's not the actual item itself, but rather an item that must be \"opened\" in game before you have and can use the item. Wrappers are an evolution of \"bundles\", which give an easy way to let you preview the contents of what you purchased while still letting you get a refund before you \"open\" it.",
                            "Attributes": []
                        }
                    },
                    {
                        "tooltipNotificationIndexes": {
                            "Name": "tooltipNotificationIndexes",
                            "Type": "array",
                            "Description": "If this is populated, it is a list of indexes into DestinyInventoryItemDefinition.tooltipNotifications for any special tooltip messages that need to be shown for this item.",
                            "Attributes": []
                        }
                    },
                    {
                        "metricHash": {
                            "Name": "metricHash",
                            "Type": "uint32",
                            "Description": "The identifier for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "metricObjective": {
                            "Name": "metricObjective",
                            "Type": "object",
                            "Description": "The objective progress for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": []
                        }
                    },
                    {
                        "versionNumber": {
                            "Name": "versionNumber",
                            "Type": "int32",
                            "Description": "The version of this item, used to index into the versions list in the item definition quality block.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "itemValueVisibility": {
                            "Name": "itemValueVisibility",
                            "Type": "array",
                            "Description": "If available, a list that describes which item values (rewards) should be shown (true) or hidden (false).",
                            "Attributes": []
                        }
                    }
                ]
            },
            "removedInventoryItems": {
                "Name": "removedInventoryItems",
                "Type": "array",
                "Description": "Items that disappeared from the inventory possibly as a result of an action.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "itemHash": {
                            "Name": "itemHash",
                            "Type": "uint32",
                            "Description": "The identifier for the item's definition, which is where most of the useful static information for the item can be found.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "itemInstanceId": {
                            "Name": "itemInstanceId",
                            "Type": "int64",
                            "Description": "If the item is instanced, it will have an instance ID. Lack of an instance ID implies that the item has no distinct local qualities aside from stack size.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "quantity": {
                            "Name": "quantity",
                            "Type": "int32",
                            "Description": "The quantity of the item in this stack. Note that Instanced items cannot stack. If an instanced item, this value will always be 1 (as the stack has exactly one item in it)",
                            "Attributes": []
                        }
                    },
                    {
                        "bindStatus": {
                            "Name": "bindStatus",
                            "Type": "int32",
                            "Description": "If the item is bound to a location, it will be specified in this enum.",
                            "Attributes": []
                        }
                    },
                    {
                        "location": {
                            "Name": "location",
                            "Type": "int32",
                            "Description": "An easy reference for where the item is located. Redundant if you got the item from an Inventory, but useful when making detail calls on specific items.",
                            "Attributes": []
                        }
                    },
                    {
                        "bucketHash": {
                            "Name": "bucketHash",
                            "Type": "uint32",
                            "Description": "The hash identifier for the specific inventory bucket in which the item is located.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "transferStatus": {
                            "Name": "transferStatus",
                            "Type": "int32",
                            "Description": "If there is a known error state that would cause this item to not be transferable, this Flags enum will indicate all of those error states. Otherwise, it will be 0 (CanTransfer).",
                            "Attributes": []
                        }
                    },
                    {
                        "lockable": {
                            "Name": "lockable",
                            "Type": "boolean",
                            "Description": "If the item can be locked, this will indicate that state.",
                            "Attributes": []
                        }
                    },
                    {
                        "state": {
                            "Name": "state",
                            "Type": "int32",
                            "Description": "A flags enumeration indicating the transient/custom states of the item that affect how it is rendered: whether it's tracked or locked for example, or whether it has a masterwork plug inserted.",
                            "Attributes": []
                        }
                    },
                    {
                        "overrideStyleItemHash": {
                            "Name": "overrideStyleItemHash",
                            "Type": "uint32",
                            "Description": "If populated, this is the hash of the item whose icon (and other secondary styles, but *not* the human readable strings) should override whatever icons/styles are on the item being sold.If you don't do this, certain items whose styles are being overridden by socketed items - such as the \"Recycle Shader\" item - would show whatever their default icon/style is, and it wouldn't be pretty or look accurate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "expirationDate": {
                            "Name": "expirationDate",
                            "Type": "date-time",
                            "Description": "If the item can expire, this is the date at which it will/did expire.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isWrapper": {
                            "Name": "isWrapper",
                            "Type": "boolean",
                            "Description": "If this is true, the object is actually a \"wrapper\" of the object it's representing. This means that it's not the actual item itself, but rather an item that must be \"opened\" in game before you have and can use the item. Wrappers are an evolution of \"bundles\", which give an easy way to let you preview the contents of what you purchased while still letting you get a refund before you \"open\" it.",
                            "Attributes": []
                        }
                    },
                    {
                        "tooltipNotificationIndexes": {
                            "Name": "tooltipNotificationIndexes",
                            "Type": "array",
                            "Description": "If this is populated, it is a list of indexes into DestinyInventoryItemDefinition.tooltipNotifications for any special tooltip messages that need to be shown for this item.",
                            "Attributes": []
                        }
                    },
                    {
                        "metricHash": {
                            "Name": "metricHash",
                            "Type": "uint32",
                            "Description": "The identifier for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "metricObjective": {
                            "Name": "metricObjective",
                            "Type": "object",
                            "Description": "The objective progress for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": []
                        }
                    },
                    {
                        "versionNumber": {
                            "Name": "versionNumber",
                            "Type": "int32",
                            "Description": "The version of this item, used to index into the versions list in the item definition quality block.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "itemValueVisibility": {
                            "Name": "itemValueVisibility",
                            "Type": "array",
                            "Description": "If available, a list that describes which item values (rewards) should be shown (true) or hidden (false).",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-InsertSocketPlug.html#operation_post_Destiny2-InsertSocketPlug"""

        request_body = {
            "actionToken": actionToken,
            "itemInstanceId": itemInstanceId,
            "plug": plug,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing InsertSocketPlug...")
            url = self.base_url + "/Destiny2/Actions/Items/InsertSocketPlug/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def InsertSocketPlugFree(
        self, plug: dict, itemId: int, characterId: int, membershipType: int
    ) -> dict:
        """Insert a 'free' plug into an item's socket. This does not require 'Advanced Write Action' authorization and is available to 3rd-party apps, but will only work on 'free and reversible' socket actions (Perks, Armor Mods, Shaders, Ornaments, etc.). You must have a valid Destiny Account, and the character must either be in a social space, in orbit, or offline.

            Args:


            Returns:
        {
            "item": {
                "characterId": {
                    "Name": "characterId",
                    "Type": "int64",
                    "Description": "If the item is on a character, this will return the ID of the character that is holding the item.",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "item": {
                    "Name": "item",
                    "Type": "object",
                    "Description": "Common data for the item relevant to its non-instanced properties.COMPONENT TYPE: ItemCommonData",
                    "Attributes": [
                        "Depends on Component \"ItemCommonData\""
                    ]
                },
                "instance": {
                    "Name": "instance",
                    "Type": "object",
                    "Description": "Basic instance data for the item.COMPONENT TYPE: ItemInstances",
                    "Attributes": [
                        "Depends on Component \"ItemInstances\""
                    ]
                },
                "objectives": {
                    "Name": "objectives",
                    "Type": "object",
                    "Description": "Information specifically about the item's objectives.COMPONENT TYPE: ItemObjectives",
                    "Attributes": [
                        "Depends on Component \"ItemObjectives\""
                    ]
                },
                "perks": {
                    "Name": "perks",
                    "Type": "object",
                    "Description": "Information specifically about the perks currently active on the item.COMPONENT TYPE: ItemPerks",
                    "Attributes": [
                        "Depends on Component \"ItemPerks\""
                    ]
                },
                "renderData": {
                    "Name": "renderData",
                    "Type": "object",
                    "Description": "Information about how to render the item in 3D.COMPONENT TYPE: ItemRenderData",
                    "Attributes": [
                        "Depends on Component \"ItemRenderData\""
                    ]
                },
                "stats": {
                    "Name": "stats",
                    "Type": "object",
                    "Description": "Information about the computed stats of the item: power, defense, etc...COMPONENT TYPE: ItemStats",
                    "Attributes": [
                        "Depends on Component \"ItemStats\""
                    ]
                },
                "talentGrid": {
                    "Name": "talentGrid",
                    "Type": "object",
                    "Description": "Information about the talent grid attached to the item. Talent nodes can provide a variety of benefits and abilities, and in Destiny 2 are used almost exclusively for the character's \"Builds\".COMPONENT TYPE: ItemTalentGrids",
                    "Attributes": [
                        "Depends on Component \"ItemTalentGrids\""
                    ]
                },
                "sockets": {
                    "Name": "sockets",
                    "Type": "object",
                    "Description": "Information about the sockets of the item: which are currently active, what potential sockets you could have and the stats/abilities/perks you can gain from them.COMPONENT TYPE: ItemSockets",
                    "Attributes": [
                        "Depends on Component \"ItemSockets\""
                    ]
                },
                "reusablePlugs": {
                    "Name": "reusablePlugs",
                    "Type": "object",
                    "Description": "Information about the Reusable Plugs for sockets on an item. These are plugs that you can insert into the given socket regardless of if you actually own an instance of that plug: they are logic-driven plugs rather than inventory-driven. These may need to be combined with Plug Set component data to get a full picture of available plugs on a given socket. COMPONENT TYPE: ItemReusablePlugs",
                    "Attributes": [
                        "Depends on Component \"ItemReusablePlugs\""
                    ]
                },
                "plugObjectives": {
                    "Name": "plugObjectives",
                    "Type": "object",
                    "Description": "Information about objectives on Plugs for a given item. See the component's documentation for more info.COMPONENT TYPE: ItemPlugObjectives",
                    "Attributes": [
                        "Depends on Component \"ItemPlugObjectives\""
                    ]
                }
            },
            "addedInventoryItems": {
                "Name": "addedInventoryItems",
                "Type": "array",
                "Description": "Items that appeared in the inventory possibly as a result of an action.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "itemHash": {
                            "Name": "itemHash",
                            "Type": "uint32",
                            "Description": "The identifier for the item's definition, which is where most of the useful static information for the item can be found.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "itemInstanceId": {
                            "Name": "itemInstanceId",
                            "Type": "int64",
                            "Description": "If the item is instanced, it will have an instance ID. Lack of an instance ID implies that the item has no distinct local qualities aside from stack size.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "quantity": {
                            "Name": "quantity",
                            "Type": "int32",
                            "Description": "The quantity of the item in this stack. Note that Instanced items cannot stack. If an instanced item, this value will always be 1 (as the stack has exactly one item in it)",
                            "Attributes": []
                        }
                    },
                    {
                        "bindStatus": {
                            "Name": "bindStatus",
                            "Type": "int32",
                            "Description": "If the item is bound to a location, it will be specified in this enum.",
                            "Attributes": []
                        }
                    },
                    {
                        "location": {
                            "Name": "location",
                            "Type": "int32",
                            "Description": "An easy reference for where the item is located. Redundant if you got the item from an Inventory, but useful when making detail calls on specific items.",
                            "Attributes": []
                        }
                    },
                    {
                        "bucketHash": {
                            "Name": "bucketHash",
                            "Type": "uint32",
                            "Description": "The hash identifier for the specific inventory bucket in which the item is located.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "transferStatus": {
                            "Name": "transferStatus",
                            "Type": "int32",
                            "Description": "If there is a known error state that would cause this item to not be transferable, this Flags enum will indicate all of those error states. Otherwise, it will be 0 (CanTransfer).",
                            "Attributes": []
                        }
                    },
                    {
                        "lockable": {
                            "Name": "lockable",
                            "Type": "boolean",
                            "Description": "If the item can be locked, this will indicate that state.",
                            "Attributes": []
                        }
                    },
                    {
                        "state": {
                            "Name": "state",
                            "Type": "int32",
                            "Description": "A flags enumeration indicating the transient/custom states of the item that affect how it is rendered: whether it's tracked or locked for example, or whether it has a masterwork plug inserted.",
                            "Attributes": []
                        }
                    },
                    {
                        "overrideStyleItemHash": {
                            "Name": "overrideStyleItemHash",
                            "Type": "uint32",
                            "Description": "If populated, this is the hash of the item whose icon (and other secondary styles, but *not* the human readable strings) should override whatever icons/styles are on the item being sold.If you don't do this, certain items whose styles are being overridden by socketed items - such as the \"Recycle Shader\" item - would show whatever their default icon/style is, and it wouldn't be pretty or look accurate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "expirationDate": {
                            "Name": "expirationDate",
                            "Type": "date-time",
                            "Description": "If the item can expire, this is the date at which it will/did expire.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isWrapper": {
                            "Name": "isWrapper",
                            "Type": "boolean",
                            "Description": "If this is true, the object is actually a \"wrapper\" of the object it's representing. This means that it's not the actual item itself, but rather an item that must be \"opened\" in game before you have and can use the item. Wrappers are an evolution of \"bundles\", which give an easy way to let you preview the contents of what you purchased while still letting you get a refund before you \"open\" it.",
                            "Attributes": []
                        }
                    },
                    {
                        "tooltipNotificationIndexes": {
                            "Name": "tooltipNotificationIndexes",
                            "Type": "array",
                            "Description": "If this is populated, it is a list of indexes into DestinyInventoryItemDefinition.tooltipNotifications for any special tooltip messages that need to be shown for this item.",
                            "Attributes": []
                        }
                    },
                    {
                        "metricHash": {
                            "Name": "metricHash",
                            "Type": "uint32",
                            "Description": "The identifier for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "metricObjective": {
                            "Name": "metricObjective",
                            "Type": "object",
                            "Description": "The objective progress for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": []
                        }
                    },
                    {
                        "versionNumber": {
                            "Name": "versionNumber",
                            "Type": "int32",
                            "Description": "The version of this item, used to index into the versions list in the item definition quality block.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "itemValueVisibility": {
                            "Name": "itemValueVisibility",
                            "Type": "array",
                            "Description": "If available, a list that describes which item values (rewards) should be shown (true) or hidden (false).",
                            "Attributes": []
                        }
                    }
                ]
            },
            "removedInventoryItems": {
                "Name": "removedInventoryItems",
                "Type": "array",
                "Description": "Items that disappeared from the inventory possibly as a result of an action.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "itemHash": {
                            "Name": "itemHash",
                            "Type": "uint32",
                            "Description": "The identifier for the item's definition, which is where most of the useful static information for the item can be found.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "itemInstanceId": {
                            "Name": "itemInstanceId",
                            "Type": "int64",
                            "Description": "If the item is instanced, it will have an instance ID. Lack of an instance ID implies that the item has no distinct local qualities aside from stack size.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "quantity": {
                            "Name": "quantity",
                            "Type": "int32",
                            "Description": "The quantity of the item in this stack. Note that Instanced items cannot stack. If an instanced item, this value will always be 1 (as the stack has exactly one item in it)",
                            "Attributes": []
                        }
                    },
                    {
                        "bindStatus": {
                            "Name": "bindStatus",
                            "Type": "int32",
                            "Description": "If the item is bound to a location, it will be specified in this enum.",
                            "Attributes": []
                        }
                    },
                    {
                        "location": {
                            "Name": "location",
                            "Type": "int32",
                            "Description": "An easy reference for where the item is located. Redundant if you got the item from an Inventory, but useful when making detail calls on specific items.",
                            "Attributes": []
                        }
                    },
                    {
                        "bucketHash": {
                            "Name": "bucketHash",
                            "Type": "uint32",
                            "Description": "The hash identifier for the specific inventory bucket in which the item is located.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "transferStatus": {
                            "Name": "transferStatus",
                            "Type": "int32",
                            "Description": "If there is a known error state that would cause this item to not be transferable, this Flags enum will indicate all of those error states. Otherwise, it will be 0 (CanTransfer).",
                            "Attributes": []
                        }
                    },
                    {
                        "lockable": {
                            "Name": "lockable",
                            "Type": "boolean",
                            "Description": "If the item can be locked, this will indicate that state.",
                            "Attributes": []
                        }
                    },
                    {
                        "state": {
                            "Name": "state",
                            "Type": "int32",
                            "Description": "A flags enumeration indicating the transient/custom states of the item that affect how it is rendered: whether it's tracked or locked for example, or whether it has a masterwork plug inserted.",
                            "Attributes": []
                        }
                    },
                    {
                        "overrideStyleItemHash": {
                            "Name": "overrideStyleItemHash",
                            "Type": "uint32",
                            "Description": "If populated, this is the hash of the item whose icon (and other secondary styles, but *not* the human readable strings) should override whatever icons/styles are on the item being sold.If you don't do this, certain items whose styles are being overridden by socketed items - such as the \"Recycle Shader\" item - would show whatever their default icon/style is, and it wouldn't be pretty or look accurate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "expirationDate": {
                            "Name": "expirationDate",
                            "Type": "date-time",
                            "Description": "If the item can expire, this is the date at which it will/did expire.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isWrapper": {
                            "Name": "isWrapper",
                            "Type": "boolean",
                            "Description": "If this is true, the object is actually a \"wrapper\" of the object it's representing. This means that it's not the actual item itself, but rather an item that must be \"opened\" in game before you have and can use the item. Wrappers are an evolution of \"bundles\", which give an easy way to let you preview the contents of what you purchased while still letting you get a refund before you \"open\" it.",
                            "Attributes": []
                        }
                    },
                    {
                        "tooltipNotificationIndexes": {
                            "Name": "tooltipNotificationIndexes",
                            "Type": "array",
                            "Description": "If this is populated, it is a list of indexes into DestinyInventoryItemDefinition.tooltipNotifications for any special tooltip messages that need to be shown for this item.",
                            "Attributes": []
                        }
                    },
                    {
                        "metricHash": {
                            "Name": "metricHash",
                            "Type": "uint32",
                            "Description": "The identifier for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "metricObjective": {
                            "Name": "metricObjective",
                            "Type": "object",
                            "Description": "The objective progress for the currently-selected metric definition, to be displayed on the emblem nameplate.",
                            "Attributes": []
                        }
                    },
                    {
                        "versionNumber": {
                            "Name": "versionNumber",
                            "Type": "int32",
                            "Description": "The version of this item, used to index into the versions list in the item definition quality block.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "itemValueVisibility": {
                            "Name": "itemValueVisibility",
                            "Type": "array",
                            "Description": "If available, a list that describes which item values (rewards) should be shown (true) or hidden (false).",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-InsertSocketPlugFree.html#operation_post_Destiny2-InsertSocketPlugFree"""

        request_body = {
            "plug": plug,
            "itemId": itemId,
            "characterId": characterId,
            "membershipType": membershipType,
        }

        try:
            self.logger.info("Executing InsertSocketPlugFree...")
            url = (
                self.base_url + "/Destiny2/Actions/Items/InsertSocketPlugFree/".format()
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostGameCarnageReport(
        self,
        activityId: int,
    ) -> dict:
        """Gets the available post game carnage report for the activity ID.

            Args:
                activityId (int): The ID of the activity whose PGCR is requested.

            Returns:
        {
            "period": {
                "Name": "period",
                "Type": "date-time",
                "Description": "Date and time for the activity.",
                "Attributes": []
            },
            "startingPhaseIndex": {
                "Name": "startingPhaseIndex",
                "Type": "int32",
                "Description": "If this activity has \"phases\", this is the phase at which the activity was started. This value is only valid for activities before the Beyond Light expansion shipped. Subsequent activities will not have a valid value here.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "activityWasStartedFromBeginning": {
                "Name": "activityWasStartedFromBeginning",
                "Type": "boolean",
                "Description": "True if the activity was started from the beginning, if that information is available and the activity was played post Witch Queen release.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "activityDetails": {
                "Name": "activityDetails",
                "Type": "object",
                "Description": "Details about the activity.",
                "Attributes": []
            },
            "entries": {
                "Name": "entries",
                "Type": "array",
                "Description": "Collection of players and their data for this activity.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "standing": {
                            "Name": "standing",
                            "Type": "int32",
                            "Description": "Standing of the player",
                            "Attributes": []
                        }
                    },
                    {
                        "score": {
                            "Name": "score",
                            "Type": "object",
                            "Description": "Score of the player if available",
                            "Attributes": []
                        }
                    },
                    {
                        "player": {
                            "Name": "player",
                            "Type": "object",
                            "Description": "Identity details of the player",
                            "Attributes": []
                        }
                    },
                    {
                        "characterId": {
                            "Name": "characterId",
                            "Type": "int64",
                            "Description": "ID of the player's character used in the activity.",
                            "Attributes": []
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the player in this activity.",
                            "Attributes": []
                        }
                    },
                    {
                        "extended": {
                            "Name": "extended",
                            "Type": "object",
                            "Description": "Extended data extracted from the activity blob.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "teams": {
                "Name": "teams",
                "Type": "array",
                "Description": "Collection of stats for the player in this activity.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "teamId": {
                            "Name": "teamId",
                            "Type": "int32",
                            "Description": "Integer ID for the team.",
                            "Attributes": []
                        }
                    },
                    {
                        "standing": {
                            "Name": "standing",
                            "Type": "object",
                            "Description": "Team's standing relative to other teams.",
                            "Attributes": []
                        }
                    },
                    {
                        "score": {
                            "Name": "score",
                            "Type": "object",
                            "Description": "Score earned by the team",
                            "Attributes": []
                        }
                    },
                    {
                        "teamName": {
                            "Name": "teamName",
                            "Type": "string",
                            "Description": "Alpha or Bravo",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetPostGameCarnageReport.html#operation_get_Destiny2-GetPostGameCarnageReport"""

        try:
            self.logger.info("Executing GetPostGameCarnageReport...")
            url = (
                self.base_url
                + f"/Destiny2/Stats/PostGameCarnageReport/{activityId}/".format(
                    activityId=activityId
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def ReportOffensivePostGameCarnageReportPlayer(
        self,
        activityId: int,
        reasonCategoryHashes: list,
        reasonHashes: list,
        offendingCharacterId: int,
    ) -> dict:
        """Report a player that you met in an activity that was engaging in ToS-violating activities. Both you and the offending player must have played in the activityId passed in. Please use this judiciously and only when you have strong suspicions of violation, pretty please.

            Args:
                activityId (int): The ID of the activity where you ran into the brigand that you're reporting.

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-ReportOffensivePostGameCarnageReportPlayer.html#operation_post_Destiny2-ReportOffensivePostGameCarnageReportPlayer"""

        request_body = {
            "reasonCategoryHashes": reasonCategoryHashes,
            "reasonHashes": reasonHashes,
            "offendingCharacterId": offendingCharacterId,
        }

        try:
            self.logger.info("Executing ReportOffensivePostGameCarnageReportPlayer...")
            url = (
                self.base_url
                + f"/Destiny2/Stats/PostGameCarnageReport/{activityId}/Report/".format(
                    activityId=activityId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStatsDefinition(
        self,
    ) -> dict:
        """Gets historical stats definitions.

            Args:


            Returns:
        {
            "statId": {
                "Name": "statId",
                "Type": "string",
                "Description": "Unique programmer friendly ID for this stat",
                "Attributes": []
            },
            "group": {
                "Name": "group",
                "Type": "int32",
                "Description": "Statistic group",
                "Attributes": []
            },
            "periodTypes": {
                "Name": "periodTypes",
                "Type": "array",
                "Description": "Time periods the statistic covers",
                "Attributes": [],
                "Array Contents": "int32"
            },
            "modes": {
                "Name": "modes",
                "Type": "array",
                "Description": "Game modes where this statistic can be reported.",
                "Attributes": [],
                "Array Contents": "int32"
            },
            "category": {
                "Name": "category",
                "Type": "int32",
                "Description": "Category for the stat.",
                "Attributes": []
            },
            "statName": {
                "Name": "statName",
                "Type": "string",
                "Description": "Display name",
                "Attributes": []
            },
            "statNameAbbr": {
                "Name": "statNameAbbr",
                "Type": "string",
                "Description": "Display name abbreviated",
                "Attributes": []
            },
            "statDescription": {
                "Name": "statDescription",
                "Type": "string",
                "Description": "Description of a stat if applicable.",
                "Attributes": []
            },
            "unitType": {
                "Name": "unitType",
                "Type": "int32",
                "Description": "Unit, if any, for the statistic",
                "Attributes": []
            },
            "iconImage": {
                "Name": "iconImage",
                "Type": "string",
                "Description": "Optional URI to an icon for the statistic",
                "Attributes": []
            },
            "mergeMethod": {
                "Name": "mergeMethod",
                "Type": "int32",
                "Description": "Optional icon for the statistic",
                "Attributes": [
                    "Nullable",
                    "Enumeration"
                ]
            },
            "unitLabel": {
                "Name": "unitLabel",
                "Type": "string",
                "Description": "Localized Unit Name for the stat.",
                "Attributes": []
            },
            "weight": {
                "Name": "weight",
                "Type": "int32",
                "Description": "Weight assigned to this stat indicating its relative impressiveness.",
                "Attributes": []
            },
            "medalTierHash": {
                "Name": "medalTierHash",
                "Type": "uint32",
                "Description": "The tier associated with this medal - be it implicitly or explicitly.",
                "Attributes": [
                    "Nullable",
                    "Mapped to Definition"
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetHistoricalStatsDefinition.html#operation_get_Destiny2-GetHistoricalStatsDefinition"""

        try:
            self.logger.info("Executing GetHistoricalStatsDefinition...")
            url = self.base_url + "/Destiny2/Stats/Definition/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanLeaderboards(
        self,
        groupId: int,
        maxtop: int,
        modes: str,
        statid: str,
    ) -> dict:
        """Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation.

            Args:
                groupId (int): Group ID of the clan whose leaderboards you wish to fetch.
                maxtop (int): Maximum number of top players to return. Use a large number to get entire leaderboard.
                modes (str): List of game modes for which to get leaderboards. See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
                statid (str): ID of stat to return rather than returning all Leaderboard stats.

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetClanLeaderboards.html#operation_get_Destiny2-GetClanLeaderboards"""

        try:
            self.logger.info("Executing GetClanLeaderboards...")
            url = (
                self.base_url
                + f"/Destiny2/Stats/Leaderboards/Clans/{groupId}/".format(
                    groupId=groupId, maxtop=maxtop, modes=modes, statid=statid
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanAggregateStats(
        self,
        groupId: int,
        modes: str,
    ) -> dict:
        """Gets aggregated stats for a clan using the same categories as the clan leaderboards. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation.

            Args:
                groupId (int): Group ID of the clan whose leaderboards you wish to fetch.
                modes (str): List of game modes for which to get leaderboards. See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.

            Returns:
        {
            "mode": {
                "Name": "mode",
                "Type": "int32",
                "Description": "The id of the mode of stats (allPvp, allPvE, etc)",
                "Attributes": []
            },
            "statId": {
                "Name": "statId",
                "Type": "string",
                "Description": "The id of the stat",
                "Attributes": []
            },
            "value": {
                "Name": "value",
                "Type": "object",
                "Description": "Value of the stat for this player",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetClanAggregateStats.html#operation_get_Destiny2-GetClanAggregateStats"""

        try:
            self.logger.info("Executing GetClanAggregateStats...")
            url = (
                self.base_url
                + f"/Destiny2/Stats/AggregateClanStats/{groupId}/".format(
                    groupId=groupId, modes=modes
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLeaderboards(
        self,
        destinyMembershipId: int,
        membershipType: int,
        maxtop: int,
        modes: str,
        statid: str,
    ) -> dict:
        """Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint has not yet been implemented. It is being returned for a preview of future functionality, and for public comment/suggestion/preparation.

            Args:
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.
                maxtop (int): Maximum number of top players to return. Use a large number to get entire leaderboard.
                modes (str): List of game modes for which to get leaderboards. See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
                statid (str): ID of stat to return rather than returning all Leaderboard stats.

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetLeaderboards.html#operation_get_Destiny2-GetLeaderboards"""

        try:
            self.logger.info("Executing GetLeaderboards...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/Leaderboards/".format(
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    maxtop=maxtop,
                    modes=modes,
                    statid=statid,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLeaderboardsForCharacter(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        maxtop: int,
        modes: str,
        statid: str,
    ) -> dict:
        """Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation.

            Args:
                characterId (int): The specific character to build the leaderboard around for the provided Destiny Membership.
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.
                maxtop (int): Maximum number of top players to return. Use a large number to get entire leaderboard.
                modes (str): List of game modes for which to get leaderboards. See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
                statid (str): ID of stat to return rather than returning all Leaderboard stats.

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetLeaderboardsForCharacter.html#operation_get_Destiny2-GetLeaderboardsForCharacter"""

        try:
            self.logger.info("Executing GetLeaderboardsForCharacter...")
            url = (
                self.base_url
                + f"/Destiny2/Stats/Leaderboards/{membershipType}/{destinyMembershipId}/{characterId}/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    maxtop=maxtop,
                    modes=modes,
                    statid=statid,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchDestinyEntities(
        self,
        searchTerm: str,
        type: str,
        page: int,
    ) -> dict:
        """Gets a page list of Destiny items.

            Args:
                searchTerm (str): The string to use when searching for Destiny entities.
                type (str): The type of entity for whom you would like results. These correspond to the entity's definition contract name. For instance, if you are looking for items, this property should be 'DestinyInventoryItemDefinition'.
                page (int): Page number to return, starting with 0.

            Returns:
        {
            "suggestedWords": {
                "Name": "suggestedWords",
                "Type": "array",
                "Description": "A list of suggested words that might make for better search results, based on the text searched for.",
                "Attributes": [],
                "Array Contents": "string"
            },
            "results": {
                "Name": "results",
                "Type": "object",
                "Description": "The items found that are matches/near matches for the searched-for term, sorted by something vaguely resembling \"relevance\". Hopefully this will get better in the future.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-SearchDestinyEntities.html#operation_get_Destiny2-SearchDestinyEntities"""

        try:
            self.logger.info("Executing SearchDestinyEntities...")
            url = (
                self.base_url
                + f"/Destiny2/Armory/Search/{type}/{searchTerm}/".format(
                    searchTerm=searchTerm, type=type, page=page
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStats(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        dayend: datetime,
        daystart: datetime,
        groups: list,
        modes: list,
        periodType: int,
    ) -> dict:
        """Gets historical stats for indicated character.

            Args:
                characterId (int): The id of the character to retrieve. You can omit this character ID or set it to 0 to get aggregate stats across all characters.
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.
                dayend (datetime): Last day to return when daily stats are requested. Use the format YYYY-MM-DD. Currently, we cannot allow more than 31 days of daily data to be requested in a single request.
                daystart (datetime): First day to return when daily stats are requested. Use the format YYYY-MM-DD. Currently, we cannot allow more than 31 days of daily data to be requested in a single request.
                groups (list): Group of stats to include, otherwise only general stats are returned. Comma separated list is allowed. Values: General, Weapons, Medals
                modes (list): Game modes to return. See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
                periodType (int): Indicates a specific period type to return. Optional. May be: Daily, AllTime, or Activity

            Returns:
        {
            "allTime": {
                "Name": "allTime",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "allTimeTier1": {
                "Name": "allTimeTier1",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "allTimeTier2": {
                "Name": "allTimeTier2",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "allTimeTier3": {
                "Name": "allTimeTier3",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "daily": {
                "Name": "daily",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "period": {
                            "Name": "period",
                            "Type": "date-time",
                            "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                            "Attributes": []
                        }
                    },
                    {
                        "activityDetails": {
                            "Name": "activityDetails",
                            "Type": "object",
                            "Description": "If the period group is for a specific activity, this property will be set.",
                            "Attributes": []
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the period.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "monthly": {
                "Name": "monthly",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "period": {
                            "Name": "period",
                            "Type": "date-time",
                            "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                            "Attributes": []
                        }
                    },
                    {
                        "activityDetails": {
                            "Name": "activityDetails",
                            "Type": "object",
                            "Description": "If the period group is for a specific activity, this property will be set.",
                            "Attributes": []
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the period.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetHistoricalStats.html#operation_get_Destiny2-GetHistoricalStats"""

        try:
            self.logger.info("Executing GetHistoricalStats...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    dayend=dayend,
                    daystart=daystart,
                    groups=groups,
                    modes=modes,
                    periodType=periodType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStatsForAccount(
        self,
        destinyMembershipId: int,
        membershipType: int,
        groups: list,
    ) -> dict:
        """Gets aggregate historical stats organized around each character for a given account.

            Args:
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.
                groups (list): Groups of stats to include, otherwise only general stats are returned. Comma separated list is allowed. Values: General, Weapons, Medals.

            Returns:
        {
            "mergedDeletedCharacters": {
                "results": {
                    "Name": "results",
                    "Type": "object",
                    "Description": "",
                    "Attributes": []
                },
                "merged": {
                    "allTime": {
                        "Name": "allTime",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier1": {
                        "Name": "allTimeTier1",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier2": {
                        "Name": "allTimeTier2",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier3": {
                        "Name": "allTimeTier3",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "daily": {
                        "Name": "daily",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "period": {
                                    "Name": "period",
                                    "Type": "date-time",
                                    "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                    "Attributes": []
                                }
                            },
                            {
                                "activityDetails": {
                                    "Name": "activityDetails",
                                    "Type": "object",
                                    "Description": "If the period group is for a specific activity, this property will be set.",
                                    "Attributes": []
                                }
                            },
                            {
                                "values": {
                                    "Name": "values",
                                    "Type": "object",
                                    "Description": "Collection of stats for the period.",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "monthly": {
                        "Name": "monthly",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "period": {
                                    "Name": "period",
                                    "Type": "date-time",
                                    "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                    "Attributes": []
                                }
                            },
                            {
                                "activityDetails": {
                                    "Name": "activityDetails",
                                    "Type": "object",
                                    "Description": "If the period group is for a specific activity, this property will be set.",
                                    "Attributes": []
                                }
                            },
                            {
                                "values": {
                                    "Name": "values",
                                    "Type": "object",
                                    "Description": "Collection of stats for the period.",
                                    "Attributes": []
                                }
                            }
                        ]
                    }
                }
            },
            "mergedAllCharacters": {
                "results": {
                    "Name": "results",
                    "Type": "object",
                    "Description": "",
                    "Attributes": []
                },
                "merged": {
                    "allTime": {
                        "Name": "allTime",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier1": {
                        "Name": "allTimeTier1",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier2": {
                        "Name": "allTimeTier2",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "allTimeTier3": {
                        "Name": "allTimeTier3",
                        "Type": "object",
                        "Description": "",
                        "Attributes": []
                    },
                    "daily": {
                        "Name": "daily",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "period": {
                                    "Name": "period",
                                    "Type": "date-time",
                                    "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                    "Attributes": []
                                }
                            },
                            {
                                "activityDetails": {
                                    "Name": "activityDetails",
                                    "Type": "object",
                                    "Description": "If the period group is for a specific activity, this property will be set.",
                                    "Attributes": []
                                }
                            },
                            {
                                "values": {
                                    "Name": "values",
                                    "Type": "object",
                                    "Description": "Collection of stats for the period.",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "monthly": {
                        "Name": "monthly",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "period": {
                                    "Name": "period",
                                    "Type": "date-time",
                                    "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                    "Attributes": []
                                }
                            },
                            {
                                "activityDetails": {
                                    "Name": "activityDetails",
                                    "Type": "object",
                                    "Description": "If the period group is for a specific activity, this property will be set.",
                                    "Attributes": []
                                }
                            },
                            {
                                "values": {
                                    "Name": "values",
                                    "Type": "object",
                                    "Description": "Collection of stats for the period.",
                                    "Attributes": []
                                }
                            }
                        ]
                    }
                }
            },
            "characters": {
                "Name": "characters",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "characterId": {
                            "Name": "characterId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "deleted": {
                            "Name": "deleted",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "results": {
                            "Name": "results",
                            "Type": "object",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "merged": {
                            "allTime": {
                                "Name": "allTime",
                                "Type": "object",
                                "Description": "",
                                "Attributes": []
                            },
                            "allTimeTier1": {
                                "Name": "allTimeTier1",
                                "Type": "object",
                                "Description": "",
                                "Attributes": []
                            },
                            "allTimeTier2": {
                                "Name": "allTimeTier2",
                                "Type": "object",
                                "Description": "",
                                "Attributes": []
                            },
                            "allTimeTier3": {
                                "Name": "allTimeTier3",
                                "Type": "object",
                                "Description": "",
                                "Attributes": []
                            },
                            "daily": {
                                "Name": "daily",
                                "Type": "array",
                                "Description": "",
                                "Attributes": [],
                                "Array Contents": [
                                    {
                                        "period": {
                                            "Name": "period",
                                            "Type": "date-time",
                                            "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "activityDetails": {
                                            "Name": "activityDetails",
                                            "Type": "object",
                                            "Description": "If the period group is for a specific activity, this property will be set.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "values": {
                                            "Name": "values",
                                            "Type": "object",
                                            "Description": "Collection of stats for the period.",
                                            "Attributes": []
                                        }
                                    }
                                ]
                            },
                            "monthly": {
                                "Name": "monthly",
                                "Type": "array",
                                "Description": "",
                                "Attributes": [],
                                "Array Contents": [
                                    {
                                        "period": {
                                            "Name": "period",
                                            "Type": "date-time",
                                            "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "activityDetails": {
                                            "Name": "activityDetails",
                                            "Type": "object",
                                            "Description": "If the period group is for a specific activity, this property will be set.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "values": {
                                            "Name": "values",
                                            "Type": "object",
                                            "Description": "Collection of stats for the period.",
                                            "Attributes": []
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetHistoricalStatsForAccount.html#operation_get_Destiny2-GetHistoricalStatsForAccount"""

        try:
            self.logger.info("Executing GetHistoricalStatsForAccount...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/".format(
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    groups=groups,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetActivityHistory(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
        count: int,
        mode: int,
        page: int,
    ) -> dict:
        """Gets activity history stats for indicated character.

            Args:
                characterId (int): The id of the character to retrieve.
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.
                count (int): Number of rows to return
                mode (int): A filter for the activity mode to be returned. None returns all activities. See the documentation for DestinyActivityModeType for valid values, and pass in string representation.
                page (int): Page number to return, starting with 0.

            Returns:
        {
            "activities": {
                "Name": "activities",
                "Type": "array",
                "Description": "List of activities, the most recent activity first.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "period": {
                            "Name": "period",
                            "Type": "date-time",
                            "Description": "Period for the group. If the stat periodType is day, then this will have a specific day. If the type is monthly, then this value will be the first day of the applicable month. This value is not set when the periodType is 'all time'.",
                            "Attributes": []
                        }
                    },
                    {
                        "activityDetails": {
                            "Name": "activityDetails",
                            "Type": "object",
                            "Description": "If the period group is for a specific activity, this property will be set.",
                            "Attributes": []
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the period.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetActivityHistory.html#operation_get_Destiny2-GetActivityHistory"""

        try:
            self.logger.info("Executing GetActivityHistory...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                    count=count,
                    mode=mode,
                    page=page,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetUniqueWeaponHistory(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
    ) -> dict:
        """Gets details about unique weapon usage, including all exotic weapons.

            Args:
                characterId (int): The id of the character to retrieve.
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.

            Returns:
        {
            "weapons": {
                "Name": "weapons",
                "Type": "array",
                "Description": "List of weapons and their perspective values.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "referenceId": {
                            "Name": "referenceId",
                            "Type": "uint32",
                            "Description": "The hash ID of the item definition that describes the weapon.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the period.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetUniqueWeaponHistory.html#operation_get_Destiny2-GetUniqueWeaponHistory"""

        try:
            self.logger.info("Executing GetUniqueWeaponHistory...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/UniqueWeapons/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetDestinyAggregateActivityStats(
        self,
        characterId: int,
        destinyMembershipId: int,
        membershipType: int,
    ) -> dict:
        """Gets all activities the character has participated in together with aggregate statistics for those activities.

            Args:
                characterId (int): The specific character whose activities should be returned.
                destinyMembershipId (int): The Destiny membershipId of the user to retrieve.
                membershipType (int): A valid non-BungieNet membership type.

            Returns:
        {
            "activities": {
                "Name": "activities",
                "Type": "array",
                "Description": "List of all activities the player has participated in.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "activityHash": {
                            "Name": "activityHash",
                            "Type": "uint32",
                            "Description": "Hash ID that can be looked up in the DestinyActivityTable.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "values": {
                            "Name": "values",
                            "Type": "object",
                            "Description": "Collection of stats for the player in this activity.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetDestinyAggregateActivityStats.html#operation_get_Destiny2-GetDestinyAggregateActivityStats"""

        try:
            self.logger.info("Executing GetDestinyAggregateActivityStats...")
            url = (
                self.base_url
                + f"/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/AggregateActivityStats/".format(
                    characterId=characterId,
                    destinyMembershipId=destinyMembershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicMilestoneContent(
        self,
        milestoneHash: int,
    ) -> dict:
        """Gets custom localized content for the milestone of the given hash, if it exists.

            Args:
                milestoneHash (int): The identifier for the milestone to be returned.

            Returns:
        {
            "about": {
                "Name": "about",
                "Type": "string",
                "Description": "The \"About this Milestone\" text from the Firehose.",
                "Attributes": []
            },
            "status": {
                "Name": "status",
                "Type": "string",
                "Description": "The Current Status of the Milestone, as driven by the Firehose.",
                "Attributes": []
            },
            "tips": {
                "Name": "tips",
                "Type": "array",
                "Description": "A list of tips, provided by the Firehose.",
                "Attributes": [],
                "Array Contents": "string"
            },
            "itemCategories": {
                "Name": "itemCategories",
                "Type": "array",
                "Description": "If DPS has defined items related to this Milestone, they can categorize those items in the Firehose. That data will then be returned as item categories here.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "title": {
                            "Name": "title",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "itemHashes": {
                            "Name": "itemHashes",
                            "Type": "array",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetPublicMilestoneContent.html#operation_get_Destiny2-GetPublicMilestoneContent"""

        try:
            self.logger.info("Executing GetPublicMilestoneContent...")
            url = (
                self.base_url
                + f"/Destiny2/Milestones/{milestoneHash}/Content/".format(
                    milestoneHash=milestoneHash
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicMilestones(
        self,
    ) -> dict:
        """Gets public information about currently available Milestones.

            Args:


            Returns:
        {
            "milestoneHash": {
                "Name": "milestoneHash",
                "Type": "uint32",
                "Description": "The hash identifier for the milestone. Use it to look up the DestinyMilestoneDefinition for static data about the Milestone.",
                "Attributes": [
                    "Mapped to Definition"
                ]
            },
            "availableQuests": {
                "Name": "availableQuests",
                "Type": "array",
                "Description": "A milestone not need have even a single quest, but if there are active quests they will be returned here.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "questItemHash": {
                            "Name": "questItemHash",
                            "Type": "uint32",
                            "Description": "Quests are defined as Items in content. As such, this is the hash identifier of the DestinyInventoryItemDefinition that represents this quest. It will have pointers to all of the steps in the quest, and display information for the quest (title, description, icon etc) Individual steps will be referred to in the Quest item's DestinyInventoryItemDefinition.setData property, and themselves are Items with their own renderable data.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "activity": {
                            "Name": "activity",
                            "Type": "object",
                            "Description": "A milestone need not have an active activity, but if there is one it will be returned here, along with any variant and additional information.",
                            "Attributes": []
                        }
                    },
                    {
                        "challenges": {
                            "Name": "challenges",
                            "Type": "array",
                            "Description": "For the given quest there could be 0-to-Many challenges: mini quests that you can perform in the course of doing this quest, that may grant you rewards and benefits.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "activities": {
                "Name": "activities",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "activityHash": {
                            "Name": "activityHash",
                            "Type": "uint32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "challengeObjectiveHashes": {
                            "Name": "challengeObjectiveHashes",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "modifierHashes": {
                            "Name": "modifierHashes",
                            "Type": "array",
                            "Description": "If the activity has modifiers, this will be the list of modifiers that all variants have in common. Perform lookups against DestinyActivityModifierDefinition which defines the modifier being applied to get at the modifier data.Note that, in the DestiyActivityDefinition, you will see many more modifiers than this being referred to: those are all *possible* modifiers for the activity, not the active ones. Use only the active ones to match what's really live.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "loadoutRequirementIndex": {
                            "Name": "loadoutRequirementIndex",
                            "Type": "int32",
                            "Description": "If returned, this is the index into the DestinyActivityDefinition's \"loadouts\" property, indicating the currently active loadout requirements.",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "phaseHashes": {
                            "Name": "phaseHashes",
                            "Type": "array",
                            "Description": "The ordered list of phases for this activity, if any. Note that we have no human readable info for phases, nor any entities to relate them to: relating these hashes to something human readable is up to you unfortunately.",
                            "Attributes": []
                        }
                    },
                    {
                        "booleanActivityOptions": {
                            "Name": "booleanActivityOptions",
                            "Type": "object",
                            "Description": "The set of activity options for this activity, keyed by an identifier that's unique for this activity (not guaranteed to be unique between or across all activities, though should be unique for every *variant* of a given *conceptual* activity: for instance, the original D2 Raid has many variant DestinyActivityDefinitions. While other activities could potentially have the same option hashes, for any given D2 base Raid variant the hash will be unique).As a concrete example of this data, the hashes you get for Raids will correspond to the currently active \"Challenge Mode\".We have no human readable information for this data, so it's up to you if you want to associate it with such info to show it.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "vendorHashes": {
                "Name": "vendorHashes",
                "Type": "array",
                "Description": "Sometimes milestones - or activities active in milestones - will have relevant vendors. These are the vendors that are currently relevant.Deprecated, already, for the sake of the new \"vendors\" property that has more data. What was I thinking.",
                "Attributes": [],
                "Array Contents": "uint32"
            },
            "vendors": {
                "Name": "vendors",
                "Type": "array",
                "Description": "This is why we can't have nice things. This is the ordered list of vendors to be shown that relate to this milestone, potentially along with other interesting data.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "vendorHash": {
                            "Name": "vendorHash",
                            "Type": "uint32",
                            "Description": "The hash identifier of the Vendor related to this Milestone. You can show useful things from this, such as thier Faction icon or whatever you might care about.",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "previewItemHash": {
                            "Name": "previewItemHash",
                            "Type": "uint32",
                            "Description": "If this vendor is featuring a specific item for this event, this will be the hash identifier of that item. I'm taking bets now on how long we go before this needs to be a list or some other, more complex representation instead and I deprecate this too. I'm going to go with 5 months. Calling it now, 2017-09-14 at 9:46pm PST.",
                            "Attributes": [
                                "Nullable",
                                "Mapped to Definition"
                            ]
                        }
                    }
                ]
            },
            "startDate": {
                "Name": "startDate",
                "Type": "date-time",
                "Description": "If known, this is the date when the Milestone started/became active.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "endDate": {
                "Name": "endDate",
                "Type": "date-time",
                "Description": "If known, this is the date when the Milestone will expire/recycle/end.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "order": {
                "Name": "order",
                "Type": "int32",
                "Description": "Used for ordering milestones in a display to match how we order them in BNet. May pull from static data, or possibly in the future from dynamic information.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-GetPublicMilestones.html#operation_get_Destiny2-GetPublicMilestones"""

        try:
            self.logger.info("Executing GetPublicMilestones...")
            url = self.base_url + "/Destiny2/Milestones/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def AwaInitializeRequest(
        self, type: int, affectedItemId: int, membershipType: int, characterId: int
    ) -> dict:
        """Initialize a request to perform an advanced write action.

            Args:


            Returns:
        {
            "correlationId": {
                "Name": "correlationId",
                "Type": "string",
                "Description": "ID used to get the token. Present this ID to the user as it will identify this specific request on their device.",
                "Attributes": []
            },
            "sentToSelf": {
                "Name": "sentToSelf",
                "Type": "boolean",
                "Description": "True if the PUSH message will only be sent to the device that made this request.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-AwaInitializeRequest.html#operation_post_Destiny2-AwaInitializeRequest"""

        request_body = {
            "type": type,
            "affectedItemId": affectedItemId,
            "membershipType": membershipType,
            "characterId": characterId,
        }

        try:
            self.logger.info("Executing AwaInitializeRequest...")
            url = self.base_url + "/Destiny2/Awa/Initialize/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def AwaProvideAuthorizationResult(
        self, selection: int, correlationId: str, nonce: list
    ) -> dict:
        """Provide the result of the user interaction. Called by the Bungie Destiny App to approve or reject a request.

            Args:


            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Destiny2-AwaProvideAuthorizationResult.html#operation_post_Destiny2-AwaProvideAuthorizationResult"""

        request_body = {
            "selection": selection,
            "correlationId": correlationId,
            "nonce": nonce,
        }

        try:
            self.logger.info("Executing AwaProvideAuthorizationResult...")
            url = (
                self.base_url + "/Destiny2/Awa/AwaProvideAuthorizationResult/".format()
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def AwaGetActionToken(
        self,
        correlationId: str,
    ) -> dict:
        """Returns the action token if user approves the request.

            Args:
                correlationId (str): The identifier for the advanced write action request.

            Returns:
        {
            "userSelection": {
                "Name": "userSelection",
                "Type": "int32",
                "Description": "Indication of how the user responded to the request. If the value is \"Approved\" the actionToken will contain the token that can be presented when performing the advanced write action.",
                "Attributes": []
            },
            "responseReason": {
                "Name": "responseReason",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "developerNote": {
                "Name": "developerNote",
                "Type": "string",
                "Description": "Message to the app developer to help understand the response.",
                "Attributes": []
            },
            "actionToken": {
                "Name": "actionToken",
                "Type": "string",
                "Description": "Credential used to prove the user authorized an advanced write action.",
                "Attributes": []
            },
            "maximumNumberOfUses": {
                "Name": "maximumNumberOfUses",
                "Type": "int32",
                "Description": "This token may be used to perform the requested action this number of times, at a maximum. If this value is 0, then there is no limit.",
                "Attributes": []
            },
            "validUntil": {
                "Name": "validUntil",
                "Type": "date-time",
                "Description": "Time, UTC, when token expires.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "type": {
                "Name": "type",
                "Type": "int32",
                "Description": "Advanced Write Action Type from the permission request.",
                "Attributes": []
            },
            "membershipType": {
                "Name": "membershipType",
                "Type": "int32",
                "Description": "MembershipType from the permission request.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Destiny2-AwaGetActionToken.html#operation_get_Destiny2-AwaGetActionToken"""

        try:
            self.logger.info("Executing AwaGetActionToken...")
            url = (
                self.base_url
                + f"/Destiny2/Awa/GetActionToken/{correlationId}/".format(
                    correlationId=correlationId
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
