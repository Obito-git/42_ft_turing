import json
import string

N = 4
LOW = list(string.ascii_lowercase[:N])
UPP = list(string.ascii_uppercase[:N])
PAIRS = [X + x for X in UPP for x in LOW]
TRIPLETS = [p + d for d in "LR" for p in PAIRS]

json.dump(
    {
        "name": "universal_turing_machine",
        "alphabet": [" ", "[", "]", ";", ".", "!", "+", "-"] + UPP + LOW,
        "blank": " ",
        "states": [
            "start",
            *[f"state_{s}" for s in UPP],
            *[f"read_{s}" for s in UPP],
            *[f"state_{s}" for s in PAIRS],
            *[f"check_state_{s}" for s in PAIRS],
            *[f"check_char_{s}" for s in PAIRS],
            *[f"skip_semicolon_{s}" for s in PAIRS],
            "get_new_state",
            "last_write",
            *[f"last_write_{s}" for s in LOW],
            *[f"finish_{s}" for s in LOW],
            *[f"get_new_char_{s}" for s in UPP],
            *[f"get_new_dir_{s}" for s in PAIRS],
            *[f"apply_{s}" for s in TRIPLETS],
            *[f"write_{s}" for s in TRIPLETS],
            *[f"move_left_{s}" for s in UPP],
            *[f"move_left_{s}" for s in PAIRS],
            *[f"move_right_{s}" for s in PAIRS],
            "HALT",
            "UNEXPECTED_TRANSITION",
            "TODO_NEG_POS",
        ],
        "initial": "start",
        "finals": ["HALT", "UNEXPECTED_TRANSITION", "TODO_NEG_POS"],
        "transitions": {
            "start": [
                {"read": s, "to_state": f"state_{s}", "write": s, "action": "RIGHT"}
                for s in UPP
            ],
            **{
                f"state_{s1}": [
                    *[
                        {
                            "read": s2,
                            "to_state": f"state_{s1}",
                            "write": s2,
                            "action": "RIGHT",
                        }
                        for s2 in UPP + LOW
                    ],
                    {
                        "read": ".",
                        "to_state": f"state_{s1}",
                        "write": ".",
                        "action": "RIGHT",
                    },
                    {
                        "read": "-",
                        "to_state": f"state_{s1}",
                        "write": "-",
                        "action": "RIGHT",
                    },
                    {
                        "read": "+",
                        "to_state": f"state_{s1}",
                        "write": "+",
                        "action": "RIGHT",
                    },
                    {
                        "read": ";",
                        "to_state": f"state_{s1}",
                        "write": ";",
                        "action": "RIGHT",
                    },
                    {
                        "read": "[",
                        "to_state": f"state_{s1}",
                        "write": "[",
                        "action": "RIGHT",
                    },
                    {
                        "read": "]",
                        "to_state": f"state_{s1}",
                        "write": "]",
                        "action": "RIGHT",
                    },
                    {
                        "read": "!",
                        "to_state": f"read_{s1}",
                        "write": "!",
                        "action": "RIGHT",
                    },
                ]
                for s1 in UPP
            },
            **{
                f"read_{s1}": [
                    {
                        "read": " ",
                        "to_state": f"state_{s1}a",
                        "write": "a",
                        "action": "LEFT",
                    },
                    *[
                        {
                            "read": s2,
                            "to_state": f"state_{s1}{s2}",
                            "write": s2,
                            "action": "LEFT",
                        }
                        for s2 in LOW
                    ],
                ]
                for s1 in UPP
            },
            **{
                f"state_{s1}": [
                    *[
                        {
                            "read": s2,
                            "to_state": f"state_{s1}",
                            "write": s2,
                            "action": "LEFT",
                        }
                        for s2 in UPP + LOW + list(".-+]!")
                    ],
                    {
                        "read": ";",
                        "to_state": f"check_state_{s1}",
                        "write": ";",
                        "action": "RIGHT",
                    },
                    {
                        "read": "[",
                        "to_state": "UNEXPECTED_TRANSITION",
                        "write": "[",
                        "action": "LEFT",
                    },
                ]
                for s1 in PAIRS
            },
            **{
                f"check_state_{s1}": [
                    {
                        "read": s2,
                        "to_state": f"check_char_{s1}",
                        "write": s2,
                        "action": "RIGHT",
                    }
                    if s2 == s1[0]
                    else {
                        "read": s2,
                        "to_state": f"skip_semicolon_{s1}",
                        "write": s2,
                        "action": "LEFT",
                    }
                    for s2 in UPP
                ]
                for s1 in PAIRS
            },
            **{
                f"check_char_{s1}": [
                    {
                        "read": s2,
                        "to_state": "get_new_state",
                        "write": s2,
                        "action": "RIGHT",
                    }
                    if s2 == s1[1]
                    else {
                        "read": s2,
                        "to_state": f"skip_semicolon_{s1}",
                        "write": s2,
                        "action": "LEFT",
                    }
                    for s2 in LOW
                ]
                for s1 in PAIRS
            },
            **{
                f"skip_semicolon_{s1}": [
                    *[
                        {
                            "read": s2,
                            "to_state": f"skip_semicolon_{s1}",
                            "write": s2,
                            "action": "LEFT",
                        }
                        for s2 in UPP
                    ],
                    {
                        "read": ";",
                        "to_state": f"state_{s1}",
                        "write": ";",
                        "action": "LEFT",
                    },
                ]
                for s1 in PAIRS
            },
            "get_new_state": [
                *[
                    {
                        "read": s,
                        "to_state": f"get_new_char_{s}",
                        "write": s,
                        "action": "RIGHT",
                    }
                    for s in UPP
                ],
                {
                    "read": ".",
                    "to_state": "last_write",
                    "write": ".",
                    "action": "RIGHT",
                },
            ],
            "last_write": [
                {
                    "read": s,
                    "to_state": f"last_write_{s}",
                    "write": s,
                    "action": "RIGHT",
                }
                for s in LOW
            ],
            **{
                f"last_write_{s1}": [
                    *[
                        {
                            "read": s2,
                            "to_state": f"last_write_{s1}",
                            "write": s2,
                            "action": "RIGHT",
                        }
                        for s2 in list(";]") + UPP + LOW + list(".-+")
                    ],
                    {
                        "read": "!",
                        "to_state": f"finish_{s1}",
                        "write": "!",
                        "action": "RIGHT",
                    },
                ]
                for s1 in LOW
            },
            **{
                f"finish_{s1}": [
                    {"read": s2, "to_state": "HALT", "write": s1, "action": "RIGHT"}
                    for s2 in [" "] + LOW
                ]
                for s1 in LOW
            },
            **{
                f"get_new_char_{s1}": [
                    {
                        "read": s2,
                        "to_state": f"get_new_dir_{s1}{s2}",
                        "write": s2,
                        "action": "RIGHT",
                    }
                    for s2 in LOW
                ]
                for s1 in UPP
            },
            "get_new_char_B": [
                {
                    "read": "a",
                    "to_state": "get_new_dir_Ba",
                    "write": "a",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "get_new_dir_Bb",
                    "write": "b",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "get_new_dir_Bc",
                    "write": "c",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "get_new_dir_Bd",
                    "write": "d",
                    "action": "RIGHT",
                },
            ],
            "get_new_char_C": [
                {
                    "read": "a",
                    "to_state": "get_new_dir_Ca",
                    "write": "a",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "get_new_dir_Cb",
                    "write": "b",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "get_new_dir_Cc",
                    "write": "c",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "get_new_dir_Cd",
                    "write": "d",
                    "action": "RIGHT",
                },
            ],
            "get_new_char_D": [
                {
                    "read": "a",
                    "to_state": "get_new_dir_Da",
                    "write": "a",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "get_new_dir_Db",
                    "write": "b",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "get_new_dir_Dc",
                    "write": "c",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "get_new_dir_Dd",
                    "write": "d",
                    "action": "RIGHT",
                },
            ],
            "get_new_dir_Aa": [
                {"read": "-", "to_state": "apply_AaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AaR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Ab": [
                {"read": "-", "to_state": "apply_AbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AbR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Ac": [
                {"read": "-", "to_state": "apply_AcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AcR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Ad": [
                {"read": "-", "to_state": "apply_AdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AdR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Ba": [
                {"read": "-", "to_state": "apply_BaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BaR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Bb": [
                {"read": "-", "to_state": "apply_BbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BbR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Bc": [
                {"read": "-", "to_state": "apply_BcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BcR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Bd": [
                {"read": "-", "to_state": "apply_BdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BdR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Ca": [
                {"read": "-", "to_state": "apply_CaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CaR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Cb": [
                {"read": "-", "to_state": "apply_CbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CbR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Cc": [
                {"read": "-", "to_state": "apply_CcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CcR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Cd": [
                {"read": "-", "to_state": "apply_CdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CdR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Da": [
                {"read": "-", "to_state": "apply_DaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DaR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Db": [
                {"read": "-", "to_state": "apply_DbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DbR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Dc": [
                {"read": "-", "to_state": "apply_DcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DcR", "write": "+", "action": "RIGHT"},
            ],
            "get_new_dir_Dd": [
                {"read": "-", "to_state": "apply_DdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DdR", "write": "+", "action": "RIGHT"},
            ],
            "apply_AaL": [
                {"read": ";", "to_state": "apply_AaL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AaL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AaL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AaL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AaL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AaL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AaL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AaL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AaL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AaL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AaL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AaL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AaL", "write": "!", "action": "RIGHT"},
            ],
            "apply_AaR": [
                {"read": ";", "to_state": "apply_AaR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AaR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AaR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AaR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AaR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AaR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AaR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AaR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AaR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AaR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AaR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AaR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AaR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AaR", "write": "!", "action": "RIGHT"},
            ],
            "apply_AbL": [
                {"read": ";", "to_state": "apply_AbL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AbL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AbL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AbL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AbL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AbL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AbL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AbL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AbL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AbL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AbL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AbL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AbL", "write": "!", "action": "RIGHT"},
            ],
            "apply_AbR": [
                {"read": ";", "to_state": "apply_AbR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AbR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AbR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AbR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AbR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AbR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AbR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AbR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AbR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AbR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AbR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AbR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AbR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AbR", "write": "!", "action": "RIGHT"},
            ],
            "apply_AcL": [
                {"read": ";", "to_state": "apply_AcL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AcL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AcL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AcL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AcL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AcL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AcL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AcL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AcL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AcL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AcL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AcL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AcL", "write": "!", "action": "RIGHT"},
            ],
            "apply_AcR": [
                {"read": ";", "to_state": "apply_AcR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AcR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AcR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AcR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AcR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AcR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AcR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AcR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AcR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AcR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AcR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AcR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AcR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AcR", "write": "!", "action": "RIGHT"},
            ],
            "apply_AdL": [
                {"read": ";", "to_state": "apply_AdL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AdL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AdL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AdL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AdL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AdL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AdL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AdL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AdL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AdL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AdL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AdL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AdL", "write": "!", "action": "RIGHT"},
            ],
            "apply_AdR": [
                {"read": ";", "to_state": "apply_AdR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_AdR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_AdR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_AdR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_AdR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_AdR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_AdR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_AdR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_AdR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_AdR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_AdR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_AdR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_AdR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_AdR", "write": "!", "action": "RIGHT"},
            ],
            "apply_BaL": [
                {"read": ";", "to_state": "apply_BaL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BaL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BaL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BaL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BaL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BaL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BaL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BaL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BaL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BaL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BaL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BaL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BaL", "write": "!", "action": "RIGHT"},
            ],
            "apply_BaR": [
                {"read": ";", "to_state": "apply_BaR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BaR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BaR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BaR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BaR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BaR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BaR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BaR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BaR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BaR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BaR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BaR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BaR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BaR", "write": "!", "action": "RIGHT"},
            ],
            "apply_BbL": [
                {"read": ";", "to_state": "apply_BbL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BbL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BbL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BbL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BbL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BbL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BbL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BbL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BbL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BbL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BbL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BbL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BbL", "write": "!", "action": "RIGHT"},
            ],
            "apply_BbR": [
                {"read": ";", "to_state": "apply_BbR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BbR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BbR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BbR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BbR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BbR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BbR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BbR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BbR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BbR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BbR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BbR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BbR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BbR", "write": "!", "action": "RIGHT"},
            ],
            "apply_BcL": [
                {"read": ";", "to_state": "apply_BcL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BcL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BcL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BcL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BcL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BcL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BcL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BcL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BcL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BcL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BcL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BcL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BcL", "write": "!", "action": "RIGHT"},
            ],
            "apply_BcR": [
                {"read": ";", "to_state": "apply_BcR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BcR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BcR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BcR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BcR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BcR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BcR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BcR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BcR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BcR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BcR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BcR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BcR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BcR", "write": "!", "action": "RIGHT"},
            ],
            "apply_BdL": [
                {"read": ";", "to_state": "apply_BdL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BdL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BdL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BdL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BdL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BdL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BdL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BdL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BdL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BdL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BdL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BdL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BdL", "write": "!", "action": "RIGHT"},
            ],
            "apply_BdR": [
                {"read": ";", "to_state": "apply_BdR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_BdR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_BdR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_BdR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_BdR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_BdR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_BdR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_BdR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_BdR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_BdR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_BdR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_BdR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_BdR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_BdR", "write": "!", "action": "RIGHT"},
            ],
            "apply_CaL": [
                {"read": ";", "to_state": "apply_CaL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CaL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CaL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CaL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CaL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CaL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CaL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CaL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CaL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CaL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CaL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CaL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CaL", "write": "!", "action": "RIGHT"},
            ],
            "apply_CaR": [
                {"read": ";", "to_state": "apply_CaR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CaR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CaR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CaR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CaR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CaR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CaR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CaR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CaR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CaR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CaR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CaR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CaR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CaR", "write": "!", "action": "RIGHT"},
            ],
            "apply_CbL": [
                {"read": ";", "to_state": "apply_CbL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CbL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CbL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CbL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CbL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CbL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CbL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CbL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CbL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CbL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CbL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CbL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CbL", "write": "!", "action": "RIGHT"},
            ],
            "apply_CbR": [
                {"read": ";", "to_state": "apply_CbR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CbR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CbR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CbR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CbR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CbR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CbR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CbR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CbR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CbR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CbR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CbR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CbR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CbR", "write": "!", "action": "RIGHT"},
            ],
            "apply_CcL": [
                {"read": ";", "to_state": "apply_CcL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CcL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CcL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CcL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CcL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CcL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CcL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CcL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CcL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CcL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CcL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CcL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CcL", "write": "!", "action": "RIGHT"},
            ],
            "apply_CcR": [
                {"read": ";", "to_state": "apply_CcR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CcR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CcR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CcR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CcR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CcR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CcR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CcR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CcR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CcR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CcR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CcR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CcR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CcR", "write": "!", "action": "RIGHT"},
            ],
            "apply_CdL": [
                {"read": ";", "to_state": "apply_CdL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CdL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CdL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CdL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CdL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CdL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CdL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CdL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CdL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CdL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CdL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CdL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CdL", "write": "!", "action": "RIGHT"},
            ],
            "apply_CdR": [
                {"read": ";", "to_state": "apply_CdR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_CdR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_CdR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_CdR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_CdR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_CdR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_CdR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_CdR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_CdR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_CdR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_CdR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_CdR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_CdR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_CdR", "write": "!", "action": "RIGHT"},
            ],
            "apply_DaL": [
                {"read": ";", "to_state": "apply_DaL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DaL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DaL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DaL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DaL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DaL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DaL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DaL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DaL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DaL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DaL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DaL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DaL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DaL", "write": "!", "action": "RIGHT"},
            ],
            "apply_DaR": [
                {"read": ";", "to_state": "apply_DaR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DaR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DaR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DaR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DaR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DaR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DaR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DaR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DaR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DaR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DaR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DaR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DaR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DaR", "write": "!", "action": "RIGHT"},
            ],
            "apply_DbL": [
                {"read": ";", "to_state": "apply_DbL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DbL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DbL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DbL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DbL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DbL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DbL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DbL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DbL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DbL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DbL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DbL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DbL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DbL", "write": "!", "action": "RIGHT"},
            ],
            "apply_DbR": [
                {"read": ";", "to_state": "apply_DbR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DbR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DbR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DbR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DbR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DbR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DbR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DbR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DbR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DbR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DbR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DbR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DbR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DbR", "write": "!", "action": "RIGHT"},
            ],
            "apply_DcL": [
                {"read": ";", "to_state": "apply_DcL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DcL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DcL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DcL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DcL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DcL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DcL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DcL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DcL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DcL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DcL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DcL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DcL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DcL", "write": "!", "action": "RIGHT"},
            ],
            "apply_DcR": [
                {"read": ";", "to_state": "apply_DcR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DcR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DcR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DcR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DcR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DcR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DcR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DcR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DcR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DcR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DcR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DcR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DcR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DcR", "write": "!", "action": "RIGHT"},
            ],
            "apply_DdL": [
                {"read": ";", "to_state": "apply_DdL", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DdL", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DdL", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DdL", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DdL", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DdL", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DdL", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DdL", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DdL", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DdL", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DdL", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DdL", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DdL", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DdL", "write": "!", "action": "RIGHT"},
            ],
            "apply_DdR": [
                {"read": ";", "to_state": "apply_DdR", "write": ";", "action": "RIGHT"},
                {"read": "]", "to_state": "apply_DdR", "write": "]", "action": "RIGHT"},
                {"read": "A", "to_state": "apply_DdR", "write": "A", "action": "RIGHT"},
                {"read": "B", "to_state": "apply_DdR", "write": "B", "action": "RIGHT"},
                {"read": "C", "to_state": "apply_DdR", "write": "C", "action": "RIGHT"},
                {"read": "D", "to_state": "apply_DdR", "write": "D", "action": "RIGHT"},
                {"read": "a", "to_state": "apply_DdR", "write": "a", "action": "RIGHT"},
                {"read": "b", "to_state": "apply_DdR", "write": "b", "action": "RIGHT"},
                {"read": "c", "to_state": "apply_DdR", "write": "c", "action": "RIGHT"},
                {"read": "d", "to_state": "apply_DdR", "write": "d", "action": "RIGHT"},
                {"read": ".", "to_state": "apply_DdR", "write": ".", "action": "RIGHT"},
                {"read": "-", "to_state": "apply_DdR", "write": "-", "action": "RIGHT"},
                {"read": "+", "to_state": "apply_DdR", "write": "+", "action": "RIGHT"},
                {"read": "!", "to_state": "write_DdR", "write": "!", "action": "RIGHT"},
            ],
            "write_AaL": [
                {
                    "read": " ",
                    "to_state": "move_left_A",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_A",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_A",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_A",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_A",
                    "write": "a",
                    "action": "LEFT",
                },
            ],
            "write_AbL": [
                {
                    "read": " ",
                    "to_state": "move_left_A",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_A",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_A",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_A",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_A",
                    "write": "b",
                    "action": "LEFT",
                },
            ],
            "write_AcL": [
                {
                    "read": " ",
                    "to_state": "move_left_A",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_A",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_A",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_A",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_A",
                    "write": "c",
                    "action": "LEFT",
                },
            ],
            "write_AdL": [
                {
                    "read": " ",
                    "to_state": "move_left_A",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_A",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_A",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_A",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_A",
                    "write": "d",
                    "action": "LEFT",
                },
            ],
            "write_BaL": [
                {
                    "read": " ",
                    "to_state": "move_left_B",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_B",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_B",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_B",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_B",
                    "write": "a",
                    "action": "LEFT",
                },
            ],
            "write_BbL": [
                {
                    "read": " ",
                    "to_state": "move_left_B",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_B",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_B",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_B",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_B",
                    "write": "b",
                    "action": "LEFT",
                },
            ],
            "write_BcL": [
                {
                    "read": " ",
                    "to_state": "move_left_B",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_B",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_B",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_B",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_B",
                    "write": "c",
                    "action": "LEFT",
                },
            ],
            "write_BdL": [
                {
                    "read": " ",
                    "to_state": "move_left_B",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_B",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_B",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_B",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_B",
                    "write": "d",
                    "action": "LEFT",
                },
            ],
            "write_CaL": [
                {
                    "read": " ",
                    "to_state": "move_left_C",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_C",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_C",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_C",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_C",
                    "write": "a",
                    "action": "LEFT",
                },
            ],
            "write_CbL": [
                {
                    "read": " ",
                    "to_state": "move_left_C",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_C",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_C",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_C",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_C",
                    "write": "b",
                    "action": "LEFT",
                },
            ],
            "write_CcL": [
                {
                    "read": " ",
                    "to_state": "move_left_C",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_C",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_C",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_C",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_C",
                    "write": "c",
                    "action": "LEFT",
                },
            ],
            "write_CdL": [
                {
                    "read": " ",
                    "to_state": "move_left_C",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_C",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_C",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_C",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_C",
                    "write": "d",
                    "action": "LEFT",
                },
            ],
            "write_DaL": [
                {
                    "read": " ",
                    "to_state": "move_left_D",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_D",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_D",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_D",
                    "write": "a",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_D",
                    "write": "a",
                    "action": "LEFT",
                },
            ],
            "write_DbL": [
                {
                    "read": " ",
                    "to_state": "move_left_D",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_D",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_D",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_D",
                    "write": "b",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_D",
                    "write": "b",
                    "action": "LEFT",
                },
            ],
            "write_DcL": [
                {
                    "read": " ",
                    "to_state": "move_left_D",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_D",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_D",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_D",
                    "write": "c",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_D",
                    "write": "c",
                    "action": "LEFT",
                },
            ],
            "write_DdL": [
                {
                    "read": " ",
                    "to_state": "move_left_D",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_left_D",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_D",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_D",
                    "write": "d",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_D",
                    "write": "d",
                    "action": "LEFT",
                },
            ],
            "move_left_A": [
                {
                    "read": "a",
                    "to_state": "move_left_Aa",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_Ab",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_Ac",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_Ad",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "!",
                    "to_state": "move_left_A",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "]",
                    "to_state": "TODO_NEG_POS",
                    "write": "]",
                    "action": "RIGHT",
                },
            ],
            "move_left_B": [
                {
                    "read": "a",
                    "to_state": "move_left_Ba",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_Bb",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_Bc",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_Bd",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "!",
                    "to_state": "move_left_B",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "]",
                    "to_state": "TODO_NEG_POS",
                    "write": "]",
                    "action": "RIGHT",
                },
            ],
            "move_left_C": [
                {
                    "read": "a",
                    "to_state": "move_left_Ca",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_Cb",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_Cc",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_Cd",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "!",
                    "to_state": "move_left_C",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "]",
                    "to_state": "TODO_NEG_POS",
                    "write": "]",
                    "action": "RIGHT",
                },
            ],
            "move_left_D": [
                {
                    "read": "a",
                    "to_state": "move_left_Da",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "b",
                    "to_state": "move_left_Db",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "c",
                    "to_state": "move_left_Dc",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "d",
                    "to_state": "move_left_Dd",
                    "write": "!",
                    "action": "RIGHT",
                },
                {
                    "read": "!",
                    "to_state": "move_left_D",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "]",
                    "to_state": "TODO_NEG_POS",
                    "write": "]",
                    "action": "RIGHT",
                },
            ],
            "move_left_Aa": [
                {"read": "!", "to_state": "state_A", "write": "a", "action": "LEFT"}
            ],
            "move_left_Ab": [
                {"read": "!", "to_state": "state_A", "write": "b", "action": "LEFT"}
            ],
            "move_left_Ac": [
                {"read": "!", "to_state": "state_A", "write": "c", "action": "LEFT"}
            ],
            "move_left_Ad": [
                {"read": "!", "to_state": "state_A", "write": "d", "action": "LEFT"}
            ],
            "move_left_Ba": [
                {"read": "!", "to_state": "state_B", "write": "a", "action": "LEFT"}
            ],
            "move_left_Bb": [
                {"read": "!", "to_state": "state_B", "write": "b", "action": "LEFT"}
            ],
            "move_left_Bc": [
                {"read": "!", "to_state": "state_B", "write": "c", "action": "LEFT"}
            ],
            "move_left_Bd": [
                {"read": "!", "to_state": "state_B", "write": "d", "action": "LEFT"}
            ],
            "move_left_Ca": [
                {"read": "!", "to_state": "state_C", "write": "a", "action": "LEFT"}
            ],
            "move_left_Cb": [
                {"read": "!", "to_state": "state_C", "write": "b", "action": "LEFT"}
            ],
            "move_left_Cc": [
                {"read": "!", "to_state": "state_C", "write": "c", "action": "LEFT"}
            ],
            "move_left_Cd": [
                {"read": "!", "to_state": "state_C", "write": "d", "action": "LEFT"}
            ],
            "move_left_Da": [
                {"read": "!", "to_state": "state_D", "write": "a", "action": "LEFT"}
            ],
            "move_left_Db": [
                {"read": "!", "to_state": "state_D", "write": "b", "action": "LEFT"}
            ],
            "move_left_Dc": [
                {"read": "!", "to_state": "state_D", "write": "c", "action": "LEFT"}
            ],
            "move_left_Dd": [
                {"read": "!", "to_state": "state_D", "write": "d", "action": "LEFT"}
            ],
            "write_AaR": [
                {
                    "read": " ",
                    "to_state": "move_right_Aa",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Aa",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Aa",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Aa",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Aa",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_AbR": [
                {
                    "read": " ",
                    "to_state": "move_right_Ab",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Ab",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Ab",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Ab",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Ab",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_AcR": [
                {
                    "read": " ",
                    "to_state": "move_right_Ac",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Ac",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Ac",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Ac",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Ac",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_AdR": [
                {
                    "read": " ",
                    "to_state": "move_right_Ad",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Ad",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Ad",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Ad",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Ad",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_BaR": [
                {
                    "read": " ",
                    "to_state": "move_right_Ba",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Ba",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Ba",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Ba",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Ba",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_BbR": [
                {
                    "read": " ",
                    "to_state": "move_right_Bb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Bb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Bb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Bb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Bb",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_BcR": [
                {
                    "read": " ",
                    "to_state": "move_right_Bc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Bc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Bc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Bc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Bc",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_BdR": [
                {
                    "read": " ",
                    "to_state": "move_right_Bd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Bd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Bd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Bd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Bd",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_CaR": [
                {
                    "read": " ",
                    "to_state": "move_right_Ca",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Ca",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Ca",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Ca",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Ca",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_CbR": [
                {
                    "read": " ",
                    "to_state": "move_right_Cb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Cb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Cb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Cb",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Cb",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_CcR": [
                {
                    "read": " ",
                    "to_state": "move_right_Cc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Cc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Cc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Cc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Cc",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_CdR": [
                {
                    "read": " ",
                    "to_state": "move_right_Cd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Cd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Cd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Cd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Cd",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_DaR": [
                {
                    "read": " ",
                    "to_state": "move_right_Da",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Da",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Da",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Da",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Da",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_DbR": [
                {
                    "read": " ",
                    "to_state": "move_right_Db",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Db",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Db",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Db",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Db",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_DcR": [
                {
                    "read": " ",
                    "to_state": "move_right_Dc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Dc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Dc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Dc",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Dc",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "write_DdR": [
                {
                    "read": " ",
                    "to_state": "move_right_Dd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "a",
                    "to_state": "move_right_Dd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "b",
                    "to_state": "move_right_Dd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "c",
                    "to_state": "move_right_Dd",
                    "write": "!",
                    "action": "LEFT",
                },
                {
                    "read": "d",
                    "to_state": "move_right_Dd",
                    "write": "!",
                    "action": "LEFT",
                },
            ],
            "move_right_Aa": [
                {"read": "!", "to_state": "state_A", "write": "a", "action": "RIGHT"}
            ],
            "move_right_Ab": [
                {"read": "!", "to_state": "state_A", "write": "b", "action": "RIGHT"}
            ],
            "move_right_Ac": [
                {"read": "!", "to_state": "state_A", "write": "c", "action": "RIGHT"}
            ],
            "move_right_Ad": [
                {"read": "!", "to_state": "state_A", "write": "d", "action": "RIGHT"}
            ],
            "move_right_Ba": [
                {"read": "!", "to_state": "state_B", "write": "a", "action": "RIGHT"}
            ],
            "move_right_Bb": [
                {"read": "!", "to_state": "state_B", "write": "b", "action": "RIGHT"}
            ],
            "move_right_Bc": [
                {"read": "!", "to_state": "state_B", "write": "c", "action": "RIGHT"}
            ],
            "move_right_Bd": [
                {"read": "!", "to_state": "state_B", "write": "d", "action": "RIGHT"}
            ],
            "move_right_Ca": [
                {"read": "!", "to_state": "state_C", "write": "a", "action": "RIGHT"}
            ],
            "move_right_Cb": [
                {"read": "!", "to_state": "state_C", "write": "b", "action": "RIGHT"}
            ],
            "move_right_Cc": [
                {"read": "!", "to_state": "state_C", "write": "c", "action": "RIGHT"}
            ],
            "move_right_Cd": [
                {"read": "!", "to_state": "state_C", "write": "d", "action": "RIGHT"}
            ],
            "move_right_Da": [
                {"read": "!", "to_state": "state_D", "write": "a", "action": "RIGHT"}
            ],
            "move_right_Db": [
                {"read": "!", "to_state": "state_D", "write": "b", "action": "RIGHT"}
            ],
            "move_right_Dc": [
                {"read": "!", "to_state": "state_D", "write": "c", "action": "RIGHT"}
            ],
            "move_right_Dd": [
                {"read": "!", "to_state": "state_D", "write": "d", "action": "RIGHT"}
            ],
        },
    },
    open("okok.json", "w"),
    indent=4,
)