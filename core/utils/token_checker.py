import random


class TokenChecker:
    def __init__(self) -> None:
        """
        Initialize a new instance of the TokenChecker class.

        Attributes:
            tree (dict): A dictionary representing the token tree.
            range (int): The range of the token IDs.
        """
        self.tree = {}
        self.range = 16**30

    def __repr__(self):
        output = []
        for i in self.tree:
            output.append(f"'{i}': {self.tree[i]}")
        return "\n".join(output)

    def find(self, id: str) -> bool:
        """
        Check if a given token ID exists in the token tree.

        Args:
            id (str): The token ID to check.

        Returns:
            bool: True if the ID exists in the tree, False otherwise.
        """
        return self._get(id) is not None

    def generate_add(self, prev_id: str = None) -> str:
        """
        Generate a new token ID and add it to the token tree.

        Args:
            prev_id (str): The ID of the previous token in the tree (optional).

        Returns:
            str: The newly generated token ID.
        """
        # https://stackoverflow.com/questions/2782229/most-lightweight-way-to-create-a-random-string-and-a-random-hexadecimal-number
        id = "%030x" % random.randrange(self.range)

        try:
            self.add(id, prev_id)
        except ValueError as e:
            # Techincally possible for an infinite loop to appear
            if str(e) == "Id key already exists":
                return self.generate_add(prev_id)
            else: 
                raise e

        return id

    def add(self, id: str, prev_id: str = None):
        """
        Add a new token ID to the token tree.

        Args:
            id (str): The token ID to add.
            prev_id (str): The ID of the previous token in the tree (optional).

        Raises:
            ValueError: If the ID already exists in the tree.
            KeyError: If the previous ID does not exist in the tree.
        """
        if self._get(id):
            raise ValueError("Id key already exists")

        if prev_id:
            prev = self._get(prev_id)

            if not prev:
                raise KeyError("Previous Id does not exist")

            if prev["next"]:
                self._remove_tree(prev_id)
                raise ValueError("Id already has a next id. Removing tree...")

            self._set(prev_id, id)

        self.tree[id] = {"prev": prev_id, "next": None}

    def _get(self, id: str):
        """
        Get the node with the given ID from the token tree.

        Args:
            id (str): The ID of the node to get.

        Returns:
            dict: A dictionary representing the node if found, None otherwise.
        """
        try:
            return self.tree[id]
        except KeyError:
            return None

    def _set(self, id: str, next_id: str):
        """
        Set the 'next' attribute of the node with the given ID to the given next ID.

        Args:
            id (str): The ID of the node to set.
            next_id (str): The ID of the next node in the tree.
        """
        self.tree[id]["next"] = next_id

    def _remove_tree(self, id: str):
        """
        Remove a node and all its children from the token tree.

        Args:
            id (str): The ID of the node to remove.
        """
        cur = self._get(id)

        if cur["prev"]:
            prev = self._get(cur["prev"])

            if prev and prev["next"] == id:
                prev_id = cur["prev"]
                self.tree[prev_id]["next"] = None
                self._remove_tree(prev_id)

        if cur["next"]:
            next = self._get(cur["next"])

            if next and next["prev"] == id:
                next_id = cur["next"]
                self.tree[next_id]["prev"] = None
                self._remove_tree(next_id)
                
        del self.tree[id]


token_checker = TokenChecker()
