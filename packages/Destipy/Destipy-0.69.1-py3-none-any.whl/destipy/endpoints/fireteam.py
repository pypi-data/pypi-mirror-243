from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Fireteam:
    """Fireteam endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetActivePrivateClanFireteamCount(
        self,
        groupId: int,
    ) -> dict:
        """Gets a count of all active non-public fireteams for the specified clan. Maximum value returned is 25.

            Args:
                groupId (int): The group id of the clan.

            Returns:
        {
            "Name": "Response",
            "Type": "int32",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Fireteam-GetActivePrivateClanFireteamCount.html#operation_get_Fireteam-GetActivePrivateClanFireteamCount"""

        try:
            self.logger.info("Executing GetActivePrivateClanFireteamCount...")
            url = self.base_url + f"/Fireteam/Clan/{groupId}/ActiveCount/".format(
                groupId=groupId
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableClanFireteams(
        self,
        activityType: int,
        dateRange: int,
        groupId: int,
        page: int,
        platform: int,
        publicOnly: int,
        slotFilter: int,
        excludeImmediate: bool,
        langFilter: str,
    ) -> dict:
        """Gets a listing of all of this clan's fireteams that are have available slots. Caller is not checked for join criteria so caching is maximized.

            Args:
                activityType (int): The activity type to filter by.
                dateRange (int): The date range to grab available fireteams.
                groupId (int): The group id of the clan.
                page (int): Zero based page
                platform (int): The platform filter.
                publicOnly (int): Determines public/private filtering.
                slotFilter (int): Filters based on available slots
                excludeImmediate (bool): If you wish the result to exclude immediate fireteams, set this to true. Immediate-only can be forced using the dateRange enum.
                langFilter (str): An optional language filter.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "fireteamId": {
                            "Name": "fireteamId",
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
                        "platform": {
                            "Name": "platform",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "activityType": {
                            "Name": "activityType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isImmediate": {
                            "Name": "isImmediate",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "scheduledTime": {
                            "Name": "scheduledTime",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "ownerMembershipId": {
                            "Name": "ownerMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "playerSlotCount": {
                            "Name": "playerSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "alternateSlotCount": {
                            "Name": "alternateSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "availablePlayerSlotCount": {
                            "Name": "availablePlayerSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "availableAlternateSlotCount": {
                            "Name": "availableAlternateSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "title": {
                            "Name": "title",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateCreated": {
                            "Name": "dateCreated",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateModified": {
                            "Name": "dateModified",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isPublic": {
                            "Name": "isPublic",
                            "Type": "boolean",
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
                        "isValid": {
                            "Name": "isValid",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "datePlayerModified": {
                            "Name": "datePlayerModified",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "titleBeforeModeration": {
                            "Name": "titleBeforeModeration",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ownerCurrentGuardianRankSnapshot": {
                            "Name": "ownerCurrentGuardianRankSnapshot",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "ownerHighestLifetimeGuardianRankSnapshot": {
                            "Name": "ownerHighestLifetimeGuardianRankSnapshot",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "ownerTotalCommendationScoreSnapshot": {
                            "Name": "ownerTotalCommendationScoreSnapshot",
                            "Type": "int32",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Fireteam-GetAvailableClanFireteams.html#operation_get_Fireteam-GetAvailableClanFireteams"""

        try:
            self.logger.info("Executing GetAvailableClanFireteams...")
            url = (
                self.base_url
                + f"/Fireteam/Clan/{groupId}/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{publicOnly}/{page}/".format(
                    activityType=activityType,
                    dateRange=dateRange,
                    groupId=groupId,
                    page=page,
                    platform=platform,
                    publicOnly=publicOnly,
                    slotFilter=slotFilter,
                    excludeImmediate=excludeImmediate,
                    langFilter=langFilter,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchPublicAvailableClanFireteams(
        self,
        activityType: int,
        dateRange: int,
        page: int,
        platform: int,
        slotFilter: int,
        excludeImmediate: bool,
        langFilter: str,
    ) -> dict:
        """Gets a listing of all public fireteams starting now with open slots. Caller is not checked for join criteria so caching is maximized.

            Args:
                activityType (int): The activity type to filter by.
                dateRange (int): The date range to grab available fireteams.
                page (int): Zero based page
                platform (int): The platform filter.
                slotFilter (int): Filters based on available slots
                excludeImmediate (bool): If you wish the result to exclude immediate fireteams, set this to true. Immediate-only can be forced using the dateRange enum.
                langFilter (str): An optional language filter.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "fireteamId": {
                            "Name": "fireteamId",
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
                        "platform": {
                            "Name": "platform",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "activityType": {
                            "Name": "activityType",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isImmediate": {
                            "Name": "isImmediate",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "scheduledTime": {
                            "Name": "scheduledTime",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "ownerMembershipId": {
                            "Name": "ownerMembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "playerSlotCount": {
                            "Name": "playerSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "alternateSlotCount": {
                            "Name": "alternateSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "availablePlayerSlotCount": {
                            "Name": "availablePlayerSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "availableAlternateSlotCount": {
                            "Name": "availableAlternateSlotCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "title": {
                            "Name": "title",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateCreated": {
                            "Name": "dateCreated",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateModified": {
                            "Name": "dateModified",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "isPublic": {
                            "Name": "isPublic",
                            "Type": "boolean",
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
                        "isValid": {
                            "Name": "isValid",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "datePlayerModified": {
                            "Name": "datePlayerModified",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "titleBeforeModeration": {
                            "Name": "titleBeforeModeration",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ownerCurrentGuardianRankSnapshot": {
                            "Name": "ownerCurrentGuardianRankSnapshot",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "ownerHighestLifetimeGuardianRankSnapshot": {
                            "Name": "ownerHighestLifetimeGuardianRankSnapshot",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": [
                                "Mapped to Definition"
                            ]
                        }
                    },
                    {
                        "ownerTotalCommendationScoreSnapshot": {
                            "Name": "ownerTotalCommendationScoreSnapshot",
                            "Type": "int32",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Fireteam-SearchPublicAvailableClanFireteams.html#operation_get_Fireteam-SearchPublicAvailableClanFireteams"""

        try:
            self.logger.info("Executing SearchPublicAvailableClanFireteams...")
            url = (
                self.base_url
                + f"/Fireteam/Search/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{page}/".format(
                    activityType=activityType,
                    dateRange=dateRange,
                    page=page,
                    platform=platform,
                    slotFilter=slotFilter,
                    excludeImmediate=excludeImmediate,
                    langFilter=langFilter,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMyClanFireteams(
        self,
        groupId: int,
        includeClosed: bool,
        page: int,
        platform: int,
        groupFilter: bool,
        langFilter: str,
    ) -> dict:
        """Gets a listing of all fireteams that caller is an applicant, a member, or an alternate of.

            Args:
                groupId (int): The group id of the clan. (This parameter is ignored unless the optional query parameter groupFilter is true).
                includeClosed (bool): If true, return fireteams that have been closed.
                page (int): Deprecated parameter, ignored.
                platform (int): The platform filter.
                groupFilter (bool): If true, filter by clan. Otherwise, ignore the clan and show all of the user's fireteams.
                langFilter (str): An optional language filter.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "Summary": {
                            "fireteamId": {
                                "Name": "fireteamId",
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
                            "platform": {
                                "Name": "platform",
                                "Type": "byte",
                                "Description": "",
                                "Attributes": []
                            },
                            "activityType": {
                                "Name": "activityType",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "isImmediate": {
                                "Name": "isImmediate",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "scheduledTime": {
                                "Name": "scheduledTime",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "ownerMembershipId": {
                                "Name": "ownerMembershipId",
                                "Type": "int64",
                                "Description": "",
                                "Attributes": []
                            },
                            "playerSlotCount": {
                                "Name": "playerSlotCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "alternateSlotCount": {
                                "Name": "alternateSlotCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "availablePlayerSlotCount": {
                                "Name": "availablePlayerSlotCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "availableAlternateSlotCount": {
                                "Name": "availableAlternateSlotCount",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            },
                            "title": {
                                "Name": "title",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "dateCreated": {
                                "Name": "dateCreated",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "dateModified": {
                                "Name": "dateModified",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": [
                                    "Nullable"
                                ]
                            },
                            "isPublic": {
                                "Name": "isPublic",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "locale": {
                                "Name": "locale",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "isValid": {
                                "Name": "isValid",
                                "Type": "boolean",
                                "Description": "",
                                "Attributes": []
                            },
                            "datePlayerModified": {
                                "Name": "datePlayerModified",
                                "Type": "date-time",
                                "Description": "",
                                "Attributes": []
                            },
                            "titleBeforeModeration": {
                                "Name": "titleBeforeModeration",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "ownerCurrentGuardianRankSnapshot": {
                                "Name": "ownerCurrentGuardianRankSnapshot",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": [
                                    "Mapped to Definition"
                                ]
                            },
                            "ownerHighestLifetimeGuardianRankSnapshot": {
                                "Name": "ownerHighestLifetimeGuardianRankSnapshot",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": [
                                    "Mapped to Definition"
                                ]
                            },
                            "ownerTotalCommendationScoreSnapshot": {
                                "Name": "ownerTotalCommendationScoreSnapshot",
                                "Type": "int32",
                                "Description": "",
                                "Attributes": []
                            }
                        }
                    },
                    {
                        "Members": {
                            "Name": "Members",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "Alternates": {
                            "Name": "Alternates",
                            "Type": "array",
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Fireteam-GetMyClanFireteams.html#operation_get_Fireteam-GetMyClanFireteams"""

        try:
            self.logger.info("Executing GetMyClanFireteams...")
            url = (
                self.base_url
                + f"/Fireteam/Clan/{groupId}/My/{platform}/{includeClosed}/{page}/".format(
                    groupId=groupId,
                    includeClosed=includeClosed,
                    page=page,
                    platform=platform,
                    groupFilter=groupFilter,
                    langFilter=langFilter,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanFireteam(
        self,
        fireteamId: int,
        groupId: int,
    ) -> dict:
        """Gets a specific fireteam.

            Args:
                fireteamId (int): The unique id of the fireteam.
                groupId (int): The group id of the clan.

            Returns:
        {
            "Summary": {
                "fireteamId": {
                    "Name": "fireteamId",
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
                "platform": {
                    "Name": "platform",
                    "Type": "byte",
                    "Description": "",
                    "Attributes": []
                },
                "activityType": {
                    "Name": "activityType",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "isImmediate": {
                    "Name": "isImmediate",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "scheduledTime": {
                    "Name": "scheduledTime",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "ownerMembershipId": {
                    "Name": "ownerMembershipId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "playerSlotCount": {
                    "Name": "playerSlotCount",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "alternateSlotCount": {
                    "Name": "alternateSlotCount",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "availablePlayerSlotCount": {
                    "Name": "availablePlayerSlotCount",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "availableAlternateSlotCount": {
                    "Name": "availableAlternateSlotCount",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                },
                "title": {
                    "Name": "title",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "dateCreated": {
                    "Name": "dateCreated",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": []
                },
                "dateModified": {
                    "Name": "dateModified",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "isPublic": {
                    "Name": "isPublic",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "locale": {
                    "Name": "locale",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "isValid": {
                    "Name": "isValid",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "datePlayerModified": {
                    "Name": "datePlayerModified",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": []
                },
                "titleBeforeModeration": {
                    "Name": "titleBeforeModeration",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ownerCurrentGuardianRankSnapshot": {
                    "Name": "ownerCurrentGuardianRankSnapshot",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": [
                        "Mapped to Definition"
                    ]
                },
                "ownerHighestLifetimeGuardianRankSnapshot": {
                    "Name": "ownerHighestLifetimeGuardianRankSnapshot",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": [
                        "Mapped to Definition"
                    ]
                },
                "ownerTotalCommendationScoreSnapshot": {
                    "Name": "ownerTotalCommendationScoreSnapshot",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                }
            },
            "Members": {
                "Name": "Members",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "destinyUserInfo": {
                            "FireteamDisplayName": {
                                "Name": "FireteamDisplayName",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "FireteamMembershipType": {
                                "Name": "FireteamMembershipType",
                                "Type": "int32",
                                "Description": "",
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
                        "characterId": {
                            "Name": "characterId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateJoined": {
                            "Name": "dateJoined",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "hasMicrophone": {
                            "Name": "hasMicrophone",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastPlatformInviteAttemptDate": {
                            "Name": "lastPlatformInviteAttemptDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastPlatformInviteAttemptResult": {
                            "Name": "lastPlatformInviteAttemptResult",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "Alternates": {
                "Name": "Alternates",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "destinyUserInfo": {
                            "FireteamDisplayName": {
                                "Name": "FireteamDisplayName",
                                "Type": "string",
                                "Description": "",
                                "Attributes": []
                            },
                            "FireteamMembershipType": {
                                "Name": "FireteamMembershipType",
                                "Type": "int32",
                                "Description": "",
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
                        "characterId": {
                            "Name": "characterId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "dateJoined": {
                            "Name": "dateJoined",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "hasMicrophone": {
                            "Name": "hasMicrophone",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastPlatformInviteAttemptDate": {
                            "Name": "lastPlatformInviteAttemptDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "lastPlatformInviteAttemptResult": {
                            "Name": "lastPlatformInviteAttemptResult",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Fireteam-GetClanFireteam.html#operation_get_Fireteam-GetClanFireteam"""

        try:
            self.logger.info("Executing GetClanFireteam...")
            url = (
                self.base_url
                + f"/Fireteam/Clan/{groupId}/Summary/{fireteamId}/".format(
                    fireteamId=fireteamId, groupId=groupId
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
