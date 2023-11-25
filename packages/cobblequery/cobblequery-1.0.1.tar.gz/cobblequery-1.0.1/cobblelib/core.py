from . import commands
from . import query_language
from . import utils

class PipelineCommandException(ValueError):
    pass

class Pipeline():
    """ Represents a squence of commands run on entries with its source """
    def __init__(self, representation):
        self.representation = representation
        self._assemble()

    def _assemble(self):
        self.functions = []
        for definition in self.representation:
            CommandCls = commands.COMMANDS.get(definition['function'])
            if not CommandCls:
                raise ValueError('Invalid function "{}"'.format(definition['function']))
            command_kwargs = dict(definition.get('kwargs', {}))
            if getattr(CommandCls, 'accepts_sub_commands', False):
                command_kwargs['inner_pipeline'] = self.__class__(definition['inner_pipeline'])
            try:
                configured_command = CommandCls(
                    *definition['args'],
                    **command_kwargs,
                )
            except Exception as e:
                message = 'Error trying to initialize function={} with args={}, kwargs={}, error={}({})'.format(
                    definition['function'],
                    str(definition.get('args', [])),
                    str(command_kwargs),
                    str(e.__class__.__name__),
                    str(e),
                )
                raise PipelineCommandException(message)

            self.functions.append(configured_command)
            if hasattr(configured_command, 'verify_arguments'):
                configured_command.verify_arguments()



    def run(self):
        generator = self.functions[0]
        processors = self.functions[1:]

        previous_iterator = generator.generate()
        for function in processors:
            previous_iterator = function.stream(previous_iterator)

        for item in previous_iterator:
            yield item

def make_pipeline(*sources):
    # TODO: Probably do some stuff around generator vs processor verification
    # Maybe distinguish between sub-pipelines? 
    aggregate_sources = []
    for source in sources:
        aggregate_sources.extend(source)
    return Pipeline(aggregate_sources)
