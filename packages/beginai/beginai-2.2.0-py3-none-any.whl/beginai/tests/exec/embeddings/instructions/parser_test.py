from beginai.exec.embeddings.instructions.parser import Parser
from freezegun import freeze_time
import json


@freeze_time("2021-05-16")
def test_parse_instructions():
    instructions = json.loads("""
    {
  "instructions": {
    "objects": {
      "user": [
        {
          "_chains": [
            [
              {
                "complexity": 1,
                "instruct": "Age",
                "order": 1,
                "params": {}
              },
              {
                "complexity": 1,
                "instruct": "Slice",
                "order": 2,
                "params": {
                  "maxv": 100,
                  "minv": 10,
                  "num_slices": 10,
                  "skip_masking": false
                }
              }
            ]
          ],
          "f_id": "userBirthDate"
        },
        {
          "complexity": 1,
          "f_id": "userBirthDate",
          "instruct": "Age",
          "params": {}
        }
      ]
    }
  },
  "interactions": {},
  "labels": {},
  "tokenize": {},
  "embedding_template": {
    "objects": {
      "user": [
        "userBirthDate",
        "chain_instruction__Age__user__userBirthDate",
        "chain_instruction__Slice__user__userBirthDate"
      ]
    },
    "interactions": {}
  }
}
    """)

    values = {
        "userbirthdate": "16-05-1991"
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [30.0, 3.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_without_matching_id():
    instructions = json.loads("""
        {
            "instructions": {
                "objects": {
                    "user": [
                        {
                            "complexity": 1,
                            "f_id": "userBirthDate",
                            "instruct": "Age",
                            "params": {}
                        }
                    ]
                },
                "interactions": {}
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "objects": {
                    "user": ["userBirthDate"]
                }
            }
        }
    """)

    values = {
        "user": {
            "10": [
                {"userBio": "bio bio"}
            ]
        }
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [0.00011],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_without_object_being_on_instructions():
    instructions = json.loads("""
        {
            "instructions":{
                "objects": {
                    "user":[
                        {
                            "complexity":1,
                            "f_id":"userBirthDate",
                            "instruct":"Age",
                            "params":{
                            }
                        }
                    ]
                }
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "user": [ "userBirthDate" ]
            }
        }
    """)

    values = {
        "doesntexist": {
            "10": [
                {"bio bio"}
            ]
        }
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("doesntexistobject")
    expected = {}
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


@freeze_time("2021-05-16")
def test_parse_instructions_with_different_camel_case_than_provided():
    instructions = json.loads("""
        {
            "instructions": {
                "objects": {
                    "user": [
                        {
                        "complexity": 1,
                        "f_id": "USERBIRTHDATE",
                        "instruct": "Age",
                        "params": {}
                        }
                    ]
                }
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "objects": {
                "user": ["USERBIRTHDATE"]
                }
            }
        }
    """)

    values = {
        "userbirthdate": "16-05-1991"
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [30.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)

@freeze_time("2021-05-16")
def test_parse_instructions_with_interactions_only():
    instructions = json.loads("""
    {
        "instructions":{
            "interactions":{
                "home":{
                    "actions":[ "test"],
                    "instructions":{ }
                },
                "product":{
                    "actions":[ "react", "dosomething" ],
                    "instructions":{
                    "react":[
                        {
                            "instruct":"Length",
                            "complexity":1,
                            "params":{},
                            "f_id":"comment"
                        },
                        {
                            "instruct":"Age",
                            "complexity":1,
                            "params":{},
                            "f_id":"date"
                        }
                    ]
                    }
                }
            }
        },
        "labels":{},
        "tokenize":{},
        "embedding_template":{
            "objects":{},
            "interactions":{
                "product":{
                    "react":[ "date", "comment"]
                }
            }
        }
    }
    """)

    values = {
        "home": {
            "100": [{
                "action": "test",
                "properties": {},
                "created_at": 123423
            }]
        },
        "product": {
            "10": [{
                "action": "react",
                "properties": {
                    "comment": "This is a comment!"
                },
                "created_at": None
            }, {
                "action": "dosomething",
                "properties": {},
                "created_at": 1234
            }],
            "20": [{
                "action": "react",
                "properties": {
                    "comment": "This is a comment!",
                    "date": "16-05-1991"
                },
                "created_at": None
            }]
        }
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("interactions")
    expected = {
        "interactions": {
            "home": {
                "100": {
                    "test": [{
                        "embedding": None,
                        "created_at": 123423
                    }]
                }
            },
            "product": {
                "10": {
                    "react": [{
                        "embedding": [0.00011, 18.0],
                        "created_at": None
                    }],
                    "dosomething": [{
                        "embedding": None,
                        "created_at": 1234
                    }]
                },
                "20": {
                    "react": [{
                        "embedding": [30.0, 18.0],
                        "created_at": None
                    }]
                }
            }
        }
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


@freeze_time("2021-05-16")
def test_parse_instructions_with_interaction_that_doesnt_exist():
    instructions = json.loads("""
{
   "instructions":{
      "interactions":{
         "product":{
            "actions":[
               "like"
            ],
            "instructions":{
               "like":[
                  {
                     "complexity":1,
                     "instruct":"Age",
                     "params":{
                        
                     },
                     "f_id":"when"
                  }
               ]
            }
         }
      }
   },
   "labels":{},
   "tokenize":{},
   "embedding_template":{
      "interactions":{
         "product":{
            "like":[
               "when"
            ]
         }
      }
   }
}
    """)

    values = {
        "product": {
            "10": [{
                "action": "like",
                "properties": {
                    "when": "01-01-2019"
                },
                "created_at": None
            }]
        },
        "differentobjectthatdoesntexist": {
            "10": [{
                "action": "like",
                "properties": {
                    "when": "01-01-2014"
                },
                "created_at": None
            }], 
            "20": [{
                "action": "like",
                "properties": {
                    "when": "03-04-2014"
                },
                "created_at": None
            }]
        }
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("interactions")
    expected = {
        "interactions": {
            "product": {
                "10": {
                    "like": [{
                        "embedding": [2.0],
                        "created_at": None
                    }]
                }
            }
        }
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_labels_that_exists():
    instructions = json.loads("""
    {
        "instructions":{
            "objects": {
                "user":{}
            }
        },
        "labels":{
            "user":[ "fake", "not_fake", "something" ],
            "product":[ "fruit", "shirt"
            ],
            "message":["something" ]
        },
        "tokenize":{}
    } """)

    values = {
        "user": {
            "labels": ["fake", "not_fake"]
        }
    }

    parser = Parser(instructions)
    parser.feed(values.get("user"))
    results = parser.parse("user")
    expected = {
        "embedding": [],
        "labels": ["fake", "not_fake"],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0}
    }
    assert results["labels"].sort() == expected["labels"].sort()


def test_parse_labels_that_dont_exist():
    instructions = json.loads("""{
        "instructions":{
            "objects": {
                "product": {}
            }
        },
        "labels":{
            "product":[ "fruit", "shirt" ]
        },
        "tokenize":{}
    }""")

    values = {
        "product": {
            "labels": ["fake", "fruit"]
        }
    }

    parser = Parser(instructions)
    parser.feed(values.get("product"))
    results = parser.parse("product")
    expected = {
        "embedding": [],
        "labels": ["fruit"],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_boolean_values():
    instructions = json.loads(""" {
        "instructions":{
            "objects": {
                "home":[
                    {
                        "instruct":"Boolean",
                        "complexity":1,
                        "params":{
                            "true":2,
                            "false":1,
                            "_GB_EMPTY": 0.00011
                        },
                        "f_id":"has_hottub"
                    },
                    {
                        "instruct":"Boolean",
                        "complexity":1,
                        "params":{
                            "true":2,
                            "false":1,
                            "_GB_EMPTY": 0.00011
                        },
                        "f_id":"has_true"
                    }
                ]
            }
        },
        "labels": {},
        "tokenize":{},
        "embedding_template": {
            "objects": {
                "home": [
                    "has_hottub",
                    "has_true"
                ]
            }
        }
    } """)

    values = {
        "has_hottub": 0,
        "has_true": 1
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("home")
    expected = {
        "embedding": [1.0, 2.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_tokenizer():
    instructions = json.loads(""" {
        "instructions":{
            "objects": {
                "user": []
            },
            "interactions":[]
        },
        "labels": {},
        "tokenize":{
            "user":[ "name", "lastName"]
        }
    } """)

    values = {
        "name": "Jane",
        "lastName": "Doe"
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [101, 4869, 3527, 2063, 102, 0, 0], "attention_mask": [1, 1, 1, 1, 1, 0, 0], "len_": 5},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_tokenizer_when_property_is_not_provided():
    instructions = json.loads(""" {
        "instructions":{
            "objects": {
                "user":[],
                "interactions":[]
            }
        },
        "tokenize":{
            "user":[ "name", "lastName" ]
        },
        "labels": {},
        "identifiers": {}
    } """)

    values = {
        "name": "Jane"
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [101, 4869, 102, 0], "attention_mask": [1, 1, 1, 0], "len_": 3},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_identifier_when_property_is_not_provided():
    instructions = json.loads(""" {
        "instructions":{
            "objects": {
                "user":[],
                "interactions":[]
            }
        },
        "identifiers":{
            "user":[ "user_id", "user_id_2" ]
        },
        "labels": {}
    } """)

    values = {
        "name": "Jane"
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {
            "user_id": "",
            "user_id_2": ""
        },
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_identifier():
    instructions = json.loads(""" {
        "instructions":{
            "objects": {
                "user":[],
                "interactions":[]
            }
        },
        "identifiers":{
            "user":[ "user_id", "user_id_2" ]
        },
        "labels": {}
    } """)

    values = {
        "name": "Jane",
        "user_id": 1,
        "identifiers": {
            "user_id": "",
            "user_id_2": ""
        }
    }

    parser = Parser(instructions)
    parser.feed(values)
    results = parser.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {
            "user_id": 1,
            "user_id_2": ""
        },
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)
