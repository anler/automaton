# -*- coding: utf-8 -*-

ENCODING = 'utf-8'


def encode(unicode_str):
    return unicode_str.encode(ENCODING)


class AbstractRegex(object):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return encode(self.__unicode__())

    def __repr__(self):
        return "R{}".format(hash(self))

    def __contains__(self, other):
        return self == other

    def __eq__(self, other):
        return self.get_value() == other.get_value()
    __cmp__ = __eq__

    def __hash__(self):
        return hash(self.reduce().__unicode__())

    def __unicode__(self):
        return u"<unknown>"

    def __nonzero__(self):
        return True

    def _alphabet(self):
        return []

    def get_value(self):
        if isinstance(self.value, AbstractRegex):
            return self.value.get_value()
        return self.value

    @property
    def accepts_lambda(self):
        return False

    def alphabet(self):
        return set(self._alphabet())

    def reduce(self):
        return self


class AbstractBinaryRegex(AbstractRegex):
    symbol = u""

    def __init__(self, left, right):
        super(AbstractBinaryRegex, self).__init__()
        self.left, self.right = left, right

    def __unicode__(self):
        return u"({} {} {})".format(self.left, self.symbol, self.right)

    def __contains__(self, other):
        return other in self.left or other in self.right

    def __eq__(self, other):
        if type(other) is type(self):
            return self.left == other.left and self.right == other.right
        return False

    def _alphabet(self):
        return [v for v in self.left._alphabet()] + [v for v in self.right._alphabet()]


class Null(AbstractRegex):
    symbol = u"∅"

    def __nonzero__(self):
        return False

    def __unicode__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()

    def derive(self, base):
        return Null()


class Lambda(Null):
    symbol = u"λ"


class Constant(AbstractRegex):
    def derive(self, base):
        return Lambda() if self.value == base else Null()

    def __unicode__(self):
        return unicode(self.value)

    def _alphabet(self):
        return [self.value]


class Choice(AbstractBinaryRegex):
    symbol = u"⋃"

    def derive(self, base):
        left = self.left.derive(base)
        right = self.right.derive(base)

        return Choice(left, right)

    def reduce(self):
        left = self.left.reduce()
        right = self.right.reduce()

        # If any of the components is ∅ or λ the result is the other component
        if right and left:
            # Reduce expressions with common factors
            if right in left:
                result = left
            elif left in right:
                result = right
            else:
                result = Choice(left, right)
        elif right:
            result = right
        elif left:
            result = left
        else:
            result = Lambda() if type(left) is Lambda or type(right) is Lambda else Null()

        return result


class Concat(AbstractBinaryRegex):
    symbol = u"∘"

    def derive(self, base):
        left = Concat(self.left.derive(base), self.right)
        right = Concat(self.delta(self.left), self.right.derive(base))

        return Choice(left, right)

    def delta(self, value):
        return Lambda() if value.accepts_lambda else Null()

    def reduce(self):
        left = self.left.reduce()
        right = self.right.reduce()

        # If any of the components is ∅ or λ the result is the other component
        if right and left:
            result = Concat(left, right)
        elif type(left) is Lambda:
            result = right
        elif type(right) is Lambda:
            result = left
        else:
            result = Null()

        return result


class Repeat(AbstractRegex):
    symbol = u"∗"

    def __unicode__(self):
        return u"{}{}".format(self.value, self.symbol)

    def _alphabet(self):
        return self.value._alphabet()

    @property
    def accepts_lambda(self):
        return True

    def derive(self, base):
        left = self.value.derive(base)
        right = Repeat(self.value)

        return Concat(left, right)
