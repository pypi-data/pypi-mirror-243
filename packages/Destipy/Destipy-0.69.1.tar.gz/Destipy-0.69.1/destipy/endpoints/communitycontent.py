from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class CommunityContent:
    """CommunityContent endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetCommunityContent(
        self,
        mediaFilter: int,
        page: int,
        sort: int,
    ) -> dict:
        """Returns community content.

            Args:
                mediaFilter (int): The type of media to get
                page (int): Zero based page
                sort (int): The sort mode.

            Returns:
        {
            "relatedPosts": {
                "Name": "relatedPosts",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "lastReplyTimestamp": {
                            "Name": "lastReplyTimestamp",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "IsPinned": {
                            "Name": "IsPinned",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "urlMediaType": {
                            "Name": "urlMediaType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "thumbnail": {
                            "Name": "thumbnail",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "popularity": {
                            "Name": "popularity",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isActive": {
                            "Name": "isActive",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isAnnouncement": {
                            "Name": "isAnnouncement",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userRating": {
                            "Name": "userRating",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userHasRated": {
                            "Name": "userHasRated",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userHasMutedPost": {
                            "Name": "userHasMutedPost",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "latestReplyPostId": {
                            "Name": "latestReplyPostId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "latestReplyAuthorId": {
                            "Name": "latestReplyAuthorId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ignoreStatus": {
                            "isIgnored": {
                                "Name": "isIgnored",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "ignoreFlags": {
                                "Name": "ignoreFlags",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            }
                        }
                    },
                    {
                        "locale": {
                            "Name": "locale",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "authors": {
                "Name": "authors",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "membershipId": {
                            "Name": "membershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "uniqueName": {
                            "Name": "uniqueName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "normalizedName": {
                            "Name": "normalizedName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "displayName": {
                            "Name": "displayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profilePicture": {
                            "Name": "profilePicture",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profileTheme": {
                            "Name": "profileTheme",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userTitle": {
                            "Name": "userTitle",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "successMessageFlags": {
                            "Name": "successMessageFlags",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isDeleted": {
                            "Name": "isDeleted",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "about": {
                            "Name": "about",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "firstAccess": {
                            "Name": "firstAccess",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "lastUpdate": {
                            "Name": "lastUpdate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "legacyPortalUID": {
                            "Name": "legacyPortalUID",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "context": {
                            "isFollowing": {
                                "Name": "isFollowing",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "ignoreStatus": {
                                "isIgnored": {
                                    "Name": "isIgnored",
                                    "Type": "boolean",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "ignoreFlags": {
                                    "Name": "ignoreFlags",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            "globalIgnoreEndDate": {
                                "Name": "globalIgnoreEndDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            }
                        }
                    },
                    {
                        "psnDisplayName": {
                            "Name": "psnDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "xboxDisplayName": {
                            "Name": "xboxDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "fbDisplayName": {
                            "Name": "fbDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "showActivity": {
                            "Name": "showActivity",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "locale": {
                            "Name": "locale",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "localeInheritDefault": {
                            "Name": "localeInheritDefault",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastBanReportId": {
                            "Name": "lastBanReportId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "showGroupMessaging": {
                            "Name": "showGroupMessaging",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profilePicturePath": {
                            "Name": "profilePicturePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profilePictureWidePath": {
                            "Name": "profilePictureWidePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profileThemeName": {
                            "Name": "profileThemeName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userTitleDisplay": {
                            "Name": "userTitleDisplay",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "statusText": {
                            "Name": "statusText",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "statusDate": {
                            "Name": "statusDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "profileBanExpire": {
                            "Name": "profileBanExpire",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "blizzardDisplayName": {
                            "Name": "blizzardDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "steamDisplayName": {
                            "Name": "steamDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "stadiaDisplayName": {
                            "Name": "stadiaDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "twitchDisplayName": {
                            "Name": "twitchDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cachedBungieGlobalDisplayName": {
                            "Name": "cachedBungieGlobalDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cachedBungieGlobalDisplayNameCode": {
                            "Name": "cachedBungieGlobalDisplayNameCode",
                            "Type": "int16",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "egsDisplayName": {
                            "Name": "egsDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "groups": {
                "Name": "groups",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "detail": {
                            "groupId": {
                                "Name": "groupId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "name": {
                                "Name": "name",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "groupType": {
                                "Name": "groupType",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "membershipIdCreated": {
                                "Name": "membershipIdCreated",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "creationDate": {
                                "Name": "creationDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "modificationDate": {
                                "Name": "modificationDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "about": {
                                "Name": "about",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "tags": {
                                "Name": "tags",
                                "Type": "array",
                                "Description": "",
                                "Attributes": [],
                                "Array Contents": "string"
                            },
                            "memberCount": {
                                "Name": "memberCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "isPublic": {
                                "Name": "isPublic",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "isPublicTopicAdminOnly": {
                                "Name": "isPublicTopicAdminOnly",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "motto": {
                                "Name": "motto",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "allowChat": {
                                "Name": "allowChat",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "isDefaultPostPublic": {
                                "Name": "isDefaultPostPublic",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "chatSecurity": {
                                "Name": "chatSecurity",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "locale": {
                                "Name": "locale",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "avatarImageIndex": {
                                "Name": "avatarImageIndex",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "homepage": {
                                "Name": "homepage",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "membershipOption": {
                                "Name": "membershipOption",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "defaultPublicity": {
                                "Name": "defaultPublicity",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "theme": {
                                "Name": "theme",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "bannerPath": {
                                "Name": "bannerPath",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "avatarPath": {
                                "Name": "avatarPath",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "conversationId": {
                                "Name": "conversationId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "enableInvitationMessagingForAdmins": {
                                "Name": "enableInvitationMessagingForAdmins",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "banExpireDate": {
                                "Name": "banExpireDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "features": {
                                "maximumMembers": {
                                    "Name": "maximumMembers",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "maximumMembershipsOfGroupType": {
                                    "Name": "maximumMembershipsOfGroupType",
                                    "Type": "int32",
                                    "Description": "Maximum number of groups of this type a typical membership may join. For example, a user may join about 50 General groups with their Bungie.net account. They may join one clan per Destiny membership.",
                                    "Attributes": []
                                },
                                "capabilities": {
                                    "Name": "capabilities",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "membershipTypes": {
                                    "Name": "membershipTypes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [],
                                    "Array Contents": "int32"
                                },
                                "invitePermissionOverride": {
                                    "Name": "invitePermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to invite new members to groupAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "updateCulturePermissionOverride": {
                                    "Name": "updateCulturePermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to update group cultureAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "hostGuidedGamePermissionOverride": {
                                    "Name": "hostGuidedGamePermissionOverride",
                                    "Type": "int32",
                                    "Description": "Minimum Member Level allowed to host guided gamesAlways Allowed: Founder, Acting Founder, AdminAllowed Overrides: None, Member, BeginnerDefault is Member for clans, None for groups, although this means nothing for groups.",
                                    "Attributes": []
                                },
                                "updateBannerPermissionOverride": {
                                    "Name": "updateBannerPermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to update bannerAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "joinLevel": {
                                    "Name": "joinLevel",
                                    "Type": "int32",
                                    "Description": "Level to join a member at when accepting an invite, application, or joining an open clanDefault is Beginner.",
                                    "Attributes": []
                                }
                            },
                            "remoteGroupId": {
                                "Name": "remoteGroupId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "clanInfo": {
                                "d2ClanProgressions": {
                                    "Name": "d2ClanProgressions",
                                    "Type": "object",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "clanCallsign": {
                                    "Name": "clanCallsign",
                                    "Type": "string",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "clanBannerData": {
                                    "decalId": {
                                        "Name": "decalId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "decalColorId": {
                                        "Name": "decalColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "decalBackgroundColorId": {
                                        "Name": "decalBackgroundColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonId": {
                                        "Name": "gonfalonId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonColorId": {
                                        "Name": "gonfalonColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonDetailId": {
                                        "Name": "gonfalonDetailId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonDetailColorId": {
                                        "Name": "gonfalonDetailColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            }
                        }
                    },
                    {
                        "founder": {
                            "memberType": {
                                "Name": "memberType",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "isOnline": {
                                "Name": "isOnline",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "lastOnlineStatusChange": {
                                "Name": "lastOnlineStatusChange",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "groupId": {
                                "Name": "groupId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "destinyUserInfo": {
                                "LastSeenDisplayName": {
                                    "Name": "LastSeenDisplayName",
                                    "Type": "string",
                                    "Description": "This will be the display name the clan server last saw the user as. If the account is an active cross save override, this will be the display name to use. Otherwise, this will match the displayName property.",
                                    "Attributes": []
                                },
                                "LastSeenDisplayNameType": {
                                    "Name": "LastSeenDisplayNameType",
                                    "Type": "int32",
                                    "Description": "The platform of the LastSeenDisplayName",
                                    "Attributes": []
                                },
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
                            },
                            "bungieNetUserInfo": {
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
                            },
                            "joinDate": {
                                "Name": "joinDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            }
                        }
                    },
                    {
                        "alliedIds": {
                            "Name": "alliedIds",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "parentGroup": {
                            "groupId": {
                                "Name": "groupId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "name": {
                                "Name": "name",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "groupType": {
                                "Name": "groupType",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "membershipIdCreated": {
                                "Name": "membershipIdCreated",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "creationDate": {
                                "Name": "creationDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "modificationDate": {
                                "Name": "modificationDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "about": {
                                "Name": "about",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "tags": {
                                "Name": "tags",
                                "Type": "array",
                                "Description": "",
                                "Attributes": [],
                                "Array Contents": "string"
                            },
                            "memberCount": {
                                "Name": "memberCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "isPublic": {
                                "Name": "isPublic",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "isPublicTopicAdminOnly": {
                                "Name": "isPublicTopicAdminOnly",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "motto": {
                                "Name": "motto",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "allowChat": {
                                "Name": "allowChat",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "isDefaultPostPublic": {
                                "Name": "isDefaultPostPublic",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "chatSecurity": {
                                "Name": "chatSecurity",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "locale": {
                                "Name": "locale",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "avatarImageIndex": {
                                "Name": "avatarImageIndex",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "homepage": {
                                "Name": "homepage",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "membershipOption": {
                                "Name": "membershipOption",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "defaultPublicity": {
                                "Name": "defaultPublicity",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "theme": {
                                "Name": "theme",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "bannerPath": {
                                "Name": "bannerPath",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "avatarPath": {
                                "Name": "avatarPath",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "conversationId": {
                                "Name": "conversationId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "enableInvitationMessagingForAdmins": {
                                "Name": "enableInvitationMessagingForAdmins",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "banExpireDate": {
                                "Name": "banExpireDate",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "features": {
                                "maximumMembers": {
                                    "Name": "maximumMembers",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "maximumMembershipsOfGroupType": {
                                    "Name": "maximumMembershipsOfGroupType",
                                    "Type": "int32",
                                    "Description": "Maximum number of groups of this type a typical membership may join. For example, a user may join about 50 General groups with their Bungie.net account. They may join one clan per Destiny membership.",
                                    "Attributes": []
                                },
                                "capabilities": {
                                    "Name": "capabilities",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "membershipTypes": {
                                    "Name": "membershipTypes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [],
                                    "Array Contents": "int32"
                                },
                                "invitePermissionOverride": {
                                    "Name": "invitePermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to invite new members to groupAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "updateCulturePermissionOverride": {
                                    "Name": "updateCulturePermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to update group cultureAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "hostGuidedGamePermissionOverride": {
                                    "Name": "hostGuidedGamePermissionOverride",
                                    "Type": "int32",
                                    "Description": "Minimum Member Level allowed to host guided gamesAlways Allowed: Founder, Acting Founder, AdminAllowed Overrides: None, Member, BeginnerDefault is Member for clans, None for groups, although this means nothing for groups.",
                                    "Attributes": []
                                },
                                "updateBannerPermissionOverride": {
                                    "Name": "updateBannerPermissionOverride",
                                    "Type": "boolean",
                                    "Description": "Minimum Member Level allowed to update bannerAlways Allowed: Founder, Acting FounderTrue means admins have this power, false means they don'tDefault is false for clans, true for groups.",
                                    "Attributes": []
                                },
                                "joinLevel": {
                                    "Name": "joinLevel",
                                    "Type": "int32",
                                    "Description": "Level to join a member at when accepting an invite, application, or joining an open clanDefault is Beginner.",
                                    "Attributes": []
                                }
                            },
                            "remoteGroupId": {
                                "Name": "remoteGroupId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "clanInfo": {
                                "d2ClanProgressions": {
                                    "Name": "d2ClanProgressions",
                                    "Type": "object",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "clanCallsign": {
                                    "Name": "clanCallsign",
                                    "Type": "string",
                                    "Description": "",
                                    "Attributes": []
                                },
                                "clanBannerData": {
                                    "decalId": {
                                        "Name": "decalId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "decalColorId": {
                                        "Name": "decalColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "decalBackgroundColorId": {
                                        "Name": "decalBackgroundColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonId": {
                                        "Name": "gonfalonId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonColorId": {
                                        "Name": "gonfalonColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonDetailId": {
                                        "Name": "gonfalonDetailId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "gonfalonDetailColorId": {
                                        "Name": "gonfalonDetailColorId",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            }
                        }
                    },
                    {
                        "allianceStatus": {
                            "Name": "allianceStatus",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "groupJoinInviteCount": {
                            "Name": "groupJoinInviteCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "currentUserMembershipsInactiveForDestiny": {
                            "Name": "currentUserMembershipsInactiveForDestiny",
                            "Type": "boolean",
                            "Description": "A convenience property that indicates if every membership you (the current user) have that is a part of this group are part of an account that is considered inactive - for example, overridden accounts in Cross Save.",
                            "Attributes": []
                        }
                    },
                    {
                        "currentUserMemberMap": {
                            "Name": "currentUserMemberMap",
                            "Type": "object",
                            "Description": "This property will be populated if the authenticated user is a member of the group. Note that because of account linking, a user can sometimes be part of a clan more than once. As such, this returns the highest member type available.",
                            "Attributes": []
                        }
                    },
                    {
                        "currentUserPotentialMemberMap": {
                            "Name": "currentUserPotentialMemberMap",
                            "Type": "object",
                            "Description": "This property will be populated if the authenticated user is an applicant or has an outstanding invitation to join. Note that because of account linking, a user can sometimes be part of a clan more than once.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "searchedTags": {
                "Name": "searchedTags",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "tagText": {
                            "Name": "tagText",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ignoreStatus": {
                            "isIgnored": {
                                "Name": "isIgnored",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "ignoreFlags": {
                                "Name": "ignoreFlags",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            }
                        }
                    }
                ]
            },
            "polls": {
                "Name": "polls",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "topicId": {
                            "Name": "topicId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "results": {
                            "Name": "results",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "totalVotes": {
                            "Name": "totalVotes",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "recruitmentDetails": {
                "Name": "recruitmentDetails",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "topicId": {
                            "Name": "topicId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "microphoneRequired": {
                            "Name": "microphoneRequired",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "intensity": {
                            "Name": "intensity",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "tone": {
                            "Name": "tone",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "approved": {
                            "Name": "approved",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "conversationId": {
                            "Name": "conversationId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "playerSlotsTotal": {
                            "Name": "playerSlotsTotal",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "playerSlotsRemaining": {
                            "Name": "playerSlotsRemaining",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "Fireteam": {
                            "Name": "Fireteam",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "kickedPlayerIds": {
                            "Name": "kickedPlayerIds",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "availablePages": {
                "Name": "availablePages",
                "Type": "int32",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "lastReplyTimestamp": {
                            "Name": "lastReplyTimestamp",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "IsPinned": {
                            "Name": "IsPinned",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "urlMediaType": {
                            "Name": "urlMediaType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "thumbnail": {
                            "Name": "thumbnail",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "popularity": {
                            "Name": "popularity",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isActive": {
                            "Name": "isActive",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isAnnouncement": {
                            "Name": "isAnnouncement",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userRating": {
                            "Name": "userRating",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userHasRated": {
                            "Name": "userHasRated",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "userHasMutedPost": {
                            "Name": "userHasMutedPost",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "latestReplyPostId": {
                            "Name": "latestReplyPostId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "latestReplyAuthorId": {
                            "Name": "latestReplyAuthorId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ignoreStatus": {
                            "isIgnored": {
                                "Name": "isIgnored",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "ignoreFlags": {
                                "Name": "ignoreFlags",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            }
                        }
                    },
                    {
                        "locale": {
                            "Name": "locale",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "totalResults": {
                "Name": "totalResults",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "hasMore": {
                "Name": "hasMore",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "query": {
                "itemsPerPage": {
                    "Name": "itemsPerPage",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "currentPage": {
                    "Name": "currentPage",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "requestContinuationToken": {
                    "Name": "requestContinuationToken",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            },
            "replacementContinuationToken": {
                "Name": "replacementContinuationToken",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "useTotalResults": {
                "Name": "useTotalResults",
                "Type": "boolean",
                "Description": "If useTotalResults is true, then totalResults represents an accurate count.If False, it does not, and may be estimated/only the size of the current page.Either way, you should probably always only trust hasMore.This is a long-held historical throwback to when we used to do paging with known total results. Those queries toasted our database, and we were left to hastily alter our endpoints and create backward- compatible shims, of which useTotalResults is one.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_CommunityContent-GetCommunityContent.html#operation_get_CommunityContent-GetCommunityContent"""

        try:
            self.logger.info("Executing GetCommunityContent...")
            url = (
                self.base_url
                + f"/CommunityContent/Get/{sort}/{mediaFilter}/{page}/".format(
                    mediaFilter=mediaFilter, page=page, sort=sort
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
