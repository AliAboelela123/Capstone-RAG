class Chunk:
    def __init__(self, uuid, text, embedding, source):
        """
        Initializes a Chunk object with main text, an integer vector, and additional text.

        Parameters:
        - uuid (str): uuid to identify the chunk
        - text (str): The string representation of the chunk
        - embedding (int): An integer vector associated with the chunk.
        - source (str): The name of the document this chunk originates from.
        """
        self.uuid = uuid
        self.text = text
        self.embedding = embedding
        self.source = source

    def find_reference(self, number):
        """
        Scans the chunk for the input number. If a match is found returns
        the surrounding sentence

        Parameters:
        - number (int): The number we're scanning for
        """
        words = self.text.split()
        for i, word in enumerate(words):
            if number in word:
                start = max(i - 10, 0)
                end = min(i + 11, len(words))
                return ' '.join(words[start:end])
        return None
