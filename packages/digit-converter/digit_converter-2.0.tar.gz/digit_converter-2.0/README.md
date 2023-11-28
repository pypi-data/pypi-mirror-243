Introduction
=============

**Abstract**

A cool tool for digits converting.

It could be applied in Genetic Algorithm to encode the solutions.

**Keywords** Converter, Digits

## Content

### Classes

    BaseConverter: .tonumber(lst), .tolist(num, L)
    DigitConverter
    BinaryConverter: subclass of DigitConverter
    IntegerConverter: only convert integer
    IntervalConverter: subclass of IntegerConverter, converts a number in an interval to an integer what is the index of the number then applies IntegerConverter

### Objects

    colorConverter: instance of BinaryConverter, transform a number (0~255) to a 8-length list of 0-1s
    unitIntervalConverter: instance of IntervalConverter, transform a number in interval [0,1] to list of 0-1s

## Grammar

### import

`import digit_converter`



### Basic usage

#### Codes

```python
    print(f'color-converter: {colorConverter.tonumber([1,0,1,0,1,1,1,0])}<->{colorConverter.tolist(174)}')

    c = BinaryConverter(exponent=3)
    d = c.tolist(12.223, L=8)
    print(f'binary-converter: {d}<->{c.tonumber(d)}={c.pretty(d)}')

    c = IntervalConverter(lb=0, ub=10)
    d = c.tolist(2.4, L=8)
    print(f'[{c.lb},{c.ub}]-converter: {d}<->{c(d)} -> {c.pretty(d)}-th number')

    c = DigitConverter(base=16)
    d = c.tolist(2.4, L=8)
    print(f'16-converter: {d}<->{c(d)}={c.pretty(d)}')
```

 *OUTPUT:*

    color-converter: 174<->[1, 0, 1, 0, 1, 1, 1, 0]
    binary-converter: [1, 1, 0, 0, 0, 0, 1, 1]<->12.1875=2^{3} + 2^{2} + 2^{-3} + 2^{-4}
    [0,10]-converter: [0, 0, 1, 1, 1, 1, 0, 1]<->2.3828125 -> 2^{5} + 2^{4} + 2^{3} + 2^{2} + 2^{0}-th number
    16-converter: [0, 2, 6, 6, 6, 6, 6, 6]<->2.399999976158142=2*16^0 + 6*16^-1 + 6*16^-2 + 6*16^-3 + 6*16^-4 + 6*16^-5 + 6*16^-6