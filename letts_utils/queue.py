class Queue:
    """
    A custom queue class for Lett's Python Utilities. \n
    Please do not change any variables without their respective methods. Doing so may result in unexpected behavior and
    should be avoided unless you know what you are doing.
    """
    in_queue = []
    left_queue = []

    def __init__(self, initial_queue=None):
        if initial_queue is None:
            initial_queue = []
        self.in_queue = initial_queue

    def __len__(self, iterable: list | dict | tuple | str):
        len(iterable)

    def get_next_item(self, remove: bool = True) -> any:
        """
        Gets the next item (index 0) from the queue.
        :param remove: Whether to remove the value from the queue and move it to the previous values queue.
        :return: Next item in the queue
        """

        value = self.in_queue[0]
        if not remove:
            return value

        self.in_queue.remove(value)
        self.left_queue.append(value)
        return value

    def get_previous_items(self, remove: bool = True, i: int = -1) -> any:
        """
        Gets the previous item (index 0) from the previous values queue.
        :param remove: Whether to remove the value from the previous values queue and move it to the queue.
        :param i: Amount to go back inside of the queue.
        :return: Previous item in the queue
        """

        value = self.left_queue[i]
        if not remove:
            return value

        for x in range(-i):
            value = self.left_queue.pop(-1)
            self.in_queue.insert(0, value)

    def append_to_queue(self, value) -> None:
        """
        Appends to the end of the queue.
        :param value: The value to append to the end of the queue.
        :return: Nothing.
        """

        self.in_queue.append(value)

    def empty(self) -> bool:
        """
        :return: If the audio queue is empty or not
        """

        return self.__len__(self.in_queue) == 0

    def empty_previous(self) -> bool:
        """
        :return: If the previous audio queue is empty or not
        """

        return self.__len__(self.in_queue) == 0


if __name__ == "__main__":
    # Testing initialization and getting next item without removing it.
    test_queue = Queue(["Lorem", "ipsum,", "dolor", "sit", "amet"])
    print(test_queue.get_next_item(False))
    print(test_queue.in_queue)

    # Testing getting the next item with removing it and retrieving it again from the previous queue
    test_queue.get_next_item()
    test_queue.get_next_item()
    print(test_queue.get_previous_items(True, -2))
    print(test_queue.in_queue)
    print(test_queue.left_queue)
