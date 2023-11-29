class MonotonicStack:
    """
    Monotonic stack class
    """
    def __init__(self, 
                 array: list):
        self.array = array

    def next_smaller_on_right(self) -> list:
        """
        Find the next right smaller element for each element in the array
        """
        stack = []
        result = [-1] * len(self.array)
        for i in range(len(self.array)):
            while stack and self.array[stack[-1]] > self.array[i]:
                result[stack.pop()] = i
            stack.append(i)
        return result
    
    def next_greater_on_right(self) -> list:
        """
        Find the next right greater element for each element in the array
        """
        stack = []
        result = [-1] * len(self.array)
        for i in range(len(self.array)):
            while stack and self.array[stack[-1]] < self.array[i]:
                result[stack.pop()] = i
            stack.append(i)
        return result
    
    def next_smaller_on_left(self) -> list:
        """
        Find the next left smaller element for each element in the array
        """
        stack = []
        result = [-1] * len(self.array)
        for i in range(len(self.array)-1, -1, -1):
            while stack and self.array[stack[-1]] > self.array[i]:
                result[stack.pop()] = i
            stack.append(i)
        return result
    
    def next_greater_on_left(self) -> list:
        """
        Find the next left greater element for each element in the array
        """
        stack = []
        result = [-1] * len(self.array)
        for i in range(len(self.array)-1, -1, -1):
            while stack and self.array[stack[-1]] < self.array[i]:
                result[stack.pop()] = i
            stack.append(i)
        return result
