from . import query_language as QL
from . import commands

import os
import sys
import time
import json
import subprocess
import tempfile

DEFAULT_GENERATOR = {
    'function': 'from',
    'args': '-',
}

def interactive_edit(content, verify=None):
    original = content
    editor = os.environ.get('EDITOR', 'vi')
    with tempfile.NamedTemporaryFile(mode='w') as tmp_file:
        tmp_file.write(content)
        tmp_file.seek(0)
        tmp_file.flush()
        while True:
            subprocess.run([editor, tmp_file.name])
            new_content = open(tmp_file.name, 'r').read()
            if verify is not None:
                try:
                    verify(new_content)
                    break
                except Exception as e:
                    print('Failed, error: ' + str(e))
                    input('Press Enter to try again')
                    continue
            break
    return new_content

def parse_shell_syntax(query_text):
    return QL.parse_pipeline(query_text)

def execute_pipeline(pipeline):
    for entry in pipeline.run():
        print(json.dumps(entry))

