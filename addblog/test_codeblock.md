title=测试用例
summary=此用例用来测试blog是否可以显示代码和公式
tags=test,ip
<ep_info>
# C++常用库函数

标签（空格分隔）： C++ LeetCode 面试

---
##[cctype](http://www.cplusplus.com/reference/cctype/)
*isalnum* *isalpha* *isdigit* *islower* *isspace* *isupper* *isxdigit* *toupper* *tolower*

##[cmath](http://www.cplusplus.com/reference/cmath/)

##partial_sum
*描述：* Assigns to every element in the range starting at result the partial sum of the corresponding elements in the range
*[示例](https://leetcode.com/problems/range-sum-query-immutable/)：*

```python
class NumArray {
public:
    NumArray(vector<int> &nums) : psum(nums.size()+1, 0) {
        partial_sum( nums.begin(), nums.end(), psum.begin()+1);
    }

    int sumRange(int i, int j) {
        return psum[j+1] - psum[i];
    }
private:
    vector<int> psum;    
};
```
$$\sum\limits_{i=1}^n i = \frac{n(n-1)}{2}$$
