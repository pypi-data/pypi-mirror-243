#! -*- coding:utf-8 -*

import bisect
from typing import List, Tuple, Dict, Union, Any


class Interval(object):
    """type of interval object.

    """

    def __init__(self, arr: list, /):
        """

        :param arr: a list which length is 5, elements from 0 to 4 respectively are
            [left, right, include_left, include_right, sn], normally sn = 0.

            examples:
            case: [2, 5, True, False, 0], represent an interval [2, 5)
                arr[2] is True, so 2 is close, likely 5 is open
            case: [3, 3, True, True, 0], represent an interval [3, 3], or can said is a discrete point 3
                note: in this case, arr[2] and arr[3] must be True
            case: [NEG_INF, 3, False, True, 0], represent an interval (-inf, 3]
                note: for NEG_INF and INF, its include must be False
            case: [NEG_INF, INF, False, False, 0], represent an interval (-inf, inf)
        """
        self.arr = arr

    @property
    def left(self):
        """left of interval.

        :return:
        """
        return self.arr[0]

    @left.setter
    def left(self, value, ):
        self.arr[0] = value

    @property
    def include_left(self) -> bool:
        """whether left itself be included.

        :return:
        """
        return self.arr[2]

    @include_left.setter
    def include_left(self, value: bool, ):
        self.arr[2] = value

    @property
    def right(self):
        """right of interval.

        :return:
        """
        return self.arr[1]

    @right.setter
    def right(self, value, ):
        self.arr[1] = value

    @property
    def include_right(self) -> bool:
        """whether right itself be included.

        :return:
        """
        return self.arr[3]

    @include_right.setter
    def include_right(self, value: bool, ):
        self.arr[3] = value

    def __repr__(self):
        """Return repr(self).

        :return:
        """
        if self.left == self.right:
            return str(self.left)
        val = str(self.left) + ', ' + str(self.right)
        if self.include_left:
            val = '[' + val
        else:
            val = '(' + val
        if self.include_right:
            val += ']'
        else:
            val += ')'
        return val


class NegInf(object):
    """Type of negative infinite.

    """

    def __repr__(self):
        return '-inf'

    def __eq__(self, other):
        return other is self or isinstance(other, NegInf)

    def __lt__(self, other):
        """Return self < other.

        :param other:
        :return:
        """
        return self != other

    def __le__(self, other):
        """Return self <= other.

        :param other:
        :return:
        """
        return True

    def __gt__(self, other):
        """Return self > other.

        :param other:
        :return:
        """
        return False

    def __ge__(self, other):
        """Return self >= other.

        :param other:
        :return:
        """
        return self == other


class Inf(object):
    """Type of positive infinite.

    """

    def __repr__(self):
        return 'inf'

    def __eq__(self, other):
        return self is other or isinstance(other, Inf)

    def __lt__(self, other):
        """Return self < other.

        :param other:
        :return:
        """
        return False

    def __le__(self, other):
        """Return self <= other.

        :param other:
        :return:
        """
        return self == other

    def __gt__(self, other):
        """Return self > other.

        :param other:
        :return:
        """
        return self != other

    def __ge__(self, other):
        """Return self >= other.

        :param other:
        :return:
        """
        return True


NEG_INF = NegInf()
INF = Inf()


class IntervalHandler(object):
    """区间处理器

    """

    def __init__(self, ):
        # 存在中间区域 (a, b)  其中，a 和 b 都不是无穷
        self._mid_interval_arrays: List[list] = []
        # 标记该区间集是个无限集 (-inf, inf)
        self.inf_flag: bool = False
        # 存在负无穷区间 (-inf, neg_inf_value)
        self._neg_inf_values: list = []
        # 存在正无穷区间 (inf_value, inf)
        self._inf_values: list = []

    def add_interval(self, left, right, /, include_left: bool = False, include_right: bool = False):
        """Add an interval.

        :param left:
        :param right:
        :param include_left:
        :param include_right:
        :return:
        """
        if self.inf_flag:
            return
        if left is not NEG_INF:
            if right is not INF:
                if left <= right:
                    # (3, 5) (3, 3)
                    if left == right:
                        include_left, include_right = True, True
                    self._mid_interval_arrays.append([left, right, include_left, include_right, 0])
                    return
                    # (3, 2)
                raise ValueError("Interval '%s' error, must left <= right."
                                 % (Interval([left, right, include_left, include_right]),))
            # (3, inf)
            self._inf_values.append((left, include_left))
            return

        if right is not INF:
            # (-inf, -3)
            self._neg_inf_values.append((right, include_right))
            return

        # (-inf, inf)
        self.inf_flag = True

    def join_neg_inf_mid_inf(self, ) -> List[list]:
        """将 负无穷区、中间区、正无穷区 连接起来，并且已排序

        :return:
        """
        if self.inf_flag:
            return [[NEG_INF, INF, False, False, 0]]

        mid_intervals = sorted(self._mid_interval_arrays)
        if self._neg_inf_values:
            neg_inf_value, neg_inf_value_included = sorted(self._neg_inf_values)[-1]
            # 存在负无穷区间 (-inf, -3) (-inf, -3]
            # 注意，此处不能和 right 进行比较，考虑 mid_intervals: [(2, 7), (3, 4)], 遇到 (-inf, 5)
            pos = bisect.bisect_left([e[0] for e in mid_intervals], neg_inf_value, )
            """
            a. [-10, -5, -3, 2, 5]  pos = 2
            b. [-10, -5, 2, 5]  pos = 2
            c. [-10, -5,]  pos = 2
            d. [2, 5]  pos = 0
            e. []  pos = 0
            a. value[:pos] < neg_inf_value <= value[pos:]
            """
            del mid_intervals[:pos]
            mid_intervals.insert(0, [NEG_INF, neg_inf_value, False, neg_inf_value_included, 0])
        if self._inf_values:
            inf_value, inf_value_included = sorted(self._inf_values)[0]
            # 存在正无穷区间 (5, inf) [5, inf)
            # 注意，此处不能和 right 进行比较，考虑 mid_intervals: [(-inf, 3) ], 遇到 (-3, inf)
            pos = bisect.bisect_right([e[0] for e in mid_intervals], inf_value, )
            """
            a. [-3, 2, 5, 10, 12]  pos = 3  
            b. [-3, 2, 10, 12]  pos = 2
            c. [10, 12]  pos = 0
            d. [-3, 2]  pos = 2
            e. []  pos = 0
            a. value[:pos] <= inf_value < value[pos:]
            """
            del mid_intervals[pos:]
            mid_intervals.append([inf_value, INF, inf_value_included, False, 0])
        return mid_intervals


class IntervalSet(object):
    """IntervalSet([itvl_lis])  --> a IntervalSet object, simply called as iset

    itvl_lis must be a list, all elements in it must be x2tuple or discre_val

    A x2tuple element represent a continuous interval like (-1, 1) but not
    contain bound_val, or say it is open, and must left_bound ≤ right_bound,
    when =, it equal to a discre_val

    A discre_val element represent a discrete value like 0 but not None

    "None" only can be used in x2tuple, represent -inf or inf

    In a itvl_lis, all of the bound_val of x2tuple and the discre_val must
    be a same data type supportting <,<=,==,>=,>,!= or has __cmp__() method

    """

    def __init__(self, interval_arrays: List[list] = None, /, *, merge: bool = True):
        """itvl_lis is optional, in that case return an empty tvs."""
        interval_arrays = interval_arrays or []
        if interval_arrays and merge:
            interval_arrays.sort()
            self.merge(interval_arrays)
        self.interval_arrays: List[list] = interval_arrays
        # 标记该区间集是个无限集 (-inf, inf)
        self.inf_flag: bool = False
        if len(interval_arrays) == 1 and interval_arrays[0][0] == NEG_INF and interval_arrays[0][1] == INF:
            self.inf_flag = True
        self.interval_handler: IntervalHandler = IntervalHandler()

    @property
    def intervals(self):
        return [Interval(e) for e in self.interval_arrays]

    @classmethod
    def inf_tvs(cls) -> 'IntervalSet':
        return cls([[NEG_INF, INF, False, False, 0]], merge=False)

    def copy(self, ) -> 'IntervalSet':
        return IntervalSet([e.copy() for e in self.interval_arrays], merge=False)

    def __len__(self):
        return len(self.intervals)

    def is_empty(self) -> bool:
        return len(self.intervals) == 0

    @classmethod
    def parse_from_str(cls, tvs_str: str, /) -> 'IntervalSet':
        """

        :param tvs_str:
        :return:
        """
        interval_handler = IntervalHandler()
        for i, group in enumerate(tvs_str.split('|')):
            group = group.strip()
            if not group:
                continue
            if group.startswith(('(', '[')):
                tmp = group[1:-1].split(',')
                if len(tmp) != 2:
                    raise ValueError(
                        "Interval '%s' error, not match like (left, right) or discrete_point." % (group,))
                left, right = [e.strip() for e in tmp]
                left = int(left) if left != '-inf' else NEG_INF
                right = int(right) if right != 'inf' else INF
                interval_handler.add_interval(
                    left, right, include_left=group[0] == '[', include_right=group[-1] == ']')
                continue
            value = int(group)
            interval_handler.add_interval(value, value, include_left=True, include_right=True)
        interval_arrays = interval_handler.join_neg_inf_mid_inf()
        return cls(interval_arrays)

    @classmethod
    def merge(cls, interval_arrays: List[list], /, *, start: int = 0, end: int = None):
        """合并，合并能够合并的区间
        1.前提：intervals 是排序过的，且：
            -.(left, right) 严格升序
            -.当相邻的两个区间的 (left, right) 相等时，按 (include_left, include_right) 排序，即
                (f, f), (f, t), (t, f), (t, t)
        2.部分排序时，必须保证 [:start] 和 [end:] 两部分已合并过

        :param interval_arrays: intervals[start: end]之间的需要合并
        :param start: 起始下标
        :param end: start + N，N≥1
        :return:
        """
        if not interval_arrays:
            return []
        start = max(min(start, len(interval_arrays) - 1) - 2, 0)
        merged_interval_arrays: List[list] = [interval_arrays[start]]
        if end is None:
            end = len(interval_arrays)
        else:
            end = min(max(end, start + 1) + 2, len(interval_arrays))
        for i in range(start + 1, end):
            cls._calc_merge(merged_interval_arrays, interval_arrays[i])

        interval_arrays[start: end] = merged_interval_arrays

    @classmethod
    def _calc_merge(cls, merged_intervals: List[list], new: list, ):
        # 前一个区间如 (2, cu) 或者 [2, cu]
        # 此时按照排序，新区间可能是 (x, y) [x, y) 必定 2 ≤ x
        cu = merged_intervals[-1]
        if new[1] < cu[1]:
            # new.right < cu.right:
            # 新区间已被包含 (2, x, y, cu)
            # cu:(2, 5) new:(3, 4)
            return
        if cu[1] < new[0] or (cu[1] == new[0] and not cu[3] and not new[2]):
            # cu.right < new.left:
            # 两个区间不相交 (2, cu <= x, y) 且等于时都不闭合
            merged_intervals.append(new)
            return
        if new[0] == cu[0] and not cu[2] and new[2]:
            # new.left == cu.left and not cu.include_left and new.include_left:
            """左端点闭合性被改变
            新区间的左端使得前一区间的左端点被包含
            cu:(2, 5)  new:[2, 5) 或 [2, 6)
            例如:
            merged_intervals: (1, 2), (2, 5), ...                      
            new:                              [2, 6),
            此时， cu.include_left 的变化，有可能又会波及到 merged_intervals[-2]
            """
            if len(merged_intervals) > 1 and cu[0] == merged_intervals[-2][1]:
                # len(merged_intervals) > 1 and cu.left == merged_intervals[-2].right:
                # 波及到前 2 区间
                # [merged_intervals[-2].left, cu.right, merged_intervals[-2].include_left, cu.include_right, 0]
                cu = merged_intervals[-1] = [merged_intervals[-2][0], cu[1],
                                             merged_intervals[-2][2], cu[3], 0]
                del merged_intervals[-2]
            else:
                # [cu.left, cu.right, True, cu.include_right, 0]
                cu = merged_intervals[-1] = [cu[0], cu[1], True, cu[3], 0]
        if new[1] == cu[1]:
            # (2, x, cu==y)
            if not cu[3] and new[3]:
                # new.right == cu.right and not cu.include_right and new.include_right:
                """右端点闭合性被改变
                新区间与前一区间右端点重合
                cu:(2, 5) new:(2, 5) 或 (3, 5)
                例如:
                intervals[]:   ..., (4, 5), (5, 8),                     
                new:        [3, 5],
                此时， cu.include_left 的变化，有可能又会波及到 merged_intervals[:end+2]
                """
                # [cu.left, cu.right, cu.include_left, True, 0]
                merged_intervals[-1] = [cu[0], cu[1], cu[2], True, 0]
            return

        # 其余情况，都需要将 cu 和 new 拼接为一个新区间
        # cu:(2, 5)  new: (2, 8) 或 (3, 8) 或 [5, 8)
        # (2, x ≤ cu < y)
        # 执行拼接
        # [cu.left, new.right, cu.include_left, new.include_right, 0]
        merged_intervals[-1] = [cu[0], new[1], cu[2], new[3], 0]

    def __getitem__(self, item: int, /) -> Interval:
        try:
            return self.intervals[item]
        except IndexError:
            raise IndexError("IntervalSet index out of range.")

    def __repr__(self):
        """Return str(self)"""
        lis = []
        for interval in self:
            lis.append(str(interval))

        return ' | '.join(lis)

    def union(self, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """union of several interval set.

        :param tvs_lis:
        :return:
        """
        if not tvs_lis:
            return self.copy()
        tvs_lis = list(tvs_lis) + [self]
        if any(tvs.inf_flag for tvs in tvs_lis):
            # 如果有任一区间为无限集
            return self.inf_tvs()
        arrays_sorted = sorted((tvs.interval_arrays for tvs in tvs_lis), key=len, reverse=True)
        longest_arr = arrays_sorted[0][:]
        self.join_many_sorted_arr_into_longest(longest_arr, *arrays_sorted[1:])
        return self.__class__(longest_arr, merge=False)

    def add(self, left, right, include_left: bool = False, include_right: bool = False, /):
        """添加一个区间

        :param left:
        :param right:
        :param include_left:
        :param include_right:
        :return:
        """
        self.join_many_sorted_arr_into_longest(self.interval_arrays, [[left, right, include_left, include_right]])
        self.__dict__ = self.__class__(self.interval_arrays, merge=False).__dict__

    @classmethod
    def join_many_sorted_arr_into_longest(cls, longest_arr: List[list], /, *other_arrays: List[list],
                                          merge: bool = True):
        """合并多个有序数组到 longest_arr 中
        内部会视情况选择相对较高效的方法进行合并。

        :param longest_arr: 必须有序
        :param other_arrays: 必须有序
        :param merge:
        :return:
        """
        if not other_arrays:
            return longest_arr
        if len(longest_arr) >= 100:
            interval_min = min(arr[0] for arr in other_arrays)
            interval_max = max(arr[-1] for arr in other_arrays)
            lo, hi = bisect.bisect_left(longest_arr, interval_min), bisect.bisect_right(longest_arr, interval_max)
            if hi - lo <= len(longest_arr) * 0.618:
                """总宽度 ≤ longest_tvs_arr 的长度 * 0.618
                此时，只需要对 longest_arr 中部分做处理即可
                """
                mid = longest_arr[lo: hi]
                for arr in other_arrays:
                    mid += arr
                mid.sort()
                longest_arr[lo:hi] = mid
                if merge:
                    cls.merge(longest_arr, start=lo, end=lo + len(mid) + 1)
                return longest_arr
            if sum(len(arr) for arr in other_arrays) <= min(100, int(len(longest_arr) / 10)):
                # 其他 arr 总长度 ≤ longest_tvs_arr 的长度 / 10，且 ≤ 100
                cls._merge_arr_into_other_by_bisect(longest_arr, other_arrays, merge=merge)
                return longest_arr

        for arr in other_arrays:
            longest_arr += arr
        longest_arr.sort()
        if merge:
            cls.merge(longest_arr)
        return longest_arr

    @classmethod
    def _merge_arr_into_other_by_bisect(cls, longest_arr: List[list], other_arrays: Tuple[List[list]],
                                        /, *,
                                        merge: bool = True):
        for arr in other_arrays:
            for v in arr:
                pos = bisect.bisect_left(longest_arr, v)
                longest_arr.insert(pos, v)
                if merge:
                    cls.merge(longest_arr, start=pos, end=pos + 1)

    def __or__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        return self.union(other)

    def __ior__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        self.__dict__ = self.union(other).__dict__
        return self

    def update(self, *tvs_lis: 'IntervalSet'):
        self.__dict__ = self.union(*tvs_lis).__dict__

    @classmethod
    def intersection_many(cls, *tvs_lis: 'IntervalSet') -> 'IntervalSet':
        """intersection of several interval set.

        :param tvs_lis:
        :return:
        """
        if not tvs_lis or any(tvs.is_empty() for tvs in tvs_lis):
            # 如果有任一个是空集
            return cls()
        if len(tvs_lis) == 1:
            return tvs_lis[0].copy()

        valid_interval_arrays = cls._prune_for_intersection(tvs_lis)
        if not valid_interval_arrays:
            return cls()
        valid_interval_arrays.sort()

        appeared_sn_dic = {}
        sn_cnt = len(tvs_lis)
        new_intervals = []
        for interval in valid_interval_arrays:
            if interval[4] in appeared_sn_dic:
                del appeared_sn_dic[interval[4]]
            # 将新区间放入
            if len(appeared_sn_dic) + 1 < sn_cnt:
                # 如果加入后也不能到总数
                appeared_sn_dic[interval[4]] = interval
                continue

            intersection_interval = cls._calc_intersection(appeared_sn_dic, interval)
            if intersection_interval:
                new_intervals.append(intersection_interval)
            appeared_sn_dic[interval[4]] = interval

        return cls(new_intervals, merge=False)

    @classmethod
    def _prune_for_intersection(cls, tvs_lis: Tuple['IntervalSet'], ) -> List[list]:
        """剪枝，将＜最大左端的区间移除掉，避免无效运算，右端同样
        先找出最大的左端点，最小的右端点
        假设 left_max: -5  right_min: 7
        (f, f), (f, t), (t, f), (t, t)

        对于左端，任意 arr[1] ＜ left_max 的区间都是无效的，例如 (l, r)，只要 r < -5，注意 r == -5 的有可能产生交点
        可以按 (-5, -5, f, f) 进行靠左二分查找，pos < lo 的都是无效区间？
        但是有可能：..., (-8, -3), (-2, 2), ...
        所以：有可能 pos = lo - 1 也有效。

        同样，对于右端，任何 right_min ＜ arr[0] 的区间都是无效的，按 (7, 7, True, True) 进行靠右二分查找
        但是有可能：..., (3, 6), [7, 10), ... 此时 l == 7 的有可能产生交点
        所以调整为 按 (7, INF, True, True) 进行靠右二分查找，则 pos >= hi 的必定是无效区间.

        有可能 hi - lo == 0, 此时意味着：
        区间集 A：(-5, 7)
        区间集 B：(-20, -10), (10, 20)
        即：对于B来说，与 [left_max, right_min] 无交集，此时求交集结果必定为空。


        :param tvs_lis:
        :return:
        """
        left_max = max(tvs.interval_arrays[0][0] for tvs in tvs_lis)
        interval_left_max = [left_max, left_max, False, False, 0]
        right_min = min(tvs.interval_arrays[-1][1] for tvs in tvs_lis)
        interval_right_min = [right_min, INF, True, True, 0]
        valid_interval_arrays = []
        sn_max = 0
        for tvs in tvs_lis:
            lo = bisect.bisect_left(tvs.interval_arrays, interval_left_max)
            if lo > 0 and left_max <= tvs.interval_arrays[lo - 1][1]:
                lo -= 1
            hi = bisect.bisect_right(tvs.interval_arrays, interval_right_min)
            if lo == hi:
                return []
            tmp_valid_arrays = tvs.interval_arrays[lo:hi]
            for arr in tmp_valid_arrays:
                arr[4] = sn_max
            valid_interval_arrays += tmp_valid_arrays
            sn_max += 1

        return valid_interval_arrays

    @classmethod
    def _calc_intersection(cls, appeared_sn_dic: Dict[int, list], interval: list) -> Union[list, None]:
        """
        到了总数，也不一定有交集
        首先，需要过滤掉已经无效的区间，存在这样一种情况：
        区间集 A：(2, 4)
        区间集 B: (5, 8)
        此时，A 的区间已失效

        :param appeared_sn_dic:
        :param interval:
        :return:
        """
        left, right, include_left, include_right = interval[:4]
        for sn in list(appeared_sn_dic.keys()):
            interval_existed = appeared_sn_dic[sn]
            if interval_existed[1] < left:
                # 已有区间 (2, 4)  新区间 (5, 8)
                del appeared_sn_dic[sn]
                return
            if interval_existed[1] == left:
                if not include_left or not interval_existed[3]:
                    # 已有区间 (2, 5) 或 [5, 5)  新区间 [5, 8)
                    del appeared_sn_dic[sn]
                    return
                # 已有区间 (2, 5] 或 [5, 5]  新区间 [5, 8)
                # 此时产生交集点 5
                right = left
                include_left = include_right = True
                continue

            # 已有区间 (2, 7) 或 (2, 8) 或 (2, 9) 或 (5, 7) 或 (5, 8)  新区间 [5, 8)
            if interval_existed[0] == left and include_left:
                # 处理左端的闭合性
                include_left = interval_existed[2]

            if interval_existed[1] < right:
                # 处理右端  已有区间 (2, 7) 或 (5, 7)   新区间 [5, 8)
                right = interval_existed[1]
                include_right = interval_existed[3]
                continue

            if interval_existed[1] == right and include_right:
                # 处理右端的闭合性
                include_right = interval_existed[3]
        return [left, right, include_left, include_right, 0]

    def intersection(self, *tvs_lis: 'IntervalSet') -> 'IntervalSet':
        """intersection of several interval set.

        :param tvs_lis:
        :return:
        """
        return self.intersection_many(self, *tvs_lis)

    def __and__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        return self.intersection(other)

    def __iand__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        self.__dict__ = self.intersection(other).__dict__
        return self

    def intersection_update(self, *tvs_lis: 'IntervalSet'):
        """intersection of several interval set.

        :param tvs_lis:
        :return:
        """
        self.__dict__ = self.intersection(*tvs_lis).__dict__

    def difference(self, *other_tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """求差集
        对于任一返回集中的区间，满足：属于 self，但不属于 tvs_lis 中的任意区间集


        :param other_tvs_lis:
        :return:
        """
        if not other_tvs_lis:
            return self.copy()
        if not self:
            return self.__class__()
        valid_interval_arrays = self._prune_for_difference(self, other_tvs_lis)
        if not valid_interval_arrays:
            return self.copy()
        valid_interval_arrays.sort()

        new_intervals = []
        i = 0
        for arr in self.interval_arrays:
            new_intervals.extend(self._calc_difference(valid_interval_arrays, arr, i))

        return self.__class__(new_intervals, merge=False)

    @classmethod
    def _prune_for_difference(cls, tvs: 'IntervalSet', tvs_lis: Tuple['IntervalSet'], ) -> List[list]:
        """剪枝，将与 tvs 无交集的区间 从 tvs_lis 中移除，避免无效运算
        先找出 tvs[0][0] tvs[-1][1]
        假设 left_min: -5  right_max: 7
        (f, f), (f, t), (t, f), (t, t)

        对于 左端，任意 arr[1] ＜ left_min 的区间都是无效的，例如 (l, r)，只要 r < -5，注意 r == -5 的有可能产生影响
        可以按 (-5, -5, f, f) 进行靠左二分查找，pos < lo 的都是无效区间？
        但是有可能：..., (-8, -3), (-2, 2), ...
        所以：有可能 pos = lo - 1 也有效。

        同样，对于右端，任何 right_max ＜ arr[0] 的区间都是无效的，按 (7, 7, True, True) 进行靠右二分查找
        但是有可能：..., (3, 6), [7, 10), ... 此时 l == 7 的有可能产生影响
        所以调整为 按 (7, INF, True, True) 进行靠右二分查找，则 pos >= hi 的必定是无效区间.

        有可能 hi - lo == 0, 此时意味着：
        tvs：(-5, 7)
        区间集 B：(-20, -10), (10, 20)
        即：对于B来说，与 [left_max, right_min] 无交集，此时 B 对对求差集无影响，忽略即可。


        :param tvs_lis:
        :return:
        """
        left_min = tvs.interval_arrays[0][0]
        interval_left_min = [left_min, left_min, False, False, 0]
        interval_right_max = [tvs.interval_arrays[-1][1], INF, True, True, 0]
        valid_interval_arrays = []
        sn_max = 0
        for tvs in tvs_lis:
            lo = bisect.bisect_left(tvs.interval_arrays, interval_left_min)
            if lo > 0 and left_min <= tvs.interval_arrays[lo - 1][1]:
                lo -= 1
            hi = bisect.bisect_right(tvs.interval_arrays, interval_right_max)
            if lo == hi:
                continue
            tmp_valid_arrays = tvs.interval_arrays[lo:hi]
            for arr in tmp_valid_arrays:
                arr[4] = sn_max
            valid_interval_arrays += tmp_valid_arrays
            sn_max += 1

        return valid_interval_arrays

    @classmethod
    def _calc_difference(cls, interval_arrays: List[list], cu_arr: list, i: int) -> list:
        """

        :param interval_arrays:
        :param cu_arr:
        :return:
        """
        sub_intervals = []
        left, right, include_left, include_right = cu_arr[:4]
        # 左端相同时，(2, 5) (2, 5] [2, 5) [2, 5] (2, 6), (2, 6], [2, 6), [2, 6], ...
        while i < len(interval_arrays):
            new = interval_arrays[i]
            if new[1] < left:
                # cu: (5, 8)  new: (2, 4)
                # new 在 cu 的左边，cu 肯定不会和 new 产生交集, 继续下一个 new
                i += 1
                continue
            if new[1] == left:
                # cu: (5, 8)  new: (2, 5)
                if include_left:
                    # cu: [5, 8)  new: (2, 5]
                    include_left = not new[3]
                # 后面还可能出现 (3, 5]，(3, 7), 所以要继续
                i += 1
                continue
            if right < new[0]:
                # cu: (5, 8)  new: (10, 12)
                break
            if right == new[0]:
                # cu: (5, 8)  new: (8, 12)
                if not include_right:
                    # cu: (5, 8)  new: (8, 12)
                    break
                # cu: (5, 8]  new: [8, 12) (8, 12)
                # 进行对于相同左端的合并，确保后面不会再出现 [8, 12) [8, 13)，从而避免 8 的闭合性又发生变化
                merged, j = cls._merge_when_same_left(interval_arrays, i)
                include_right = not merged[2]
                if j > i + 1:
                    # 此时代表发生了 merge
                    interval_arrays.insert(j, merged)
                    i = j
                continue

            j = i + 1
            if left < new[0]:
                # cu: (5, 8)  new: (6, x)
                new, j = cls._merge_when_same_left(interval_arrays, i)
                sub_intervals.append([left, new[0], include_left, not new[2], 0])

            if left == new[0]:
                # cu: (5, 8)  new: (5, x)
                new, j = cls._merge_when_same_left(interval_arrays, i)
                if include_left and not new[2]:
                    # cu: [5, 8)  new: (5, x)
                    sub_intervals.append([left, left, True, True, 0])

            if right < new[1]:
                # cu: (5, 8)  new: (x, 9)
                if j == i + 1:
                    return sub_intervals
                # 此时代表发生了 merge
                interval_arrays.insert(j, new)
                i = j
            if new[1] < right:
                # cu: (5, 8)  new: (x, 7)
                left = new[1]
                include_left = not new[3]
                i = max(i + 1, j)
                continue
            if new[1] == right:
                # cu: (5, 8)  new: (x, 8)
                if not include_right or new[3]:
                    # cu: (5, 8)  new: (x, 8) (x, 8]
                    # cu: (5, 8]  new: (x, 8]
                    # 代表 cu 被耗尽，new 后续也无用
                    return sub_intervals
                # cu: (5, 8]  new: (x, 8)
                # 产生孤立点，还需要继续
                left = right
                include_left = True
                i = max(i + 1, j)

        sub_intervals.append([left, right, include_left, include_right, 0])
        return sub_intervals

    @classmethod
    def _merge_when_same_left(cls, interval_arrays: List[list], start: int, ) -> Tuple[list, int]:
        """左端相同时，进行合并
        左端相同时，(2, 5) (2, 5] [2, 5) [2, 5] (2, 6), (2, 6], [2, 6), [2, 6], ...

        :param interval_arrays:
        :param start:
        :return: 合并至极限的区间, 后续待处理的下标
        """
        cu = interval_arrays[start].copy()
        j = start + 1
        while j < len(interval_arrays) and interval_arrays[j][0] == cu[0]:
            new_j = interval_arrays[j]
            # 如果左端点相等
            cu[2] |= new_j[2]
            if cu[1] < new_j[1]:
                # 从 (2, 5) 变成 (2, 6)
                cu[1] = new_j[1]
                cu[3] = new_j[3]
            else:
                # 只调整右端闭合性
                cu[3] |= new_j[3]
            j += 1

        return cu, j

    def __sub__(self, other: 'IntervalSet', ):
        return self.difference(other)

    def __isub__(self, other: 'IntervalSet', ):
        self.__dict__ = self.difference(other).__dict__
        return self

    def difference_update(self, *other_tvs_lis: 'IntervalSet', ):
        self.__dict__ = self.difference(*other_tvs_lis).__dict__

    @classmethod
    def symmetric_difference_many(cls, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """求对称差集
        对于任一返回集中的区间，满足：属于且仅属于 tvs_lis 中单个区间集
        特别说明：三个及以上的多个区间集，一次性进行对称差集运算，与依次进行对称差集运算，是不一样的，结果通常不同。
        例如，symmetric_difference(t1, t2, t3)，与 t1 ^ t2 ^ t3，两者的结果通常不同的。
        后者等于是 symmetric_difference(symmetric_difference(t1, t2), t3)


        :param tvs_lis:
        :return:
        """
        # 过滤出非空区间集
        tvs_lis = [e for e in tvs_lis if e]
        if not tvs_lis or sum(tvs.inf_flag for tvs in tvs_lis) > 1:
            return cls()
        if len(tvs_lis) == 1:
            return tvs_lis[0].copy()
        valid_arrays: List[list] = []
        sn_max = 0
        for tvs in tvs_lis:
            for arr in tvs.interval_arrays:
                arr[4] = sn_max
            valid_arrays.append(tvs.interval_arrays)
            sn_max += 1

        arrays_sorted = sorted(valid_arrays, key=len, reverse=True)
        longest_arr: List[list] = arrays_sorted[0].copy()

        cls.join_many_sorted_arr_into_longest(longest_arr, *arrays_sorted[1:], merge=False)

        new_intervals, value_close, checked_value = [], False, NEG_INF
        cu = longest_arr[0].copy()
        i = 1
        while i < len(longest_arr):
            """总计如下情况：
            cu: (2, 5) 
            一、不相交或者外切
            1. cu.left, cu.right < new.left, new.right  (7, y)
            2. cu.left, cu.right == new.left, new.right (5, y)
            3. new.left, new.right < cu.left, cu.right  (x, 0)  忽略
            4. new.left, new.right == cu.left, cu.right (x, 2)  忽略
            二、左端
            1. new.left < cu.left  (-3, y)
            2. cu.left == new.left (2, y)
            3. cu.left < new.left  (4, y)
            三、右端
            1. new.right < cu.right  (x, 3)  
            2. cu.right == new.right (x, 5)
            3. cu.right < new.right  (x, 7)
            """
            new = longest_arr[i]
            if new[4] == cu[4] or cu[1] < new[0]:
                """
                case: 同一 sn 的两个区间必定不相交，所以下一个出现时，上一个必定属于对称差集结果
                case: cu.right < new.left, 如 cu: (2, 5) new: (6, 10)  new 完全处于 cu 的右侧
                """
                # 或者不相交 cu: (2, 5) new: (6, 10)  new 完全处于 cu 的右侧
                new_intervals.append(cu)
                cu = new.copy()
                i += 1
                continue
            if cu[1] == new[0]:
                # 在 cu 右侧外切  cu: (2, 5) (5, 5) new: (5, y) (5, 5)
                # 需要检查 cu.right 的闭合性
                value_close, checked_value = cls._check_close(longest_arr, cu[1], cu[3] + new[2], i + 1, value_close,
                                                              checked_value)
                if value_close:
                    # 5 是闭合的, cu 变为 (2, y)
                    cu[1] = new[1]
                    cu[3] = new[3]
                    cu[4] = new[4]
                    """下一个区间的可能性：
                    case: (5, z) 此时，(2, 5) 析出，且不需要重复检查 5 的闭合度
                    case: (6, z) 此时，(2, 6) 析出，但需要检查 6 的闭合度
                    case: (y, z) 此时，(2, y) 析出，但需要检查 y 的闭合度
                    case: (y+1, z) 此时，(2, y) 析出，也不需要检查 y 的闭合度
                    """
                else:
                    # 5 不闭合
                    if cu[0] < cu[1]:
                        # (2, 5) 被析出
                        cu[3] = False
                        new_intervals.append(cu)
                    if cu[1] < new[1]:
                        # cu 变为 (5, y) y>5
                        cu = new.copy()
                        cu[2] = False
                        """下一个区间的可能性：
                        case: (5, z) 此时，cu -> (y, z)，不需要重复检查 5 的闭合度
                        case: (6, z) 此时，(5, 6) 析出，不需要重复检查 5 的闭合度, 但需要检查 6 的闭合度
                        case: (y, z) 此时，(y, y) 析出，cu -> (y, z)，需要检查 y 的闭合度
                        case: (y+1, z) 此时，(5, y) 析出，也不需要检查 y 的闭合度
                        """
                    else:
                        # 此时 new 是 (5, 5)，需要重新定位 cu
                        cu, i = cls._lookup_next_cu(longest_arr, i + 1, new[1])
                i += 1
                continue

            # 走到此处时，必定 new.left < cu.right
            if cu[0] < new[0]:
                """cu.left < new.left < cu.right  如 cu: (2, 5) new: (3, y)
                """
                value_close, checked_value = cls._check_close(longest_arr, new[0], 1 + new[2], i + 1, value_close,
                                                              checked_value)
                new_intervals.append([cu[0], new[0], cu[2], value_close, 0])
            elif cu[0] == new[0]:
                """cu.left=new.left  如 cu: (2, 5) new: (2, y)           
                """
                value_close, checked_value = cls._check_close(longest_arr, new[0], cu[2] + new[2], i + 1, value_close,
                                                              checked_value)
                if value_close:
                    # 析出孤立点 2
                    new_intervals.append([cu[0], cu[0], True, True, 0])
            if cu[1] < new[1]:
                """new.left < cu.right < new.right, 如 cu: (2, 5) new: (3, 7)                
                next 有可能是 (3, 8) (4, 7) (5, 7) (6, 9)
                """
                value_close, checked_value = cls._check_close(longest_arr, cu[1], 1 + cu[3], i + 1, value_close,
                                                              checked_value)
                cu = [cu[1], new[1], value_close, new[3], new[4]]
            elif cu[1] == new[1]:
                """new.left < cu.right == new.right, 如 cu: (2, 7) new: (3, 7)  
                """
                value_close, checked_value = cls._check_close(longest_arr, new[1], cu[3] + new[3], i + 1, value_close,
                                                              checked_value)
                if value_close:
                    # cu 变成孤立点，且 sn 设置为 -1，因为相当于改变了 new.right 的闭合性，导致 new 与 下一个区间变的相交
                    cu = [cu[1], cu[1], True, True, -1]
                else:
                    """此时 cu 被耗尽，怎么办？
                    next 有可能是 (3, 8) (4, 5) (4, 12) (5, 6) (5, 9) (7, 7) (7, 11) (8, 12)
                    """
                    cu, i = cls._lookup_next_cu(longest_arr, i + 1, new[1])
            else:
                """new.left < new.right < cu.right, 如 cu: (2, 5) new: (3, 4)                
                next 有可能是 (3, 8) (4, 7) (5, 7) (6, 9)
                """
                value_close, checked_value = cls._check_close(longest_arr, new[1], 1 + new[3], i + 1, value_close,
                                                              checked_value)
                cu = [new[1], cu[1], value_close, cu[3], cu[4]]
            i += 1
        if cu:
            new_intervals.append(cu)
        return cls(new_intervals, merge=False)

    @classmethod
    def _lookup_next_cu(cls, interval_arrays: List[list], start: int, lg_value, ) -> Tuple[list, int]:
        """找出 right > lg_value 的第一个区间

        :param interval_arrays:
        :param start:
        :param lg_value:
        :return: 区间，区间的下标
        """
        cu = []
        while start < len(interval_arrays):
            if lg_value < interval_arrays[start][1]:
                cu = interval_arrays[start].copy()
                if cu[0] <= lg_value:
                    cu[0] = lg_value
                    cu[2] = False
                break
            start += 1
        return cu, start

    @classmethod
    def _check_close(cls, interval_arrays: List[list], to_check_value, close_degree: int, start: int,
                     latest_checked_close: bool, latest_checked_value, ) -> Tuple[bool, Any]:
        """检查左端的闭合度
        左端相同时，(2, 5) (2, 5] [2, 5) [2, 5] (2, 6), (2, 6], [2, 6), [2, 6], ...

        case: [2, 2] [2, 2] (2, 5) (2, 8) 合并后 返回 1[5, 8), i+4, 2
        case: (2, 5) [2, 5] (2, 7) (2, 12) 合并后 返回 1[7, 8), i+4, 1
        case: (2, 5) [2, 5]  合并后 返回 [5, 5], i+2, 1
        case: (2, 5] [2, 5]  合并后 返回 (5, 5), i+2, 1
        case: (2, 2) [2, 5] [2, 5]  合并后 返回 (5, 5), i+3, 1

        :param interval_arrays:
        :param start:
        :return: 合并至极限的单一覆盖区间, 后续待处理的下标, left_close_num
            区间的闭合性不是简单的 boo 值，而是总计闭合度
        """
        if to_check_value == latest_checked_value:
            return latest_checked_close, latest_checked_value
        if close_degree > 1:
            return False, to_check_value
        for j in range(start, len(interval_arrays)):
            # 假定 to_check_value = 5
            new = interval_arrays[j]
            if to_check_value < new[0]:
                # (6, y)
                break
            # (x, y) 且 x<=to_check_value
            if new[0] == to_check_value:
                # (5, y)
                close_degree += new[2]
            elif new[1] == to_check_value:
                # (x, 5)
                close_degree += new[3]
            elif to_check_value < new[1]:
                # (4, 6)
                close_degree += 1
            if close_degree > 1:
                return False, to_check_value
        return close_degree == 1, to_check_value

    def symmetric_difference(self, *other_tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """返回 self 和 other_tvs_lis 一起的对称差集
        等价于 cls.symmetric_difference_many(self, *other_tvs_lis)

        :param other_tvs_lis:
        :return:
        """
        return self.symmetric_difference_many(self, *other_tvs_lis)

    def __xor__(self, other: 'IntervalSet', ):
        return self.symmetric_difference(other)

    def __ixor__(self, other: 'IntervalSet', ):
        self.__dict__ = self.symmetric_difference(other).__dict__
        return self

    def symmetric_difference_update(self, other: 'IntervalSet', ):
        self.__dict__ = self.symmetric_difference(other).__dict__

    @classmethod
    def complementary_many(cls, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """求若干区间集相对于 (-inf, inf) 的补集

        :param tvs_lis:
        :return:
        """
        if not tvs_lis:
            return cls()
        return cls.difference(cls.inf_tvs(), *tvs_lis)

    def complementary(self, ) -> 'IntervalSet':
        """求自身相对于 (-inf, inf) 的补集

        :return:
        """
        self.__dict__ = self.complementary_many(self).__dict__
        return self
