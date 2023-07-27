# Push Interface 3.0 - User Manual

Type: Glossary
Status: Done
Authors: Ankit Singhal
Repository: sn-push
Last edited time: July 19, 2023 5:38 PM
Created time: December 9, 2021 8:09 AM
Slack Channel: #push-platform

### **Change History**

- @Dixen Cheng 2022/12/27 : Added new interface `/api/v2/push` for supporting sending the push in the near feature specific time.
- @Ankit Singhal May 11, 2023 : Refactored the document to make it clear and added the User.Query.Key = SPECIFIED_TARGETING

---

# Overview Push Platform Design

[https://whimsical.com/detailed-design-push-platform-v2-J5yRbumQsdQyxV1fs2KXj4](https://whimsical.com/detailed-design-push-platform-v2-J5yRbumQsdQyxV1fs2KXj4)

# Service Endpoint

- Development: `http://sn-push-interface.sn-push.dev.smartnews.net`
- Staging: `http://sn-push-interface.sn-push.stg.smartnews.net`
- Production: `http://sn-push-interface.sn-push.smartnews.net`

# API endpoints

- (Deprecated)`/api/v1/push`

<aside>
⚠️ We suggest users to not use the `v1` API for future use cases as it is not maintained now.

</aside>

- (Supported)`/api/v2/push`

# API Request Body

POST request JSON format (For `v2` API):

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| pushId | int | No | If provided, will be used as Push ID, otherwise, default to expiredEpochSecond |
| pushType | String | Yes | Push type name |
| edition | String | Yes | Edition, possible value: en_US or ja_JP |
| expiredEpochSecond | int | Yes | The message TTL. Users won’t receive push after expired timestamp. If the push is not time sensitive, request time + 10+hours is recommended |
| https://www.notion.so/Push-Interface-3-0-User-Manual-5b55200f4f5c4eb9bf51f4bd7ee35e05?pvs=21 | Object | Yes | UserQuery object to define how to query users |
| https://www.notion.so/Push-Interface-3-0-User-Manual-5b55200f4f5c4eb9bf51f4bd7ee35e05?pvs=21 | Object | Yes | List of PushCandidate objects to define push content. If there’re more then 1 article to send, please make sure the linkId and url is different from each other. (especially in deep link case) |
| additionalInfo | Map<String, Object> | No | Additional info map. Will be passed to various custom processors. Please see the backend service code for more references. |
| https://www.notion.so/Push-Interface-3-0-User-Manual-5b55200f4f5c4eb9bf51f4bd7ee35e05?pvs=21 | Object | Yes | Registrar push which accept by registering the future specific time for the delivery. |

### Object Definitions

`userQuery`

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| key | String | Yes | Possible value: VIRTUAL_ID_LIST, GEO_ENVELOP, SPECIFIED_TARGETING
GEO_CIRCLE (deprecated), , GEO_POLYGON (deprecated) |
| value | Object | Yes | If key is VIRTUAL_ID_LIST, the value should be a list of strings representing virtual ids of the users whom the push is intended for.
If key is https://www.notion.so/Push-Interface-3-0-User-Manual-5b55200f4f5c4eb9bf51f4bd7ee35e05?pvs=21, the value is expected to be List<TargetingCondition>
If key is geo_envelope, the value should be a https://www.notion.so/Push-Interface-3-0-User-Manual-5b55200f4f5c4eb9bf51f4bd7ee35e05?pvs=21 object.
If key is geo_circle, the value should be a GeoQueryCirlce object.
If key is geo_polygon, the value should be a geo polygon JSON object. |

`TargetingConditions` (When UserQuery.Key = `SPECIFIED_TARGETING`)

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| targetType | String | Yes | (Future Scope)FEATURE_FLAGS 
(Existing)AB_TEST_VARIANT_IDS, CHANNEL_IDENTIFIERS, PREFECTURE_CODES |
| targetValue | Object | Yes | If the key is FEATURE_FLAG, the expected value is as defined https://www.notion.so/sn-push-Extending-Push-Interface-Support-2dee2ff2104648dfaa6f12b1b5cd7ec7?pvs=21
If the key is AB_TEST_VARIANT_IDS, the expected value is as defined https://www.notion.so/sn-push-Extending-Push-Interface-Support-2dee2ff2104648dfaa6f12b1b5cd7ec7?pvs=21 
If the key is CHANNEL_IDENTIFIERS, the expected value is as defined https://www.notion.so/sn-push-Extending-Push-Interface-Support-2dee2ff2104648dfaa6f12b1b5cd7ec7?pvs=21 
If the key is PREFECTURE_CODES, the expected value is as defined https://www.notion.so/sn-push-Extending-Push-Interface-Support-2dee2ff2104648dfaa6f12b1b5cd7ec7?pvs=21  |

### The logical relationship between various Targeting Conditions :

[https://whimsical.com/logical-processing-UkTnn5U5txQtorzan69eG4](https://whimsical.com/logical-processing-UkTnn5U5txQtorzan69eG4)

When `TargetingConditions.Key = FEATURE_FLAG` ***(Not supported currently)***, the value will look as : 

| targetValue | List<Map<String, Object>> | Filtering condition with key and value. It’s used to check the users feature-flag is same as this config.

Note : This is treated as an “AND” operation where the users having “ALL THE GIVEN” FF identifers are targeted.

Sample:
[
    {
      "key": "pacer_mix_algo_id",
      "value": “hello_pacer_v1”
    },
    {
      "key": "ignoreRefreshTriggerOnboarding",
      "value": true
    }
]

In the above example, users with FF as pacer_mix_algo_id = hello_pacer_v1 AND ignoreRefreshTriggerOnboarding = true are selected. |
| --- | --- | --- |

When `TargetingConditions.Key = AB_TEST_VARIANT_IDS`, the value will look as : 

| targetValue | List<String> | Any AB_TEST_VARIANT_IDS which can be found out from ABTest V3 platform. 

Sample:  [”2234”, “3442”, “1343”] |
| --- | --- | --- |

When `TargetingConditions.Key = CHANNEL_IDENTIFIERS`, the value will look as : 

| targetValue | List<String> | List of Channel Identifiers which are subscribed by users. 

Note : This is treated as an “OR” operation where the users belonging to any of the channels in the list gets selected.

Sample : [”cr_ja_entertainment”, “cr_ja_premium_content”] |
| --- | --- | --- |

When `TargetingConditions.Key = PREFECTURE_CODES`, the value will look as : 

| targetValue | List<String> | List of Prefecture Code IDs which the user belong to. (Very much specific to JP Edition users only as Prefecture Concept is prevalent in Japan only)

Note : This is treated as an “OR” operation where the users belonging to any of the Prefecture codes in the list gets selected.

Sample : [”14”, “15”]

The prefecture code to prefecture name mapping can be found out from prefecture table in SmartNews DB.  |
| --- | --- | --- |

`pushCandidate`

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| linkId | String | Yes | Link ID. If not an indexed article, use "-1". |
| url | String | No | URL of the push link if an indexed article. |
| title | String | No | Title of the push. |
| label | String | No | Label of the push. Shows above the title on the screen. |
| thumbnailUrl | String | No | ThumbnailUrl of the push. Shows the thumbnail on the screen. |
| recommendType | String | No | for ranking system to pass this info for later analysis |
| metadata | Map | No | Refrain to use it because the logic would be messy while processing free formed data |

`pushStrategy` 

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| pushSemantics | String | Yes | Accepted values : 
IMMEDIATE: Push is expected to be dispatched as soon as possible as it is received on the interface. 
LATER: Push is prepared earlier and is expected to be dispatched at later point in time. |
| registrationDetails | Object | Conditional (Required if pushSemantics=LATER) | Container object containing the information about dispatch properties.
Refer More details here : dispatchDetails : Container object containing the information about dispatch properties (https://www.notion.so/dispatchDetails-Container-object-containing-the-information-about-dispatch-properties-cfe5b1996b8445bf9dc38c1892b36ffa?pvs=21)  |

`GeoQueryEnvelope` Object definition:

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| leftTopLat | double | Yes | Latitude of top left corner of the envelope |
| leftTopLon | double | Yes | Longitude of top left corner of the envelope |
| rightBottomLat | double | Yes | Latitude of bottom right corner of the envelope |
| rightBottomLon | double | Yes | Longitude of bottom right corner of the envelope |

`~~GeoQueryCircle` (Deprecated) Object definition:~~

| Field Name | Field Type | Required | Description |
| --- | --- | --- | --- |
| lat | double | Yes | Latitude of geo circle center |
| lon | double | Yes | Longitude of geo circle center |
| rad | double | Yes | Radius of geo circle |

# API Response Body

- **pushFunnelQueryId**: the id that caller can query push funnel to get the whole journey in push platform

[New Push Funnel Platform - User Manual](https://www.notion.so/New-Push-Funnel-Platform-User-Manual-3c664e2cf2ab45e6ac8932ea12fb50b3?pvs=21)

- **requestTraceId**: the id that can query the request detail exist on interface data store. `Only exist for 14 days`
- message and statusCode: provide more info if something get wrong.

```jsx
api/v1/push

{
	"pushFunnelQueryId":"weather_rain_radar:20220309044515:v01",
  "requestTraceId":"0d8bf310-79b7-4d6a-9d82-fd4146def0e7",
  "message":"accept",
  "statusCode":202
}

api/v2/push
{
  "pushSemantics": "LATER"
	"message":"accept",
  "statusCode":202
}
```

# Model definition

### Request

- [PushInterfaceRequestV2](https://github.com/smartnews/sn-push-queue/blob/master/src/main/java/com/smartnews/push/queue/pushinterface/PushInterfaceRequestV2.java) (Derived Class)
- [PushInterfaceRequest](https://github.com/smartnews/sn-push-queue/blob/master/src/main/java/com/smartnews/push/queue/pushinterface/PushInterfaceRequest.java) (Base Class)
- [PushInterfaceBaseRequest](https://github.com/smartnews/sn-push-queue/blob/master/src/main/java/com/smartnews/push/queue/pushinterface/PushInterfaceBaseRequest.java) (Super Base Class)

### Response

- [PushTaskResponse](https://github.com/smartnews/sn-push-interface/blob/master/sn-push-interface/src/main/java/com/smartnews/push/pushinterface/model/PushTaskResponse.java)

# Request Samples

<aside>
🚫 ***V1 Push*** are deprecated and only to be used for pre-existing APIs

</aside>

<aside>
✅ ***V2 Push*** is recommended to be used currently.

</aside>

### (V2 Push) UserQuery.Key = VIRTUAL_ID_LIST Example

```bash
curl -X POST -H "content-type:application/json" -d '{
    "pushType": "testType",
    "edition": "en_US",
    "expiredEpochSecond": 12345,
    "userQuery": {
        "key": "VIRTUAL_ID_LIST",
        "value": ["WEwZzvmUR-uWId7L9Dz6Hw"]
    },
    "pushCandidates": [
        {
            "linkId": "-1",
            "title": "testTitle",
            "url": "testUrl",
            "label": "testLabel"
        }
    ],
    "additionalInfo": null,
		"pushStrategy": {
        "pushSemantics": "IMMEDIATE"
    }
}' sn-push-interface.sn-push.dev.smartnews.net/api/v1/push
```

### (V1 Push) JP Rain Radar Push

```json
{
    "pushType": "weather_rain_radar",
    "edition": "ja_JP",
    "expectedTimestamp": 12345,
    "userQuery": {
        "key": "GEO_ENVELOPE",
        "value": {
					"leftTopLat": 123.00,
					"leftTopLon": 123.00,
					"rightBottomLat": 456.00,
					"rightBottomLon": 456.00
				}
    },
    "pushCandidates": [
        {
            "linkId": "-1",
            "title": "testTitle",
            "url": "testUrl",
            "label": "testLabel"
        }
    ],
    "additionalInfo": {
			"tilesRainForecast": <tile_rain_forecast_data_json>,
		}
}
```

### (V2 Push) tomorrow_weather_push **(Semantic = LATER)**

```json
{
    "pushId": 1670292411,
    "pushType": "us_daily_weather",
    "edition": "en_US",
    "userQuery": {
        "key": "VIRTUAL_ID_LIST",
        "value": [
            "9r2Pir7QgruG2ylztI7RYw"
        ]
    },
    "pushStrategy": {
        "pushSemantics": "LATER",
        "registrationDetails": {
            "dispatchTime": "2022-12-26T11:30+0900",
            "dispatchExpireTime": "2022-12-26T19:57+0900",
            "registrationElasticity": "ELASTIC",
            "registerTimeElasticMinutes": "50",
            "registerExpireTime": "2022-12-26T20:17+0900"
        }
    },
    "clientExpireTime": "2022-12-26T22:17+0900",
    "pushCandidates": [
        {
            "linkId": "-1",
            "url": "smartnews://openWeather?referrer=weather_tomorrow_push&type=fixed",
            "label": "SmartNews",
            "title": "明日の天気は⛈",
            "thumbnailUrl": "https://assets.smartnews.com/today-web/2022/01/20220101.png",
            "recommendType": ""
        }
    ],
    "customPayload": null,
    "additionalInfo": null,
    "contentType": "custom_link",
    "pushVersion": "1.0"
}
```

### (V2 Push) Tomorrow_weather_push **(Semantic = IMMEDIATE)**

```json
{
    "pushType": "438",
    "edition": "ja_JP",
    "userQuery": {
        "key": "VIRTUAL_ID_LIST",
        "value": [
            "9r2Pir7QgruG2ylztI7RYw"
        ]
    },
    "pushCandidates": [
        {
            "linkId": "-1",
            "url": "smartnews://openLink?url=https%3A%2F%2Ftoday.smartnews.com/20220101",
            "label": "SmartNews",
            "title": "TITLE",
            "thumbnailUrl": "https://assets.smartnews.com/today-web/2022/01/20220101.png"
        }
    ],
    "additionalInfo": null,
    "pushStrategy": {
        "pushSemantics": "IMMEDIATE"
    }
}
```

### (V2 Push) Push With `Specified_Targeting` **(Semantic = LATER)**

```json
{
    "pushType": "some_push_type",
    "edition": "ja_JP",
    "userQuery": {
        "key": "SPECIFIED_TARGETING",
        "value": [
        	{
            "targetType": "CHANNEL_IDENTIFIERS",
        		"targetValue": ["cr_ja_entertainment", "cr_ja_premium_content"]
        	},
        	{
        		"targetType": "AB_TEST_VARIANT_IDS",
        		"targetValue": ["1212", "1221"]
        	},
          {
                "targetType": "PREFECTURE_CODES",
                "targetValue": ["12", "13", "15"]
          }
        ]
    },
    "pushCandidates": [
        {
            "linkId": "-1",
            "url": "smartnews://openLink?url=https%3A%2F%2Ftoday.smartnews.com/20220101",
            "label": "SmartNews",
            "title": "TITLE",
            "thumbnailUrl": "https://assets.smartnews.com/today-web/2022/01/20220101.png"
        }
    ],
    "additionalInfo": null,
    "pushStrategy": {
        "pushSemantics": "LATER",
        "registrationDetails": {
            "dispatchTime": "2022-12-26T11:30+0900",
            "dispatchExpireTime": "2022-12-26T19:57+0900",
            "registrationElasticity": "ELASTIC",
            "registerTimeElasticMinutes": "50",
            "registerExpireTime": "2022-12-26T20:17+0900"
        }
    }
}
```

# Push Test

Users can try doing the PushTest on Dev envt (and Production envt) from the following link : 

[](https://push-platform-admin.smartnews.net/development/pushTest)

### For users that require passing custom payloads for push validation

Custom payload example: [https://docs.google.com/spreadsheets/d/1uSTnBAmkPtfHoTSF4w74rHTbVtUHqueIzpD91Sk2Ebw/edit#gid=0](https://docs.google.com/spreadsheets/d/1uSTnBAmkPtfHoTSF4w74rHTbVtUHqueIzpD91Sk2Ebw/edit#gid=0)

```json
{
  "pushType":"breaking_simple",
  "edition": "en_US",
  "customPayload": "[PUT CUSTOMPAYLOAD HERE]", <-- copy payload to this property
  "userQuery": {
    "key": "VIRTUAL_ID_LIST",
    "value": []
  },
  "pushCandidates": [
    {
      "linkId": "-1",
      "url": "smartnews://openLink?url=https%3A%2F%2Ftoday.smartnews.com/20220101",
      "label": "SmartNews",
      "title": "TITLE",
      "thumbnailUrl": "https://assets.smartnews.com/today-web/2022/01/20220101.png"
    }
  ],
  "additionalInfo": null,
	"pushStrategy": {
        "pushSemantics": "IMMEDIATE"
    }
}
```
