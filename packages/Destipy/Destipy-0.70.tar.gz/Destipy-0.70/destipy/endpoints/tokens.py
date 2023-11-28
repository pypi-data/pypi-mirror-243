from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Tokens:
    """Tokens endpoints."""

    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.base_url = "https://www.bungie.net/Platform"

    async def ForceDropsRepair(self, access_token: str) -> dict:
        """Twitch Drops self-repair function - scans twitch for drops not marked as fulfilled and resyncs them.

            Args:
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Tokens-ForceDropsRepair.html#operation_post_Tokens-ForceDropsRepair"""

        try:
            self.logger.info("Executing ForceDropsRepair...")
            url = self.base_url + "/Tokens/Partner/ForceDropsRepair/".format()
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ClaimPartnerOffer(
        self,
        PartnerOfferId: str,
        BungieNetMembershipId: int,
        TransactionId: str,
        access_token: str,
    ) -> dict:
        """Claim a partner offer as the authenticated user.

            Args:
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Tokens-ClaimPartnerOffer.html#operation_post_Tokens-ClaimPartnerOffer"""

        request_body = {
            "PartnerOfferId": PartnerOfferId,
            "BungieNetMembershipId": BungieNetMembershipId,
            "TransactionId": TransactionId,
        }

        try:
            self.logger.info("Executing ClaimPartnerOffer...")
            url = self.base_url + "/Tokens/Partner/ClaimOffer/".format()
            return await self.requester.request(
                method=HTTPMethod.POST,
                url=url,
                data=request_body,
                access_token=access_token,
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def ApplyMissingPartnerOffersWithoutClaim(
        self, partnerApplicationId: int, targetBnetMembershipId: int, access_token: str
    ) -> dict:
        """Apply a partner offer to the targeted user. This endpoint does not claim a new offer, but any already claimed offers will be applied to the game if not already.

            Args:
                partnerApplicationId (int): The partner application identifier.
                targetBnetMembershipId (int): The bungie.net user to apply missing offers to. If not self, elevated permissions are required.
                access_token (str): OAuth token

            Returns:
        {
            "Name": "Response",
            "Type": "boolean",
            "Description": "",
            "Attributes": []
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_post_Tokens-ApplyMissingPartnerOffersWithoutClaim.html#operation_post_Tokens-ApplyMissingPartnerOffersWithoutClaim"""

        try:
            self.logger.info("Executing ApplyMissingPartnerOffersWithoutClaim...")
            url = (
                self.base_url
                + f"/Tokens/Partner/ApplyMissingOffers/{partnerApplicationId}/{targetBnetMembershipId}/".format(
                    partnerApplicationId=partnerApplicationId,
                    targetBnetMembershipId=targetBnetMembershipId,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.POST, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPartnerOfferSkuHistory(
        self, partnerApplicationId: int, targetBnetMembershipId: int, access_token: str
    ) -> dict:
        """Returns the partner sku and offer history of the targeted user. Elevated permissions are required to see users that are not yourself.

            Args:
                partnerApplicationId (int): The partner application identifier.
                targetBnetMembershipId (int): The bungie.net user to apply missing offers to. If not self, elevated permissions are required.
                access_token (str): OAuth token

            Returns:
        {
            "SkuIdentifier": {
                "Name": "SkuIdentifier",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "LocalizedName": {
                "Name": "LocalizedName",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "LocalizedDescription": {
                "Name": "LocalizedDescription",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "ClaimDate": {
                "Name": "ClaimDate",
                "Type": "date-time",
                "Description": "",
                "Attributes": []
            },
            "AllOffersApplied": {
                "Name": "AllOffersApplied",
                "Type": "boolean",
                "Description": "",
                "Attributes": []
            },
            "TransactionId": {
                "Name": "TransactionId",
                "Type": "string",
                "Description": "",
                "Attributes": []
            },
            "SkuOffers": {
                "Name": "SkuOffers",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "PartnerOfferKey": {
                            "Name": "PartnerOfferKey",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "MembershipId": {
                            "Name": "MembershipId",
                            "Type": "int64",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "MembershipType": {
                            "Name": "MembershipType",
                            "Type": "int32",
                            "Description": "\"All\" is only valid for searching capabilities: you need to pass the actual matching BungieMembershipType for any query where you pass a known membershipId.",
                            "Attributes": [
                                "Nullable",
                                "Enumeration"
                            ]
                        }
                    },
                    {
                        "LocalizedName": {
                            "Name": "LocalizedName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "LocalizedDescription": {
                            "Name": "LocalizedDescription",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "IsConsumable": {
                            "Name": "IsConsumable",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "QuantityApplied": {
                            "Name": "QuantityApplied",
                            "Type": "int32",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ApplyDate": {
                            "Name": "ApplyDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Tokens-GetPartnerOfferSkuHistory.html#operation_get_Tokens-GetPartnerOfferSkuHistory"""

        try:
            self.logger.info("Executing GetPartnerOfferSkuHistory...")
            url = (
                self.base_url
                + f"/Tokens/Partner/History/{partnerApplicationId}/{targetBnetMembershipId}/".format(
                    partnerApplicationId=partnerApplicationId,
                    targetBnetMembershipId=targetBnetMembershipId,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPartnerRewardHistory(
        self, partnerApplicationId: int, targetBnetMembershipId: int, access_token: str
    ) -> dict:
        """Returns the partner rewards history of the targeted user, both partner offers and Twitch drops.

            Args:
                partnerApplicationId (int): The partner application identifier.
                targetBnetMembershipId (int): The bungie.net user to return reward history for.
                access_token (str): OAuth token

            Returns:
        {
            "PartnerOffers": {
                "Name": "PartnerOffers",
                "Type": "array",
                "Description": "",
                "Attributes": [],
                "Array Contents": [
                    {
                        "SkuIdentifier": {
                            "Name": "SkuIdentifier",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "LocalizedName": {
                            "Name": "LocalizedName",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "LocalizedDescription": {
                            "Name": "LocalizedDescription",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "ClaimDate": {
                            "Name": "ClaimDate",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "AllOffersApplied": {
                            "Name": "AllOffersApplied",
                            "Type": "boolean",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "TransactionId": {
                            "Name": "TransactionId",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "SkuOffers": {
                            "Name": "SkuOffers",
                            "Type": "array",
                            "Description": "",
                            "Attributes": []
                        }
                    }
                ]
            },
            "TwitchDrops": {
                "Name": "TwitchDrops",
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
                        "Description": {
                            "Name": "Description",
                            "Type": "string",
                            "Description": "",
                            "Attributes": []
                        }
                    },
                    {
                        "CreatedAt": {
                            "Name": "CreatedAt",
                            "Type": "date-time",
                            "Description": "",
                            "Attributes": [
                                "Nullable"
                            ]
                        }
                    },
                    {
                        "ClaimState": {
                            "Name": "ClaimState",
                            "Type": "byte",
                            "Description": "",
                            "Attributes": [
                                "Nullable",
                                "Enumeration"
                            ]
                        }
                    }
                ]
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Tokens-GetPartnerRewardHistory.html#operation_get_Tokens-GetPartnerRewardHistory"""

        try:
            self.logger.info("Executing GetPartnerRewardHistory...")
            url = (
                self.base_url
                + f"/Tokens/Partner/History/{targetBnetMembershipId}/Application/{partnerApplicationId}/".format(
                    partnerApplicationId=partnerApplicationId,
                    targetBnetMembershipId=targetBnetMembershipId,
                )
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsForUser(
        self, membershipId: int, access_token: str
    ) -> dict:
        """Returns the bungie rewards for the targeted user.

            Args:
                membershipId (int): bungie.net user membershipId for requested user rewards. If not self, elevated permissions are required.
                access_token (str): OAuth token

            Returns:
        {
            "UserRewardAvailabilityModel": {
                "AvailabilityModel": {
                    "HasExistingCode": {
                        "Name": "HasExistingCode",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "RecordDefinitions": {
                        "Name": "RecordDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "displayProperties": {
                                    "description": {
                                        "Name": "description",
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
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                        "Attributes": []
                                    },
                                    "iconSequences": {
                                        "Name": "iconSequences",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "frames": {
                                                    "Name": "frames",
                                                    "Type": "array",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "highResIcon": {
                                        "Name": "highResIcon",
                                        "Type": "string",
                                        "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                        "Attributes": []
                                    },
                                    "hasIcon": {
                                        "Name": "hasIcon",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "scope": {
                                    "Name": "scope",
                                    "Type": "int32",
                                    "Description": "Indicates whether this Record's state is determined on a per-character or on an account-wide basis.",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationInfo": {
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "parentPresentationNodeHashes": {
                                        "Name": "parentPresentationNodeHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "displayStyle": {
                                        "Name": "displayStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "loreHash": {
                                    "Name": "loreHash",
                                    "Type": "uint32",
                                    "Description": "",
                                    "Attributes": [
                                        "Nullable",
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "objectiveHashes": {
                                    "Name": "objectiveHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "recordValueStyle": {
                                    "Name": "recordValueStyle",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "forTitleGilding": {
                                    "Name": "forTitleGilding",
                                    "Type": "boolean",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "shouldShowLargeIcons": {
                                    "Name": "shouldShowLargeIcons",
                                    "Type": "boolean",
                                    "Description": "A hint to show a large icon for a reward",
                                    "Attributes": []
                                }
                            },
                            {
                                "titleInfo": {
                                    "hasTitle": {
                                        "Name": "hasTitle",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGender": {
                                        "Name": "titlesByGender",
                                        "Type": "object",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGenderHash": {
                                        "Name": "titlesByGenderHash",
                                        "Type": "object",
                                        "Description": "For those who prefer to use the definitions.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "gildingTrackingRecordHash": {
                                        "Name": "gildingTrackingRecordHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    }
                                }
                            },
                            {
                                "completionInfo": {
                                    "partialCompletionObjectiveCountThreshold": {
                                        "Name": "partialCompletionObjectiveCountThreshold",
                                        "Type": "int32",
                                        "Description": "The number of objectives that must be completed before the objective is considered \"complete\"",
                                        "Attributes": []
                                    },
                                    "ScoreValue": {
                                        "Name": "ScoreValue",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "shouldFireToast": {
                                        "Name": "shouldFireToast",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "toastStyle": {
                                        "Name": "toastStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "stateInfo": {
                                    "featuredPriority": {
                                        "Name": "featuredPriority",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "obscuredName": {
                                        "Name": "obscuredName",
                                        "Type": "string",
                                        "Description": "A display name override to show when this record is 'obscured' instead of the default obscured display name.",
                                        "Attributes": []
                                    },
                                    "obscuredDescription": {
                                        "Name": "obscuredDescription",
                                        "Type": "string",
                                        "Description": "A display description override to show when this record is 'obscured' instead of the default obscured display description.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "requirements": {
                                    "entitlementUnavailableMessage": {
                                        "Name": "entitlementUnavailableMessage",
                                        "Type": "string",
                                        "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "expirationInfo": {
                                    "hasExpiration": {
                                        "Name": "hasExpiration",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "description": {
                                        "Name": "description",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "intervalInfo": {
                                    "Name": "intervalInfo",
                                    "Type": "object",
                                    "Description": "Some records have multiple 'interval' objectives, and the record may be claimed at each completed interval",
                                    "Attributes": []
                                }
                            },
                            {
                                "rewardItems": {
                                    "Name": "rewardItems",
                                    "Type": "array",
                                    "Description": "If there is any publicly available information about rewards earned for achieving this record, this is the list of those items. However, note that some records intentionally have \"hidden\" rewards. These will not be returned in this list.",
                                    "Attributes": []
                                }
                            },
                            {
                                "recordTypeName": {
                                    "Name": "recordTypeName",
                                    "Type": "string",
                                    "Description": "A display name for the type of record this is (Triumphs, Lore, Medals, Seasonal Challenge, etc.).",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationNodeType": {
                                    "Name": "presentationNodeType",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitIds": {
                                    "Name": "traitIds",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitHashes": {
                                    "Name": "traitHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "parentNodeHashes": {
                                    "Name": "parentNodeHashes",
                                    "Type": "array",
                                    "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "hash": {
                                    "Name": "hash",
                                    "Type": "uint32",
                                    "Description": "The unique identifier for this entity. Guaranteed to be unique for the type of entity, but not globally.When entities refer to each other in Destiny content, it is this hash that they are referring to.",
                                    "Attributes": []
                                }
                            },
                            {
                                "index": {
                                    "Name": "index",
                                    "Type": "int32",
                                    "Description": "The index of the entity as it was found in the investment tables.",
                                    "Attributes": []
                                }
                            },
                            {
                                "redacted": {
                                    "Name": "redacted",
                                    "Type": "boolean",
                                    "Description": "If this is true, then there is an entity with this identifier/type combination, but BNet is not yet allowed to show it. Sorry!",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "CollectibleDefinitions": {
                        "Name": "CollectibleDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "CollectibleDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "scope": {
                                        "Name": "scope",
                                        "Type": "int32",
                                        "Description": "Indicates whether the state of this Collectible is determined on a per-character or on an account-wide basis.",
                                        "Attributes": []
                                    },
                                    "sourceString": {
                                        "Name": "sourceString",
                                        "Type": "string",
                                        "Description": "A human readable string for a hint about how to acquire the item.",
                                        "Attributes": []
                                    },
                                    "sourceHash": {
                                        "Name": "sourceHash",
                                        "Type": "uint32",
                                        "Description": "This is a hash identifier we are building on the BNet side in an attempt to let people group collectibles by similar sources.I can't promise that it's going to be 100% accurate, but if the designers were consistent in assigning the same source strings to items with the same sources, it *ought to* be. No promises though.This hash also doesn't relate to an actual definition, just to note: we've got nothing useful other than the source string for this data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "itemHash": {
                                        "Name": "itemHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "acquisitionInfo": {
                                        "acquireMaterialRequirementHash": {
                                            "Name": "acquireMaterialRequirementHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "acquireTimestampUnlockValueHash": {
                                            "Name": "acquireTimestampUnlockValueHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        }
                                    },
                                    "stateInfo": {
                                        "obscuredOverrideItemHash": {
                                            "Name": "obscuredOverrideItemHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "requirements": {
                                            "entitlementUnavailableMessage": {
                                                "Name": "entitlementUnavailableMessage",
                                                "Type": "string",
                                                "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                                "Attributes": []
                                            }
                                        }
                                    },
                                    "presentationInfo": {
                                        "presentationNodeType": {
                                            "Name": "presentationNodeType",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        },
                                        "parentPresentationNodeHashes": {
                                            "Name": "parentPresentationNodeHashes",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [
                                                "Mapped to Definition"
                                            ],
                                            "Array Contents": "uint32"
                                        },
                                        "displayStyle": {
                                            "Name": "displayStyle",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "parentNodeHashes": {
                                        "Name": "parentNodeHashes",
                                        "Type": "array",
                                        "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
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
                            },
                            {
                                "DestinyInventoryItemDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "tooltipNotifications": {
                                        "Name": "tooltipNotifications",
                                        "Type": "array",
                                        "Description": "Tooltips that only come up conditionally for the item. Check the live data DestinyItemComponent.tooltipNotificationIndexes property for which of these should be shown at runtime.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "displayString": {
                                                    "Name": "displayString",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "displayStyle": {
                                                    "Name": "displayStyle",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "collectibleHash": {
                                        "Name": "collectibleHash",
                                        "Type": "uint32",
                                        "Description": "If this item has a collectible related to it, this is the hash identifier of that collectible entry.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "iconWatermark": {
                                        "Name": "iconWatermark",
                                        "Type": "string",
                                        "Description": "If available, this is the original 'active' release watermark overlay for the icon. If the item has different versions, this can be overridden by the 'display version watermark icon' from the 'quality' block. Alternatively, if there is no watermark for the version, and the item version has a power cap below the current season power cap, this can be overridden by the iconWatermarkShelved property.",
                                        "Attributes": []
                                    },
                                    "iconWatermarkShelved": {
                                        "Name": "iconWatermarkShelved",
                                        "Type": "string",
                                        "Description": "If available, this is the 'shelved' release watermark overlay for the icon. If the item version has a power cap below the current season power cap, it can be treated as 'shelved', and should be shown with this 'shelved' watermark overlay.",
                                        "Attributes": []
                                    },
                                    "secondaryIcon": {
                                        "Name": "secondaryIcon",
                                        "Type": "string",
                                        "Description": "A secondary icon associated with the item. Currently this is used in very context specific applications, such as Emblem Nameplates.",
                                        "Attributes": []
                                    },
                                    "secondaryOverlay": {
                                        "Name": "secondaryOverlay",
                                        "Type": "string",
                                        "Description": "Pulled from the secondary icon, this is the \"secondary background\" of the secondary icon. Confusing? Sure, that's why I call it \"overlay\" here: because as far as it's been used thus far, it has been for an optional overlay image. We'll see if that holds up, but at least for now it explains what this image is a bit better.",
                                        "Attributes": []
                                    },
                                    "secondarySpecial": {
                                        "Name": "secondarySpecial",
                                        "Type": "string",
                                        "Description": "Pulled from the Secondary Icon, this is the \"special\" background for the item. For Emblems, this is the background image used on the Details view: but it need not be limited to that for other types of items.",
                                        "Attributes": []
                                    },
                                    "backgroundColor": {
                                        "Name": "backgroundColor",
                                        "Type": "object",
                                        "Description": "Sometimes, an item will have a background color. Most notably this occurs with Emblems, who use the Background Color for small character nameplates such as the \"friends\" view you see in-game. There are almost certainly other items that have background color as well, though I have not bothered to investigate what items have it nor what purposes they serve: use it as you will.",
                                        "Attributes": []
                                    },
                                    "screenshot": {
                                        "Name": "screenshot",
                                        "Type": "string",
                                        "Description": "If we were able to acquire an in-game screenshot for the item, the path to that screenshot will be returned here. Note that not all items have screenshots: particularly not any non-equippable items.",
                                        "Attributes": []
                                    },
                                    "itemTypeDisplayName": {
                                        "Name": "itemTypeDisplayName",
                                        "Type": "string",
                                        "Description": "The localized title/name of the item's type. This can be whatever the designers want, and has no guarantee of consistency between items.",
                                        "Attributes": []
                                    },
                                    "flavorText": {
                                        "Name": "flavorText",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "uiItemDisplayStyle": {
                                        "Name": "uiItemDisplayStyle",
                                        "Type": "string",
                                        "Description": "A string identifier that the game's UI uses to determine how the item should be rendered in inventory screens and the like. This could really be anything - at the moment, we don't have the time to really breakdown and maintain all the possible strings this could be, partly because new ones could be added ad hoc. But if you want to use it to dictate your own UI, or look for items with a certain display style, go for it!",
                                        "Attributes": []
                                    },
                                    "itemTypeAndTierDisplayName": {
                                        "Name": "itemTypeAndTierDisplayName",
                                        "Type": "string",
                                        "Description": "It became a common enough pattern in our UI to show Item Type and Tier combined into a single localized string that I'm just going to go ahead and start pre-creating these for items.",
                                        "Attributes": []
                                    },
                                    "displaySource": {
                                        "Name": "displaySource",
                                        "Type": "string",
                                        "Description": "In theory, it is a localized string telling you about how you can find the item. I really wish this was more consistent. Many times, it has nothing. Sometimes, it's instead a more narrative-forward description of the item. Which is cool, and I wish all properties had that data, but it should really be its own property.",
                                        "Attributes": []
                                    },
                                    "tooltipStyle": {
                                        "Name": "tooltipStyle",
                                        "Type": "string",
                                        "Description": "An identifier that the game UI uses to determine what type of tooltip to show for the item. These have no corresponding definitions that BNet can link to: so it'll be up to you to interpret and display your UI differently according to these styles (or ignore it).",
                                        "Attributes": []
                                    },
                                    "action": {
                                        "Name": "action",
                                        "Type": "object",
                                        "Description": "If the item can be \"used\", this block will be non-null, and will have data related to the action performed when using the item. (Guess what? 99% of the time, this action is \"dismantle\". Shocker)",
                                        "Attributes": []
                                    },
                                    "crafting": {
                                        "Name": "crafting",
                                        "Type": "object",
                                        "Description": "Recipe items will have relevant crafting information available here.",
                                        "Attributes": []
                                    },
                                    "inventory": {
                                        "Name": "inventory",
                                        "Type": "object",
                                        "Description": "If this item can exist in an inventory, this block will be non-null. In practice, every item that currently exists has one of these blocks. But note that it is not necessarily guaranteed.",
                                        "Attributes": []
                                    },
                                    "setData": {
                                        "Name": "setData",
                                        "Type": "object",
                                        "Description": "If this item is a quest, this block will be non-null. In practice, I wish I had called this the Quest block, but at the time it wasn't clear to me whether it would end up being used for purposes other than quests. It will contain data about the steps in the quest, and mechanics we can use for displaying and tracking the quest.",
                                        "Attributes": []
                                    },
                                    "stats": {
                                        "Name": "stats",
                                        "Type": "object",
                                        "Description": "If this item can have stats (such as a weapon, armor, or vehicle), this block will be non-null and populated with the stats found on the item.",
                                        "Attributes": []
                                    },
                                    "emblemObjectiveHash": {
                                        "Name": "emblemObjectiveHash",
                                        "Type": "uint32",
                                        "Description": "If the item is an emblem that has a special Objective attached to it - for instance, if the emblem tracks PVP Kills, or what-have-you. This is a bit different from, for example, the Vanguard Kill Tracker mod, which pipes data into the \"art channel\". When I get some time, I would like to standardize these so you can get at the values they expose without having to care about what they're being used for and how they are wired up, but for now here's the raw data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "equippingBlock": {
                                        "Name": "equippingBlock",
                                        "Type": "object",
                                        "Description": "If this item can be equipped, this block will be non-null and will be populated with the conditions under which it can be equipped.",
                                        "Attributes": []
                                    },
                                    "translationBlock": {
                                        "Name": "translationBlock",
                                        "Type": "object",
                                        "Description": "If this item can be rendered, this block will be non-null and will be populated with rendering information.",
                                        "Attributes": []
                                    },
                                    "preview": {
                                        "Name": "preview",
                                        "Type": "object",
                                        "Description": "If this item can be Used or Acquired to gain other items (for instance, how Eververse Boxes can be consumed to get items from the box), this block will be non-null and will give summary information for the items that can be acquired.",
                                        "Attributes": []
                                    },
                                    "quality": {
                                        "Name": "quality",
                                        "Type": "object",
                                        "Description": "If this item can have a level or stats, this block will be non-null and will be populated with default quality (item level, \"quality\", and infusion) data. See the block for more details, there's often less upfront information in D2 so you'll want to be aware of how you use quality and item level on the definition level now.",
                                        "Attributes": []
                                    },
                                    "value": {
                                        "Name": "value",
                                        "Type": "object",
                                        "Description": "The conceptual \"Value\" of an item, if any was defined. See the DestinyItemValueBlockDefinition for more details.",
                                        "Attributes": []
                                    },
                                    "sourceData": {
                                        "Name": "sourceData",
                                        "Type": "object",
                                        "Description": "If this item has a known source, this block will be non-null and populated with source information. Unfortunately, at this time we are not generating sources: that is some aggressively manual work which we didn't have time for, and I'm hoping to get back to at some point in the future.",
                                        "Attributes": []
                                    },
                                    "objectives": {
                                        "Name": "objectives",
                                        "Type": "object",
                                        "Description": "If this item has Objectives (extra tasks that can be accomplished related to the item... most frequently when the item is a Quest Step and the Objectives need to be completed to move on to the next Quest Step), this block will be non-null and the objectives defined herein.",
                                        "Attributes": []
                                    },
                                    "metrics": {
                                        "Name": "metrics",
                                        "Type": "object",
                                        "Description": "If this item has available metrics to be shown, this block will be non-null have the appropriate hashes defined.",
                                        "Attributes": []
                                    },
                                    "plug": {
                                        "Name": "plug",
                                        "Type": "object",
                                        "Description": "If this item *is* a Plug, this will be non-null and the info defined herein. See DestinyItemPlugDefinition for more information.",
                                        "Attributes": []
                                    },
                                    "gearset": {
                                        "Name": "gearset",
                                        "Type": "object",
                                        "Description": "If this item has related items in a \"Gear Set\", this will be non-null and the relationships defined herein.",
                                        "Attributes": []
                                    },
                                    "sack": {
                                        "Name": "sack",
                                        "Type": "object",
                                        "Description": "If this item is a \"reward sack\" that can be opened to provide other items, this will be non-null and the properties of the sack contained herein.",
                                        "Attributes": []
                                    },
                                    "sockets": {
                                        "Name": "sockets",
                                        "Type": "object",
                                        "Description": "If this item has any Sockets, this will be non-null and the individual sockets on the item will be defined herein.",
                                        "Attributes": []
                                    },
                                    "summary": {
                                        "Name": "summary",
                                        "Type": "object",
                                        "Description": "Summary data about the item.",
                                        "Attributes": []
                                    },
                                    "talentGrid": {
                                        "Name": "talentGrid",
                                        "Type": "object",
                                        "Description": "If the item has a Talent Grid, this will be non-null and the properties of the grid defined herein. Note that, while many items still have talent grids, the only ones with meaningful Nodes still on them will be Subclass/\"Build\" items.",
                                        "Attributes": []
                                    },
                                    "investmentStats": {
                                        "Name": "investmentStats",
                                        "Type": "array",
                                        "Description": "If the item has stats, this block will be defined. It has the \"raw\" investment stats for the item. These investment stats don't take into account the ways that the items can spawn, nor do they take into account any Stat Group transformations. I have retained them for debugging purposes, but I do not know how useful people will find them.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "statTypeHash": {
                                                    "Name": "statTypeHash",
                                                    "Type": "uint32",
                                                    "Description": "The hash identifier for the DestinyStatDefinition defining this stat.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "value": {
                                                    "Name": "value",
                                                    "Type": "int32",
                                                    "Description": "The raw \"Investment\" value for the stat, before transformations are performed to turn this raw stat into stats that are displayed in the game UI.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "isConditionallyActive": {
                                                    "Name": "isConditionallyActive",
                                                    "Type": "boolean",
                                                    "Description": "If this is true, the stat will only be applied on the item in certain game state conditions, and we can't know statically whether or not this stat will be applied. Check the \"live\" API data instead for whether this value is being applied on a specific instance of the item in question, and you can use this to decide whether you want to show the stat on the generic view of the item, or whether you want to show some kind of caveat or warning about the stat value being conditional on game state.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "perks": {
                                        "Name": "perks",
                                        "Type": "array",
                                        "Description": "If the item has any *intrinsic* Perks (Perks that it will provide regardless of Sockets, Talent Grid, and other transitory state), they will be defined here.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "requirementDisplayString": {
                                                    "Name": "requirementDisplayString",
                                                    "Type": "string",
                                                    "Description": "If this perk is not active, this is the string to show for why it's not providing its benefits.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "perkHash": {
                                                    "Name": "perkHash",
                                                    "Type": "uint32",
                                                    "Description": "A hash identifier for the DestinySandboxPerkDefinition being provided on the item.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "perkVisibility": {
                                                    "Name": "perkVisibility",
                                                    "Type": "int32",
                                                    "Description": "Indicates whether this perk should be shown, or if it should be shown disabled.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "loreHash": {
                                        "Name": "loreHash",
                                        "Type": "uint32",
                                        "Description": "If the item has any related Lore (DestinyLoreDefinition), this will be the hash identifier you can use to look up the lore definition.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "summaryItemHash": {
                                        "Name": "summaryItemHash",
                                        "Type": "uint32",
                                        "Description": "There are times when the game will show you a \"summary/vague\" version of an item - such as a description of its type represented as a DestinyInventoryItemDefinition - rather than display the item itself.This happens sometimes when summarizing possible rewards in a tooltip. This is the item displayed instead, if it exists.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "animations": {
                                        "Name": "animations",
                                        "Type": "array",
                                        "Description": "If any animations were extracted from game content for this item, these will be the definitions of those animations.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "animName": {
                                                    "Name": "animName",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "animIdentifier": {
                                                    "Name": "animIdentifier",
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
                                            }
                                        ]
                                    },
                                    "allowActions": {
                                        "Name": "allowActions",
                                        "Type": "boolean",
                                        "Description": "BNet may forbid the execution of actions on this item via the API. If that is occurring, allowActions will be set to false.",
                                        "Attributes": []
                                    },
                                    "links": {
                                        "Name": "links",
                                        "Type": "array",
                                        "Description": "If we added any help or informational URLs about this item, these will be those links.",
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
                                                "url": {
                                                    "Name": "url",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "doesPostmasterPullHaveSideEffects": {
                                        "Name": "doesPostmasterPullHaveSideEffects",
                                        "Type": "boolean",
                                        "Description": "The boolean will indicate to us (and you!) whether something *could* happen when you transfer this item from the Postmaster that might be considered a \"destructive\" action.It is not feasible currently to tell you (or ourelves!) in a consistent way whether this *will* actually cause a destructive action, so we are playing it safe: if it has the potential to do so, we will not allow it to be transferred from the Postmaster by default. You will need to check for this flag before transferring an item from the Postmaster, or else you'll end up receiving an error.",
                                        "Attributes": []
                                    },
                                    "nonTransferrable": {
                                        "Name": "nonTransferrable",
                                        "Type": "boolean",
                                        "Description": "The intrinsic transferability of an item.I hate that this boolean is negative - but there's a reason.Just because an item is intrinsically transferrable doesn't mean that it can be transferred, and we don't want to imply that this is the only source of that transferability.",
                                        "Attributes": []
                                    },
                                    "itemCategoryHashes": {
                                        "Name": "itemCategoryHashes",
                                        "Type": "array",
                                        "Description": "BNet attempts to make a more formal definition of item \"Categories\", as defined by DestinyItemCategoryDefinition. This is a list of all Categories that we were able to algorithmically determine that this item is a member of. (for instance, that it's a \"Weapon\", that it's an \"Auto Rifle\", etc...)The algorithm for these is, unfortunately, volatile. If you believe you see a miscategorized item, please let us know on the Bungie API forums.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "specialItemType": {
                                        "Name": "specialItemType",
                                        "Type": "int32",
                                        "Description": "In Destiny 1, we identified some items as having particular categories that we'd like to know about for various internal logic purposes. These are defined in SpecialItemType, and while these days the itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemType": {
                                        "Name": "itemType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"base\" the of the item. This enum is a useful but dramatic oversimplification of what it means for an item to have a \"Type\". Still, it's handy in many situations.itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemSubType": {
                                        "Name": "itemSubType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"sub-type\" of the item. For instance, where an item might have an itemType value \"Weapon\", this will be something more specific like \"Auto Rifle\".itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "classType": {
                                        "Name": "classType",
                                        "Type": "int32",
                                        "Description": "We run a similarly weak-sauce algorithm to try and determine whether an item is restricted to a specific class. If we find it to be restricted in such a way, we set this classType property to match the class' enumeration value so that users can easily identify class restricted items.If you see a mis-classed item, please inform the developers in the Bungie API forum.",
                                        "Attributes": []
                                    },
                                    "breakerType": {
                                        "Name": "breakerType",
                                        "Type": "int32",
                                        "Description": "Some weapons and plugs can have a \"Breaker Type\": a special ability that works sort of like damage type vulnerabilities. This is (almost?) always set on items by plugs.",
                                        "Attributes": []
                                    },
                                    "breakerTypeHash": {
                                        "Name": "breakerTypeHash",
                                        "Type": "uint32",
                                        "Description": "Since we also have a breaker type definition, this is the hash for that breaker type for your convenience. Whether you use the enum or hash and look up the definition depends on what's cleanest for your code.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "equippable": {
                                        "Name": "equippable",
                                        "Type": "boolean",
                                        "Description": "If true, then you will be allowed to equip the item if you pass its other requirements.This being false means that you cannot equip the item under any circumstances.",
                                        "Attributes": []
                                    },
                                    "damageTypeHashes": {
                                        "Name": "damageTypeHashes",
                                        "Type": "array",
                                        "Description": "Theoretically, an item can have many possible damage types. In *practice*, this is not true, but just in case weapons start being made that have multiple (for instance, an item where a socket has reusable plugs for every possible damage type that you can choose from freely), this field will return all of the possible damage types that are available to the weapon by default.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "damageTypes": {
                                        "Name": "damageTypes",
                                        "Type": "array",
                                        "Description": "This is the list of all damage types that we know ahead of time the item can take on. Unfortunately, this does not preclude the possibility of something funky happening to give the item a damage type that cannot be predicted beforehand: for example, if some designer decides to create arbitrary non-reusable plugs that cause damage type to change.This damage type prediction will only use the following to determine potential damage types:- Intrinsic perks- Talent Node perks- Known, reusable plugs for sockets",
                                        "Attributes": [],
                                        "Array Contents": "int32"
                                    },
                                    "defaultDamageType": {
                                        "Name": "defaultDamageType",
                                        "Type": "int32",
                                        "Description": "If the item has a damage type that could be considered to be default, it will be populated here.For various upsetting reasons, it's surprisingly cumbersome to figure this out. I hope you're happy.",
                                        "Attributes": []
                                    },
                                    "defaultDamageTypeHash": {
                                        "Name": "defaultDamageTypeHash",
                                        "Type": "uint32",
                                        "Description": "Similar to defaultDamageType, but represented as the hash identifier for a DestinyDamageTypeDefinition.I will likely regret leaving in the enumeration versions of these properties, but for now they're very convenient.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "seasonHash": {
                                        "Name": "seasonHash",
                                        "Type": "uint32",
                                        "Description": "If this item is related directly to a Season of Destiny, this is the hash identifier for that season.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "isWrapper": {
                                        "Name": "isWrapper",
                                        "Type": "boolean",
                                        "Description": "If true, this is a dummy vendor-wrapped item template. Items purchased from Eververse will be \"wrapped\" by one of these items so that we can safely provide refund capabilities before the item is \"unwrapped\".",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "Traits are metadata tags applied to this item. For example: armor slot, weapon type, foundry, faction, etc. These IDs come from the game and don't map to any content, but should still be useful.",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "These are the corresponding trait definition hashes for the entries in traitIds.",
                                        "Attributes": [],
                                        "Array Contents": "uint32"
                                    },
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
                            }
                        ]
                    },
                    "IsOffer": {
                        "Name": "IsOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "HasOffer": {
                        "Name": "HasOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "OfferApplied": {
                        "Name": "OfferApplied",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "DecryptedToken": {
                        "Name": "DecryptedToken",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "IsLoyaltyReward": {
                        "Name": "IsLoyaltyReward",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "ShopifyEndDate": {
                        "Name": "ShopifyEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": [
                            "Nullable"
                        ]
                    },
                    "GameEarnByDate": {
                        "Name": "GameEarnByDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "RedemptionEndDate": {
                        "Name": "RedemptionEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    }
                },
                "IsAvailableForUser": {
                    "Name": "IsAvailableForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "IsUnlockedForUser": {
                    "Name": "IsUnlockedForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                }
            },
            "ObjectiveDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            },
            "RewardDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Tokens-GetBungieRewardsForUser.html#operation_get_Tokens-GetBungieRewardsForUser"""

        try:
            self.logger.info("Executing GetBungieRewardsForUser...")
            url = (
                self.base_url
                + f"/Tokens/Rewards/GetRewardsForUser/{membershipId}/".format(
                    membershipId=membershipId
                )
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsForPlatformUser(
        self, membershipId: int, membershipType: int, access_token: str
    ) -> dict:
        """Returns the bungie rewards for the targeted user when a platform membership Id and Type are used.

            Args:
                membershipId (int): users platform membershipId for requested user rewards. If not self, elevated permissions are required.
                membershipType (int): The target Destiny 2 membership type.
                access_token (str): OAuth token

            Returns:
        {
            "UserRewardAvailabilityModel": {
                "AvailabilityModel": {
                    "HasExistingCode": {
                        "Name": "HasExistingCode",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "RecordDefinitions": {
                        "Name": "RecordDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "displayProperties": {
                                    "description": {
                                        "Name": "description",
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
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                        "Attributes": []
                                    },
                                    "iconSequences": {
                                        "Name": "iconSequences",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "frames": {
                                                    "Name": "frames",
                                                    "Type": "array",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "highResIcon": {
                                        "Name": "highResIcon",
                                        "Type": "string",
                                        "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                        "Attributes": []
                                    },
                                    "hasIcon": {
                                        "Name": "hasIcon",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "scope": {
                                    "Name": "scope",
                                    "Type": "int32",
                                    "Description": "Indicates whether this Record's state is determined on a per-character or on an account-wide basis.",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationInfo": {
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "parentPresentationNodeHashes": {
                                        "Name": "parentPresentationNodeHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "displayStyle": {
                                        "Name": "displayStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "loreHash": {
                                    "Name": "loreHash",
                                    "Type": "uint32",
                                    "Description": "",
                                    "Attributes": [
                                        "Nullable",
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "objectiveHashes": {
                                    "Name": "objectiveHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "recordValueStyle": {
                                    "Name": "recordValueStyle",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "forTitleGilding": {
                                    "Name": "forTitleGilding",
                                    "Type": "boolean",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "shouldShowLargeIcons": {
                                    "Name": "shouldShowLargeIcons",
                                    "Type": "boolean",
                                    "Description": "A hint to show a large icon for a reward",
                                    "Attributes": []
                                }
                            },
                            {
                                "titleInfo": {
                                    "hasTitle": {
                                        "Name": "hasTitle",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGender": {
                                        "Name": "titlesByGender",
                                        "Type": "object",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGenderHash": {
                                        "Name": "titlesByGenderHash",
                                        "Type": "object",
                                        "Description": "For those who prefer to use the definitions.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "gildingTrackingRecordHash": {
                                        "Name": "gildingTrackingRecordHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    }
                                }
                            },
                            {
                                "completionInfo": {
                                    "partialCompletionObjectiveCountThreshold": {
                                        "Name": "partialCompletionObjectiveCountThreshold",
                                        "Type": "int32",
                                        "Description": "The number of objectives that must be completed before the objective is considered \"complete\"",
                                        "Attributes": []
                                    },
                                    "ScoreValue": {
                                        "Name": "ScoreValue",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "shouldFireToast": {
                                        "Name": "shouldFireToast",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "toastStyle": {
                                        "Name": "toastStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "stateInfo": {
                                    "featuredPriority": {
                                        "Name": "featuredPriority",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "obscuredName": {
                                        "Name": "obscuredName",
                                        "Type": "string",
                                        "Description": "A display name override to show when this record is 'obscured' instead of the default obscured display name.",
                                        "Attributes": []
                                    },
                                    "obscuredDescription": {
                                        "Name": "obscuredDescription",
                                        "Type": "string",
                                        "Description": "A display description override to show when this record is 'obscured' instead of the default obscured display description.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "requirements": {
                                    "entitlementUnavailableMessage": {
                                        "Name": "entitlementUnavailableMessage",
                                        "Type": "string",
                                        "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "expirationInfo": {
                                    "hasExpiration": {
                                        "Name": "hasExpiration",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "description": {
                                        "Name": "description",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "intervalInfo": {
                                    "Name": "intervalInfo",
                                    "Type": "object",
                                    "Description": "Some records have multiple 'interval' objectives, and the record may be claimed at each completed interval",
                                    "Attributes": []
                                }
                            },
                            {
                                "rewardItems": {
                                    "Name": "rewardItems",
                                    "Type": "array",
                                    "Description": "If there is any publicly available information about rewards earned for achieving this record, this is the list of those items. However, note that some records intentionally have \"hidden\" rewards. These will not be returned in this list.",
                                    "Attributes": []
                                }
                            },
                            {
                                "recordTypeName": {
                                    "Name": "recordTypeName",
                                    "Type": "string",
                                    "Description": "A display name for the type of record this is (Triumphs, Lore, Medals, Seasonal Challenge, etc.).",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationNodeType": {
                                    "Name": "presentationNodeType",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitIds": {
                                    "Name": "traitIds",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitHashes": {
                                    "Name": "traitHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "parentNodeHashes": {
                                    "Name": "parentNodeHashes",
                                    "Type": "array",
                                    "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "hash": {
                                    "Name": "hash",
                                    "Type": "uint32",
                                    "Description": "The unique identifier for this entity. Guaranteed to be unique for the type of entity, but not globally.When entities refer to each other in Destiny content, it is this hash that they are referring to.",
                                    "Attributes": []
                                }
                            },
                            {
                                "index": {
                                    "Name": "index",
                                    "Type": "int32",
                                    "Description": "The index of the entity as it was found in the investment tables.",
                                    "Attributes": []
                                }
                            },
                            {
                                "redacted": {
                                    "Name": "redacted",
                                    "Type": "boolean",
                                    "Description": "If this is true, then there is an entity with this identifier/type combination, but BNet is not yet allowed to show it. Sorry!",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "CollectibleDefinitions": {
                        "Name": "CollectibleDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "CollectibleDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "scope": {
                                        "Name": "scope",
                                        "Type": "int32",
                                        "Description": "Indicates whether the state of this Collectible is determined on a per-character or on an account-wide basis.",
                                        "Attributes": []
                                    },
                                    "sourceString": {
                                        "Name": "sourceString",
                                        "Type": "string",
                                        "Description": "A human readable string for a hint about how to acquire the item.",
                                        "Attributes": []
                                    },
                                    "sourceHash": {
                                        "Name": "sourceHash",
                                        "Type": "uint32",
                                        "Description": "This is a hash identifier we are building on the BNet side in an attempt to let people group collectibles by similar sources.I can't promise that it's going to be 100% accurate, but if the designers were consistent in assigning the same source strings to items with the same sources, it *ought to* be. No promises though.This hash also doesn't relate to an actual definition, just to note: we've got nothing useful other than the source string for this data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "itemHash": {
                                        "Name": "itemHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "acquisitionInfo": {
                                        "acquireMaterialRequirementHash": {
                                            "Name": "acquireMaterialRequirementHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "acquireTimestampUnlockValueHash": {
                                            "Name": "acquireTimestampUnlockValueHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        }
                                    },
                                    "stateInfo": {
                                        "obscuredOverrideItemHash": {
                                            "Name": "obscuredOverrideItemHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "requirements": {
                                            "entitlementUnavailableMessage": {
                                                "Name": "entitlementUnavailableMessage",
                                                "Type": "string",
                                                "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                                "Attributes": []
                                            }
                                        }
                                    },
                                    "presentationInfo": {
                                        "presentationNodeType": {
                                            "Name": "presentationNodeType",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        },
                                        "parentPresentationNodeHashes": {
                                            "Name": "parentPresentationNodeHashes",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [
                                                "Mapped to Definition"
                                            ],
                                            "Array Contents": "uint32"
                                        },
                                        "displayStyle": {
                                            "Name": "displayStyle",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "parentNodeHashes": {
                                        "Name": "parentNodeHashes",
                                        "Type": "array",
                                        "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
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
                            },
                            {
                                "DestinyInventoryItemDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "tooltipNotifications": {
                                        "Name": "tooltipNotifications",
                                        "Type": "array",
                                        "Description": "Tooltips that only come up conditionally for the item. Check the live data DestinyItemComponent.tooltipNotificationIndexes property for which of these should be shown at runtime.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "displayString": {
                                                    "Name": "displayString",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "displayStyle": {
                                                    "Name": "displayStyle",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "collectibleHash": {
                                        "Name": "collectibleHash",
                                        "Type": "uint32",
                                        "Description": "If this item has a collectible related to it, this is the hash identifier of that collectible entry.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "iconWatermark": {
                                        "Name": "iconWatermark",
                                        "Type": "string",
                                        "Description": "If available, this is the original 'active' release watermark overlay for the icon. If the item has different versions, this can be overridden by the 'display version watermark icon' from the 'quality' block. Alternatively, if there is no watermark for the version, and the item version has a power cap below the current season power cap, this can be overridden by the iconWatermarkShelved property.",
                                        "Attributes": []
                                    },
                                    "iconWatermarkShelved": {
                                        "Name": "iconWatermarkShelved",
                                        "Type": "string",
                                        "Description": "If available, this is the 'shelved' release watermark overlay for the icon. If the item version has a power cap below the current season power cap, it can be treated as 'shelved', and should be shown with this 'shelved' watermark overlay.",
                                        "Attributes": []
                                    },
                                    "secondaryIcon": {
                                        "Name": "secondaryIcon",
                                        "Type": "string",
                                        "Description": "A secondary icon associated with the item. Currently this is used in very context specific applications, such as Emblem Nameplates.",
                                        "Attributes": []
                                    },
                                    "secondaryOverlay": {
                                        "Name": "secondaryOverlay",
                                        "Type": "string",
                                        "Description": "Pulled from the secondary icon, this is the \"secondary background\" of the secondary icon. Confusing? Sure, that's why I call it \"overlay\" here: because as far as it's been used thus far, it has been for an optional overlay image. We'll see if that holds up, but at least for now it explains what this image is a bit better.",
                                        "Attributes": []
                                    },
                                    "secondarySpecial": {
                                        "Name": "secondarySpecial",
                                        "Type": "string",
                                        "Description": "Pulled from the Secondary Icon, this is the \"special\" background for the item. For Emblems, this is the background image used on the Details view: but it need not be limited to that for other types of items.",
                                        "Attributes": []
                                    },
                                    "backgroundColor": {
                                        "Name": "backgroundColor",
                                        "Type": "object",
                                        "Description": "Sometimes, an item will have a background color. Most notably this occurs with Emblems, who use the Background Color for small character nameplates such as the \"friends\" view you see in-game. There are almost certainly other items that have background color as well, though I have not bothered to investigate what items have it nor what purposes they serve: use it as you will.",
                                        "Attributes": []
                                    },
                                    "screenshot": {
                                        "Name": "screenshot",
                                        "Type": "string",
                                        "Description": "If we were able to acquire an in-game screenshot for the item, the path to that screenshot will be returned here. Note that not all items have screenshots: particularly not any non-equippable items.",
                                        "Attributes": []
                                    },
                                    "itemTypeDisplayName": {
                                        "Name": "itemTypeDisplayName",
                                        "Type": "string",
                                        "Description": "The localized title/name of the item's type. This can be whatever the designers want, and has no guarantee of consistency between items.",
                                        "Attributes": []
                                    },
                                    "flavorText": {
                                        "Name": "flavorText",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "uiItemDisplayStyle": {
                                        "Name": "uiItemDisplayStyle",
                                        "Type": "string",
                                        "Description": "A string identifier that the game's UI uses to determine how the item should be rendered in inventory screens and the like. This could really be anything - at the moment, we don't have the time to really breakdown and maintain all the possible strings this could be, partly because new ones could be added ad hoc. But if you want to use it to dictate your own UI, or look for items with a certain display style, go for it!",
                                        "Attributes": []
                                    },
                                    "itemTypeAndTierDisplayName": {
                                        "Name": "itemTypeAndTierDisplayName",
                                        "Type": "string",
                                        "Description": "It became a common enough pattern in our UI to show Item Type and Tier combined into a single localized string that I'm just going to go ahead and start pre-creating these for items.",
                                        "Attributes": []
                                    },
                                    "displaySource": {
                                        "Name": "displaySource",
                                        "Type": "string",
                                        "Description": "In theory, it is a localized string telling you about how you can find the item. I really wish this was more consistent. Many times, it has nothing. Sometimes, it's instead a more narrative-forward description of the item. Which is cool, and I wish all properties had that data, but it should really be its own property.",
                                        "Attributes": []
                                    },
                                    "tooltipStyle": {
                                        "Name": "tooltipStyle",
                                        "Type": "string",
                                        "Description": "An identifier that the game UI uses to determine what type of tooltip to show for the item. These have no corresponding definitions that BNet can link to: so it'll be up to you to interpret and display your UI differently according to these styles (or ignore it).",
                                        "Attributes": []
                                    },
                                    "action": {
                                        "Name": "action",
                                        "Type": "object",
                                        "Description": "If the item can be \"used\", this block will be non-null, and will have data related to the action performed when using the item. (Guess what? 99% of the time, this action is \"dismantle\". Shocker)",
                                        "Attributes": []
                                    },
                                    "crafting": {
                                        "Name": "crafting",
                                        "Type": "object",
                                        "Description": "Recipe items will have relevant crafting information available here.",
                                        "Attributes": []
                                    },
                                    "inventory": {
                                        "Name": "inventory",
                                        "Type": "object",
                                        "Description": "If this item can exist in an inventory, this block will be non-null. In practice, every item that currently exists has one of these blocks. But note that it is not necessarily guaranteed.",
                                        "Attributes": []
                                    },
                                    "setData": {
                                        "Name": "setData",
                                        "Type": "object",
                                        "Description": "If this item is a quest, this block will be non-null. In practice, I wish I had called this the Quest block, but at the time it wasn't clear to me whether it would end up being used for purposes other than quests. It will contain data about the steps in the quest, and mechanics we can use for displaying and tracking the quest.",
                                        "Attributes": []
                                    },
                                    "stats": {
                                        "Name": "stats",
                                        "Type": "object",
                                        "Description": "If this item can have stats (such as a weapon, armor, or vehicle), this block will be non-null and populated with the stats found on the item.",
                                        "Attributes": []
                                    },
                                    "emblemObjectiveHash": {
                                        "Name": "emblemObjectiveHash",
                                        "Type": "uint32",
                                        "Description": "If the item is an emblem that has a special Objective attached to it - for instance, if the emblem tracks PVP Kills, or what-have-you. This is a bit different from, for example, the Vanguard Kill Tracker mod, which pipes data into the \"art channel\". When I get some time, I would like to standardize these so you can get at the values they expose without having to care about what they're being used for and how they are wired up, but for now here's the raw data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "equippingBlock": {
                                        "Name": "equippingBlock",
                                        "Type": "object",
                                        "Description": "If this item can be equipped, this block will be non-null and will be populated with the conditions under which it can be equipped.",
                                        "Attributes": []
                                    },
                                    "translationBlock": {
                                        "Name": "translationBlock",
                                        "Type": "object",
                                        "Description": "If this item can be rendered, this block will be non-null and will be populated with rendering information.",
                                        "Attributes": []
                                    },
                                    "preview": {
                                        "Name": "preview",
                                        "Type": "object",
                                        "Description": "If this item can be Used or Acquired to gain other items (for instance, how Eververse Boxes can be consumed to get items from the box), this block will be non-null and will give summary information for the items that can be acquired.",
                                        "Attributes": []
                                    },
                                    "quality": {
                                        "Name": "quality",
                                        "Type": "object",
                                        "Description": "If this item can have a level or stats, this block will be non-null and will be populated with default quality (item level, \"quality\", and infusion) data. See the block for more details, there's often less upfront information in D2 so you'll want to be aware of how you use quality and item level on the definition level now.",
                                        "Attributes": []
                                    },
                                    "value": {
                                        "Name": "value",
                                        "Type": "object",
                                        "Description": "The conceptual \"Value\" of an item, if any was defined. See the DestinyItemValueBlockDefinition for more details.",
                                        "Attributes": []
                                    },
                                    "sourceData": {
                                        "Name": "sourceData",
                                        "Type": "object",
                                        "Description": "If this item has a known source, this block will be non-null and populated with source information. Unfortunately, at this time we are not generating sources: that is some aggressively manual work which we didn't have time for, and I'm hoping to get back to at some point in the future.",
                                        "Attributes": []
                                    },
                                    "objectives": {
                                        "Name": "objectives",
                                        "Type": "object",
                                        "Description": "If this item has Objectives (extra tasks that can be accomplished related to the item... most frequently when the item is a Quest Step and the Objectives need to be completed to move on to the next Quest Step), this block will be non-null and the objectives defined herein.",
                                        "Attributes": []
                                    },
                                    "metrics": {
                                        "Name": "metrics",
                                        "Type": "object",
                                        "Description": "If this item has available metrics to be shown, this block will be non-null have the appropriate hashes defined.",
                                        "Attributes": []
                                    },
                                    "plug": {
                                        "Name": "plug",
                                        "Type": "object",
                                        "Description": "If this item *is* a Plug, this will be non-null and the info defined herein. See DestinyItemPlugDefinition for more information.",
                                        "Attributes": []
                                    },
                                    "gearset": {
                                        "Name": "gearset",
                                        "Type": "object",
                                        "Description": "If this item has related items in a \"Gear Set\", this will be non-null and the relationships defined herein.",
                                        "Attributes": []
                                    },
                                    "sack": {
                                        "Name": "sack",
                                        "Type": "object",
                                        "Description": "If this item is a \"reward sack\" that can be opened to provide other items, this will be non-null and the properties of the sack contained herein.",
                                        "Attributes": []
                                    },
                                    "sockets": {
                                        "Name": "sockets",
                                        "Type": "object",
                                        "Description": "If this item has any Sockets, this will be non-null and the individual sockets on the item will be defined herein.",
                                        "Attributes": []
                                    },
                                    "summary": {
                                        "Name": "summary",
                                        "Type": "object",
                                        "Description": "Summary data about the item.",
                                        "Attributes": []
                                    },
                                    "talentGrid": {
                                        "Name": "talentGrid",
                                        "Type": "object",
                                        "Description": "If the item has a Talent Grid, this will be non-null and the properties of the grid defined herein. Note that, while many items still have talent grids, the only ones with meaningful Nodes still on them will be Subclass/\"Build\" items.",
                                        "Attributes": []
                                    },
                                    "investmentStats": {
                                        "Name": "investmentStats",
                                        "Type": "array",
                                        "Description": "If the item has stats, this block will be defined. It has the \"raw\" investment stats for the item. These investment stats don't take into account the ways that the items can spawn, nor do they take into account any Stat Group transformations. I have retained them for debugging purposes, but I do not know how useful people will find them.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "statTypeHash": {
                                                    "Name": "statTypeHash",
                                                    "Type": "uint32",
                                                    "Description": "The hash identifier for the DestinyStatDefinition defining this stat.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "value": {
                                                    "Name": "value",
                                                    "Type": "int32",
                                                    "Description": "The raw \"Investment\" value for the stat, before transformations are performed to turn this raw stat into stats that are displayed in the game UI.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "isConditionallyActive": {
                                                    "Name": "isConditionallyActive",
                                                    "Type": "boolean",
                                                    "Description": "If this is true, the stat will only be applied on the item in certain game state conditions, and we can't know statically whether or not this stat will be applied. Check the \"live\" API data instead for whether this value is being applied on a specific instance of the item in question, and you can use this to decide whether you want to show the stat on the generic view of the item, or whether you want to show some kind of caveat or warning about the stat value being conditional on game state.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "perks": {
                                        "Name": "perks",
                                        "Type": "array",
                                        "Description": "If the item has any *intrinsic* Perks (Perks that it will provide regardless of Sockets, Talent Grid, and other transitory state), they will be defined here.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "requirementDisplayString": {
                                                    "Name": "requirementDisplayString",
                                                    "Type": "string",
                                                    "Description": "If this perk is not active, this is the string to show for why it's not providing its benefits.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "perkHash": {
                                                    "Name": "perkHash",
                                                    "Type": "uint32",
                                                    "Description": "A hash identifier for the DestinySandboxPerkDefinition being provided on the item.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "perkVisibility": {
                                                    "Name": "perkVisibility",
                                                    "Type": "int32",
                                                    "Description": "Indicates whether this perk should be shown, or if it should be shown disabled.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "loreHash": {
                                        "Name": "loreHash",
                                        "Type": "uint32",
                                        "Description": "If the item has any related Lore (DestinyLoreDefinition), this will be the hash identifier you can use to look up the lore definition.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "summaryItemHash": {
                                        "Name": "summaryItemHash",
                                        "Type": "uint32",
                                        "Description": "There are times when the game will show you a \"summary/vague\" version of an item - such as a description of its type represented as a DestinyInventoryItemDefinition - rather than display the item itself.This happens sometimes when summarizing possible rewards in a tooltip. This is the item displayed instead, if it exists.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "animations": {
                                        "Name": "animations",
                                        "Type": "array",
                                        "Description": "If any animations were extracted from game content for this item, these will be the definitions of those animations.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "animName": {
                                                    "Name": "animName",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "animIdentifier": {
                                                    "Name": "animIdentifier",
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
                                            }
                                        ]
                                    },
                                    "allowActions": {
                                        "Name": "allowActions",
                                        "Type": "boolean",
                                        "Description": "BNet may forbid the execution of actions on this item via the API. If that is occurring, allowActions will be set to false.",
                                        "Attributes": []
                                    },
                                    "links": {
                                        "Name": "links",
                                        "Type": "array",
                                        "Description": "If we added any help or informational URLs about this item, these will be those links.",
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
                                                "url": {
                                                    "Name": "url",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "doesPostmasterPullHaveSideEffects": {
                                        "Name": "doesPostmasterPullHaveSideEffects",
                                        "Type": "boolean",
                                        "Description": "The boolean will indicate to us (and you!) whether something *could* happen when you transfer this item from the Postmaster that might be considered a \"destructive\" action.It is not feasible currently to tell you (or ourelves!) in a consistent way whether this *will* actually cause a destructive action, so we are playing it safe: if it has the potential to do so, we will not allow it to be transferred from the Postmaster by default. You will need to check for this flag before transferring an item from the Postmaster, or else you'll end up receiving an error.",
                                        "Attributes": []
                                    },
                                    "nonTransferrable": {
                                        "Name": "nonTransferrable",
                                        "Type": "boolean",
                                        "Description": "The intrinsic transferability of an item.I hate that this boolean is negative - but there's a reason.Just because an item is intrinsically transferrable doesn't mean that it can be transferred, and we don't want to imply that this is the only source of that transferability.",
                                        "Attributes": []
                                    },
                                    "itemCategoryHashes": {
                                        "Name": "itemCategoryHashes",
                                        "Type": "array",
                                        "Description": "BNet attempts to make a more formal definition of item \"Categories\", as defined by DestinyItemCategoryDefinition. This is a list of all Categories that we were able to algorithmically determine that this item is a member of. (for instance, that it's a \"Weapon\", that it's an \"Auto Rifle\", etc...)The algorithm for these is, unfortunately, volatile. If you believe you see a miscategorized item, please let us know on the Bungie API forums.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "specialItemType": {
                                        "Name": "specialItemType",
                                        "Type": "int32",
                                        "Description": "In Destiny 1, we identified some items as having particular categories that we'd like to know about for various internal logic purposes. These are defined in SpecialItemType, and while these days the itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemType": {
                                        "Name": "itemType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"base\" the of the item. This enum is a useful but dramatic oversimplification of what it means for an item to have a \"Type\". Still, it's handy in many situations.itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemSubType": {
                                        "Name": "itemSubType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"sub-type\" of the item. For instance, where an item might have an itemType value \"Weapon\", this will be something more specific like \"Auto Rifle\".itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "classType": {
                                        "Name": "classType",
                                        "Type": "int32",
                                        "Description": "We run a similarly weak-sauce algorithm to try and determine whether an item is restricted to a specific class. If we find it to be restricted in such a way, we set this classType property to match the class' enumeration value so that users can easily identify class restricted items.If you see a mis-classed item, please inform the developers in the Bungie API forum.",
                                        "Attributes": []
                                    },
                                    "breakerType": {
                                        "Name": "breakerType",
                                        "Type": "int32",
                                        "Description": "Some weapons and plugs can have a \"Breaker Type\": a special ability that works sort of like damage type vulnerabilities. This is (almost?) always set on items by plugs.",
                                        "Attributes": []
                                    },
                                    "breakerTypeHash": {
                                        "Name": "breakerTypeHash",
                                        "Type": "uint32",
                                        "Description": "Since we also have a breaker type definition, this is the hash for that breaker type for your convenience. Whether you use the enum or hash and look up the definition depends on what's cleanest for your code.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "equippable": {
                                        "Name": "equippable",
                                        "Type": "boolean",
                                        "Description": "If true, then you will be allowed to equip the item if you pass its other requirements.This being false means that you cannot equip the item under any circumstances.",
                                        "Attributes": []
                                    },
                                    "damageTypeHashes": {
                                        "Name": "damageTypeHashes",
                                        "Type": "array",
                                        "Description": "Theoretically, an item can have many possible damage types. In *practice*, this is not true, but just in case weapons start being made that have multiple (for instance, an item where a socket has reusable plugs for every possible damage type that you can choose from freely), this field will return all of the possible damage types that are available to the weapon by default.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "damageTypes": {
                                        "Name": "damageTypes",
                                        "Type": "array",
                                        "Description": "This is the list of all damage types that we know ahead of time the item can take on. Unfortunately, this does not preclude the possibility of something funky happening to give the item a damage type that cannot be predicted beforehand: for example, if some designer decides to create arbitrary non-reusable plugs that cause damage type to change.This damage type prediction will only use the following to determine potential damage types:- Intrinsic perks- Talent Node perks- Known, reusable plugs for sockets",
                                        "Attributes": [],
                                        "Array Contents": "int32"
                                    },
                                    "defaultDamageType": {
                                        "Name": "defaultDamageType",
                                        "Type": "int32",
                                        "Description": "If the item has a damage type that could be considered to be default, it will be populated here.For various upsetting reasons, it's surprisingly cumbersome to figure this out. I hope you're happy.",
                                        "Attributes": []
                                    },
                                    "defaultDamageTypeHash": {
                                        "Name": "defaultDamageTypeHash",
                                        "Type": "uint32",
                                        "Description": "Similar to defaultDamageType, but represented as the hash identifier for a DestinyDamageTypeDefinition.I will likely regret leaving in the enumeration versions of these properties, but for now they're very convenient.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "seasonHash": {
                                        "Name": "seasonHash",
                                        "Type": "uint32",
                                        "Description": "If this item is related directly to a Season of Destiny, this is the hash identifier for that season.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "isWrapper": {
                                        "Name": "isWrapper",
                                        "Type": "boolean",
                                        "Description": "If true, this is a dummy vendor-wrapped item template. Items purchased from Eververse will be \"wrapped\" by one of these items so that we can safely provide refund capabilities before the item is \"unwrapped\".",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "Traits are metadata tags applied to this item. For example: armor slot, weapon type, foundry, faction, etc. These IDs come from the game and don't map to any content, but should still be useful.",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "These are the corresponding trait definition hashes for the entries in traitIds.",
                                        "Attributes": [],
                                        "Array Contents": "uint32"
                                    },
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
                            }
                        ]
                    },
                    "IsOffer": {
                        "Name": "IsOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "HasOffer": {
                        "Name": "HasOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "OfferApplied": {
                        "Name": "OfferApplied",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "DecryptedToken": {
                        "Name": "DecryptedToken",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "IsLoyaltyReward": {
                        "Name": "IsLoyaltyReward",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "ShopifyEndDate": {
                        "Name": "ShopifyEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": [
                            "Nullable"
                        ]
                    },
                    "GameEarnByDate": {
                        "Name": "GameEarnByDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "RedemptionEndDate": {
                        "Name": "RedemptionEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    }
                },
                "IsAvailableForUser": {
                    "Name": "IsAvailableForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "IsUnlockedForUser": {
                    "Name": "IsUnlockedForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                }
            },
            "ObjectiveDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            },
            "RewardDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Tokens-GetBungieRewardsForPlatformUser.html#operation_get_Tokens-GetBungieRewardsForPlatformUser"""

        try:
            self.logger.info("Executing GetBungieRewardsForPlatformUser...")
            url = (
                self.base_url
                + f"/Tokens/Rewards/GetRewardsForPlatformUser/{membershipId}/{membershipType}/".format(
                    membershipId=membershipId, membershipType=membershipType
                )
            )
            return await self.requester.request(
                method=HTTPMethod.GET, url=url, access_token=access_token
            )
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsList(self) -> dict:
        """Returns a list of the current bungie rewards

            Args:

            Returns:
        {
            "UserRewardAvailabilityModel": {
                "AvailabilityModel": {
                    "HasExistingCode": {
                        "Name": "HasExistingCode",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "RecordDefinitions": {
                        "Name": "RecordDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "displayProperties": {
                                    "description": {
                                        "Name": "description",
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
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                        "Attributes": []
                                    },
                                    "iconSequences": {
                                        "Name": "iconSequences",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "frames": {
                                                    "Name": "frames",
                                                    "Type": "array",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "highResIcon": {
                                        "Name": "highResIcon",
                                        "Type": "string",
                                        "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                        "Attributes": []
                                    },
                                    "hasIcon": {
                                        "Name": "hasIcon",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "scope": {
                                    "Name": "scope",
                                    "Type": "int32",
                                    "Description": "Indicates whether this Record's state is determined on a per-character or on an account-wide basis.",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationInfo": {
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "parentPresentationNodeHashes": {
                                        "Name": "parentPresentationNodeHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "displayStyle": {
                                        "Name": "displayStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "loreHash": {
                                    "Name": "loreHash",
                                    "Type": "uint32",
                                    "Description": "",
                                    "Attributes": [
                                        "Nullable",
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "objectiveHashes": {
                                    "Name": "objectiveHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "recordValueStyle": {
                                    "Name": "recordValueStyle",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "forTitleGilding": {
                                    "Name": "forTitleGilding",
                                    "Type": "boolean",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "shouldShowLargeIcons": {
                                    "Name": "shouldShowLargeIcons",
                                    "Type": "boolean",
                                    "Description": "A hint to show a large icon for a reward",
                                    "Attributes": []
                                }
                            },
                            {
                                "titleInfo": {
                                    "hasTitle": {
                                        "Name": "hasTitle",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGender": {
                                        "Name": "titlesByGender",
                                        "Type": "object",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "titlesByGenderHash": {
                                        "Name": "titlesByGenderHash",
                                        "Type": "object",
                                        "Description": "For those who prefer to use the definitions.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "gildingTrackingRecordHash": {
                                        "Name": "gildingTrackingRecordHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    }
                                }
                            },
                            {
                                "completionInfo": {
                                    "partialCompletionObjectiveCountThreshold": {
                                        "Name": "partialCompletionObjectiveCountThreshold",
                                        "Type": "int32",
                                        "Description": "The number of objectives that must be completed before the objective is considered \"complete\"",
                                        "Attributes": []
                                    },
                                    "ScoreValue": {
                                        "Name": "ScoreValue",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "shouldFireToast": {
                                        "Name": "shouldFireToast",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "toastStyle": {
                                        "Name": "toastStyle",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "stateInfo": {
                                    "featuredPriority": {
                                        "Name": "featuredPriority",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "obscuredName": {
                                        "Name": "obscuredName",
                                        "Type": "string",
                                        "Description": "A display name override to show when this record is 'obscured' instead of the default obscured display name.",
                                        "Attributes": []
                                    },
                                    "obscuredDescription": {
                                        "Name": "obscuredDescription",
                                        "Type": "string",
                                        "Description": "A display description override to show when this record is 'obscured' instead of the default obscured display description.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "requirements": {
                                    "entitlementUnavailableMessage": {
                                        "Name": "entitlementUnavailableMessage",
                                        "Type": "string",
                                        "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "expirationInfo": {
                                    "hasExpiration": {
                                        "Name": "hasExpiration",
                                        "Type": "boolean",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "description": {
                                        "Name": "description",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "icon": {
                                        "Name": "icon",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    }
                                }
                            },
                            {
                                "intervalInfo": {
                                    "Name": "intervalInfo",
                                    "Type": "object",
                                    "Description": "Some records have multiple 'interval' objectives, and the record may be claimed at each completed interval",
                                    "Attributes": []
                                }
                            },
                            {
                                "rewardItems": {
                                    "Name": "rewardItems",
                                    "Type": "array",
                                    "Description": "If there is any publicly available information about rewards earned for achieving this record, this is the list of those items. However, note that some records intentionally have \"hidden\" rewards. These will not be returned in this list.",
                                    "Attributes": []
                                }
                            },
                            {
                                "recordTypeName": {
                                    "Name": "recordTypeName",
                                    "Type": "string",
                                    "Description": "A display name for the type of record this is (Triumphs, Lore, Medals, Seasonal Challenge, etc.).",
                                    "Attributes": []
                                }
                            },
                            {
                                "presentationNodeType": {
                                    "Name": "presentationNodeType",
                                    "Type": "int32",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitIds": {
                                    "Name": "traitIds",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": []
                                }
                            },
                            {
                                "traitHashes": {
                                    "Name": "traitHashes",
                                    "Type": "array",
                                    "Description": "",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "parentNodeHashes": {
                                    "Name": "parentNodeHashes",
                                    "Type": "array",
                                    "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                    "Attributes": [
                                        "Mapped to Definition"
                                    ]
                                }
                            },
                            {
                                "hash": {
                                    "Name": "hash",
                                    "Type": "uint32",
                                    "Description": "The unique identifier for this entity. Guaranteed to be unique for the type of entity, but not globally.When entities refer to each other in Destiny content, it is this hash that they are referring to.",
                                    "Attributes": []
                                }
                            },
                            {
                                "index": {
                                    "Name": "index",
                                    "Type": "int32",
                                    "Description": "The index of the entity as it was found in the investment tables.",
                                    "Attributes": []
                                }
                            },
                            {
                                "redacted": {
                                    "Name": "redacted",
                                    "Type": "boolean",
                                    "Description": "If this is true, then there is an entity with this identifier/type combination, but BNet is not yet allowed to show it. Sorry!",
                                    "Attributes": []
                                }
                            }
                        ]
                    },
                    "CollectibleDefinitions": {
                        "Name": "CollectibleDefinitions",
                        "Type": "array",
                        "Description": "",
                        "Attributes": [],
                        "Array Contents": [
                            {
                                "CollectibleDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "scope": {
                                        "Name": "scope",
                                        "Type": "int32",
                                        "Description": "Indicates whether the state of this Collectible is determined on a per-character or on an account-wide basis.",
                                        "Attributes": []
                                    },
                                    "sourceString": {
                                        "Name": "sourceString",
                                        "Type": "string",
                                        "Description": "A human readable string for a hint about how to acquire the item.",
                                        "Attributes": []
                                    },
                                    "sourceHash": {
                                        "Name": "sourceHash",
                                        "Type": "uint32",
                                        "Description": "This is a hash identifier we are building on the BNet side in an attempt to let people group collectibles by similar sources.I can't promise that it's going to be 100% accurate, but if the designers were consistent in assigning the same source strings to items with the same sources, it *ought to* be. No promises though.This hash also doesn't relate to an actual definition, just to note: we've got nothing useful other than the source string for this data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "itemHash": {
                                        "Name": "itemHash",
                                        "Type": "uint32",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "acquisitionInfo": {
                                        "acquireMaterialRequirementHash": {
                                            "Name": "acquireMaterialRequirementHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "acquireTimestampUnlockValueHash": {
                                            "Name": "acquireTimestampUnlockValueHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        }
                                    },
                                    "stateInfo": {
                                        "obscuredOverrideItemHash": {
                                            "Name": "obscuredOverrideItemHash",
                                            "Type": "uint32",
                                            "Description": "",
                                            "Attributes": [
                                                "Nullable",
                                                "Mapped to Definition"
                                            ]
                                        },
                                        "requirements": {
                                            "entitlementUnavailableMessage": {
                                                "Name": "entitlementUnavailableMessage",
                                                "Type": "string",
                                                "Description": "If this node is not accessible due to Entitlements (for instance, you don't own the required game expansion), this is the message to show.",
                                                "Attributes": []
                                            }
                                        }
                                    },
                                    "presentationInfo": {
                                        "presentationNodeType": {
                                            "Name": "presentationNodeType",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        },
                                        "parentPresentationNodeHashes": {
                                            "Name": "parentPresentationNodeHashes",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [
                                                "Mapped to Definition"
                                            ],
                                            "Array Contents": "uint32"
                                        },
                                        "displayStyle": {
                                            "Name": "displayStyle",
                                            "Type": "int32",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "presentationNodeType": {
                                        "Name": "presentationNodeType",
                                        "Type": "int32",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "parentNodeHashes": {
                                        "Name": "parentNodeHashes",
                                        "Type": "array",
                                        "Description": "A quick reference to presentation nodes that have this node as a child. Presentation nodes can be parented under multiple parents.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
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
                            },
                            {
                                "DestinyInventoryItemDefinition": {
                                    "displayProperties": {
                                        "description": {
                                            "Name": "description",
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
                                        "icon": {
                                            "Name": "icon",
                                            "Type": "string",
                                            "Description": "Note that \"icon\" is sometimes misleading, and should be interpreted in the context of the entity. For instance, in Destiny 1 the DestinyRecordBookDefinition's icon was a big picture of a book.But usually, it will be a small square image that you can use as... well, an icon.They are currently represented as 96px x 96px images.",
                                            "Attributes": []
                                        },
                                        "iconSequences": {
                                            "Name": "iconSequences",
                                            "Type": "array",
                                            "Description": "",
                                            "Attributes": [],
                                            "Array Contents": [
                                                {
                                                    "frames": {
                                                        "Name": "frames",
                                                        "Type": "array",
                                                        "Description": "",
                                                        "Attributes": []
                                                    }
                                                }
                                            ]
                                        },
                                        "highResIcon": {
                                            "Name": "highResIcon",
                                            "Type": "string",
                                            "Description": "If this item has a high-res icon (at least for now, many things won't), then the path to that icon will be here.",
                                            "Attributes": []
                                        },
                                        "hasIcon": {
                                            "Name": "hasIcon",
                                            "Type": "boolean",
                                            "Description": "",
                                            "Attributes": []
                                        }
                                    },
                                    "tooltipNotifications": {
                                        "Name": "tooltipNotifications",
                                        "Type": "array",
                                        "Description": "Tooltips that only come up conditionally for the item. Check the live data DestinyItemComponent.tooltipNotificationIndexes property for which of these should be shown at runtime.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "displayString": {
                                                    "Name": "displayString",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "displayStyle": {
                                                    "Name": "displayStyle",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "collectibleHash": {
                                        "Name": "collectibleHash",
                                        "Type": "uint32",
                                        "Description": "If this item has a collectible related to it, this is the hash identifier of that collectible entry.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "iconWatermark": {
                                        "Name": "iconWatermark",
                                        "Type": "string",
                                        "Description": "If available, this is the original 'active' release watermark overlay for the icon. If the item has different versions, this can be overridden by the 'display version watermark icon' from the 'quality' block. Alternatively, if there is no watermark for the version, and the item version has a power cap below the current season power cap, this can be overridden by the iconWatermarkShelved property.",
                                        "Attributes": []
                                    },
                                    "iconWatermarkShelved": {
                                        "Name": "iconWatermarkShelved",
                                        "Type": "string",
                                        "Description": "If available, this is the 'shelved' release watermark overlay for the icon. If the item version has a power cap below the current season power cap, it can be treated as 'shelved', and should be shown with this 'shelved' watermark overlay.",
                                        "Attributes": []
                                    },
                                    "secondaryIcon": {
                                        "Name": "secondaryIcon",
                                        "Type": "string",
                                        "Description": "A secondary icon associated with the item. Currently this is used in very context specific applications, such as Emblem Nameplates.",
                                        "Attributes": []
                                    },
                                    "secondaryOverlay": {
                                        "Name": "secondaryOverlay",
                                        "Type": "string",
                                        "Description": "Pulled from the secondary icon, this is the \"secondary background\" of the secondary icon. Confusing? Sure, that's why I call it \"overlay\" here: because as far as it's been used thus far, it has been for an optional overlay image. We'll see if that holds up, but at least for now it explains what this image is a bit better.",
                                        "Attributes": []
                                    },
                                    "secondarySpecial": {
                                        "Name": "secondarySpecial",
                                        "Type": "string",
                                        "Description": "Pulled from the Secondary Icon, this is the \"special\" background for the item. For Emblems, this is the background image used on the Details view: but it need not be limited to that for other types of items.",
                                        "Attributes": []
                                    },
                                    "backgroundColor": {
                                        "Name": "backgroundColor",
                                        "Type": "object",
                                        "Description": "Sometimes, an item will have a background color. Most notably this occurs with Emblems, who use the Background Color for small character nameplates such as the \"friends\" view you see in-game. There are almost certainly other items that have background color as well, though I have not bothered to investigate what items have it nor what purposes they serve: use it as you will.",
                                        "Attributes": []
                                    },
                                    "screenshot": {
                                        "Name": "screenshot",
                                        "Type": "string",
                                        "Description": "If we were able to acquire an in-game screenshot for the item, the path to that screenshot will be returned here. Note that not all items have screenshots: particularly not any non-equippable items.",
                                        "Attributes": []
                                    },
                                    "itemTypeDisplayName": {
                                        "Name": "itemTypeDisplayName",
                                        "Type": "string",
                                        "Description": "The localized title/name of the item's type. This can be whatever the designers want, and has no guarantee of consistency between items.",
                                        "Attributes": []
                                    },
                                    "flavorText": {
                                        "Name": "flavorText",
                                        "Type": "string",
                                        "Description": "",
                                        "Attributes": []
                                    },
                                    "uiItemDisplayStyle": {
                                        "Name": "uiItemDisplayStyle",
                                        "Type": "string",
                                        "Description": "A string identifier that the game's UI uses to determine how the item should be rendered in inventory screens and the like. This could really be anything - at the moment, we don't have the time to really breakdown and maintain all the possible strings this could be, partly because new ones could be added ad hoc. But if you want to use it to dictate your own UI, or look for items with a certain display style, go for it!",
                                        "Attributes": []
                                    },
                                    "itemTypeAndTierDisplayName": {
                                        "Name": "itemTypeAndTierDisplayName",
                                        "Type": "string",
                                        "Description": "It became a common enough pattern in our UI to show Item Type and Tier combined into a single localized string that I'm just going to go ahead and start pre-creating these for items.",
                                        "Attributes": []
                                    },
                                    "displaySource": {
                                        "Name": "displaySource",
                                        "Type": "string",
                                        "Description": "In theory, it is a localized string telling you about how you can find the item. I really wish this was more consistent. Many times, it has nothing. Sometimes, it's instead a more narrative-forward description of the item. Which is cool, and I wish all properties had that data, but it should really be its own property.",
                                        "Attributes": []
                                    },
                                    "tooltipStyle": {
                                        "Name": "tooltipStyle",
                                        "Type": "string",
                                        "Description": "An identifier that the game UI uses to determine what type of tooltip to show for the item. These have no corresponding definitions that BNet can link to: so it'll be up to you to interpret and display your UI differently according to these styles (or ignore it).",
                                        "Attributes": []
                                    },
                                    "action": {
                                        "Name": "action",
                                        "Type": "object",
                                        "Description": "If the item can be \"used\", this block will be non-null, and will have data related to the action performed when using the item. (Guess what? 99% of the time, this action is \"dismantle\". Shocker)",
                                        "Attributes": []
                                    },
                                    "crafting": {
                                        "Name": "crafting",
                                        "Type": "object",
                                        "Description": "Recipe items will have relevant crafting information available here.",
                                        "Attributes": []
                                    },
                                    "inventory": {
                                        "Name": "inventory",
                                        "Type": "object",
                                        "Description": "If this item can exist in an inventory, this block will be non-null. In practice, every item that currently exists has one of these blocks. But note that it is not necessarily guaranteed.",
                                        "Attributes": []
                                    },
                                    "setData": {
                                        "Name": "setData",
                                        "Type": "object",
                                        "Description": "If this item is a quest, this block will be non-null. In practice, I wish I had called this the Quest block, but at the time it wasn't clear to me whether it would end up being used for purposes other than quests. It will contain data about the steps in the quest, and mechanics we can use for displaying and tracking the quest.",
                                        "Attributes": []
                                    },
                                    "stats": {
                                        "Name": "stats",
                                        "Type": "object",
                                        "Description": "If this item can have stats (such as a weapon, armor, or vehicle), this block will be non-null and populated with the stats found on the item.",
                                        "Attributes": []
                                    },
                                    "emblemObjectiveHash": {
                                        "Name": "emblemObjectiveHash",
                                        "Type": "uint32",
                                        "Description": "If the item is an emblem that has a special Objective attached to it - for instance, if the emblem tracks PVP Kills, or what-have-you. This is a bit different from, for example, the Vanguard Kill Tracker mod, which pipes data into the \"art channel\". When I get some time, I would like to standardize these so you can get at the values they expose without having to care about what they're being used for and how they are wired up, but for now here's the raw data.",
                                        "Attributes": [
                                            "Nullable"
                                        ]
                                    },
                                    "equippingBlock": {
                                        "Name": "equippingBlock",
                                        "Type": "object",
                                        "Description": "If this item can be equipped, this block will be non-null and will be populated with the conditions under which it can be equipped.",
                                        "Attributes": []
                                    },
                                    "translationBlock": {
                                        "Name": "translationBlock",
                                        "Type": "object",
                                        "Description": "If this item can be rendered, this block will be non-null and will be populated with rendering information.",
                                        "Attributes": []
                                    },
                                    "preview": {
                                        "Name": "preview",
                                        "Type": "object",
                                        "Description": "If this item can be Used or Acquired to gain other items (for instance, how Eververse Boxes can be consumed to get items from the box), this block will be non-null and will give summary information for the items that can be acquired.",
                                        "Attributes": []
                                    },
                                    "quality": {
                                        "Name": "quality",
                                        "Type": "object",
                                        "Description": "If this item can have a level or stats, this block will be non-null and will be populated with default quality (item level, \"quality\", and infusion) data. See the block for more details, there's often less upfront information in D2 so you'll want to be aware of how you use quality and item level on the definition level now.",
                                        "Attributes": []
                                    },
                                    "value": {
                                        "Name": "value",
                                        "Type": "object",
                                        "Description": "The conceptual \"Value\" of an item, if any was defined. See the DestinyItemValueBlockDefinition for more details.",
                                        "Attributes": []
                                    },
                                    "sourceData": {
                                        "Name": "sourceData",
                                        "Type": "object",
                                        "Description": "If this item has a known source, this block will be non-null and populated with source information. Unfortunately, at this time we are not generating sources: that is some aggressively manual work which we didn't have time for, and I'm hoping to get back to at some point in the future.",
                                        "Attributes": []
                                    },
                                    "objectives": {
                                        "Name": "objectives",
                                        "Type": "object",
                                        "Description": "If this item has Objectives (extra tasks that can be accomplished related to the item... most frequently when the item is a Quest Step and the Objectives need to be completed to move on to the next Quest Step), this block will be non-null and the objectives defined herein.",
                                        "Attributes": []
                                    },
                                    "metrics": {
                                        "Name": "metrics",
                                        "Type": "object",
                                        "Description": "If this item has available metrics to be shown, this block will be non-null have the appropriate hashes defined.",
                                        "Attributes": []
                                    },
                                    "plug": {
                                        "Name": "plug",
                                        "Type": "object",
                                        "Description": "If this item *is* a Plug, this will be non-null and the info defined herein. See DestinyItemPlugDefinition for more information.",
                                        "Attributes": []
                                    },
                                    "gearset": {
                                        "Name": "gearset",
                                        "Type": "object",
                                        "Description": "If this item has related items in a \"Gear Set\", this will be non-null and the relationships defined herein.",
                                        "Attributes": []
                                    },
                                    "sack": {
                                        "Name": "sack",
                                        "Type": "object",
                                        "Description": "If this item is a \"reward sack\" that can be opened to provide other items, this will be non-null and the properties of the sack contained herein.",
                                        "Attributes": []
                                    },
                                    "sockets": {
                                        "Name": "sockets",
                                        "Type": "object",
                                        "Description": "If this item has any Sockets, this will be non-null and the individual sockets on the item will be defined herein.",
                                        "Attributes": []
                                    },
                                    "summary": {
                                        "Name": "summary",
                                        "Type": "object",
                                        "Description": "Summary data about the item.",
                                        "Attributes": []
                                    },
                                    "talentGrid": {
                                        "Name": "talentGrid",
                                        "Type": "object",
                                        "Description": "If the item has a Talent Grid, this will be non-null and the properties of the grid defined herein. Note that, while many items still have talent grids, the only ones with meaningful Nodes still on them will be Subclass/\"Build\" items.",
                                        "Attributes": []
                                    },
                                    "investmentStats": {
                                        "Name": "investmentStats",
                                        "Type": "array",
                                        "Description": "If the item has stats, this block will be defined. It has the \"raw\" investment stats for the item. These investment stats don't take into account the ways that the items can spawn, nor do they take into account any Stat Group transformations. I have retained them for debugging purposes, but I do not know how useful people will find them.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "statTypeHash": {
                                                    "Name": "statTypeHash",
                                                    "Type": "uint32",
                                                    "Description": "The hash identifier for the DestinyStatDefinition defining this stat.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "value": {
                                                    "Name": "value",
                                                    "Type": "int32",
                                                    "Description": "The raw \"Investment\" value for the stat, before transformations are performed to turn this raw stat into stats that are displayed in the game UI.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "isConditionallyActive": {
                                                    "Name": "isConditionallyActive",
                                                    "Type": "boolean",
                                                    "Description": "If this is true, the stat will only be applied on the item in certain game state conditions, and we can't know statically whether or not this stat will be applied. Check the \"live\" API data instead for whether this value is being applied on a specific instance of the item in question, and you can use this to decide whether you want to show the stat on the generic view of the item, or whether you want to show some kind of caveat or warning about the stat value being conditional on game state.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "perks": {
                                        "Name": "perks",
                                        "Type": "array",
                                        "Description": "If the item has any *intrinsic* Perks (Perks that it will provide regardless of Sockets, Talent Grid, and other transitory state), they will be defined here.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "requirementDisplayString": {
                                                    "Name": "requirementDisplayString",
                                                    "Type": "string",
                                                    "Description": "If this perk is not active, this is the string to show for why it's not providing its benefits.",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "perkHash": {
                                                    "Name": "perkHash",
                                                    "Type": "uint32",
                                                    "Description": "A hash identifier for the DestinySandboxPerkDefinition being provided on the item.",
                                                    "Attributes": [
                                                        "Mapped to Definition"
                                                    ]
                                                }
                                            },
                                            {
                                                "perkVisibility": {
                                                    "Name": "perkVisibility",
                                                    "Type": "int32",
                                                    "Description": "Indicates whether this perk should be shown, or if it should be shown disabled.",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "loreHash": {
                                        "Name": "loreHash",
                                        "Type": "uint32",
                                        "Description": "If the item has any related Lore (DestinyLoreDefinition), this will be the hash identifier you can use to look up the lore definition.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "summaryItemHash": {
                                        "Name": "summaryItemHash",
                                        "Type": "uint32",
                                        "Description": "There are times when the game will show you a \"summary/vague\" version of an item - such as a description of its type represented as a DestinyInventoryItemDefinition - rather than display the item itself.This happens sometimes when summarizing possible rewards in a tooltip. This is the item displayed instead, if it exists.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "animations": {
                                        "Name": "animations",
                                        "Type": "array",
                                        "Description": "If any animations were extracted from game content for this item, these will be the definitions of those animations.",
                                        "Attributes": [],
                                        "Array Contents": [
                                            {
                                                "animName": {
                                                    "Name": "animName",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            },
                                            {
                                                "animIdentifier": {
                                                    "Name": "animIdentifier",
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
                                            }
                                        ]
                                    },
                                    "allowActions": {
                                        "Name": "allowActions",
                                        "Type": "boolean",
                                        "Description": "BNet may forbid the execution of actions on this item via the API. If that is occurring, allowActions will be set to false.",
                                        "Attributes": []
                                    },
                                    "links": {
                                        "Name": "links",
                                        "Type": "array",
                                        "Description": "If we added any help or informational URLs about this item, these will be those links.",
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
                                                "url": {
                                                    "Name": "url",
                                                    "Type": "string",
                                                    "Description": "",
                                                    "Attributes": []
                                                }
                                            }
                                        ]
                                    },
                                    "doesPostmasterPullHaveSideEffects": {
                                        "Name": "doesPostmasterPullHaveSideEffects",
                                        "Type": "boolean",
                                        "Description": "The boolean will indicate to us (and you!) whether something *could* happen when you transfer this item from the Postmaster that might be considered a \"destructive\" action.It is not feasible currently to tell you (or ourelves!) in a consistent way whether this *will* actually cause a destructive action, so we are playing it safe: if it has the potential to do so, we will not allow it to be transferred from the Postmaster by default. You will need to check for this flag before transferring an item from the Postmaster, or else you'll end up receiving an error.",
                                        "Attributes": []
                                    },
                                    "nonTransferrable": {
                                        "Name": "nonTransferrable",
                                        "Type": "boolean",
                                        "Description": "The intrinsic transferability of an item.I hate that this boolean is negative - but there's a reason.Just because an item is intrinsically transferrable doesn't mean that it can be transferred, and we don't want to imply that this is the only source of that transferability.",
                                        "Attributes": []
                                    },
                                    "itemCategoryHashes": {
                                        "Name": "itemCategoryHashes",
                                        "Type": "array",
                                        "Description": "BNet attempts to make a more formal definition of item \"Categories\", as defined by DestinyItemCategoryDefinition. This is a list of all Categories that we were able to algorithmically determine that this item is a member of. (for instance, that it's a \"Weapon\", that it's an \"Auto Rifle\", etc...)The algorithm for these is, unfortunately, volatile. If you believe you see a miscategorized item, please let us know on the Bungie API forums.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "specialItemType": {
                                        "Name": "specialItemType",
                                        "Type": "int32",
                                        "Description": "In Destiny 1, we identified some items as having particular categories that we'd like to know about for various internal logic purposes. These are defined in SpecialItemType, and while these days the itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemType": {
                                        "Name": "itemType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"base\" the of the item. This enum is a useful but dramatic oversimplification of what it means for an item to have a \"Type\". Still, it's handy in many situations.itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "itemSubType": {
                                        "Name": "itemSubType",
                                        "Type": "int32",
                                        "Description": "A value indicating the \"sub-type\" of the item. For instance, where an item might have an itemType value \"Weapon\", this will be something more specific like \"Auto Rifle\".itemCategoryHashes are the preferred way of identifying types, we have retained this enum for its convenience.",
                                        "Attributes": []
                                    },
                                    "classType": {
                                        "Name": "classType",
                                        "Type": "int32",
                                        "Description": "We run a similarly weak-sauce algorithm to try and determine whether an item is restricted to a specific class. If we find it to be restricted in such a way, we set this classType property to match the class' enumeration value so that users can easily identify class restricted items.If you see a mis-classed item, please inform the developers in the Bungie API forum.",
                                        "Attributes": []
                                    },
                                    "breakerType": {
                                        "Name": "breakerType",
                                        "Type": "int32",
                                        "Description": "Some weapons and plugs can have a \"Breaker Type\": a special ability that works sort of like damage type vulnerabilities. This is (almost?) always set on items by plugs.",
                                        "Attributes": []
                                    },
                                    "breakerTypeHash": {
                                        "Name": "breakerTypeHash",
                                        "Type": "uint32",
                                        "Description": "Since we also have a breaker type definition, this is the hash for that breaker type for your convenience. Whether you use the enum or hash and look up the definition depends on what's cleanest for your code.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "equippable": {
                                        "Name": "equippable",
                                        "Type": "boolean",
                                        "Description": "If true, then you will be allowed to equip the item if you pass its other requirements.This being false means that you cannot equip the item under any circumstances.",
                                        "Attributes": []
                                    },
                                    "damageTypeHashes": {
                                        "Name": "damageTypeHashes",
                                        "Type": "array",
                                        "Description": "Theoretically, an item can have many possible damage types. In *practice*, this is not true, but just in case weapons start being made that have multiple (for instance, an item where a socket has reusable plugs for every possible damage type that you can choose from freely), this field will return all of the possible damage types that are available to the weapon by default.",
                                        "Attributes": [
                                            "Mapped to Definition"
                                        ],
                                        "Array Contents": "uint32"
                                    },
                                    "damageTypes": {
                                        "Name": "damageTypes",
                                        "Type": "array",
                                        "Description": "This is the list of all damage types that we know ahead of time the item can take on. Unfortunately, this does not preclude the possibility of something funky happening to give the item a damage type that cannot be predicted beforehand: for example, if some designer decides to create arbitrary non-reusable plugs that cause damage type to change.This damage type prediction will only use the following to determine potential damage types:- Intrinsic perks- Talent Node perks- Known, reusable plugs for sockets",
                                        "Attributes": [],
                                        "Array Contents": "int32"
                                    },
                                    "defaultDamageType": {
                                        "Name": "defaultDamageType",
                                        "Type": "int32",
                                        "Description": "If the item has a damage type that could be considered to be default, it will be populated here.For various upsetting reasons, it's surprisingly cumbersome to figure this out. I hope you're happy.",
                                        "Attributes": []
                                    },
                                    "defaultDamageTypeHash": {
                                        "Name": "defaultDamageTypeHash",
                                        "Type": "uint32",
                                        "Description": "Similar to defaultDamageType, but represented as the hash identifier for a DestinyDamageTypeDefinition.I will likely regret leaving in the enumeration versions of these properties, but for now they're very convenient.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "seasonHash": {
                                        "Name": "seasonHash",
                                        "Type": "uint32",
                                        "Description": "If this item is related directly to a Season of Destiny, this is the hash identifier for that season.",
                                        "Attributes": [
                                            "Nullable",
                                            "Mapped to Definition"
                                        ]
                                    },
                                    "isWrapper": {
                                        "Name": "isWrapper",
                                        "Type": "boolean",
                                        "Description": "If true, this is a dummy vendor-wrapped item template. Items purchased from Eververse will be \"wrapped\" by one of these items so that we can safely provide refund capabilities before the item is \"unwrapped\".",
                                        "Attributes": []
                                    },
                                    "traitIds": {
                                        "Name": "traitIds",
                                        "Type": "array",
                                        "Description": "Traits are metadata tags applied to this item. For example: armor slot, weapon type, foundry, faction, etc. These IDs come from the game and don't map to any content, but should still be useful.",
                                        "Attributes": [],
                                        "Array Contents": "string"
                                    },
                                    "traitHashes": {
                                        "Name": "traitHashes",
                                        "Type": "array",
                                        "Description": "These are the corresponding trait definition hashes for the entries in traitIds.",
                                        "Attributes": [],
                                        "Array Contents": "uint32"
                                    },
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
                            }
                        ]
                    },
                    "IsOffer": {
                        "Name": "IsOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "HasOffer": {
                        "Name": "HasOffer",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "OfferApplied": {
                        "Name": "OfferApplied",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "DecryptedToken": {
                        "Name": "DecryptedToken",
                        "Type": "string",
                        "Description": "",
                        "Attributes": []
                    },
                    "IsLoyaltyReward": {
                        "Name": "IsLoyaltyReward",
                        "Type": "boolean",
                        "Description": "",
                        "Attributes": []
                    },
                    "ShopifyEndDate": {
                        "Name": "ShopifyEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": [
                            "Nullable"
                        ]
                    },
                    "GameEarnByDate": {
                        "Name": "GameEarnByDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    },
                    "RedemptionEndDate": {
                        "Name": "RedemptionEndDate",
                        "Type": "date-time",
                        "Description": "",
                        "Attributes": []
                    }
                },
                "IsAvailableForUser": {
                    "Name": "IsAvailableForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                },
                "IsUnlockedForUser": {
                    "Name": "IsUnlockedForUser",
                    "Type": "boolean",
                    "Description": "",
                    "Attributes": []
                }
            },
            "ObjectiveDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            },
            "RewardDisplayProperties": {
                "Name": {
                    "Name": "Name",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "Description": {
                    "Name": "Description",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                },
                "ImagePath": {
                    "Name": "ImagePath",
                    "Type": "string",
                    "Description": "",
                    "Attributes": []
                }
            }
        }


        .. seealso:: https://bungie-net.github.io/multi/operation_get_Tokens-GetBungieRewardsList.html#operation_get_Tokens-GetBungieRewardsList"""

        try:
            self.logger.info("Executing GetBungieRewardsList...")
            url = self.base_url + "/Tokens/Rewards/BungieRewards/".format()
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
