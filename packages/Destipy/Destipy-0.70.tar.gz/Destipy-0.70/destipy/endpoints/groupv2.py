from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class GroupV2:
    """GroupV2 endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetAvailableAvatars(self) -> dict:
        """Returns a list of all available group avatars for the signed-in user.

            Args:

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetAvailableAvatars.html#operation_get_GroupV2-GetAvailableAvatars"""

        try:
            self.logger.info("Executing GetAvailableAvatars...")
            url = self.base_url + "/GroupV2/GetAvailableAvatars/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableThemes(self) -> dict:
        """Returns a list of all available group themes.

            Args:

            Returns:
        {
            "name": {
                "Name": "name",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "folder": {
                "Name": "folder",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "description": {
                "Name": "description",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetAvailableThemes.html#operation_get_GroupV2-GetAvailableThemes"""

        try:
            self.logger.info("Executing GetAvailableThemes...")
            url = self.base_url + "/GroupV2/GetAvailableThemes/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetUserClanInviteSetting(self, mType: int, access_token: str) -> dict:
        """Gets the state of the user's clan invite preferences for a particular membership type - true if they wish to be invited to clans, false otherwise.

            Args:
                mType (int): The Destiny membership type of the account we wish to access settings.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetUserClanInviteSetting.html#operation_get_GroupV2-GetUserClanInviteSetting"""

        try:
            self.logger.info("Executing GetUserClanInviteSetting...")
            url = self.base_url + f"/GroupV2/GetUserClanInviteSetting/{mType}/".format(
                mType=mType
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetRecommendedGroups(
        self, createDateRange: int, groupType: int, access_token: str
    ) -> dict:
        """Gets groups recommended for you based on the groups to whom those you follow belong.

            Args:
                createDateRange (int): Requested range in which to pull recommended groups
                groupType (int): Type of groups requested
                access_token (str): OAuth token

            Returns:
        {
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
            "creationDate": {
                "Name": "creationDate",
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
            "motto": {
                "Name": "motto",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "memberCount": {
                "Name": "memberCount",
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
            "membershipOption": {
                "Name": "membershipOption",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "capabilities": {
                "Name": "capabilities",
                "Type": "int32",
                "Description": "",
                "Attributes": []
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
            },
            "avatarPath": {
                "Name": "avatarPath",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "theme": {
                "Name": "theme",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-GetRecommendedGroups.html#operation_post_GroupV2-GetRecommendedGroups"""

        try:
            self.logger.info("Executing GetRecommendedGroups...")
            url = (
                self.base_url
                + f"/GroupV2/Recommended/{groupType}/{createDateRange}/".format(
                    createDateRange=createDateRange, groupType=groupType
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GroupSearch(
        self,
        name: str,
        groupType: int,
        creationDate: int,
        sortBy: int,
        groupMemberCountFilter: int,
        localeFilter: str,
        tagText: str,
        itemsPerPage: int,
        currentPage: int,
        requestContinuationToken: str,
    ) -> dict:
        """Search for Groups.

            Args:

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "name": {
                            "Name": "name",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "groupType": {
                            "Name": "groupType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "creationDate": {
                            "Name": "creationDate",
                            "Type": "date-time",
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
                        "motto": {
                            "Name": "motto",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "memberCount": {
                            "Name": "memberCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
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
                        "membershipOption": {
                            "Name": "membershipOption",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "capabilities": {
                            "Name": "capabilities",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "remoteGroupId": {
                            "Name": "remoteGroupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "clanInfo": {
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
                    },
                    {
                        "avatarPath": {
                            "Name": "avatarPath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "theme": {
                            "Name": "theme",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-GroupSearch.html#operation_post_GroupV2-GroupSearch"""

        request_body = {
            "name": name,
            "groupType": groupType,
            "creationDate": creationDate,
            "sortBy": sortBy,
            "groupMemberCountFilter": groupMemberCountFilter,
            "localeFilter": localeFilter,
            "tagText": tagText,
            "itemsPerPage": itemsPerPage,
            "currentPage": currentPage,
            "requestContinuationToken": requestContinuationToken,
        }

        try:
            self.logger.info("Executing GroupSearch...")
            url = self.base_url + "/GroupV2/Search/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroup(self, groupId: int) -> dict:
        """Get information about a specific group of the given ID.

            Args:
                groupId (int): Requested group's id.

            Returns:
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
            },
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
            },
            "alliedIds": {
                "Name": "alliedIds",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": "int64"
            },
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
            },
            "allianceStatus": {
                "Name": "allianceStatus",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "groupJoinInviteCount": {
                "Name": "groupJoinInviteCount",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "currentUserMembershipsInactiveForDestiny": {
                "Name": "currentUserMembershipsInactiveForDestiny",
                "Type": "boolean",
                "Description": "A convenience property that indicates if every membership you (the current user) have that is a part of this group are part of an account that is considered inactive - for example, overridden accounts in Cross Save.",
                "Attributes": []
            },
            "currentUserMemberMap": {
                "Name": "currentUserMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is a member of the group. Note that because of account linking, a user can sometimes be part of a clan more than once. As such, this returns the highest member type available.",
                "Attributes": []
            },
            "currentUserPotentialMemberMap": {
                "Name": "currentUserPotentialMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is an applicant or has an outstanding invitation to join. Note that because of account linking, a user can sometimes be part of a clan more than once.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroup.html#operation_get_GroupV2-GetGroup"""

        try:
            self.logger.info("Executing GetGroup...")
            url = self.base_url + f"/GroupV2/{groupId}/".format(groupId=groupId)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupByName(self, groupName: str, groupType: int) -> dict:
        """Get information about a specific group with the given name and type.

            Args:
                groupName (str): Exact name of the group to find.
                groupType (int): Type of group to find.

            Returns:
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
            },
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
            },
            "alliedIds": {
                "Name": "alliedIds",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": "int64"
            },
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
            },
            "allianceStatus": {
                "Name": "allianceStatus",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "groupJoinInviteCount": {
                "Name": "groupJoinInviteCount",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "currentUserMembershipsInactiveForDestiny": {
                "Name": "currentUserMembershipsInactiveForDestiny",
                "Type": "boolean",
                "Description": "A convenience property that indicates if every membership you (the current user) have that is a part of this group are part of an account that is considered inactive - for example, overridden accounts in Cross Save.",
                "Attributes": []
            },
            "currentUserMemberMap": {
                "Name": "currentUserMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is a member of the group. Note that because of account linking, a user can sometimes be part of a clan more than once. As such, this returns the highest member type available.",
                "Attributes": []
            },
            "currentUserPotentialMemberMap": {
                "Name": "currentUserPotentialMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is an applicant or has an outstanding invitation to join. Note that because of account linking, a user can sometimes be part of a clan more than once.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroupByName.html#operation_get_GroupV2-GetGroupByName"""

        try:
            self.logger.info("Executing GetGroupByName...")
            url = self.base_url + f"/GroupV2/Name/{groupName}/{groupType}/".format(
                groupName=groupName, groupType=groupType
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupByNameV2(self, groupName: str, groupType: int) -> dict:
        """Get information about a specific group with the given name and type. The POST version.

            Args:

            Returns:
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
            },
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
            },
            "alliedIds": {
                "Name": "alliedIds",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": "int64"
            },
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
            },
            "allianceStatus": {
                "Name": "allianceStatus",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "groupJoinInviteCount": {
                "Name": "groupJoinInviteCount",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "currentUserMembershipsInactiveForDestiny": {
                "Name": "currentUserMembershipsInactiveForDestiny",
                "Type": "boolean",
                "Description": "A convenience property that indicates if every membership you (the current user) have that is a part of this group are part of an account that is considered inactive - for example, overridden accounts in Cross Save.",
                "Attributes": []
            },
            "currentUserMemberMap": {
                "Name": "currentUserMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is a member of the group. Note that because of account linking, a user can sometimes be part of a clan more than once. As such, this returns the highest member type available.",
                "Attributes": []
            },
            "currentUserPotentialMemberMap": {
                "Name": "currentUserPotentialMemberMap",
                "Type": "object",
                "Description": "This property will be populated if the authenticated user is an applicant or has an outstanding invitation to join. Note that because of account linking, a user can sometimes be part of a clan more than once.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-GetGroupByNameV2.html#operation_post_GroupV2-GetGroupByNameV2"""

        request_body = {"groupName": groupName, "groupType": groupType}

        try:
            self.logger.info("Executing GetGroupByNameV2...")
            url = self.base_url + "/GroupV2/NameV2/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, data=request_body
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupOptionalConversations(self, groupId: int) -> dict:
        """Gets a list of available optional conversation channels and their settings.

            Args:
                groupId (int): Requested group's id.

            Returns:
        {
            "groupId": {
                "Name": "groupId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "conversationId": {
                "Name": "conversationId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "chatEnabled": {
                "Name": "chatEnabled",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "chatName": {
                "Name": "chatName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "chatSecurity": {
                "Name": "chatSecurity",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroupOptionalConversations.html#operation_get_GroupV2-GetGroupOptionalConversations"""

        try:
            self.logger.info("Executing GetGroupOptionalConversations...")
            url = self.base_url + f"/GroupV2/{groupId}/OptionalConversations/".format(
                groupId=groupId
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def EditGroup(
        self,
        groupId: int,
        name: str,
        about: str,
        motto: str,
        theme: str,
        avatarImageIndex: int,
        tags: str,
        isPublic: bool,
        membershipOption: int,
        isPublicTopicAdminOnly: bool,
        allowChat: bool,
        chatSecurity: int,
        callsign: str,
        locale: str,
        homepage: int,
        enableInvitationMessagingForAdmins: bool,
        defaultPublicity: int,
        access_token: str,
    ) -> dict:
        """Edit an existing group. You must have suitable permissions in the group to perform this operation. This latest revision will only edit the fields you pass in - pass null for properties you want to leave unaltered.

            Args:
                groupId (int): Group ID of the group to edit.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-EditGroup.html#operation_post_GroupV2-EditGroup"""

        request_body = {
            "name": name,
            "about": about,
            "motto": motto,
            "theme": theme,
            "avatarImageIndex": avatarImageIndex,
            "tags": tags,
            "isPublic": isPublic,
            "membershipOption": membershipOption,
            "isPublicTopicAdminOnly": isPublicTopicAdminOnly,
            "allowChat": allowChat,
            "chatSecurity": chatSecurity,
            "callsign": callsign,
            "locale": locale,
            "homepage": homepage,
            "enableInvitationMessagingForAdmins": enableInvitationMessagingForAdmins,
            "defaultPublicity": defaultPublicity,
        }

        try:
            self.logger.info("Executing EditGroup...")
            url = self.base_url + f"/GroupV2/{groupId}/Edit/".format(groupId=groupId)
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EditClanBanner(
        self,
        groupId: int,
        decalId: int,
        decalColorId: int,
        decalBackgroundColorId: int,
        gonfalonId: int,
        gonfalonColorId: int,
        gonfalonDetailId: int,
        gonfalonDetailColorId: int,
        access_token: str,
    ) -> dict:
        """Edit an existing group's clan banner. You must have suitable permissions in the group to perform this operation. All fields are required.

            Args:
                groupId (int): Group ID of the group to edit.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-EditClanBanner.html#operation_post_GroupV2-EditClanBanner"""

        request_body = {
            "decalId": decalId,
            "decalColorId": decalColorId,
            "decalBackgroundColorId": decalBackgroundColorId,
            "gonfalonId": gonfalonId,
            "gonfalonColorId": gonfalonColorId,
            "gonfalonDetailId": gonfalonDetailId,
            "gonfalonDetailColorId": gonfalonDetailColorId,
        }

        try:
            self.logger.info("Executing EditClanBanner...")
            url = self.base_url + f"/GroupV2/{groupId}/EditClanBanner/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EditFounderOptions(
        self,
        groupId: int,
        InvitePermissionOverride: bool,
        UpdateCulturePermissionOverride: bool,
        HostGuidedGamePermissionOverride: int,
        UpdateBannerPermissionOverride: bool,
        JoinLevel: int,
        access_token: str,
    ) -> dict:
        """Edit group options only available to a founder. You must have suitable permissions in the group to perform this operation.

            Args:
                groupId (int): Group ID of the group to edit.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-EditFounderOptions.html#operation_post_GroupV2-EditFounderOptions"""

        request_body = {
            "InvitePermissionOverride": InvitePermissionOverride,
            "UpdateCulturePermissionOverride": UpdateCulturePermissionOverride,
            "HostGuidedGamePermissionOverride": HostGuidedGamePermissionOverride,
            "UpdateBannerPermissionOverride": UpdateBannerPermissionOverride,
            "JoinLevel": JoinLevel,
        }

        try:
            self.logger.info("Executing EditFounderOptions...")
            url = self.base_url + f"/GroupV2/{groupId}/EditFounderOptions/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def AddOptionalConversation(
        self, groupId: int, chatName: str, chatSecurity: int, access_token: str
    ) -> dict:
        """Add a new optional conversation/chat channel. Requires admin permissions to the group.

            Args:
                groupId (int): Group ID of the group to edit.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int64",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-AddOptionalConversation.html#operation_post_GroupV2-AddOptionalConversation"""

        request_body = {"chatName": chatName, "chatSecurity": chatSecurity}

        try:
            self.logger.info("Executing AddOptionalConversation...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/OptionalConversations/Add/".format(
                    groupId=groupId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def EditOptionalConversation(
        self,
        conversationId: int,
        groupId: int,
        chatEnabled: bool,
        chatName: str,
        chatSecurity: int,
        access_token: str,
    ) -> dict:
        """Edit the settings of an optional conversation/chat channel. Requires admin permissions to the group.

            Args:
                conversationId (int): Conversation Id of the channel being edited.
                groupId (int): Group ID of the group to edit.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int64",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-EditOptionalConversation.html#operation_post_GroupV2-EditOptionalConversation"""

        request_body = {
            "chatEnabled": chatEnabled,
            "chatName": chatName,
            "chatSecurity": chatSecurity,
        }

        try:
            self.logger.info("Executing EditOptionalConversation...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/OptionalConversations/Edit/{conversationId}/".format(
                    conversationId=conversationId, groupId=groupId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembersOfGroup(
        self, currentpage: int, groupId: int, memberType: int, nameSearch: str
    ) -> dict:
        """Get the list of members in a given group.

            Args:
                currentpage (int): Page number (starting with 1). Each page has a fixed size of 50 items per page.
                groupId (int): The ID of the group.
                memberType (int): Filter out other member types. Use None for all members.
                nameSearch (str): The name fragment upon which a search should be executed for members with matching display or unique names.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "memberType": {
                            "Name": "memberType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isOnline": {
                            "Name": "isOnline",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastOnlineStatusChange": {
                            "Name": "lastOnlineStatusChange",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
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
                        }
                    },
                    {
                        "joinDate": {
                            "Name": "joinDate",
                            "Type": "date-time",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html#operation_get_GroupV2-GetMembersOfGroup"""

        try:
            self.logger.info("Executing GetMembersOfGroup...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/".format(
                currentpage=currentpage,
                groupId=groupId,
                memberType=memberType,
                nameSearch=nameSearch,
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAdminsAndFounderOfGroup(self, currentpage: int, groupId: int) -> dict:
        """Get the list of members in a given group who are of admin level or higher.

            Args:
                currentpage (int): Page number (starting with 1). Each page has a fixed size of 50 items per page.
                groupId (int): The ID of the group.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "memberType": {
                            "Name": "memberType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isOnline": {
                            "Name": "isOnline",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastOnlineStatusChange": {
                            "Name": "lastOnlineStatusChange",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
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
                        }
                    },
                    {
                        "joinDate": {
                            "Name": "joinDate",
                            "Type": "date-time",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetAdminsAndFounderOfGroup.html#operation_get_GroupV2-GetAdminsAndFounderOfGroup"""

        try:
            self.logger.info("Executing GetAdminsAndFounderOfGroup...")
            url = self.base_url + f"/GroupV2/{groupId}/AdminsAndFounder/".format(
                currentpage=currentpage, groupId=groupId
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def EditGroupMembership(
        self,
        groupId: int,
        membershipId: int,
        membershipType: int,
        memberType: int,
        access_token: str,
    ) -> dict:
        """Edit the membership type of a given member. You must have suitable permissions in the group to perform this operation.

            Args:
                groupId (int): ID of the group to which the member belongs.
                membershipId (int): Membership ID to modify.
                membershipType (int): Membership type of the provide membership ID.
                memberType (int): New membertype for the specified member.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-EditGroupMembership.html#operation_post_GroupV2-EditGroupMembership"""

        try:
            self.logger.info("Executing EditGroupMembership...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/SetMembershipType/{memberType}/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                    memberType=memberType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def KickMember(
        self, groupId: int, membershipId: int, membershipType: int, access_token: str
    ) -> dict:
        """Kick a member from the given group, forcing them to reapply if they wish to re-join the group. You must have suitable permissions in the group to perform this operation.

            Args:
                groupId (int): Group ID to kick the user from.
                membershipId (int): Membership ID to kick.
                membershipType (int): Membership type of the provided membership ID.
                access_token (str): OAuth token

            Returns:
        {
            "group": {
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
            },
            "groupDeleted": {
                "Name": "groupDeleted",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-KickMember.html#operation_post_GroupV2-KickMember"""

        try:
            self.logger.info("Executing KickMember...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Kick/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def BanMember(
        self,
        groupId: int,
        membershipId: int,
        membershipType: int,
        comment: str,
        length: int,
        access_token: str,
    ) -> dict:
        """Bans the requested member from the requested group for the specified period of time.

            Args:
                groupId (int): Group ID that has the member to ban.
                membershipId (int): Membership ID of the member to ban from the group.
                membershipType (int): Membership type of the provided membership ID.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-BanMember.html#operation_post_GroupV2-BanMember"""

        request_body = {"comment": comment, "length": length}

        try:
            self.logger.info("Executing BanMember...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Ban/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def UnbanMember(
        self, groupId: int, membershipId: int, membershipType: int, access_token: str
    ) -> dict:
        """Unbans the requested member, allowing them to re-apply for membership.

            Args:
                groupId (int):
                membershipId (int): Membership ID of the member to unban from the group
                membershipType (int): Membership type of the provided membership ID.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-UnbanMember.html#operation_post_GroupV2-UnbanMember"""

        try:
            self.logger.info("Executing UnbanMember...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Unban/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBannedMembersOfGroup(
        self, currentpage: int, groupId: int, access_token: str
    ) -> dict:
        """Get the list of banned members in a given group. Only accessible to group Admins and above. Not applicable to all groups. Check group features.

            Args:
                currentpage (int): Page number (starting with 1). Each page has a fixed size of 50 entries.
                groupId (int): Group ID whose banned members you are fetching
                access_token (str): OAuth token

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastModifiedBy": {
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
                    },
                    {
                        "createdBy": {
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
                    },
                    {
                        "dateBanned": {
                            "Name": "dateBanned",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateExpires": {
                            "Name": "dateExpires",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "comment": {
                            "Name": "comment",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetBannedMembersOfGroup.html#operation_get_GroupV2-GetBannedMembersOfGroup"""

        try:
            self.logger.info("Executing GetBannedMembersOfGroup...")
            url = self.base_url + f"/GroupV2/{groupId}/Banned/".format(
                currentpage=currentpage, groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def AbdicateFoundership(
        self, founderIdNew: int, groupId: int, membershipType: int
    ) -> dict:
        """An administrative method to allow the founder of a group or clan to give up their position to another admin permanently.

            Args:
                founderIdNew (int): The new founder for this group. Must already be a group admin.
                groupId (int): The target group id.
                membershipType (int): Membership type of the provided founderIdNew.

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-AbdicateFoundership.html#operation_post_GroupV2-AbdicateFoundership"""

        try:
            self.logger.info("Executing AbdicateFoundership...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Admin/AbdicateFoundership/{membershipType}/{founderIdNew}/".format(
                    founderIdNew=founderIdNew,
                    groupId=groupId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.POST, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPendingMemberships(
        self, currentpage: int, groupId: int, access_token: str
    ) -> dict:
        """Get the list of users who are awaiting a decision on their application to join a given group. Modified to include application info.

            Args:
                currentpage (int): Page number (starting with 1). Each page has a fixed size of 50 items per page.
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "creationDate": {
                            "Name": "creationDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveState": {
                            "Name": "resolveState",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveDate": {
                            "Name": "resolveDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "resolvedByMembershipId": {
                            "Name": "resolvedByMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "requestMessage": {
                            "Name": "requestMessage",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveMessage": {
                            "Name": "resolveMessage",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetPendingMemberships.html#operation_get_GroupV2-GetPendingMemberships"""

        try:
            self.logger.info("Executing GetPendingMemberships...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/Pending/".format(
                currentpage=currentpage, groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetInvitedIndividuals(
        self, currentpage: int, groupId: int, access_token: str
    ) -> dict:
        """Get the list of users who have been invited into the group.

            Args:
                currentpage (int): Page number (starting with 1). Each page has a fixed size of 50 items per page.
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "groupId": {
                            "Name": "groupId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "creationDate": {
                            "Name": "creationDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveState": {
                            "Name": "resolveState",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveDate": {
                            "Name": "resolveDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "resolvedByMembershipId": {
                            "Name": "resolvedByMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "requestMessage": {
                            "Name": "requestMessage",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "resolveMessage": {
                            "Name": "resolveMessage",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetInvitedIndividuals.html#operation_get_GroupV2-GetInvitedIndividuals"""

        try:
            self.logger.info("Executing GetInvitedIndividuals...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/InvitedIndividuals/".format(
                    currentpage=currentpage, groupId=groupId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ApproveAllPending(
        self, groupId: int, message: str, access_token: str
    ) -> dict:
        """Approve all of the pending users for the given group.

            Args:
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "entityId": {
                "Name": "entityId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "result": {
                "Name": "result",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-ApproveAllPending.html#operation_post_GroupV2-ApproveAllPending"""

        request_body = {"message": message}

        try:
            self.logger.info("Executing ApproveAllPending...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/ApproveAll/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def DenyAllPending(
        self, groupId: int, message: str, access_token: str
    ) -> dict:
        """Deny all of the pending users for the given group.

            Args:
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "entityId": {
                "Name": "entityId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "result": {
                "Name": "result",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-DenyAllPending.html#operation_post_GroupV2-DenyAllPending"""

        request_body = {"message": message}

        try:
            self.logger.info("Executing DenyAllPending...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/DenyAll/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ApprovePendingForList(
        self, groupId: int, memberships: list, message: str, access_token: str
    ) -> dict:
        """Approve all of the pending users for the given group.

            Args:
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "entityId": {
                "Name": "entityId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "result": {
                "Name": "result",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-ApprovePendingForList.html#operation_post_GroupV2-ApprovePendingForList"""

        request_body = {"memberships": memberships, "message": message}

        try:
            self.logger.info("Executing ApprovePendingForList...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/ApproveList/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ApprovePending(
        self,
        groupId: int,
        membershipId: int,
        membershipType: int,
        message: str,
        access_token: str,
    ) -> dict:
        """Approve the given membershipId to join the group/clan as long as they have applied.

            Args:
                groupId (int): ID of the group.
                membershipId (int): The membership id being approved.
                membershipType (int): Membership type of the supplied membership ID.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-ApprovePending.html#operation_post_GroupV2-ApprovePending"""

        request_body = {"message": message}

        try:
            self.logger.info("Executing ApprovePending...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/Approve/{membershipType}/{membershipId}/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def DenyPendingForList(
        self, groupId: int, memberships: list, message: str, access_token: str
    ) -> dict:
        """Deny all of the pending users for the given group that match the passed-in .

            Args:
                groupId (int): ID of the group.
                access_token (str): OAuth token

            Returns:
        {
            "entityId": {
                "Name": "entityId",
                "Type": "int64",
                "Description": "",
                "Attributes": []
            },
            "result": {
                "Name": "result",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-DenyPendingForList.html#operation_post_GroupV2-DenyPendingForList"""

        request_body = {"memberships": memberships, "message": message}

        try:
            self.logger.info("Executing DenyPendingForList...")
            url = self.base_url + f"/GroupV2/{groupId}/Members/DenyList/".format(
                groupId=groupId
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupsForMember(
        self, filter: int, groupType: int, membershipId: int, membershipType: int
    ) -> dict:
        """Get information about the groups that a given member has joined.

            Args:
                filter (int): Filter apply to list of joined groups.
                groupType (int): Type of group the supplied member founded.
                membershipId (int): Membership ID to for which to find founded groups.
                membershipType (int): Membership type of the supplied membership ID.

            Returns:
        {
            "areAllMembershipsInactive": {
                "Name": "areAllMembershipsInactive",
                "Type": "object",
                "Description": "A convenience property that indicates if every membership this user has that is a part of this group are part of an account that is considered inactive - for example, overridden accounts in Cross Save. The key is the Group ID for the group being checked, and the value is true if the users' memberships for that group are all inactive.",
                "Attributes": []
            },
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "member": {
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
                        "group": {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroupsForMember.html#operation_get_GroupV2-GetGroupsForMember"""

        try:
            self.logger.info("Executing GetGroupsForMember...")
            url = (
                self.base_url
                + f"/GroupV2/User/{membershipType}/{membershipId}/{filter}/{groupType}/".format(
                    filter=filter,
                    groupType=groupType,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def RecoverGroupForFounder(
        self, groupType: int, membershipId: int, membershipType: int
    ) -> dict:
        """Allows a founder to manually recover a group they can see in game but not on bungie.net

            Args:
                groupType (int): Type of group the supplied member founded.
                membershipId (int): Membership ID to for which to find founded groups.
                membershipType (int): Membership type of the supplied membership ID.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "member": {
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
                        "group": {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-RecoverGroupForFounder.html#operation_get_GroupV2-RecoverGroupForFounder"""

        try:
            self.logger.info("Executing RecoverGroupForFounder...")
            url = (
                self.base_url
                + f"/GroupV2/Recover/{membershipType}/{membershipId}/{groupType}/".format(
                    groupType=groupType,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPotentialGroupsForMember(
        self, filter: int, groupType: int, membershipId: int, membershipType: int
    ) -> dict:
        """Get information about the groups that a given member has applied to or been invited to.

            Args:
                filter (int): Filter apply to list of potential joined groups.
                groupType (int): Type of group the supplied member applied.
                membershipId (int): Membership ID to for which to find applied groups.
                membershipType (int): Membership type of the supplied membership ID.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "member": {
                            "potentialStatus": {
                                "Name": "potentialStatus",
                                "Type": "int32",
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
                        "group": {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_GroupV2-GetPotentialGroupsForMember.html#operation_get_GroupV2-GetPotentialGroupsForMember"""

        try:
            self.logger.info("Executing GetPotentialGroupsForMember...")
            url = (
                self.base_url
                + f"/GroupV2/User/Potential/{membershipType}/{membershipId}/{filter}/{groupType}/".format(
                    filter=filter,
                    groupType=groupType,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def IndividualGroupInvite(
        self,
        groupId: int,
        membershipId: int,
        membershipType: int,
        message: str,
        access_token: str,
    ) -> dict:
        """Invite a user to join this group.

            Args:
                groupId (int): ID of the group you would like to join.
                membershipId (int): Membership id of the account being invited.
                membershipType (int): MembershipType of the account being invited.
                access_token (str): OAuth token

            Returns:
        {
            "resolution": {
                "Name": "resolution",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-IndividualGroupInvite.html#operation_post_GroupV2-IndividualGroupInvite"""

        request_body = {"message": message}

        try:
            self.logger.info("Executing IndividualGroupInvite...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/IndividualInvite/{membershipType}/{membershipId}/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def IndividualGroupInviteCancel(
        self, groupId: int, membershipId: int, membershipType: int, access_token: str
    ) -> dict:
        """Cancels a pending invitation to join a group.

            Args:
                groupId (int): ID of the group you would like to join.
                membershipId (int): Membership id of the account being cancelled.
                membershipType (int): MembershipType of the account being cancelled.
                access_token (str): OAuth token

            Returns:
        {
            "resolution": {
                "Name": "resolution",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_GroupV2-IndividualGroupInviteCancel.html#operation_post_GroupV2-IndividualGroupInviteCancel"""

        try:
            self.logger.info("Executing IndividualGroupInviteCancel...")
            url = (
                self.base_url
                + f"/GroupV2/{groupId}/Members/IndividualInviteCancel/{membershipType}/{membershipId}/".format(
                    groupId=groupId,
                    membershipId=membershipId,
                    membershipType=membershipType,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)
