from beginai.exec.embeddings.worker import BeginWorker
from beginai.exec.embeddings.apply import AlgorithmsApplier
from beginai.orchapi.api import OrchAPI


class BeginWorkerMock(BeginWorker):

    def __init__(self, app_id, license_key):
        super().__init__(app_id, license_key)
        self.orchapi = _FakeOrchAPI()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_embeddings(self):
        return self.orchapi.embeddings


class BeginAlgorithmsApplierMock(AlgorithmsApplier):

    def __init__(self, app_id, license_key, use_hero_schema=False, use_session_data=False):
        super().__init__(app_id, license_key)
        self.orchapi = _FakeOrchForCSVAPI(use_hero_schema, use_session_data)

    def get_data(self):
        return self.data

    def get_embeddings(self):
        return self.orchapi.embeddings

    def get_intervention_data(self):
        return self.orchapi.intervention_data

class _FakeOrchAPI(OrchAPI):

    def fetch_instructions(self):
        instructions_id = 1
        version_number = 0

        instructions_list = {
            "instructions": {
                "objects": {
                    "user": [
                        {
                            "instruct": "Age",
                            "complexity": 1,
                            "params": {},
                            "f_id": "dateOfBirth",
                        },
                        {
                            "_chains": [
                                [
                                    {
                                        "instruct": "Age",
                                        "complexity": 1,
                                        "params": {

                                        },
                                        "order": 1
                                    },
                                    {
                                        "instruct": "Slice",
                                        "complexity": 1,
                                        "params": {
                                            "minv": 10,
                                            "maxv": 100,
                                            "num_slices": 10,
                                            "skip_masking": False
                                        },
                                        "order": 2
                                    }
                                ]
                            ],
                            "f_id": "dateOfBirth",
                        },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": False
                            },
                            "f_id": "numberField",
                        },
                        {
                            "instruct": "Length",
                            "complexity": 1,
                            "params": {

                            },
                            "f_id": "textField",
                        }
                    ],
                    "product": [{
                        "instruct": "Length",
                        "complexity": 1,
                        "params": {

                        },
                        "f_id": "description",
                    },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": False
                            },
                            "f_id": "randomNumber",
                    },
                        {
                            "instruct": "Age",
                            "complexity": 1,
                            "params": {

                            },
                            "f_id": "publishedDate",
                    },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": True
                            },
                            "f_id": "randomnumberskippingmask",
                    }
                    ],
                    "session": []
                },
                "interactions": {
                    "noembedding": {
                        "actions": ["just_action"],
                        "instructions": {}
                    },
                    "user": {
                        "actions": ["followed", "report", "dosomething"],
                        "instructions": {
                            "followed": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "report": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ]
                        }
                    },
                    "product": {
                        "actions": ["like", "dislike", "comment"],
                        "instructions": {
                            "like": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "dislike": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "comment": [
                                {
                                    "instruct": "Length",
                                    "complexity": 1,
                                    "params": {},
                                    "f_id": "commentLength",
                                },
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ]
                        }},
                    "session": {
                        "actions": ["plays"],
                        "instructions": {
                            "plays": [
                                {
                                    "instruct": "Slice",
                                    "complexity": 1,
                                    "params": {
                                        "minv": 0,
                                        "maxv": 0,
                                        "num_slices": 0,
                                        "skip_masking": True
                                    },
                                    "f_id": "duration",
                                    "higher_order": 1
                                }
                            ]
                        }
                    }
                },
            },
            "tokenize": {
                "user": [
                    "name",
                    "lastName"
                ],
                "product": [
                    "gender",
                    "name"
                ]
            },
            "labels": {
                "user": ["fake", "not_fake"],
                "product": ["fiction", "comedy", "mystery"]
            },
            "identifiers": {
                "user": ["user_specific_id", "another_user_specific_id"],
                "product": ['product_specific_id']
            },
            "embedding_template": {
                "objects": {
                    "user": ["dateOfBirth", "chain_instruction__Age__user__dateOfBirth", "chain_instruction__Slice__user__dateOfBirth", "numberField", "textField"],
                    "product": ["description", "randomNumber", "publishedDate", "randomnumberskippingmask"]
                },
                "interactions": {
                    "user": {
                        "followed": ["date"],
                        "report": ["date"]
                    },
                    "session": {
                        "plays": ["duration"]
                    },
                    "product": {
                        "like": ["date"],
                        "dislike": ["date"],
                        "comment": ["date", "commentLength"]
                    }
                }
            }
        }
        return instructions_id, version_number, instructions_list

    def submit_embeddings(self, embeddings, instruction_id, version_number):
        self.embeddings = embeddings


class _FakeOrchForCSVAPI(OrchAPI):

    def __init__(self, use_hero_schema=False, use_session_data=False):
        self.use_hero_schema = use_hero_schema
        self.use_session_data = use_session_data
        self.embeddings = []
        self.intervention_data = []

    def fetch_instructions(self):
        instructions_id = 1
        version_number = 0

        if self.use_hero_schema:
            instructions_list = {
                "instructions": {
                    "objects": {
                        "user": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {},
                                    "f_id": "age",
                                    "higher_order": 1
                                },
                            {
                                    "instruct": "Sequence",
                                    "complexity": 1,
                                    "params": {
                                        "sequence_map": {
                                            "brazil": "1",
                                            "canada": "2",
                                            "usa": "3",
                                            "_GB_EMPTY": 4
                                        }
                                    },
                                    "f_id": "country",
                                    "higher_order": 2
                                }
                        ],
                        "hero": [
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                            "small": "1",
                                            "big": "2",
                                            "medium": "3",
                                            "tiny": "4",
                                            "_GB_EMPTY": 5
                                    }
                                },
                                "f_id": "size",
                                "higher_order": 1
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 0,
                                    "num_slices": 0,
                                    "skip_masking": True
                                },
                                "f_id": "random_number",
                                "higher_order": 2
                            }
                        ],
                        "mission": [
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 0,
                                    "num_slices": 0,
                                    "skip_masking": True
                                },
                                "f_id": "coins_earned",
                                "higher_order": 1
                            }
                        ]
                    },
                    "interactions": {
                        "hero": {
                            "actions": [
                                "has", "played"
                            ],
                            "instructions": {
                                "has": [
                                    {
                                        "instruct": "Age",
                                        "complexity": 1,
                                        "params": {},
                                        "f_id": "acquired_date",
                                        "higher_order": 1
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "is_winner",
                                        "higher_order": 2
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "competed_before",
                                        "higher_order": 3
                                    },
                                    {
                                        "instruct": "Sequence",
                                        "complexity": 1,
                                        "params": {
                                            "sequence_map": {
                                                    "test123": "1",
                                                    "big": "2",
                                                    "something": "3",
                                                    "_GB_EMPTY": 4
                                            }
                                        },
                                        "f_id": "type",
                                        "higher_order": 4
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "is_new",
                                        "higher_order": 5
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "another",
                                        "higher_order": 6
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "bla",
                                        "higher_order": 7
                                    },
                                    {
                                        "instruct": "Boolean",
                                        "complexity": 1,
                                        "params": {
                                            "true": 2,
                                            "false": 1,
                                            "_GB_EMPTY": 0.00011
                                        },
                                        "f_id": "asd",
                                        "higher_order": 8
                                    }
                                ],
                                "played": []
                            }
                        },
                        "mission": {
                            "actions": [
                                "played"
                            ],
                            "instructions": {
                                "played": []
                            }
                        }
                    }
                },
                "labels": {},
                "tokenize": {},
                "identifiers": {},
                "embedding_template": {
                    "objects": {
                        "user": [
                            "age",
                            "country"
                        ],
                        "hero": [
                            "size",
                            "random_number"
                        ],
                        "mission": [
                            "coins_earned"
                        ]
                    },
                    "interactions": {
                        "hero": {
                            "has": [
                                "acquired_date",
                                "is_winner",
                                "competed_before",
                                "type",
                                "is_new",
                                "another",
                                "bla",
                                "asd"
                            ],
                            "played": []
                        }
                    }
                }
            }
        elif self.use_session_data:
            instructions_list = {"instructions": {
                "objects": {
                    "user": [],
                    "session": []
                },
                "interactions": {
                    "session": {
                        "actions": [
                            "plays"
                        ],
                        "instructions": {
                            "plays": [
                                {
                                    "instruct": "Slice",
                                    "complexity": 1,
                                    "params": {
                                        "minv": 0,
                                        "maxv": 0,
                                        "num_slices": 0,
                                        "skip_masking": True
                                    },
                                    "f_id": "duration",
                                    "higher_order": 1
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "ds",
                                    "higher_order": 2
                                }
                            ]
                        }
                    },
                    "hero": {
                        "actions": [
                            "has", "played"
                        ],
                        "instructions": {
                            "has": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {},
                                    "f_id": "acquired_date",
                                    "higher_order": 1
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "is_winner",
                                    "higher_order": 2
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "competed_before",
                                    "higher_order": 3
                                },
                                {
                                    "instruct": "Sequence",
                                    "complexity": 1,
                                    "params": {
                                        "sequence_map": {
                                                "test123": "1",
                                                "big": "2",
                                                "something": "3",
                                            "_GB_EMPTY": 4
                                        }
                                    },
                                    "f_id": "type",
                                    "higher_order": 4
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "is_new",
                                    "higher_order": 5
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "another",
                                    "higher_order": 6
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "bla",
                                    "higher_order": 7
                                },
                                {
                                    "instruct": "Boolean",
                                    "complexity": 1,
                                    "params": {
                                        "true": 2,
                                        "false": 1,
                                        "_GB_EMPTY": 0.00011
                                    },
                                    "f_id": "asd",
                                    "higher_order": 8
                                }
                            ],
                            "played": []
                        }
                    }
                }
            },
                "labels": {},
                "tokenize": {},
                "identifiers": {},
                "embedding_template": {
                "objects": {},
                "interactions": {
                    "session": {
                        "plays": [
                            "duration",
                            "ds"
                        ]
                    },
                    "hero": {
                        "has": [
                            "acquired_date",
                            "is_winner",
                            "competed_before",
                            "type",
                            "is_new",
                            "another",
                            "bla",
                            "asd"
                        ],
                        "played": []
                    }
                }
            }}
        else:
            instructions_list = {
                "instructions": {
                    "objects": {
                        "user": [],
                        "book": [
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 100000,
                                    "num_slices": 241,
                                    "skip_masking": False
                                },
                                "f_id": "text_reviews_count",
                                "higher_order": 1
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "true": "1",
                                        "False": "2",
                                        "_GB_EMPTY": 3
                                    }
                                },
                                "f_id": "is_ebook",
                                "higher_order": 2
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 5,
                                    "num_slices": 33,
                                    "skip_masking": False
                                },
                                "f_id": "average_rating",
                                "higher_order": 3
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 10,
                                    "maxv": 1500,
                                    "num_slices": 153,
                                    "skip_masking": False
                                },
                                "f_id": "num_pages",
                                "higher_order": 4
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "1": "1",
                                        "2": "2",
                                        "3": "3",
                                        "4": "4",
                                        "5": "5",
                                        "6": "6",
                                        "7": "7",
                                        "8": "8",
                                        "9": "9",
                                        "10": "10",
                                        "11": "11",
                                        "12": "12",
                                        "_GB_EMPTY": 13
                                    }
                                },
                                "f_id": "publication_month",
                                "higher_order": 5
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "1376": "114",
                                        "1378": "109",
                                        "1806": "103",
                                        "1897": "112",
                                        "1900": "93",
                                        "1901": "98",
                                        "1902": "90",
                                        "1904": "78",
                                        "1906": "101",
                                        "1908": "100",
                                        "1909": "107",
                                        "1910": "88",
                                        "1911": "77",
                                        "1914": "85",
                                        "1917": "97",
                                        "1919": "110",
                                        "1920": "45",
                                        "1921": "92",
                                        "1922": "111",
                                        "1923": "71",
                                        "1924": "91",
                                        "1925": "66",
                                        "1926": "74",
                                        "1927": "83",
                                        "1928": "81",
                                        "1929": "82",
                                        "1930": "64",
                                        "1931": "84",
                                        "1932": "80",
                                        "1933": "89",
                                        "1934": "87",
                                        "1935": "102",
                                        "1936": "63",
                                        "1937": "60",
                                        "1938": "75",
                                        "1939": "73",
                                        "1940": "59",
                                        "1941": "38",
                                        "1942": "50",
                                        "1943": "68",
                                        "1944": "96",
                                        "1945": "70",
                                        "1946": "62",
                                        "1947": "69",
                                        "1948": "67",
                                        "1949": "79",
                                        "1950": "55",
                                        "1951": "49",
                                        "1952": "23",
                                        "1953": "48",
                                        "1954": "54",
                                        "1955": "61",
                                        "1956": "46",
                                        "1957": "58",
                                        "1958": "31",
                                        "1959": "47",
                                        "1960": "43",
                                        "1961": "30",
                                        "1962": "40",
                                        "1963": "51",
                                        "1964": "52",
                                        "1965": "37",
                                        "1966": "44",
                                        "1967": "56",
                                        "1968": "29",
                                        "1969": "53",
                                        "1970": "39",
                                        "1971": "34",
                                        "1972": "42",
                                        "1973": "41",
                                        "1974": "32",
                                        "1975": "36",
                                        "1976": "33",
                                        "1977": "35",
                                        "1978": "21",
                                        "1979": "15",
                                        "1980": "22",
                                        "1981": "26",
                                        "1982": "17",
                                        "1983": "14",
                                        "1984": "28",
                                        "1985": "18",
                                        "1986": "20",
                                        "1987": "24",
                                        "1988": "8",
                                        "1989": "27",
                                        "1990": "25",
                                        "1991": "3",
                                        "1992": "19",
                                        "1993": "6",
                                        "1994": "11",
                                        "1995": "16",
                                        "1996": "7",
                                        "1997": "13",
                                        "1998": "10",
                                        "1999": "4",
                                        "2000": "5",
                                        "2001": "2",
                                        "2002": "1",
                                        "2003": "12",
                                        "2004": "9",
                                        "2005": "57",
                                        "2006": "106",
                                        "2008": "108",
                                        "2010": "99",
                                        "2011": "65",
                                        "2012": "105",
                                        "2020": "72",
                                        "2021": "104",
                                        "2024": "113",
                                        "2026": "95",
                                        "2030": "76",
                                        "2037": "115",
                                        "2038": "94",
                                        "2050": "86",
                                        "_GB_EMPTY": 116
                                    }
                                },
                                "f_id": "publication_year",
                                "higher_order": 6
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 10,
                                    "maxv": 600,
                                    "num_slices": 134,
                                    "skip_masking": False
                                },
                                "f_id": "ratings_count",
                                "higher_order": 7
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 5,
                                    "num_slices": 33,
                                    "skip_masking": False
                                },
                                "f_id": "avg_author_rating",
                                "higher_order": 8
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 99990,
                                    "num_slices": 241,
                                    "skip_masking": False
                                },
                                "f_id": "avg_author_reviews_count",
                                "higher_order": 9
                            },
                            {
                                "instruct": "Slice",
                                "complexity": 1,
                                "params": {
                                    "minv": 0,
                                    "maxv": 50,
                                    "num_slices": 82,
                                    "skip_masking": False
                                },
                                "f_id": "sum_all_author_ratings",
                                "higher_order": 10
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "children": "1",
                                        "comics_graphic": "2",
                                        "fantasy_paranormal": "3",
                                        "fiction": "4",
                                        "history_historicalfiction_biography": "5",
                                        "mystery_thriller_crime": "6",
                                        "non-fiction": "7",
                                        "poetry": "8",
                                        "romance": "9",
                                        "young-adult": "10",
                                        "_GB_EMPTY": 11
                                    }
                                },
                                "f_id": "genre_1",
                                "higher_order": 11
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "children": "1",
                                        "comics_graphic": "2",
                                        "fantasy_paranormal": "3",
                                        "fiction": "4",
                                        "history_historicalfiction_biography": "5",
                                        "mystery_thriller_crime": "6",
                                        "non-fiction": "7",
                                        "poetry": "8",
                                        "romance": "9",
                                        "young-adult": "10",
                                        "_GB_EMPTY": 11
                                    }
                                },
                                "f_id": "genre_2",
                                "higher_order": 12
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "children": "1",
                                        "comics_graphic": "2",
                                        "fantasy_paranormal": "3",
                                        "fiction": "4",
                                        "history_historicalfiction_biography": "5",
                                        "mystery_thriller_crime": "6",
                                        "non-fiction": "7",
                                        "poetry": "8",
                                        "romance": "9",
                                        "young-adult": "10",
                                        "_GB_EMPTY": 11
                                    }
                                },
                                "f_id": "genre_3",
                                "higher_order": 13
                            },
                            {
                                "instruct": "Sequence",
                                "complexity": 1,
                                "params": {
                                    "sequence_map": {
                                        "children": "1",
                                        "comics_graphic": "2",
                                        "fantasy_paranormal": "3",
                                        "fiction": "4",
                                        "history_historicalfiction_biography": "5",
                                        "mystery_thriller_crime": "6",
                                        "non-fiction": "7",
                                        "poetry": "8",
                                        "romance": "9",
                                        "young-adult": "10",
                                        "_GB_EMPTY": 11
                                    }
                                },
                                "f_id": "genre_4",
                                "higher_order": 14
                            }
                        ]
                    },
                    "interactions": {
                        "book": {
                            "actions": [
                                "rated_1",
                                "rated_2",
                                "rated_3",
                                "rated_4",
                                "rated_5"
                            ],
                            "instructions": {
                                "rated_1": [],
                                "rated_2": [],
                                "rated_3": [],
                                "rated_4": [],
                                "rated_5": []
                            }
                        }
                    }
                },
                "labels": {},
                "tokenize": {},
                "identifiers": {},
                "embedding_template": {
                    "objects": {
                        "book": [
                            "text_reviews_count",
                            "is_ebook",
                            "average_rating",
                            "num_pages",
                            "publication_month",
                            "publication_year",
                            "ratings_count",
                            "avg_author_rating",
                            "avg_author_reviews_count",
                            "sum_all_author_ratings",
                            "genre_1",
                            "genre_2",
                            "genre_3",
                            "genre_4"
                        ]
                    }
                }
            }

        return instructions_id, version_number, instructions_list

    def submit_embeddings_batch(self, embeddings, instr_id, version_number, type, target_object, update=False):
        self.embeddings += embeddings

    def submit_intervention_dates_batch(self, data):
        self.intervention_data = data

    def get_intervention_data(self):
        return self.intervention_data