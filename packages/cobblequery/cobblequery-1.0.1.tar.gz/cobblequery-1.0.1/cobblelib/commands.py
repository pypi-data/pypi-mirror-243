from . import parsers
from . import utils
from . import query_language
from . import aggregators
from .extractor import Extractor

from contextlib import contextmanager
from collections import namedtuple
import re
import os
import sys
import json
import copy

class SkipError(ValueError):
    pass

class GenerateSeries():
    is_generator = True
    
    def __init__(self, end=20, start=0, subquery=None):
        self.start = int(start)
        self.end = int(end)

    def generate(self):
        for i in range(self.start, self.end):
            yield {'i': i}

class FileLoader():
    is_generator = True
    PARSERS = {
        None: parsers.parse_text,
        'csv': parsers.parse_csv,
        'json_rows': parsers.json_rows,
    }
    
    def __init__(self, path, loader=None, parser=None):
        self.path = path
        self.loader = loader
        self.parser_name = parser

    @contextmanager
    def load(self, *args, **kwargs):
        if self.path == '-':
            f = sys.stdin
            should_close = False
        else:
            f = open(self.path, 'r')
            should_close = True
        try:
            yield f
        finally:
            if should_close:
                f.close()

    def sniff(self, text):
        if text.startswith('{'):
            try:
                loaded = json.loads(text)
                return 'json_rows'
            except Exception as e:
                pass
        if ',' in text:
            return 'csv'
        return None

    def generate(self):
        with self.load() as source:
            if self.parser_name is None:
                source = utils.StreamPeek(source)
                self.parser_name = self.sniff(source.peek(lines=1))
            self.parser = self.PARSERS.get(self.parser_name)

            for entry in self.parser(source):
                yield entry

class PyExecFilter():
    def __init__(self, *args):
        self.executors = []
        for filter_clause in args:
            self.executors.append(utils.py_executor(filter_clause))

    def stream(self, source):
        for entry in source:
            context = {'value': utils.DotWrapper(entry)}
            expression_results = []
            for e in self.executors:
                expression_results.append(e(context)[1])
            if all(expression_results):
                yield entry

class SearchFilter():
    def __init__(self, *args, **kwargs):
        self.filters = {}
        for key, value in kwargs.items():
            self.filters[key] = {'extractor': Extractor(key), 'static_value': value}

    def stream(self, source):
        for entry in source:
            for name, filter_conf in self.filters.items():
                filter_static_value = filter_conf.get('static_value')
                value = filter_conf['extractor'](entry)
                if filter_static_value is not None and value != filter_static_value:
                    continue
                else:
                    yield entry

class SliceFilter():
    def __init__(self, *args):
        if len(args) == 1:
            start = 0
            end = int(args[0])
        elif len(args) > 1:
            start = int(args[0])
            end = int(args[1])
        if end < 1:
            end = None
        if start < 0:
            start = 0
        self.end = end
        self.start = start

    def stream(self, source):
        for i, entry in enumerate(source):
            if self.start is not None and i < self.start:
                continue
            if self.end is not None and i >= self.end:
                continue
            yield entry

class PyExecSet():
    def __init__(self, **kwargs):
        self.executors = {}
        for target, expression in kwargs.items():
            self.executors[target] = utils.py_executor(expression)

    def stream(self, source):
        for entry in source:
            context = {'value': utils.DotWrapper(entry)}
            for target, executor in self.executors.items():
                result = executor(context)[1]
                entry[target] = result
            yield entry

class Aggregate():
    def __init__(self, *args, **kwargs):
        if 'by' in kwargs:
            self.by_fields = kwargs.pop('by').split(',')
        elif args:
            args.remove('by')
            self.by_fields = args
        else:
            self.by_fields = None

        self.by_extractors = None
        if self.by_fields:
            self.by_extractors = [Extractor(f) for f in self.by_fields]
        self.aggregation_funcs = self.parse_aggregations(kwargs)

    def parse_aggregations(self, specs):
        aggregations = {}
        for target, operation in specs.items():
            agg_name, source = query_language.parse_function_syntax(operation)
            agg_func = aggregators.AGG_FUNCTIONS.get(agg_name, None)
            if agg_func is  None:
                raise ValueError('Aggregation function "{}" does not exist'.format(agg_name))
            aggregations[target] = {
                'extractor': Extractor(source).extract,
                'source': source,
                'func': agg_func,
            }
        return aggregations
        
    def get_by_value(self, entry):
        if self.by_fields is None:
            return None
        if len(self.by_fields) == 1:
            return self.by_extractors[0](entry)
        return tuple(extractor(entry) in self.by_extractors)

    def get_key_pairs(self, key_values):
        if self.by_fields is None:
            return {}
        if len(self.by_fields) == 1:
            return {self.by_fields[0]: key_values}
        else:
            return dict(zip(self.by_fields, key_values))

    def create_aggregations(self):
        aggs_for_key = []
        for target, agg in self.aggregation_funcs.items():
            aggs_for_key.append({
                'extractor': agg['extractor'],
                'aggregator': agg['func'](),
                'target': target,
            })
        return aggs_for_key

    def stream(self, source):
        aggs_by_key = {}
        for entry in source:
            key = self.get_by_value(entry)
            aggs_for_key = aggs_by_key.get(key)
            if key not in aggs_by_key:
                aggs_for_key = self.create_aggregations()
                aggs_by_key[key] = aggs_for_key

            for agg in aggs_for_key:
                source_value = agg['extractor'](entry)
                agg['aggregator'].handle(source_value)

        for key_value, aggs in aggs_by_key.items():
            key_pairs = self.get_key_pairs(key_value)
            agg_results = {agg['target']: agg['aggregator'].result() for agg in aggs}

            record = {}
            record.update(key_pairs)
            record.update(agg_results)
            yield record

class UnpackField():
    def __init__(self, selector):
        self.selector = selector

    def stream(self, source):
        for entry in source:
            s = utils.PowerSelector(self.selector)
            value = s.get(entry, default=None)
            if value is None or type(value) not in (list, tuple):
                yield entry
            for i in value:
                new_entry = copy.deepcopy(entry)
                new_entry = s.set(new_entry, i)
                yield new_entry

class JoinPipeline():
    """
        type=(left|right|inner|outer)
            left :: All values in the main data set with added values from the joined dataset where available
            right :: All vluaes in the joined dataset with values from the main set where available
            inner :: Entries representing matches between main and joined datasets; omitting orphan values from main and joined dataset
            outer :: At least one entry from source and target dataset joined when matching
        target=(first|last|agg|agg_str|expand)
            first :: Joined dataset will contain the properties from the first matched entry by key
            last :: Joined dataset will contain the properties from the last matched entry by key
            agg :: Joined dataset will contain an array containing the values from each entry from joined dataset by key
            agg_str :: Joined dataset will contain a string combining the values from each entry from joined dataset by key
            expand :: Joined dataset will contain multiple (cloned) records for each target match with the variance being the selection
        select=Dot separated path String to target fields
            String value representing the json dotted path target to the value to add. If optional all fields will be added
    """
    accepts_sub_commands = True

    JOIN_TYPES = ('left', 'inner', 'outer')
    TARGETS = ('expand', 'first', 'last', 'agg', 'agg_str')

    UNSET = type('Unique value representing unset')
    DEFAULT_AGG_STR_DELIMITER = os.environ.get('AGG_STR_DELIMITER', ',')

    def __init__(self, *keys, type='left', target='expand', select=None, inner_pipeline=None, agg_str_delimiter=DEFAULT_AGG_STR_DELIMITER):
        assert type in self.JOIN_TYPES, "Join type must be one of: " + str(self.JOIN_TYPES)
        assert target in self.TARGETS, "Target must be one of: " + str(self.TARGETS)
        assert keys is not None and keys != '', "You must specify at least one Key"
        self.target = target
        self.inner_pipeline = inner_pipeline
        self.join_keys = self._parse_join_keys(keys)
        self.join_extractors = [(Extractor(s), Extractor(t)) for (s, t) in self.join_keys]
        self.selectors = self._parse_selectors(select)

        self.agg_str_delimiter = agg_str_delimiter

        self.join_type = type
        self.track_used = self.join_type == 'outer'

    def _parse_selectors(self, select):
        if select is None:
            return None
        if type(select) == str:
            select = select.split(',')
        assert type(select) in (tuple, list), 'Join selector must be a string or list'
        return {s: Extractor(s) for s in select}

    def _recompose_join_key_values(self, join_key, target=False):
        if target:
            i = 1
        else:
            i = 0
        join_labels = [k[i] for k  in self.join_keys]
        return dict(zip(join_labels,join_key))

    def _parse_join_keys(self, keys):
        selector_pairs = []
        for key in keys:
            if type(key) in (list, tuple):
                source_selector, target_selector = key
            else:
                parts = key.split(':')
                if len(parts) == 1:
                    source_selector = parts[0]
                    target_selector = parts[0]
                else:
                    source_selector = parts[0]
                    target_selector = parts[1]
            selector_pairs.append((source_selector, target_selector))
        return selector_pairs

    def get_join_key(self, entry, target=False):
        if target:
            extractor_index = 1
        else:
            extractor_index = 0 
        if self.join_keys is None:
            return None
        if len(self.join_keys) == 1:
            return self.join_extractors[0][extractor_index](entry)
        return tuple(e[extractor_index](entry) for e in self.join_extractors)

    def get_join_selection(self, entry):
        if self.selectors is None:
            return entry

        return {
            field_name: extractor(entry)
            for field_name, extractor in self.selectors.items()
        }

    def _merge_selection(self, existing, new):
        assert self.target in ('agg', 'agg_str')
        key_hits = set()
        result = {}
        for field, existing_value in existing.items():
            key_hits.add(field)
            new_value = new.get(field, self.UNSET)
            if new_value != self.UNSET:
                if self.target == 'agg':
                    result[field] = [existing_value, new_value]
                elif self.target == 'agg_str': 
                    result[field] = str(existing_value) + self.agg_str_delimiter + str(new_value)

        for field, value in new.items():
            if field not in key_hits:
                result[key] = value
        return result

    def prepare_substream(self):
        self._index = {} # whoa, this is going to get big fast
        self._used = set()

        for entry in self.inner_pipeline.run():
            join_key = self.get_join_key(entry, target=True)
            if self.target == 'first' and join_key in self._index:
                continue
                
            target_selection = self.get_join_selection(entry)
            if self.target in ('expand', 'agg', 'agg_str'):
                # We need to get any existing value to merge/append
                existing_value = self._index.get(join_key, self.UNSET)

                # Handle the "expand" mode by grouping up the whole target into an array 
                if existing_value == self.UNSET and self.target == 'expand':
                    target_selection = [target_selection]
                elif self.target == 'expand':
                    # Just add another entry
                    existing_value.append(target_selection)
                    target_selection = existing_value
                elif existing_value != self.UNSET and self.target in ('agg', 'agg_str'):
                    target_selection = self._merge_selection(existing_value, target_selection)

            self._index[join_key] = target_selection

    def stream(self, source):
        self.prepare_substream()
        for entry in source:
            join_key = self.get_join_key(entry)
            match = self._index.get(join_key, None)
            if self.join_type == 'inner' and not match:
                continue
            if match:
                # Track seen join keys
                if self.join_type == 'outer':
                    self._used.add(join_key)

                # For expansion case we need to yield multiple entries for each matching target simulating a "normal" SQL join
                if self.target == 'expand':
                    for match_entity in match:
                        clone = copy.deepcopy(entry)
                        clone.update(match_entity)
                        yield clone
                else:
                    entry.update(match)
                    yield entry
            else:
                yield entry


        if self.join_type == 'outer':
            for key, entry in self._index.items():
                if key not in self._used:
                    recomposed_key_value = self._recompose_join_key_values(key, target=True)
                    if self.target == 'expand':
                        for i in entry:
                            i.update(recomposed_key_value)
                            yield i
                    else:
                        entry.update(recomposed_key_value)
                        yield entry

class Table():
    def __init__(self, *args):
        self.extractors = [(f, Extractor(f)) for f in args]

    def stream(self, source):
        for entry in source:
            new_entry = {f: e(entry) for f, e in self.extractors}
            yield new_entry 

class RenameFields():
    def __init__(self, **kwargs):
        self.field_pairs = []
        for target, source in kwargs.items():
            target_selector = utils.PowerSelector(target)
            source_selector = utils.PowerSelector(source)
            self.field_pairs.append((source_selector, target_selector))

    def stream(self, source):
        empty = utils.PowerSelector.EMPTY
        for entry in source:
            for source_selector, target_selector in self.field_pairs:
                field_value = source_selector.get(entry, default=empty)
                if field_value == empty:
                    continue
                target_selector.set(entry, field_value)
                source_selector.set(entry, empty)
            yield entry

class AppendPipeline():
    accepts_sub_commands = True

    def __init__(self, inner_pipeline=None):
        self.inner_pipeline = inner_pipeline

    def stream(self, source):
        for entry in source:
            yield entry

        for entry in self.inner_pipeline.run():
            yield entry

COMMANDS = {
    'from': FileLoader,
    'range': GenerateSeries,
    'append': AppendPipeline,
    'where': PyExecFilter,
    'search': SearchFilter,
    'slice': SliceFilter,
    'set': PyExecSet,
    'eval': PyExecSet,          # Alias
    'aggregate': Aggregate,
    'stats': Aggregate,         # Alias
    'agg': Aggregate,         # Alias
    'join': JoinPipeline,
    'unpack': UnpackField,
    'rename': RenameFields,
    'table': Table,
}
