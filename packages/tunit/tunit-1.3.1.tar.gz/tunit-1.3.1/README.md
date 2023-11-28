# TUnit
---
Time unit types. For transparency, safety and readability.

## Examples:

```python
from tunit import Days, Hours, Minutes, Seconds, Milliseconds

# Type annotations:
def timestamp() -> Milliseconds:
    # Time unit conversions:
    return Milliseconds(Seconds(1))  # 1_000 ms

# Converting to smaller units:
assert Hours(Days(1)) == Hours(24) == 24

# Converting to bigger units:
assert Minutes(Seconds(65)) == Minutes(1) == 1

# Converting floats to time units:
assert Seconds(Minutes(0.5)) == Seconds(0) == 0  # Time units hold integers!
assert Seconds.fromRawUnit(Minutes, 0.5) == Seconds(500) == 500  # Better approach when fractions matter!

# Converting time units to floats:
assert float(Seconds(Milliseconds(1_500))) == 1.0  # Loses precision!
assert Milliseconds(1_500).toRawUnit(Seconds) == 1.5  # Converts to float representing different time unit with precision.
```

## License
MIT
