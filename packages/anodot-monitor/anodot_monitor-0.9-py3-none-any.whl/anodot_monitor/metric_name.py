import io


class MetricName:

    def __init__(self):
        self._dictionary = {}

    def __with_property(self, property_name, property_value):
        self._dictionary.setdefault(property_name, property_value)

    def properties(self):
        return self._dictionary.items()

    @staticmethod
    def builder(what):
        return MetricNameBuilder(what)

    def as_string(self):
        if not self._dictionary.keys():
            return ""

        keys = self._dictionary.keys()
        out = io.StringIO()

        for key in keys:
            out.write(key)
            out.write("=")
            out.write(self._dictionary[key])
            out.write(".")

        result = out.getvalue()
        out.close()

        return result[:-1]


class MetricNameBuilder:

    def __init__(self, what):
        self._metric_name = MetricName()
        self.with_property("what", what)

    def with_property(self, property_name, property_value):
        if property_name and property_value:
            self._metric_name._MetricName__with_property(property_name=property_name, property_value=property_value)
        # else:
        #     raise ValueError('MetricNameBuilder.with_property() received null', property_name, property_value)
        return self

    def build(self):
        return self._metric_name
