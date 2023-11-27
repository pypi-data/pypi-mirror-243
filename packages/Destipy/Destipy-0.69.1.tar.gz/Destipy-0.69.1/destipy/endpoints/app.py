from datetime import datetime
from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class App:
    """App endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def GetApplicationApiUsage(
        self,
        applicationId: int,
        end: datetime,
        start: datetime,
    ) -> dict:
        """Get API usage by application for time frame specified. You can go as far back as 30 days ago, and can ask for up to a 48 hour window of time in a single request. You must be authenticated with at least the ReadUserData permission to access this endpoint.

            Args:
                applicationId (int): ID of the application to get usage statistics.
                end (datetime): End time for query. Goes to now if not specified.
                start (datetime): Start time for query. Goes to 24 hours ago if not specified.

            Returns:
        {
            "apiCalls": {
                "Name": "apiCalls",
                "Type": "array",
                "Description": "Counts for on API calls made for the time range.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "datapoints": {
                            "Name": "datapoints",
                            "Type": "array",
                            "Description": "Collection of samples with time and value.",
                            "Attributes": []
                        }
                    },
                    {
                        "target": {
                            "Name": "target",
                            "Type": "string",
                            "Description": "Target to which to datapoints apply.",
                            "Attributes": []
                        }
                    }
                ]
            },
            "throttledRequests": {
                "Name": "throttledRequests",
                "Type": "array",
                "Description": "Instances of blocked requests or requests that crossed the warn threshold during the time range.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "datapoints": {
                            "Name": "datapoints",
                            "Type": "array",
                            "Description": "Collection of samples with time and value.",
                            "Attributes": []
                        }
                    },
                    {
                        "target": {
                            "Name": "target",
                            "Type": "string",
                            "Description": "Target to which to datapoints apply.",
                            "Attributes": []
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_App-GetApplicationApiUsage.html#operation_get_App-GetApplicationApiUsage"""

        try:
            self.logger.info("Executing GetApplicationApiUsage...")
            url = self.base_url + f"/App/ApiUsage/{applicationId}/".format(
                applicationId=applicationId, end=end, start=start
            )
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieApplications(
        self,
    ) -> dict:
        """Get list of applications created by Bungie.

            Args:


            Returns:
        {
            "applicationId": {
                "Name": "applicationId",
                "Type": "int32",
                "Description": "Unique ID assigned to the application",
                "Attributes": []
            },
            "name": {
                "Name": "name",
                "Type": "string",
                "Description": "Name of the application",
                "Attributes": []
            },
            "redirectUrl": {
                "Name": "redirectUrl",
                "Type": "string",
                "Description": "URL used to pass the user's authorization code to the application",
                "Attributes": []
            },
            "link": {
                "Name": "link",
                "Type": "string",
                "Description": "Link to website for the application where a user can learn more about the app.",
                "Attributes": []
            },
            "scope": {
                "Name": "scope",
                "Type": "int64",
                "Description": "Permissions the application needs to work",
                "Attributes": []
            },
            "origin": {
                "Name": "origin",
                "Type": "string",
                "Description": "Value of the Origin header sent in requests generated by this application.",
                "Attributes": []
            },
            "status": {
                "Name": "status",
                "Type": "int32",
                "Description": "Current status of the application.",
                "Attributes": []
            },
            "creationDate": {
                "Name": "creationDate",
                "Type": "date-time",
                "Description": "Date the application was first added to our database.",
                "Attributes": []
            },
            "statusChanged": {
                "Name": "statusChanged",
                "Type": "date-time",
                "Description": "Date the application status last changed.",
                "Attributes": []
            },
            "firstPublished": {
                "Name": "firstPublished",
                "Type": "date-time",
                "Description": "Date the first time the application status entered the 'Public' status.",
                "Attributes": []
            },
            "team": {
                "Name": "team",
                "Type": "array",
                "Description": "List of team members who manage this application on Bungie.net. Will always consist of at least the application owner.",
                "Attributes": [],
                "Array Contents": [
                    {
                        "role": {
                            "Name": "role",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "apiEulaVersion": {
                            "Name": "apiEulaVersion",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "user": {
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
            "overrideAuthorizeViewName": {
                "Name": "overrideAuthorizeViewName",
                "Type": "string",
                "Description": "An optional override for the Authorize view name.",
                "Attributes": []
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_App-GetBungieApplications.html#operation_get_App-GetBungieApplications"""

        try:
            self.logger.info("Executing GetBungieApplications...")
            url = self.base_url + "/App/FirstParty/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
