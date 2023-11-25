# shell-complete-py
python package to generate shell-completion for your CLI

> Warning: This project is in the earliest phase possible

## Usage

Either import and use the `generate(parser: ArgumentParser)` function or directly the `ActionGenerate`

```python
from argparse import ArgumentParser
from shell_complete.argparse import ActionGenerate  # note: currently not available

parser = ArgumentParser()
...
parser.add_argument('--completion', action=ActionGenerate,
                    help="Generate a bash-completion-script")
```

You can also execute the module itself

```bash
python3 -m shell_complete [args...]
```

Or run the console-script

```bash
shell-complete [args...]
```
