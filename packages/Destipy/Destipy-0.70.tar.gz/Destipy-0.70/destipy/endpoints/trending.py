from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Trending:
    """Trending endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetTrendingCategories(self) -> dict:
        """Returns trending items for Bungie.net, collapsed into the first page of items per category. For pagination within a category, call GetTrendingCategory.

            Args:

            Returns:
        {
            "categories": {
                "Name": "categories",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "categoryName": {
                            "Name": "categoryName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "entries": {
                            "results": {
                                "Name": "results",
                                "Type": "array",
                                "Description": "",
                                "Attributes": [],
                                "Array Contents": [
                                    {
                                        "weight": {
                                            "Name": "weight",
                                            "Type": "double",
                                            "Description": "The weighted score of this trending item.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "isFeatured": {
                                            "Name": "isFeatured",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "identifier": {
                                            "Name": "identifier",
                                            "Type": "string",
                                            "Description": "We don't know whether the identifier will be a string, a uint, or a long... so we're going to cast it all to a string. But either way, we need any trending item created to have a single unique identifier for its type.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "entityType": {
                                            "Name": "entityType",
                                            "Type": "int32",
                                            "Description": "An enum - unfortunately - dictating all of the possible kinds of trending items that you might get in your result set, in case you want to do custom rendering or call to get the details of the item.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "displayName": {
                                            "Name": "displayName",
                                            "Type": "string",
                                            "Description": "The localized \"display name/article title/'primary localized identifier'\" of the entity.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "tagline": {
                                            "Name": "tagline",
                                            "Type": "string",
                                            "Description": "If the entity has a localized tagline/subtitle/motto/whatever, that is found here.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "image": {
                                            "Name": "image",
                                            "Type": "string",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "startDate": {
                                            "Name": "startDate",
                                            "Type": "date-time",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable"
                                            ]
                                        }
                                    },
                                    {
                                        "endDate": {
                                            "Name": "endDate",
                                            "Type": "date-time",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable"
                                            ]
                                        }
                                    },
                                    {
                                        "link": {
                                            "Name": "link",
                                            "Type": "string",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "webmVideo": {
                                            "Name": "webmVideo",
                                            "Type": "string",
                                            "Description": "If this is populated, the entry has a related WebM video to show. I am 100% certain I am going to regret putting this directly on TrendingEntry, but it will work so yolo",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "mp4Video": {
                                            "Name": "mp4Video",
                                            "Type": "string",
                                            "Description": "If this is populated, the entry has a related MP4 video to show. I am 100% certain I am going to regret putting this directly on TrendingEntry, but it will work so yolo",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "featureImage": {
                                            "Name": "featureImage",
                                            "Type": "string",
                                            "Description": "If isFeatured, this image will be populated with whatever the featured image is. Note that this will likely be a very large image, so don't use it all the time.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "items": {
                                            "Name": "items",
                                            "Type": "array",
                                            "Description": "If the item is of entityType TrendingEntryType.Container, it may have items - also Trending Entries - contained within it. This is the ordered list of those to display under the Container's header.",
                                            "Attributes": []
                                        }
                                    },
                                    {
                                        "creationDate": {
                                            "Name": "creationDate",
                                            "Type": "date-time",
                                            "Description": "If the entry has a date at which it was created, this is that date.",
                                            "Attributes": [
                                                "Nullable"
                                            ]
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
                    },
                    {
                        "categoryId": {
                            "Name": "categoryId",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Trending-GetTrendingCategories.html#operation_get_Trending-GetTrendingCategories"""

        try:
            self.logger.info("Executing GetTrendingCategories...")
            url = self.base_url + "/Trending/Categories/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetTrendingCategory(self, categoryId: str, pageNumber: int) -> dict:
        """Returns paginated lists of trending items for a category.

            Args:
                categoryId (str): The ID of the category for whom you want additional results.
                pageNumber (int): The page # of results to return.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "weight": {
                            "Name": "weight",
                            "Type": "double",
                            "Description": "The weighted score of this trending item.",
                            "Attributes": []
                        }
                    },
                    {
                        "isFeatured": {
                            "Name": "isFeatured",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "identifier": {
                            "Name": "identifier",
                            "Type": "string",
                            "Description": "We don't know whether the identifier will be a string, a uint, or a long... so we're going to cast it all to a string. But either way, we need any trending item created to have a single unique identifier for its type.",
                            "Attributes": []
                        }
                    },
                    {
                        "entityType": {
                            "Name": "entityType",
                            "Type": "int32",
                            "Description": "An enum - unfortunately - dictating all of the possible kinds of trending items that you might get in your result set, in case you want to do custom rendering or call to get the details of the item.",
                            "Attributes": []
                        }
                    },
                    {
                        "displayName": {
                            "Name": "displayName",
                            "Type": "string",
                            "Description": "The localized \"display name/article title/'primary localized identifier'\" of the entity.",
                            "Attributes": []
                        }
                    },
                    {
                        "tagline": {
                            "Name": "tagline",
                            "Type": "string",
                            "Description": "If the entity has a localized tagline/subtitle/motto/whatever, that is found here.",
                            "Attributes": []
                        }
                    },
                    {
                        "image": {
                            "Name": "image",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "startDate": {
                            "Name": "startDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "endDate": {
                            "Name": "endDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "link": {
                            "Name": "link",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "webmVideo": {
                            "Name": "webmVideo",
                            "Type": "string",
                            "Description": "If this is populated, the entry has a related WebM video to show. I am 100% certain I am going to regret putting this directly on TrendingEntry, but it will work so yolo",
                            "Attributes": []
                        }
                    },
                    {
                        "mp4Video": {
                            "Name": "mp4Video",
                            "Type": "string",
                            "Description": "If this is populated, the entry has a related MP4 video to show. I am 100% certain I am going to regret putting this directly on TrendingEntry, but it will work so yolo",
                            "Attributes": []
                        }
                    },
                    {
                        "featureImage": {
                            "Name": "featureImage",
                            "Type": "string",
                            "Description": "If isFeatured, this image will be populated with whatever the featured image is. Note that this will likely be a very large image, so don't use it all the time.",
                            "Attributes": []
                        }
                    },
                    {
                        "items": {
                            "Name": "items",
                            "Type": "array",
                            "Description": "If the item is of entityType TrendingEntryType.Container, it may have items - also Trending Entries - contained within it. This is the ordered list of those to display under the Container's header.",
                            "Attributes": []
                        }
                    },
                    {
                        "creationDate": {
                            "Name": "creationDate",
                            "Type": "date-time",
                            "Description": "If the entry has a date at which it was created, this is that date.",
                            "Attributes": [
                                "Nullable"
                            ]
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Trending-GetTrendingCategory.html#operation_get_Trending-GetTrendingCategory"""

        try:
            self.logger.info("Executing GetTrendingCategory...")
            url = (
                self.base_url
                + f"/Trending/Categories/{categoryId}/{pageNumber}/".format(
                    categoryId=categoryId, pageNumber=pageNumber
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetTrendingEntryDetail(
        self, identifier: str, trendingEntryType: int
    ) -> dict:
        """Returns the detailed results for a specific trending entry. Note that trending entries are uniquely identified by a combination of *both* the TrendingEntryType *and* the identifier: the identifier alone is not guaranteed to be globally unique.

            Args:
                identifier (str): The identifier for the entity to be returned.
                trendingEntryType (int): The type of entity to be returned.

            Returns:
        {
            "identifier": {
                "Name": "identifier",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "entityType": {
                "Name": "entityType",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "news": {
                "article": {
                    "contentId": {
                        "Name": "contentId",
                        "Type": "int64",
                        "Description": "",
                        "Attributes": []
                    },
                    "cType": {
                        "Name": "cType",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "cmsPath": {
                        "Name": "cmsPath",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "creationDate": {
                        "Name": "creationDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "modifyDate": {
                        "Name": "modifyDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "allowComments": {
                        "Name": "allowComments",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "hasAgeGate": {
                        "Name": "hasAgeGate",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "minimumAge": {
                        "Name": "minimumAge",
                        "Type": "int32",
                        "Description": "",
                        "Attributes": []
                    },
                    "ratingImagePath": {
                        "Name": "ratingImagePath",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "author": {
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
                    },
                    "autoEnglishPropertyFallback": {
                        "Name": "autoEnglishPropertyFallback",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "properties": {
                        "Name": "properties",
                        "Type": "object",
                        "Description": "Firehose content is really a collection of metadata and \"properties\", which are the potentially-but-not-strictly localizable data that comprises the meat of whatever content is being shown.As Cole Porter would have crooned, \"Anything Goes\" with Firehose properties. They are most often strings, but they can theoretically be anything. They are JSON encoded, and could be JSON structures, simple strings, numbers etc... The Content Type of the item (cType) will describe the properties, and thus how they ought to be deserialized.",
                        "Attributes": []
                    },
                    "representations": {
                        "Name": "representations",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "name": {
                                    "Name": "name",
                                    "Type": "string",
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
                            },
                            {
                                "validationString": {
                                    "Name": "validationString",
                                    "Type": "string",
                                    "Description": "",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "tags": {
                        "Name": "tags",
                        "Type": "array",
                        "Description": "NOTE: Tags will always be lower case.",
                        "Attributes": [],
                        "Array Contents": "string"
                    },
                    "commentSummary": {
                        "topicId": {
                            "Name": "topicId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        },
                        "commentCount": {
                            "Name": "commentCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                }
            },
            "support": {
                "article": {
                    "contentId": {
                        "Name": "contentId",
                        "Type": "int64",
                        "Description": "",
                        "Attributes": []
                    },
                    "cType": {
                        "Name": "cType",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "cmsPath": {
                        "Name": "cmsPath",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "creationDate": {
                        "Name": "creationDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "modifyDate": {
                        "Name": "modifyDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "allowComments": {
                        "Name": "allowComments",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "hasAgeGate": {
                        "Name": "hasAgeGate",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "minimumAge": {
                        "Name": "minimumAge",
                        "Type": "int32",
                        "Description": "",
                        "Attributes": []
                    },
                    "ratingImagePath": {
                        "Name": "ratingImagePath",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "author": {
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
                    },
                    "autoEnglishPropertyFallback": {
                        "Name": "autoEnglishPropertyFallback",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "properties": {
                        "Name": "properties",
                        "Type": "object",
                        "Description": "Firehose content is really a collection of metadata and \"properties\", which are the potentially-but-not-strictly localizable data that comprises the meat of whatever content is being shown.As Cole Porter would have crooned, \"Anything Goes\" with Firehose properties. They are most often strings, but they can theoretically be anything. They are JSON encoded, and could be JSON structures, simple strings, numbers etc... The Content Type of the item (cType) will describe the properties, and thus how they ought to be deserialized.",
                        "Attributes": []
                    },
                    "representations": {
                        "Name": "representations",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "name": {
                                    "Name": "name",
                                    "Type": "string",
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
                            },
                            {
                                "validationString": {
                                    "Name": "validationString",
                                    "Type": "string",
                                    "Description": "",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "tags": {
                        "Name": "tags",
                        "Type": "array",
                        "Description": "NOTE: Tags will always be lower case.",
                        "Attributes": [],
                        "Array Contents": "string"
                    },
                    "commentSummary": {
                        "topicId": {
                            "Name": "topicId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        },
                        "commentCount": {
                            "Name": "commentCount",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                }
            },
            "destinyItem": {
                "itemHash": {
                    "Name": "itemHash",
                    "Type": "uint32",
                    "Description": "",
                    "Attributes": []
                }
            },
            "destinyActivity": {
                "activityHash": {
                    "Name": "activityHash",
                    "Type": "uint32",
                    "Description": "",
                    "Attributes": []
                },
                "status": {
                    "challengeObjectiveHashes": {
                        "Name": "challengeObjectiveHashes",
                        "Type": "array",
                        "Description": "Active Challenges for the activity, if any - represented as hashes for DestinyObjectiveDefinitions.",
                        "Attributes": [
                            "Mapped to Definition"
                        ],
                        "Array Contents": "uint32"
                    },
                    "modifierHashes": {
                        "Name": "modifierHashes",
                        "Type": "array",
                        "Description": "The active modifiers on this activity, if any - represented as hashes for DestinyActivityModifierDefinitions.",
                        "Attributes": [
                            "Mapped to Definition"
                        ],
                        "Array Contents": "uint32"
                    },
                    "rewardTooltipItems": {
                        "Name": "rewardTooltipItems",
                        "Type": "array",
                        "Description": "If the activity itself provides any specific \"mock\" rewards, this will be the items and their quantity.Why \"mock\", you ask? Because these are the rewards as they are represented in the tooltip of the Activity.These are often pointers to fake items that look good in a tooltip, but represent an abstract concept of what you will get for a reward rather than the specific items you may obtain.",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "itemHash": {
                                    "Name": "itemHash",
                                    "Type": "uint32",
                                    "Description": "The hash identifier for the item in question. Use it to look up the item's DestinyInventoryItemDefinition.",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "itemInstanceId": {
                                    "Name": "itemInstanceId",
                                    "Type": "int64",
                                    "Description": "If this quantity is referring to a specific instance of an item, this will have the item's instance ID. Normally, this will be null.",
                                    "Attributes": [
                                        "Nullable"
                                    ]
                                }
                            },
                            {
                                "quantity": {
                                    "Name": "quantity",
                                    "Type": "int32",
                                    "Description": "The amount of the item needed/available depending on the context of where DestinyItemQuantity is being used.",
                                    "Attributes": []
                                }
                            },
                            {
                                "hasConditionalVisibility": {
                                    "Name": "hasConditionalVisibility",
                                    "Type": "boolean",
                                    "Description": "Indicates that this item quantity may be conditionally shown or hidden, based on various sources of state. For example: server flags, account state, or character progress.",
                                    "Attributes": []
                                }
                            }
                        ]
                    }
                }
            },
            "destinyRitual": {
                "image": {
                    "Name": "image",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "icon": {
                    "Name": "icon",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "title": {
                    "Name": "title",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "subtitle": {
                    "Name": "subtitle",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "dateStart": {
                    "Name": "dateStart",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "dateEnd": {
                    "Name": "dateEnd",
                    "Type": "date-time",
                    "Description": "",
                    "Attributes": [
                        "Nullable"
                    ]
                },
                "milestoneDetails": {
                    "Name": "milestoneDetails",
                    "Type": "object",
                    "Description": "A destiny event does not necessarily have a related Milestone, but if it does the details will be returned here.",
                    "Attributes": []
                },
                "eventContent": {
                    "Name": "eventContent",
                    "Type": "object",
                    "Description": "A destiny event will not necessarily have milestone \"custom content\", but if it does the details will be here.",
                    "Attributes": []
                }
            },
            "creation": {
                "media": {
                    "Name": "media",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "title": {
                    "Name": "title",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "author": {
                    "Name": "author",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "authorMembershipId": {
                    "Name": "authorMembershipId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "postId": {
                    "Name": "postId",
                    "Type": "int64",
                    "Description": "",
                    "Attributes": []
                },
                "body": {
                    "Name": "body",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "upvotes": {
                    "Name": "upvotes",
                    "Type": "int32",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Trending-GetTrendingEntryDetail.html#operation_get_Trending-GetTrendingEntryDetail"""

        try:
            self.logger.info("Executing GetTrendingEntryDetail...")
            url = (
                self.base_url
                + f"/Trending/Details/{trendingEntryType}/{identifier}/".format(
                    identifier=identifier, trendingEntryType=trendingEntryType
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
