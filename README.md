# regex-build
Build complex one-line regex strings.

The preferred way of building is using a one line chain of calls on the `RegexBuild` instance.
For anything more complex, using it as a context manager will allow for multiple calls to be made on the same instance.

Instances of `RegexBuild` may be used interchangeably with strings, allowing for multiple nested instances to be used.

```python
>>> original_regex = r'.*\\Roaming\\(Microsoft|NVIDIA|Adobe\\.*(Asset|Native)Cache)\\'

# Complex example
>>> with RegexBuild(r'.*\\Roaming\\') as build_regex:
...     build_regex(
...         'Microsoft', 'NVIDIA', RegexBuild(r'Adobe\\.*')('Asset', 'Native')('Cache'),
...     )(r'\\')

>>> original_regex == str(build_regex)
True

# Different ways to build the same regex
>>> with RegexBuild('(?i)', exit='$') as case_insensitive:
...     # As one line
...     case_insensitive('prefix1_')('word1', 'word2')('_suffix1')
...
...     # As context managers
...     with case_insensitive('prefix2_') as prefix:
...         with prefix('word2', 'word3') as words:
...             words('_suffix2')
...
...     # As context manager using the "end" parameter
...     with case_insensitive('prefix3_', end='_suffix3') as prefix:
...         prefix('word4')
...         prefix('word5')
...

>>> case_insensitive
'(?i)(prefix1_(word1|word2)_suffix1|prefix2_(word3|word4)_suffix2|prefix3_(word5|word6)_suffix3)$'
```
