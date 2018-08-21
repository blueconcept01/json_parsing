class ObjectFlattener:
    KEY_INDEX = "__index"

    def __init__(self, key_set=None):
        """
        Initialize ObjectFlattener with optional parameters
        :param key_set: keys for unique identifying child to parent relationships
        """
        self.flatten_dict_list = {}
        self.KEY_FIELD_NAMES = {"id", "date", self.KEY_INDEX}
        if key_set:
            self.KEY_FIELD_NAMES.update(key_set)

    def flatten(self, json, name="", keys=None, _index=None):
        """
        Root function to call to start the flattening process
        :param json: could be a list or dict that holds the data to flatten
        :param name: name to recursively add to
        :param keys: unique ids to identify child to parent relationship
        :param _index: index if object is part of a list
        """
        if isinstance(json, dict):
            self.dict_flatten(json, name=name, keys=keys, _index=_index)
        if isinstance(json, list):
            self.list_flatten(json, name=name, keys=keys)

    def dict_flatten(self, dct, name="", keys=None, _index=None):
        """
        Creates and adds dictionary to flatten_dict_list
        :param dct: dict to iterate through
        :param name: name of the object
        :param keys: unique ids to identify child to parent relationship
        :param _index: index if object is part of a list
        """
        if keys:
            new_obj = keys.copy()
        else:
            keys = {}
            new_obj = {}
        keys = self.get_keys(keys, dct)

        if _index is not None:
            new_obj[self.KEY_INDEX] = str(_index)

        for k, v in dct.items():
            if is_data(v):
                new_obj[k] = str(v)
            else:
                self.flatten(v, name=combine_words(strip_s(name), strip_s(k)), keys=keys, _index=_index)

        self.add_json(new_obj, name)

    def list_flatten(self, lst, name="", keys=None):
        """
        Iterates through list to recursively create and add dict objects
        :param lst: list to iterate through to get individual objects
        :param name: name of current objects
        :param keys: unique ids to identify child to parent relationship
        """
        if len(lst) == 1:
            self.flatten(lst[0], name=name, keys=keys)
        else:
            for i, d in enumerate(lst):
                self.flatten(d, name=name, keys=keys, _index=i)

    def add_json(self, json, name):
        """
        Adds the json object to the flatten_dict_list
        :param json: input json
        :param name: name of that object json
        """
        if json:
            if self.flatten_dict_list.get(name):
                self.flatten_dict_list[name].append(json)
            else:
                self.flatten_dict_list[name] = [json]

    def get_keys(self, keys, dct):
        """
        Gets keys from dict based KEY_FIELD_NAMES
        :param keys: dict of unique ids and their values
        :param dct: dct containing object data
        :return: dict with key and their values
        """
        for k, v in dct.items():
            if k in self.KEY_FIELD_NAMES:
                keys[k] = v
        return keys


def is_data(obj):
    """
    Checks if obj is data or to a data structure to recurse on
    :param obj: input obj to check
    :return: True if data or a list with only data, false otherwise
    """
    if isinstance(obj, (float, int, str)):
        return True
    elif isinstance(obj, list):
        for n in obj:
            if isinstance(n, dict):
                return False
        return True
    return False


def strip_s(word):
    """
    Rudimentary (dumb) function to remove plurity from names
    :param word: input word to remove the s/es from
    :return: singular word
    """
    if len(word) <= 1:
        return word
    if word[-1] == 's':
        if word[-2:] == "ss":
            return word
        if len(word) == 2:
            return word[:-1]
        if word[-2:] == 'es':
            if word[-3] == 's':
                return word[:-2]
        return word[:-1]
    else:
        return word


def combine_words(word_a, word_b):
    """
    Combines 2 words
    :return: words combined, if 1 word was empty returns the non empty word.
    """
    if word_a and word_b:
        return "%s_%s" % (word_a, word_b)
    elif word_a:
        return word_a
    elif word_b:
        return word_b
    else:
        return ""
