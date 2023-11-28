import json

from openai import OpenAI

import gandai as ts
from gandai import secrets

client = OpenAI(
    api_key=secrets.access_secret_version("OPENAI_KEY"),
)

## gpt4


def ask_gpt4(messages: list) -> json:
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-1106-preview",
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    #
    print(chat_completion.usage)
    return json.loads(chat_completion.choices[0].message.content)


def ask_gpt35(messages: list) -> json:
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo-1106",
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    #
    print(chat_completion.usage)
    return json.loads(chat_completion.choices[0].message.content)


HOW_TO_RESPOND = """
You will respond with an JSON object that looks like this:
{
    "events": List[Event],
}
"""

HOW_TO_GOOGLE_MAPS = """
To search the Google Maps Places API
You will respond with this
{"events": List[asdict(Event)]}

Unless otherwise directed you will return 10 centroids

There are 20 results per centroid
So if the user asks for 100 results you will return the count divided by 20

Give me the query strings you would use to search for 
Each query string should be small enough for a Google Maps search

For example to search throughout Dallas you might use:
dentists in Dallas, TX
dentists in Highland Park, TX
dentists in Grapevine, TX
dentists in Plano, TX

Now give me the queries that you would use

Here's some Event examples:
[{
    "type": "maps",
    "search_uid": 1700,
    "actor_key": "7138248581",
    "data": {
        "query": "dentists in Dallas, TX"
    }
}]

"""

HOW_TO_IMPORT = """
// example Import(Event)
{
    "search_uid": 19696114,
    "domain": null,
    "actor_key": "4805705555",
    "type": "import",
    "data": {
        "stage": "advance",
        "domains": [
            "buybits.com",
            "lidoradio.com",
            "rocklandcustomproducts.com",
            "sigmasafety.ca",
        ],
    },
}

Here are the stages along with their labels:
The only valid stages are labelMap.keys()
const labelMap = {
    "create": "Inbox",
    "advance": "Review",
    "validate": "Validated",
    "send": "Client Inbox",
    "client_approve": "Client Approved",
    "sync": "Synced",
    "reject": "Reject",
    "conflict": "Conflict",
    "client_conflict": "Client Conflict",
    "client_reject": "Client Reject"
}
"""

HOW_TO_TRANSITION = """
To move a target to a different stage you will create an event with the targets domain and the stage you want to move it to.

domain should include domain only, no subdomain or protocol

// example Event
{
    "search_uid": 19696114,
    "domain": "acme.com",
    "actor_key": "5558248581",
    "type": "send",
    "data": {"key": "value"},
}


Here are the stages along with their labels:
The only valid event types are the labelMap.keys()
const labelMap = {
    "create": "Inbox",
    "advance": "Review",
    "validate": "Validated",
    "send": "Client Inbox",
    "client_approve": "Client Approved",
    "sync": "Synced",
    "reject": "Reject",
    "conflict": "Conflict",
    "client_conflict": "Client Conflict",
    "client_reject": "Client Reject"
}
"""

HOW_TO_GOOGLE = """

To search Google, you will create an Event object.

@dataclass
class Google(Event):
    search_uid: int  # fk # add index
    actor_key: str  # fk
    type: str  
    data: dict = field(default_factory=dict)
    id: int = field(default=None)  # pk
    # created: int = field(init=False)

List[Event] examples asdict:

[{
  'search_uid': 200,
  'domain': null,
  'actor_key': '3125740050',
  'type': 'google',
  'data': {'q': '"golf cart" AND audio'},
  'created': 1697813193},
{
  'search_uid': 5255570,
  'domain': null,
  'actor_key': '3102835279',
  'type': 'google',
  'data': {'q': '"commercial" AND "door" AND ("repair" OR "maintenance" OR "replacement") AND "new York City"'},
  'created': 1697814555}]

The type is 'google'
You will not set the id or created fields.
The default count is 10

"""

HOW_TO_REVIEW = """


To respond to a prompt directing Review a company, create an Event
Here we will iterate through a list of domains as prompted by the user 

You will respond with a JSON object, 

{"events": List[asdict(Event)]}

@dataclass
class Event:
    search_uid: int  
    actor_key: str # your actor_key is "gpt"
    type: str  # enum
    domain: Optional[str] = None  # fk
    data: dict = field(default_factory=dict)

@dataclass
class Review(ts.models.Event):
    type: str = "review"

    def __post_init__(self):
        assert len(self.data.keys()) > 0, "data must have at least one key"

You will review the company for acquisition.
You will help us prepare the data for the Client to review

You will read the company's website text, which you will consider the most up to date information.
You will review company data from Grata

You will include the orginal prompt in the data field

Example Event:

{
    "actor_key": "gpt",
    "type": "review",
    "domain": "acme.com",
    "data": {
        "prompt": THE USER PROMPT YOU ARE RESPONDING TO
    }
}


"""