"""
Ghizmo main library.
"""


import logging as log
import sys
import re
import json
import yaml
import inspect
import getpass
from collections import namedtuple
<<<<<<<-ours
from collections import OrderedDict
from functools import lru_cache
=======
from functools32 import lru_cache  # functools32 pip
>>>>>>>-theirs
import github3  # github3.py pip
from github3.null import NullObject

from ghizmo import configs
from ghizmo import commands

__author__ = 'jlevy'

def read_login_info(username=None):
  if not username:
    username = eval(input("GitHub username: "))
  return (username, getpass.getpass())


def login(username=None):
  token = configs.get_access_token()
  if token:
    log.info("Using access token authentication")
    return github3.login(token=token)
  else:
    username = username or configs.get_username()
    return github3.login(*read_login_info(username=username))


def format_to_string(obj, format=None):
  if not format:
    format = "json"

  if isinstance(obj, NullObject):
    raise ValueError("Command returned null type (invalid input?): %s" % repr(obj))

  # Heuristic to convert github3 objects to serializable form.
  if hasattr(obj, "as_dict"):
    obj = obj.as_dict()

  if format == "json":
    return json.dumps(obj, sort_keys=True, indent=2) + "\n"
  elif format == "yaml":
    return yaml.safe_dump(obj, default_style='"')
  else:
    raise AssertionError("Invalid format: %s" % format)


def print_formatter(format=None):
  def printer(obj):
    print(format_to_string(obj, format), end="")
    sys.stdout.flush()

  return printer


# All data used by the run of a command.
Config = namedtuple("Config", "github repo formatter")


def _to_dash(name):
  return name.replace("_", "-")


def _to_underscore(name):
  return name.replace("-", "_")


def all_command_functions():
  def is_public_func(f):
    return inspect.isfunction(f) and not f.__name__.startswith("_")

<<<<<<< ours
  # If there is a ghizmo_commands.py file in the current directory, use it too.
  if os.path.exists("ghizmo_commands.py"):
    sys.path.insert(1, '.')  # This is needed only on some installations.
    modules.append(importlib.import_module("ghizmo_commands"))

  log.info("Imported command modules: %s", modules)

  func_map = {}
  for module in modules:
    for (name, func) in inspect.getmembers(module, predicate=_is_public_func):
      if name in func_map:
        raise ValueError("Duplicate function name for command: %s" % name)
      func_map[name] = func
  # Sort items first by module, then by name.
  return OrderedDict(sorted(list(func_map.items()), key=lambda name_func: (name_func[1].__module__, name_func[0])))
=======
  return inspect.getmembers(commands, predicate=is_public_func)
>>>>>>>-theirs


@lru_cache()
def command_directory(use_dashes=True):
  def doc_for_function(func):
    doc = func.__doc__ and re.sub("\s+", " ", func.__doc__).strip()
    if not doc:
      doc = "(no pydoc)"
    return doc

  transform = _to_dash if use_dashes else lambda x: x
<<<<<<<-ours
  return [(func.__module__, transform(name), doc_for_function(func)) for (name, func) in
          all_command_functions().items()]
=======
  return [(transform(name), doc_for_function(func)) for (name, func) in all_command_functions()]
>>>>>>>-theirs


@lru_cache()
def list_commands(use_dashes=True):
  return [command for (command, doc) in command_directory(use_dashes=use_dashes)]


def get_command_func(command):
  command = _to_underscore(command)
  if not command in list_commands(use_dashes=False):
    raise ValueError("invalid command: %s" % command)
  return getattr(commands, command)


def run_command(command, config, args):
  command_func = get_command_func(command)
  log.info("Command '%s' (%s)", command, command_func)
  log.info("Config: %s", config)
  log.info("Args: %s", args)
  # This executes the command step by step, either just to display results, or to display progress
  # on an action with side effects.
<<<<<<< ours
  iterable_result = command_func(config, args)
  if iterable_result:
    for result in iterable_result:
      config.formatter(result)

# TODO:
# Control pretty-printing, using one object per line by default, but with --pretty option to print nicely
# Proper reading of JSON streams (as opposed to line-by-line), for use in piping
=======
  for result in command_func(config, args):
    config.formatter(result)

# TODO:
# Automagic loading of ghizmo_commands.py files from current directory.
# Proper streaming of JSON items (as opposed to line-by-line), for use in piping.
>>>>>>>-theirs
# Prettier SIGPIPE handling
