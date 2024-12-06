class Company(dict):
    def __init__(self, input_dict):
        super().__init__(input_dict)

    def __key(self):
        """
        Create a tuple of attributes used for comparison and hashing.
        """
        # Use specific keys to determine equality and hashing
        return (self.get("name"), self.get("website"), self.get("year_of_founding"))

    def __hash__(self):
        """
        Hash the object based on the selected attributes.
        """
        return hash(self.__key())

    def __eq__(self, other):
        """
        Compare two Company objects for equality based on selected attributes.
        """
        if not isinstance(other, Company):
            return False
        return self.__key() == other.__key()
