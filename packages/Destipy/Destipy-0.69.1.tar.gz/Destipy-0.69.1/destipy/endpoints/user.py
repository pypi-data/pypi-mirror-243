from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class User:
    """User endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetBungieNetUserById(
        self,
        id: int,
    ) -> dict:
        """Loads a bungienet user by membership id.

            Args:
                id (int): The requested Bungie.net membership id.

            Returns:
        {
            "membershipId": {
                "Name": "membershipId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "uniqueName": {
                "Name": "uniqueName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "normalizedName": {
                "Name": "normalizedName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "displayName": {
                "Name": "displayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "profilePicture": {
                "Name": "profilePicture",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "profileTheme": {
                "Name": "profileTheme",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "userTitle": {
                "Name": "userTitle",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "successMessageFlags": {
                "Name": "successMessageFlags",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "isDeleted": {
                "Name": "isDeleted",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "about": {
                "Name": "about",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "firstAccess": {
                "Name": "firstAccess",
                "Type": "date-time",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "lastUpdate": {
                "Name": "lastUpdate",
                "Type": "date-time",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "legacyPortalUID": {
                "Name": "legacyPortalUID",
                "Type": "int64",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
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
            },
            "psnDisplayName": {
                "Name": "psnDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "xboxDisplayName": {
                "Name": "xboxDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "fbDisplayName": {
                "Name": "fbDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "showActivity": {
                "Name": "showActivity",
                "Type": "boolean",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "locale": {
                "Name": "locale",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "localeInheritDefault": {
                "Name": "localeInheritDefault",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "lastBanReportId": {
                "Name": "lastBanReportId",
                "Type": "int64",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "showGroupMessaging": {
                "Name": "showGroupMessaging",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "profilePicturePath": {
                "Name": "profilePicturePath",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "profilePictureWidePath": {
                "Name": "profilePictureWidePath",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "profileThemeName": {
                "Name": "profileThemeName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "userTitleDisplay": {
                "Name": "userTitleDisplay",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "statusText": {
                "Name": "statusText",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "statusDate": {
                "Name": "statusDate",
                "Type": "date-time",
                "Description": "",
                "Attributes": []
            },
            "profileBanExpire": {
                "Name": "profileBanExpire",
                "Type": "date-time",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "blizzardDisplayName": {
                "Name": "blizzardDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "steamDisplayName": {
                "Name": "steamDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "stadiaDisplayName": {
                "Name": "stadiaDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "twitchDisplayName": {
                "Name": "twitchDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "cachedBungieGlobalDisplayName": {
                "Name": "cachedBungieGlobalDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "cachedBungieGlobalDisplayNameCode": {
                "Name": "cachedBungieGlobalDisplayNameCode",
                "Type": "int16",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "egsDisplayName": {
                "Name": "egsDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetBungieNetUserById.html#operation_get_User-GetBungieNetUserById"""

        try:
            self.logger.info("Executing GetBungieNetUserById...")
            url = self.base_url + f"/User/GetBungieNetUserById/{id}/".format(id=id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetSanitizedPlatformDisplayNames(
        self,
        membershipId: int,
    ) -> dict:
        """Gets a list of all display names linked to this membership id but sanitized (profanity filtered). Obeys all visibility rules of calling user and is heavily cached.

            Args:
                membershipId (int): The requested membership id to load.

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetSanitizedPlatformDisplayNames.html#operation_get_User-GetSanitizedPlatformDisplayNames"""

        try:
            self.logger.info("Executing GetSanitizedPlatformDisplayNames...")
            url = (
                self.base_url
                + f"/User/GetSanitizedPlatformDisplayNames/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCredentialTypesForTargetAccount(
        self,
        membershipId: int,
    ) -> dict:
        """Returns a list of credential types attached to the requested account

            Args:
                membershipId (int): The user's membership id

            Returns:
        {
            "credentialType": {
                "Name": "credentialType",
                "Type": "byte",
                "Description": "",
                "Attributes": []
            },
            "credentialDisplayName": {
                "Name": "credentialDisplayName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "isPublic": {
                "Name": "isPublic",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "credentialAsString": {
                "Name": "credentialAsString",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetCredentialTypesForTargetAccount.html#operation_get_User-GetCredentialTypesForTargetAccount"""

        try:
            self.logger.info("Executing GetCredentialTypesForTargetAccount...")
            url = (
                self.base_url
                + f"/User/GetCredentialTypesForTargetAccount/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableThemes(
        self,
    ) -> dict:
        """Returns a list of all available user themes.

            Args:


            Returns:
        {
            "userThemeId": {
                "Name": "userThemeId",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "userThemeName": {
                "Name": "userThemeName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "userThemeDescription": {
                "Name": "userThemeDescription",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetAvailableThemes.html#operation_get_User-GetAvailableThemes"""

        try:
            self.logger.info("Executing GetAvailableThemes...")
            url = self.base_url + "/User/GetAvailableThemes/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipDataById(
        self,
        membershipId: int,
        membershipType: int,
    ) -> dict:
        """Returns a list of accounts associated with the supplied membership ID and membership type. This will include all linked accounts (even when hidden) if supplied credentials permit it.

            Args:
                membershipId (int): The membership ID of the target user.
                membershipType (int): Type of the supplied membership ID.

            Returns:
        {
            "destinyMemberships": {
                "Name": "destinyMemberships",
                "Type": "array",
                "Description": "this allows you to see destiny memberships that are visible and linked to this account (regardless of whether or not they have characters on the world server)",
                "Attributes": [],
                "Array Contents": [
                    {
                        "LastSeenDisplayName": {
                            "Name": "LastSeenDisplayName",
                            "Type": "string",
                            "Description": "This will be the display name the clan server last saw the user as. If the account is an active cross save override, this will be the display name to use. Otherwise, this will match the displayName property.",
                            "Attributes": []
                        }
                    },
                    {
                        "LastSeenDisplayNameType": {
                            "Name": "LastSeenDisplayNameType",
                            "Type": "int32",
                            "Description": "The platform of the LastSeenDisplayName",
                            "Attributes": []
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
            "primaryMembershipId": {
                "Name": "primaryMembershipId",
                "Type": "int64",
                "Description": "If this property is populated, it will have the membership ID of the account considered to be \"primary\" in this user's cross save relationship. If null, this user has no cross save relationship, nor primary account.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "bungieNetUser": {
                "membershipId": {
                    "Name": "membershipId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "uniqueName": {
                    "Name": "uniqueName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "normalizedName": {
                    "Name": "normalizedName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "displayName": {
                    "Name": "displayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profilePicture": {
                    "Name": "profilePicture",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "profileTheme": {
                    "Name": "profileTheme",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "userTitle": {
                    "Name": "userTitle",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "successMessageFlags": {
                    "Name": "successMessageFlags",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "isDeleted": {
                    "Name": "isDeleted",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "about": {
                    "Name": "about",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "firstAccess": {
                    "Name": "firstAccess",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "lastUpdate": {
                    "Name": "lastUpdate",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "legacyPortalUID": {
                    "Name": "legacyPortalUID",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
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
                },
                "psnDisplayName": {
                    "Name": "psnDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "xboxDisplayName": {
                    "Name": "xboxDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "fbDisplayName": {
                    "Name": "fbDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "showActivity": {
                    "Name": "showActivity",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "locale": {
                    "Name": "locale",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "localeInheritDefault": {
                    "Name": "localeInheritDefault",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "lastBanReportId": {
                    "Name": "lastBanReportId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "showGroupMessaging": {
                    "Name": "showGroupMessaging",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "profilePicturePath": {
                    "Name": "profilePicturePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profilePictureWidePath": {
                    "Name": "profilePictureWidePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profileThemeName": {
                    "Name": "profileThemeName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "userTitleDisplay": {
                    "Name": "userTitleDisplay",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "statusText": {
                    "Name": "statusText",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "statusDate": {
                    "Name": "statusDate",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": []
                },
                "profileBanExpire": {
                    "Name": "profileBanExpire",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "blizzardDisplayName": {
                    "Name": "blizzardDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "steamDisplayName": {
                    "Name": "steamDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "stadiaDisplayName": {
                    "Name": "stadiaDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "twitchDisplayName": {
                    "Name": "twitchDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "cachedBungieGlobalDisplayName": {
                    "Name": "cachedBungieGlobalDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "cachedBungieGlobalDisplayNameCode": {
                    "Name": "cachedBungieGlobalDisplayNameCode",
                    "Type": "int16",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "egsDisplayName": {
                    "Name": "egsDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetMembershipDataById.html#operation_get_User-GetMembershipDataById"""

        try:
            self.logger.info("Executing GetMembershipDataById...")
            url = (
                self.base_url
                + f"/User/GetMembershipsById/{membershipId}/{membershipType}/".format(
                    membershipId=membershipId, membershipType=membershipType
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipDataForCurrentUser(
        self,
    ) -> dict:
        """Returns a list of accounts associated with signed in user. This is useful for OAuth implementations that do not give you access to the token response.

            Args:


            Returns:
        {
            "destinyMemberships": {
                "Name": "destinyMemberships",
                "Type": "array",
                "Description": "this allows you to see destiny memberships that are visible and linked to this account (regardless of whether or not they have characters on the world server)",
                "Attributes": [],
                "Array Contents": [
                    {
                        "LastSeenDisplayName": {
                            "Name": "LastSeenDisplayName",
                            "Type": "string",
                            "Description": "This will be the display name the clan server last saw the user as. If the account is an active cross save override, this will be the display name to use. Otherwise, this will match the displayName property.",
                            "Attributes": []
                        }
                    },
                    {
                        "LastSeenDisplayNameType": {
                            "Name": "LastSeenDisplayNameType",
                            "Type": "int32",
                            "Description": "The platform of the LastSeenDisplayName",
                            "Attributes": []
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
            "primaryMembershipId": {
                "Name": "primaryMembershipId",
                "Type": "int64",
                "Description": "If this property is populated, it will have the membership ID of the account considered to be \"primary\" in this user's cross save relationship. If null, this user has no cross save relationship, nor primary account.",
                "Attributes": [
                    "Nullable"
                ]
            },
            "bungieNetUser": {
                "membershipId": {
                    "Name": "membershipId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "uniqueName": {
                    "Name": "uniqueName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "normalizedName": {
                    "Name": "normalizedName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "displayName": {
                    "Name": "displayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profilePicture": {
                    "Name": "profilePicture",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "profileTheme": {
                    "Name": "profileTheme",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "userTitle": {
                    "Name": "userTitle",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "successMessageFlags": {
                    "Name": "successMessageFlags",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "isDeleted": {
                    "Name": "isDeleted",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "about": {
                    "Name": "about",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "firstAccess": {
                    "Name": "firstAccess",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "lastUpdate": {
                    "Name": "lastUpdate",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "legacyPortalUID": {
                    "Name": "legacyPortalUID",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
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
                },
                "psnDisplayName": {
                    "Name": "psnDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "xboxDisplayName": {
                    "Name": "xboxDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "fbDisplayName": {
                    "Name": "fbDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "showActivity": {
                    "Name": "showActivity",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "locale": {
                    "Name": "locale",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "localeInheritDefault": {
                    "Name": "localeInheritDefault",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "lastBanReportId": {
                    "Name": "lastBanReportId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "showGroupMessaging": {
                    "Name": "showGroupMessaging",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "profilePicturePath": {
                    "Name": "profilePicturePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profilePictureWidePath": {
                    "Name": "profilePictureWidePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "profileThemeName": {
                    "Name": "profileThemeName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "userTitleDisplay": {
                    "Name": "userTitleDisplay",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "statusText": {
                    "Name": "statusText",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "statusDate": {
                    "Name": "statusDate",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": []
                },
                "profileBanExpire": {
                    "Name": "profileBanExpire",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "blizzardDisplayName": {
                    "Name": "blizzardDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "steamDisplayName": {
                    "Name": "steamDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "stadiaDisplayName": {
                    "Name": "stadiaDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "twitchDisplayName": {
                    "Name": "twitchDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "cachedBungieGlobalDisplayName": {
                    "Name": "cachedBungieGlobalDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "cachedBungieGlobalDisplayNameCode": {
                    "Name": "cachedBungieGlobalDisplayNameCode",
                    "Type": "int16",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "egsDisplayName": {
                    "Name": "egsDisplayName",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetMembershipDataForCurrentUser.html#operation_get_User-GetMembershipDataForCurrentUser"""

        try:
            self.logger.info("Executing GetMembershipDataForCurrentUser...")
            url = self.base_url + "/User/GetMembershipsForCurrentUser/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipFromHardLinkedCredential(
        self,
        credential: str,
        crType: int,
    ) -> dict:
        """Gets any hard linked membership given a credential. Only works for credentials that are public (just SteamID64 right now). Cross Save aware.

            Args:
                credential (str): The credential to look up. Must be a valid SteamID64.
                crType (int): The credential type. 'SteamId' is the only valid value at present.

            Returns:
        {
            "membershipType": {
                "Name": "membershipType",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "membershipId": {
                "Name": "membershipId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "CrossSaveOverriddenType": {
                "Name": "CrossSaveOverriddenType",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "CrossSaveOverriddenMembershipId": {
                "Name": "CrossSaveOverriddenMembershipId",
                "Type": "int64",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-GetMembershipFromHardLinkedCredential.html#operation_get_User-GetMembershipFromHardLinkedCredential"""

        try:
            self.logger.info("Executing GetMembershipFromHardLinkedCredential...")
            url = (
                self.base_url
                + f"/User/GetMembershipFromHardLinkedCredential/{crType}/{credential}/".format(
                    credential=credential, crType=crType
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchByGlobalNamePrefix(
        self,
        displayNamePrefix: str,
        page: int,
    ) -> dict:
        """[OBSOLETE] Do not use this to search users, use SearchByGlobalNamePost instead.

            Args:
                displayNamePrefix (str): The display name prefix you're looking for.
                page (int): The zero-based page of results you desire.

            Returns:
        {
            "searchResults": {
                "Name": "searchResults",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "bungieGlobalDisplayName": {
                            "Name": "bungieGlobalDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "bungieGlobalDisplayNameCode": {
                            "Name": "bungieGlobalDisplayNameCode",
                            "Type": "int16",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "bungieNetMembershipId": {
                            "Name": "bungieNetMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "destinyMemberships": {
                            "Name": "destinyMemberships",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "page": {
                "Name": "page",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "hasMore": {
                "Name": "hasMore",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_User-SearchByGlobalNamePrefix.html#operation_get_User-SearchByGlobalNamePrefix"""

        try:
            self.logger.info("Executing SearchByGlobalNamePrefix...")
            url = (
                self.base_url
                + f"/User/Search/Prefix/{displayNamePrefix}/{page}/".format(
                    displayNamePrefix=displayNamePrefix, page=page
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchByGlobalNamePost(self, page: int, displayNamePrefix: str) -> dict:
        """Given the prefix of a global display name, returns all users who share that name.

            Args:
                page (int): The zero-based page of results you desire.

            Returns:
        {
            "searchResults": {
                "Name": "searchResults",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "bungieGlobalDisplayName": {
                            "Name": "bungieGlobalDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "bungieGlobalDisplayNameCode": {
                            "Name": "bungieGlobalDisplayNameCode",
                            "Type": "int16",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "bungieNetMembershipId": {
                            "Name": "bungieNetMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "destinyMemberships": {
                            "Name": "destinyMemberships",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "page": {
                "Name": "page",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "hasMore": {
                "Name": "hasMore",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_User-SearchByGlobalNamePost.html#operation_post_User-SearchByGlobalNamePost"""

        request_body = {"displayNamePrefix": displayNamePrefix}

        try:
            self.logger.info("Executing SearchByGlobalNamePost...")
            url = self.base_url + f"/User/Search/GlobalName/{page}/".format(page=page)
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)
