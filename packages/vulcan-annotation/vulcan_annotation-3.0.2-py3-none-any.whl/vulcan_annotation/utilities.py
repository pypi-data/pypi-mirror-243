from Levenshtein import distance as sdist


def divergence(from_dict, to_dict):
    if from_dict is None:
        if to_dict is None:
            return 0
        elif "value" not in to_dict:
            return 1
        elif isinstance(to_dict["value"], str):
            return 1 + len(to_dict["value"])
        elif isinstance(to_dict["value"], dict):
            return 1 + divergence(None, to_dict["value"])
        elif isinstance(to_dict["value"], list):
            return 1 + sum([divergence(None, i) for i in to_dict["value"]])
    else:
        if to_dict is None:
            return 1
        
        if to_dict["key"] != from_dict["key"]:
            return 1 + divergence(None, to_dict)

        if "value" not in to_dict:
            return 2
        elif isinstance(to_dict["value"], str):
            return sdist(from_dict["value"], to_dict["value"])
        elif isinstance(to_dict["value"], dict):
            return divergence(from_dict["value"], to_dict["value"])
        elif isinstance(to_dict["value"], list):
            fdv_hash = {
                i["key"]: i
                for i in from_dict["value"]
            }
            tdv_hash = {
                i["key"]: i
                for i in to_dict["value"]
            }

            div = 0
            # for each key in fdv not in tdv, div += 1
            for k in fdv_hash:
                if k not in tdv_hash:
                    div += 1
            
            # for each key in tdv, div += divergence(fdv[k], tdv[k])
            for k in tdv_hash:
                if k not in fdv_hash:
                    div += divergence(None, tdv_hash[k])
                else:
                    div += divergence(fdv_hash[k], tdv_hash[k])

            return div


if __name__ == '__main__':
    assert(sdist("theresa", "tesla") == 4)

    from_dict = {
        "key": "1",
        "value": [
            {
                "key": "1",
                "value": {
                    "key": "1"
                }
            },
            {
                "key": "2",
                "value": "tesla"
            }
        ]
    }

    to_dict = {
        "key": "1",
        "value": [
            {
                "key": "0",
                "value": {
                    "key": "1",
                    "value": "test"
                }
            },
            {
                "key": "2",
                "value": "theresa"
            },
            {
                "key": "3"
            }
        ]
    }
    
    assert(divergence(None, from_dict) == 5 + 4)
    assert(divergence(None, to_dict) == 5 + 11)

    assert(divergence(from_dict, to_dict) == 4 + 4 + 4)

