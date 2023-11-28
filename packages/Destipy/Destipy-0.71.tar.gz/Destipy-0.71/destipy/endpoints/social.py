from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Social:
    """Social endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetFriendList(self, access_token: str) -> dict:
        """Returns your Bungie Friend list

            Args:
                access_token (str): OAuth token

            Returns:
        {
            "friends": {
                "Name": "friends",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "lastSeenAsMembershipId": {
                            "Name": "lastSeenAsMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastSeenAsBungieMembershipType": {
                            "Name": "lastSeenAsBungieMembershipType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
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
                        "onlineStatus": {
                            "Name": "onlineStatus",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "onlineTitle": {
                            "Name": "onlineTitle",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "relationship": {
                            "Name": "relationship",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Social-GetFriendList.html#operation_get_Social-GetFriendList"""

        try:
            self.logger.info("Executing GetFriendList...")
            url = self.base_url + "/Social/Friends/".format()
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetFriendRequestList(self, access_token: str) -> dict:
        """Returns your friend request queue.

            Args:
                access_token (str): OAuth token

            Returns:
        {
            "incomingRequests": {
                "Name": "incomingRequests",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "lastSeenAsMembershipId": {
                            "Name": "lastSeenAsMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastSeenAsBungieMembershipType": {
                            "Name": "lastSeenAsBungieMembershipType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
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
                        "onlineStatus": {
                            "Name": "onlineStatus",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "onlineTitle": {
                            "Name": "onlineTitle",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "relationship": {
                            "Name": "relationship",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                ]
            },
            "outgoingRequests": {
                "Name": "outgoingRequests",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "lastSeenAsMembershipId": {
                            "Name": "lastSeenAsMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastSeenAsBungieMembershipType": {
                            "Name": "lastSeenAsBungieMembershipType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
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
                        "onlineStatus": {
                            "Name": "onlineStatus",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "onlineTitle": {
                            "Name": "onlineTitle",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "relationship": {
                            "Name": "relationship",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Social-GetFriendRequestList.html#operation_get_Social-GetFriendRequestList"""

        try:
            self.logger.info("Executing GetFriendRequestList...")
            url = self.base_url + "/Social/Friends/Requests/".format()
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def IssueFriendRequest(self, membershipId: str, access_token: str) -> dict:
        """Requests a friend relationship with the target user. Any of the target user's linked membership ids are valid inputs.

            Args:
                membershipId (str): The membership id of the user you wish to add.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Social-IssueFriendRequest.html#operation_post_Social-IssueFriendRequest"""

        try:
            self.logger.info("Executing IssueFriendRequest...")
            url = self.base_url + f"/Social/Friends/Add/{membershipId}/".format(
                membershipId=membershipId
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def AcceptFriendRequest(self, membershipId: str, access_token: str) -> dict:
        """Accepts a friend relationship with the target user. The user must be on your incoming friend request list, though no error will occur if they are not.

            Args:
                membershipId (str): The membership id of the user you wish to accept.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Social-AcceptFriendRequest.html#operation_post_Social-AcceptFriendRequest"""

        try:
            self.logger.info("Executing AcceptFriendRequest...")
            url = (
                self.base_url
                + f"/Social/Friends/Requests/Accept/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def DeclineFriendRequest(self, membershipId: str, access_token: str) -> dict:
        """Declines a friend relationship with the target user. The user must be on your incoming friend request list, though no error will occur if they are not.

            Args:
                membershipId (str): The membership id of the user you wish to decline.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Social-DeclineFriendRequest.html#operation_post_Social-DeclineFriendRequest"""

        try:
            self.logger.info("Executing DeclineFriendRequest...")
            url = (
                self.base_url
                + f"/Social/Friends/Requests/Decline/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def RemoveFriend(self, membershipId: str, access_token: str) -> dict:
        """Remove a friend relationship with the target user. The user must be on your friend list, though no error will occur if they are not.

            Args:
                membershipId (str): The membership id of the user you wish to remove.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Social-RemoveFriend.html#operation_post_Social-RemoveFriend"""

        try:
            self.logger.info("Executing RemoveFriend...")
            url = self.base_url + f"/Social/Friends/Remove/{membershipId}/".format(
                membershipId=membershipId
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def RemoveFriendRequest(self, membershipId: str, access_token: str) -> dict:
        """Remove a friend relationship with the target user. The user must be on your outgoing request friend list, though no error will occur if they are not.

            Args:
                membershipId (str): The membership id of the user you wish to remove.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Social-RemoveFriendRequest.html#operation_post_Social-RemoveFriendRequest"""

        try:
            self.logger.info("Executing RemoveFriendRequest...")
            url = (
                self.base_url
                + f"/Social/Friends/Requests/Remove/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPlatformFriendList(self, friendPlatform: int, page: str) -> dict:
        """Gets the platform friend of the requested type, with additional information if they have Bungie accounts. Must have a recent login session with said platform.

            Args:
                friendPlatform (int): The platform friend type.
                page (str): The zero based page to return. Page size is 100.

            Returns:
        {
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
            "hasMore": {
                "Name": "hasMore",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "platformFriends": {
                "Name": "platformFriends",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "platformDisplayName": {
                            "Name": "platformDisplayName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "friendPlatform": {
                            "Name": "friendPlatform",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "destinyMembershipId": {
                            "Name": "destinyMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "destinyMembershipType": {
                            "Name": "destinyMembershipType",
                            "Type": "int32",
                            "Description": "\"All\" is only valid for searching capabilities: you need to pass the actual matching BungieMembershipType for any query where you pass a known membershipId.",
                            "Attributes": [
                                "Nullable",
                                "Enumeration"
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
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Social-GetPlatformFriendList.html#operation_get_Social-GetPlatformFriendList"""

        try:
            self.logger.info("Executing GetPlatformFriendList...")
            url = (
                self.base_url
                + f"/Social/PlatformFriends/{friendPlatform}/{page}/".format(
                    friendPlatform=friendPlatform, page=page
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
