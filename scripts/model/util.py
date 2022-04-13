class LinearInterpolation:
    """
    Interpolate values in between given target values.
    For example, if the targets are 0% in 2020, 5% in 2030, 15% in 2040 and 30% in 2050 then
    they ar represented as a dictionary {2020: 0, 2030:5, 2040: 15, 2050: 30}
    and the method get_value(2034) would return 9.
    """
    def __init__(self, targets, factor=1):
        """
        :param targets: dictionary of target values for given keys
        :param factor: for example, use factor=0.01 if the target values are given as percentages
        """
        self._values = {}
        keys = list(targets.keys())
        keys.sort()
        key_first = keys[0]
        key_last = keys[-1]
        index = 1
        key_low = key_first
        key_high = keys[1]
        value_low = targets.get(key_low)
        value_high = targets.get(key_high)
        for key in range(key_first, key_last + 1):
            if key > key_high:
                index += 1
                key_low = key_high
                key_high = keys[index]
                value_low = value_high
                value_high = targets.get(key_high)
            value = (key - key_low) / (key_high - key_low) * (value_high - value_low) + value_low
            self._values[key] = value * factor

    def get_value(self, key):
        return self._values.get(key)


class DemandGrowth:
    def __init__(self, baseline, growth_marks_pct):
        """
        :param baseline: demand value for the first key
        :param growth_marks_pct: percentage growth for given years
            (last value is ignored, it used just to indicate the last key)
        """
        self._values = {}
        keys = list(growth_marks_pct.keys())
        keys.sort()
        key_first = keys[0]
        key_last = keys[-1]
        value = baseline
        growth = 0
        for key in range(key_first, key_last + 1):
            if key in growth_marks_pct:
                growth = growth_marks_pct.get(key) / 100
            value *= (1 + growth)
            self._values[key] = value

    def get_value(self, key):
        return self._values.get(key)
