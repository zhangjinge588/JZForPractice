from leetcode.basicDataStructures import *

class Solution(object):
    # There are several things to consider
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        p1 = l1
        p2 = l2
        
        carry_over = []

        if p1 == None:
            return l2

        if p2 == None:
            return l1
        
        while p1.next != None and p2.next != None:
            
            p1 = p1.next
            p2 = p2.next
        
        num_off_digits = 0
        
        is_p1 = 0

        print (p1, p2)
        
        if p1.next == None and p2.next == None:
            
            is_p1 = -1
        
        elif p1.next == None:
            
            while p2.next != None:
                
                p2 = p2.next
                num_off_digits += 1
            is_p1 = 1
                
        else:
            
            while p1.next != None:
                
                p1 = p1.next
                num_off_digits += 1
        
        if is_p1 == 1:

            
            new_node = ListNode(0)
            temp_p = new_node
            
            for i in range(num_off_digits-1):
                
                temp_p.next = ListNode(0)
                temp_p = temp_p.next

            temp_p.next = l1
            
            p1 = new_node
            p2 = l2

        elif is_p1 == 0:
            
            new_node = ListNode(0)
            temp_p = new_node
            
            for i in range(num_off_digits-1):
                
                temp_p.next = ListNode(0)
                temp_p = temp_p.next

            temp_p.next = l2
            
            p1 = l1
            p2 = new_node
        
        else:
            
            p1 = l1
            p2 = l2
        
        return self.addNumbersSameLen(p1, p2)
    
    def addNumbersSameLen(self, l1, l2):
        
        p1 = l1
        p2 = l2
     
        result = []
        
        carry_over = []
        
        front_carry_over = 0
        
        length = 0
        
        while p1 != None and p2 != None:
            
            sum_ = p1.val + p2.val
            
            if sum_ > 9:
                
                if length == 0:
                    
                    front_carry_over = sum_ / 10

                else:
                    carry_over.append((length - 1, sum_ / 10))
                
                sum_ = sum_ % 10
            
            result.append(sum_)
            
            length += 1
            
            p1 = p1.next
            p2 = p2.next
          
        result_l = None
        
        result_carry_over = [0] * length

        
        for item in carry_over:
            
            result_carry_over[item[0]] = item[1]

        while sum(result_carry_over) != 0:

            for i in range(len(result_carry_over)):

                index = length - 1 - i

                print (result_carry_over[index], result[index])

                sum_ = result_carry_over[index] + result[index]

                if sum_ > 9:

                    if index == 0:

                        front_carry_over += 1
                        result_carry_over[index] = 0

                        result[index] = sum_ % 10

                    else:
                        result_carry_over[index] = 0
                        result_carry_over[index - 1] = sum_ / 10

                        result[index] = sum_ % 10
                else:
                    result_carry_over[index] = 0
                    result[index] = sum_ % 10

        final_result = [sum(x) for x in zip(result, result_carry_over)]

        if front_carry_over != 0:
            
            result_l = ListNode(front_carry_over)

            temp_p = result_l
        
        for item in final_result:

            item = int(item)
            
            if result_l == None:
                
                result_l = ListNode(item)

                temp_p = result_l

            else:
                temp_p.next = ListNode(item)

                temp_p = temp_p.next
        
        return result_l