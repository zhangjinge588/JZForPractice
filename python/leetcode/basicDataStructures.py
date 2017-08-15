# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x, _next=None):
        self.val = x
        self.next = _next

    def __repr__(self):

        p = self

        s = ""

        while p != None:

            s += str(p.val) + "->"

            p = p.next

        return s[:-2]

