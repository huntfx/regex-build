__version__ = '1.0.0'


class RegexBuild(object):
    """Build extremely complex one-line regex strings.
    This can be used as a context manager, or in-line as part of other instances.

    Example:
        >>> original_regex = r'.*\\AppData\\Roaming\\(Microsoft|NVIDIA|Adobe\\.*(CT Font |FontFeature|Asset|Native)Cache)\\'

        >>> with RegexBuild(r'.*\\AppData\\Roaming\\') as build_regex:
        ...     build_regex('Microsoft', 'NVIDIA',
        ...         RegexBuild(r'Adobe\\.*')('CT Font ', 'FontFeature', 'Asset', 'Native')('Cache'),
        ...     )(r'\\')

        >>> original_regex == str(build_regex)
        True
    """

    def __init__(self, *text, **kwargs):
        """Setup regex matches.

        Parameters:
            text (str or RegexBuild): Individual regex matches.
            exit (str or RegexBuild): Add regex after all the matches.
                An common example is RegexBuild('(?i)', exit='$') for
                case insensitive matching.
        """
        self.parent = kwargs.get('_parent')
        self.data = list(text)
        self.exit = kwargs.get('exit', None)
        self.count = len(self.data) - 1

        # Add data to parent
        if self.parent is not None:
            try:
                self.parent.data[kwargs.get('_count', 0)].append(self.data)
            except IndexError:
                self.parent.data.append(self.data)

        # Add exit data
        if self.exit is not None:
            self.data.append([])
            self.data.append(self.exit)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.data)

    def __call__(self, *text, **kwargs):
        """Create a new match group.
        This can work inline or as a context manager.

        Example:
            #>>> RegexBuild('a')('b', 'c')
            'a(b|c)'

            #>>> with RegexBuild('a') as build:
            ...     build('b', 'c')
            #>>> build
            'a(b|c)'
        """
        self.count += 1

        # Force the exit regex to be placed at the end of the data
        if self.exit is not None:
            data = self.data.pop(-1)
            while True:
                try:
                    self.data[self.count]
                except IndexError:
                    self.data.append([])
                else:
                    break
            self.data.append(data)

        return self.__class__(*text, _parent=self, _count=self.count, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if any(args):
            return False

    def __str__(self, data=None):
        """Convert the data to valid regex."""
        # If the parent exists, then get the full path
        # Without this, RegexBuild('a')('b')('c') will only return 'c'
        if self.parent is not None:
            return str(self.parent)

        if data is None:
            data = self.data

        # Split the data into 3 parts
        prefix = []
        body = []
        suffix = []
        current = prefix
        for offset, item in enumerate(data):
            if isinstance(item, list):
                body.append(self.__str__(item))
                current = suffix
            else:
                current.append(item)

        if prefix:
            if len(prefix) > 1:
                prefix = '({})'.format('|'.join(map(str, prefix)))
            else:
                prefix = prefix[0]
        else:
            prefix = ''

        if suffix:
            if len(suffix) > 1:
                suffix = '({})'.format('|'.join(map(str, suffix)))
            else:
                suffix = suffix[0]
        else:
            suffix = ''

        if body:
            if len(body) == 1:
                return '{}{}{}'.format(prefix, body[0], suffix)
            return '{}({}){}'.format(prefix, '|'.join(map(str, body)), suffix)
        return prefix
