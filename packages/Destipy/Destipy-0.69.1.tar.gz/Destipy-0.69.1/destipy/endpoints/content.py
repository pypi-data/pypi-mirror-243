from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Content:
    """Content endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetContentType(
        self,
        type: str,
    ) -> dict:
        """Gets an object describing a particular variant of content.

            Args:
                type (str):

            Returns:
        {
            "cType": {
                "Name": "cType",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "name": {
                "Name": "name",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "contentDescription": {
                "Name": "contentDescription",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "previewImage": {
                "Name": "previewImage",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "priority": {
                "Name": "priority",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "reminder": {
                "Name": "reminder",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "properties": {
                "Name": "properties",
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
                        "rootPropertyName": {
                            "Name": "rootPropertyName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "readableName": {
                            "Name": "readableName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "value": {
                            "Name": "value",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "propertyDescription": {
                            "Name": "propertyDescription",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "localizable": {
                            "Name": "localizable",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "fallback": {
                            "Name": "fallback",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "enabled": {
                            "Name": "enabled",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "order": {
                            "Name": "order",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "visible": {
                            "Name": "visible",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isTitle": {
                            "Name": "isTitle",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "required": {
                            "Name": "required",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "maxLength": {
                            "Name": "maxLength",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "maxByteLength": {
                            "Name": "maxByteLength",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "maxFileSize": {
                            "Name": "maxFileSize",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "regexp": {
                            "Name": "regexp",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "validateAs": {
                            "Name": "validateAs",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "rssAttribute": {
                            "Name": "rssAttribute",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "visibleDependency": {
                            "Name": "visibleDependency",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "visibleOn": {
                            "Name": "visibleOn",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "datatype": {
                            "Name": "datatype",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "attributes": {
                            "Name": "attributes",
                            "Type": "object",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "childProperties": {
                            "Name": "childProperties",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "contentTypeAllowed": {
                            "Name": "contentTypeAllowed",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "bindToProperty": {
                            "Name": "bindToProperty",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "boundRegex": {
                            "Name": "boundRegex",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "representationSelection": {
                            "Name": "representationSelection",
                            "Type": "object",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "defaultValues": {
                            "Name": "defaultValues",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isExternalAllowed": {
                            "Name": "isExternalAllowed",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "propertySection": {
                            "Name": "propertySection",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "weight": {
                            "Name": "weight",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "entitytype": {
                            "Name": "entitytype",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isCombo": {
                            "Name": "isCombo",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "suppressProperty": {
                            "Name": "suppressProperty",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "legalContentTypes": {
                            "Name": "legalContentTypes",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "representationValidationString": {
                            "Name": "representationValidationString",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "minWidth": {
                            "Name": "minWidth",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "maxWidth": {
                            "Name": "maxWidth",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "minHeight": {
                            "Name": "minHeight",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "maxHeight": {
                            "Name": "maxHeight",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isVideo": {
                            "Name": "isVideo",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "isImage": {
                            "Name": "isImage",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "tagMetadata": {
                "Name": "tagMetadata",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "description": {
                            "Name": "description",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "order": {
                            "Name": "order",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "items": {
                            "Name": "items",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "datatype": {
                            "Name": "datatype",
                            "Type": "string",
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
                        "isRequired": {
                            "Name": "isRequired",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "tagMetadataItems": {
                "Name": "tagMetadataItems",
                "Type": "object",
                "Description": "",
                "Attributes": []
            },
            "usageExamples": {
                "Name": "usageExamples",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": "string"
            },
            "showInContentEditor": {
                "Name": "showInContentEditor",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "typeOf": {
                "Name": "typeOf",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "bindIdentifierToProperty": {
                "Name": "bindIdentifierToProperty",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "boundRegex": {
                "Name": "boundRegex",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "forceIdentifierBinding": {
                "Name": "forceIdentifierBinding",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "allowComments": {
                "Name": "allowComments",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "autoEnglishPropertyFallback": {
                "Name": "autoEnglishPropertyFallback",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "bulkUploadable": {
                "Name": "bulkUploadable",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "previews": {
                "Name": "previews",
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
                        "itemInSet": {
                            "Name": "itemInSet",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "setTag": {
                            "Name": "setTag",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "setNesting": {
                            "Name": "setNesting",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "useSetId": {
                            "Name": "useSetId",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "suppressCmsPath": {
                "Name": "suppressCmsPath",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "propertySections": {
                "Name": "propertySections",
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
                        "readableName": {
                            "Name": "readableName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "collapsed": {
                            "Name": "collapsed",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-GetContentType.html#operation_get_Content-GetContentType"""

        try:
            self.logger.info("Executing GetContentType...")
            url = self.base_url + f"/Content/GetContentType/{type}/".format(type=type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetContentById(
        self,
        id: int,
        locale: str,
        head: bool,
    ) -> dict:
        """Returns a content item referenced by id

            Args:
                id (int):
                locale (str):
                head (bool): false

            Returns:
        {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-GetContentById.html#operation_get_Content-GetContentById"""

        try:
            self.logger.info("Executing GetContentById...")
            url = self.base_url + f"/Content/GetContentById/{id}/{locale}/".format(
                id=id, locale=locale, head=head
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetContentByTagAndType(
        self,
        locale: str,
        tag: str,
        type: str,
        head: bool,
    ) -> dict:
        """Returns the newest item that matches a given tag and Content Type.

            Args:
                locale (str):
                tag (str):
                type (str):
                head (bool): Not used.

            Returns:
        {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-GetContentByTagAndType.html#operation_get_Content-GetContentByTagAndType"""

        try:
            self.logger.info("Executing GetContentByTagAndType...")
            url = (
                self.base_url
                + f"/Content/GetContentByTagAndType/{tag}/{type}/{locale}/".format(
                    locale=locale, tag=tag, type=type, head=head
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchContentWithText(
        self,
        locale: str,
        ctype: str,
        currentpage: int,
        head: bool,
        searchtext: str,
        source: str,
        tag: str,
    ) -> dict:
        """Gets content based on querystring information passed in. Provides basic search and text search capabilities.

            Args:
                locale (str):
                ctype (str): Content type tag: Help, News, etc. Supply multiple ctypes separated by space.
                currentpage (int): Page number for the search results, starting with page 1.
                head (bool): Not used.
                searchtext (str): Word or phrase for the search.
                source (str): For analytics, hint at the part of the app that triggered the search. Optional.
                tag (str): Tag used on the content to be searched.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "contentId": {
                            "Name": "contentId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cType": {
                            "Name": "cType",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cmsPath": {
                            "Name": "cmsPath",
                            "Type": "string",
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
                        "modifyDate": {
                            "Name": "modifyDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "allowComments": {
                            "Name": "allowComments",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "hasAgeGate": {
                            "Name": "hasAgeGate",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "minimumAge": {
                            "Name": "minimumAge",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ratingImagePath": {
                            "Name": "ratingImagePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
                        "autoEnglishPropertyFallback": {
                            "Name": "autoEnglishPropertyFallback",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "properties": {
                            "Name": "properties",
                            "Type": "object",
                            "Description": "Firehose content is really a collection of metadata and \"properties\", which are the potentially-but-not-strictly localizable data that comprises the meat of whatever content is being shown.As Cole Porter would have crooned, \"Anything Goes\" with Firehose properties. They are most often strings, but they can theoretically be anything. They are JSON encoded, and could be JSON structures, simple strings, numbers etc... The Content Type of the item (cType) will describe the properties, and thus how they ought to be deserialized.",
                            "Attributes": []
                        }
                    },
                    {
                        "representations": {
                            "Name": "representations",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "tags": {
                            "Name": "tags",
                            "Type": "array",
                            "Description": "NOTE: Tags will always be lower case.",
                            "Attributes": []
                        }
                    },
                    {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-SearchContentWithText.html#operation_get_Content-SearchContentWithText"""

        try:
            self.logger.info("Executing SearchContentWithText...")
            url = self.base_url + f"/Content/Search/{locale}/".format(
                locale=locale,
                ctype=ctype,
                currentpage=currentpage,
                head=head,
                searchtext=searchtext,
                source=source,
                tag=tag,
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchContentByTagAndType(
        self,
        locale: str,
        tag: str,
        type: str,
        currentpage: int,
        head: bool,
        itemsperpage: int,
    ) -> dict:
        """Searches for Content Items that match the given Tag and Content Type.

            Args:
                locale (str):
                tag (str):
                type (str):
                currentpage (int): Page number for the search results starting with page 1.
                head (bool): Not used.
                itemsperpage (int): Not used.

            Returns:
        {
            "results": {
                "Name": "results",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "contentId": {
                            "Name": "contentId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cType": {
                            "Name": "cType",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "cmsPath": {
                            "Name": "cmsPath",
                            "Type": "string",
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
                        "modifyDate": {
                            "Name": "modifyDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "allowComments": {
                            "Name": "allowComments",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "hasAgeGate": {
                            "Name": "hasAgeGate",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "minimumAge": {
                            "Name": "minimumAge",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ratingImagePath": {
                            "Name": "ratingImagePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
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
                        }
                    },
                    {
                        "autoEnglishPropertyFallback": {
                            "Name": "autoEnglishPropertyFallback",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "properties": {
                            "Name": "properties",
                            "Type": "object",
                            "Description": "Firehose content is really a collection of metadata and \"properties\", which are the potentially-but-not-strictly localizable data that comprises the meat of whatever content is being shown.As Cole Porter would have crooned, \"Anything Goes\" with Firehose properties. They are most often strings, but they can theoretically be anything. They are JSON encoded, and could be JSON structures, simple strings, numbers etc... The Content Type of the item (cType) will describe the properties, and thus how they ought to be deserialized.",
                            "Attributes": []
                        }
                    },
                    {
                        "representations": {
                            "Name": "representations",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "tags": {
                            "Name": "tags",
                            "Type": "array",
                            "Description": "NOTE: Tags will always be lower case.",
                            "Attributes": []
                        }
                    },
                    {
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


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-SearchContentByTagAndType.html#operation_get_Content-SearchContentByTagAndType"""

        try:
            self.logger.info("Executing SearchContentByTagAndType...")
            url = (
                self.base_url
                + f"/Content/SearchContentByTagAndType/{tag}/{type}/{locale}/".format(
                    locale=locale,
                    tag=tag,
                    type=type,
                    currentpage=currentpage,
                    head=head,
                    itemsperpage=itemsperpage,
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchHelpArticles(
        self,
        searchtext: str,
        size: str,
    ) -> dict:
        """Search for Help Articles.

            Args:
                searchtext (str):
                size (str):

            Returns:
        {
            "Name": "Response",
            "Type": "object",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-SearchHelpArticles.html#operation_get_Content-SearchHelpArticles"""

        try:
            self.logger.info("Executing SearchHelpArticles...")
            url = (
                self.base_url
                + f"/Content/SearchHelpArticles/{searchtext}/{size}/".format(
                    searchtext=searchtext, size=size
                )
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def RssNewsArticles(
        self,
        pageToken: str,
        categoryfilter: str,
        includebody: bool,
    ) -> dict:
        """Returns a JSON string response that is the RSS feed for news articles.

            Args:
                pageToken (str): Zero-based pagination token for paging through result sets.
                categoryfilter (str): Optionally filter response to only include news items in a certain category.
                includebody (bool): Optionally include full content body for each news item.

            Returns:
        {
            "CurrentPaginationToken": {
                "Name": "CurrentPaginationToken",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "NextPaginationToken": {
                "Name": "NextPaginationToken",
                "Type": "int32",
                "Description": "",
                "Attributes": [
                    "Nullable"
                ]
            },
            "ResultCountThisPage": {
                "Name": "ResultCountThisPage",
                "Type": "int32",
                "Description": "",
                "Attributes": []
            },
            "NewsArticles": {
                "Name": "NewsArticles",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "Title": {
                            "Name": "Title",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "Link": {
                            "Name": "Link",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "PubDate": {
                            "Name": "PubDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "UniqueIdentifier": {
                            "Name": "UniqueIdentifier",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "Description": {
                            "Name": "Description",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "HtmlContent": {
                            "Name": "HtmlContent",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ImagePath": {
                            "Name": "ImagePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "OptionalMobileImagePath": {
                            "Name": "OptionalMobileImagePath",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "CategoryFilter": {
                "Name": "CategoryFilter",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "PagerAction": {
                "Name": "PagerAction",
                "Type": "string",
                "Description": "",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Content-RssNewsArticles.html#operation_get_Content-RssNewsArticles"""

        try:
            self.logger.info("Executing RssNewsArticles...")
            url = self.base_url + f"/Content/Rss/NewsArticles/{pageToken}/".format(
                pageToken=pageToken,
                categoryfilter=categoryfilter,
                includebody=includebody,
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
