import numpy as np

import pandas as pd

from leetcode.basicDataStructures import *
from leetcode.addTwoNumbersII import *

l1 = ListNode(7, ListNode(2, ListNode(4, ListNode(3))))

l2 = ListNode(5, ListNode(6, ListNode(4)))

l3 = ListNode(2, ListNode(4, ListNode(3)))

l4 = ListNode(2)

l5 = ListNode(8, ListNode(9, ListNode(9, ListNode(9))))

solution = Solution()

print (l4)
print (l5)

print ("##############")

print (solution.addTwoNumbers(l4, l5))
