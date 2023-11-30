def ped(x: str, y: str, delta: int) -> int:
    """

    Computes the prefix edit distance PED(x,y) for the two given strings x and
    y. Returns PED(x,y) if it is smaller or equal to the given delta; delta + 1
    otherwise.

    """
    pass


InvertedList = list[tuple[int, int]]


def k_merge(lists: list[InvertedList]) -> InvertedList:
    """

    Merges the given inverted lists using a k-way merge, where each list
    contains (ID, freq) tuples.

    """
    pass


def sort_merge(lists: list[InvertedList]) -> InvertedList:
    """

    Merges the given inverted lists using a sort-based merge, where each list
    contains (ID, freq) tuples.

    """
    pass


class QGramIndex:
    """

    A QGram-Index.

    """

    def __init__(self, q: int, use_syns: bool = False) -> None:
        """

        Creates an empty qgram index.

        """
        pass

    def build_from_file(self, file_name: str) -> None:
        """

        Builds the index from the given file.

        The file should contain one entity per line, in the following format:
            name\tscore\tsynonyms\tinfo1\tinfo2\t...

        Synonyms are separated by a semicolon.

        An example line:
            Albert Einstein\t275\tEinstein;A. Einstein\tGerman physicist\t..."

        The entity IDs are one-based (starting with one).

        """
        pass

    def compute_qgrams(self, word: str) -> list[str]:
        """

        Compute q-grams for padded version of given string.

        """
        pass

    def find_matches(
        self,
        prefix: str,
        delta: int
    ) -> list[tuple[int, int]]:
        """

        Finds all entities y with PED(x, y) <= delta for a given integer delta
        and a given (normalized) prefix x.

        It returns a list of (ID, PED) ordered first by PED and
        then entity score.

        The IDs are one-based (starting with 1).

        """
        pass

    def get_infos(
        self,
        id: int
    ) -> tuple[str, str, int, list[str]] | None:
        """

        Returns the synonym, name, score and additional info for the given ID.
        If the index was built without synonyms, the synonym is always
        equal to the name.
        Returns None if the ID is invalid.

        """
        pass

    def normalize(self, word: str) -> str:
        """

        Normalize the given string (remove non-word characters and lower case).

        """
        pass
