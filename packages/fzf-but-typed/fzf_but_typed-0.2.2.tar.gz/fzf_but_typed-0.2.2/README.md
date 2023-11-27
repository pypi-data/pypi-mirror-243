# Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [API Overview and Examples](#api-overview-and-examples)
  * [Main Content](#main-content)
  * [`fzf` Free Function](#fzf-free-function)
  * [`fzf_iter` Free Function](#fzf_iter-free-function)
  * [`FuzzyFinderBuilder` class](#fuzzyfinderbuilder-class)
  * [Going Nuts with All These Features](#going-nuts-with-all-these-features)
- [`fzf` Version Compatibility](#fzf-version-compatibility)


# Introduction

`fzf_but_typed` is a python wrapper for [fzf](https://github.com/junegunn/fzf/).  
It's different from other existing wrappers because it wraps all of fzf's CLI 
options and their possible values into neat types, so that you can leverage 
your IDE/LSP/type-checker as a means of correctly using fzf, without having to 
lookup usage details in the manpages. Furthermore, being able to use your 
editor's autocompletion features instead of having to manually type CLI 
arguments is much more comfortable.


# Installation

With pip:

    pip install fzf_but_typed

With poetry:
    
    poetry add fzf_but_typed


# API Overview and Examples

## Main Content

The following items are the bread and butter of this package:
-  `fzf` (free function)
-  `fzf_iter` (free function)
-  `FuzzyFinder` (class)
-  `FuzzyFinderBuilder` (class)
-  `FuzzyFinderOutput` (class)

Many other classes, parts of `FuzzyFinderBuilder`'s configuration are also 
included, but you're not always going to have to use each of them, so, in this 
guide, I'll only mention them when necessary, in appropriate examples.

## `fzf` Free Function

Basic Usage:

```python
from fzf_but_typed.lib import fzf, SearchOptions, DisplayOptions, Color, 

# Basic usage
chosen_items = fzf(input_text="first\nsecond\nthird")
print("you chose:", chosen_items[0])
```

Through `fzf`, you can pass arguments to `FuzzyFinderBuilder` too, as keyword 
arguments, like this:

```python
from fzf_but_typed.lib import (fzf,
    SearchOptions, DisplayOptions, Color, BaseColorScheme)

chosen_items = fzf(
    input_text="first\nsecond\nthird",
    search=SearchOptions(exact=True, case_sensitive=False),
    display=DisplayOptions(color=Color(base_scheme=BaseColorScheme.LIGHT_256)),
)
print("you chose:", chosen_items[0])
```

## `fzf_iter` Free Function

In the spirit of python's duck typing, this module ships `fzf_iter`, to which 
you can pass a list of anything that can be converted into a `str`, as input.  
See the example below

```python
from fzf_but_typed.lib import fzf_iter, Key as SomeStrEnum

a_heterogenous_collection = [
    123123123,
    "aaaaaa",
    12.32,
    SomeStrEnum.CTRL_A,
]
print("you chose:", fzf_iter(input=a_heterogenous_collection)[0])
```

You can pass keyword arguments to `FuzzyFinderBuilder` through this function 
too, just like you did in `fzf` previously! See the example below

```python
from fzf_but_typed.lib import fzf_iter, InterfaceOptions, ScriptingOptions

a_heterogenous_collection = [123123123, "aaaaaa"]
chosen = fzf_iter(
    input=a_heterogenous_collection,
    interface=InterfaceOptions(multi=True, cycle=True),
    scripting=ScriptingOptions(print0=True),
)

print("you chose:", chosen[0])
```

## `FuzzyFinderBuilder` class

Using `FuzzyFinderBuilder` (instead of `fzf` or `fzf_iter`) allows you to cache 
`FuzzyFinder` objects with predefined settings for later use, being a little 
bit more efficient than building a new `FuzzyFinder` every time. It may receive 
many `*Options` parameters, as well as a `Path` to where your `fzf` binary is 
located (defaults to whatever `shutil.which` returns).

```python
from fzf_but_typed.lib import (
    FuzzyFinderBuilder, SearchOptions, ResultsOptions, DisplayOptions,
    PreviewOptions, FuzzyFinder, FuzzyFinderOutput, ExitStatusCode)

# These keyword arguments are also accepted by the previously mentioned 'fzf'
# and 'fzf_iter' functions
builder: FuzzyFinderBuilder = FuzzyFinderBuilder(
    search=SearchOptions(exact=True, case_sensitive=False),
    results=ResultsOptions(tac=True),
    display=DisplayOptions(ansi=True),
    preview=PreviewOptions(preview_command="echo {} | tr [:lower:] [:upper:]"),
)

# This object can be cached to be used again later (thats more efficient than
# calling 'fzf' or 'fzf_iter' multiple times, because this way, you don't have 
# to implicitly instantiate new builders over and over again
fuzzy_finder: FuzzyFinder = builder.build()

# You can access the 'built' command-line arguments through FuzzyFinder
# instances, as well as query the location of the binary to be used
print(f"{fuzzy_finder.binary_path=}")
print(f"{fuzzy_finder.args=}")

# When you feel like it, you can call 'run()' on 'FuzzyFinder' objects. Upon
# completion, they return 'FuzzyFinderOutput' objects
fzf_output: FuzzyFinderOutput = fuzzy_finder.run(input_lines="\n".join([
    "first line", "second line", "yet another line"])

# 'FuzzyFinderOutput' objects contain an 'exit_status_code' field, which is an
# enum, and a output field, which is a 'list' of 'str'
match fzf_output.exit_status_code:
    case ExitStatusCode.ERROR:
        print("something went wrong")
    case other_status_code:
        print("this is what happened:", other_status_code.name)

print("here's what you've selected:")
for item in fzf_output.output:
    print('\t', item)
```

## Going Nuts with All These Features

```python
from fzf_but_typed.lib import (
    Event, Key, ActionSimple, ActionWithArg, ActionWithArgType,
    ActionArgSeparator, FuzzyFinderBuilder, SearchOptions, ResultsOptions,
    InterfaceOptions, LayoutOptions, LayoutType, BorderType, DisplayOptions,
    Color, BaseColorScheme, HistoryOptions, PreviewOptions, ScriptingOptions
)

binds = [
    Binding(Event.ONE, [ActionSimple.ACCEPT]),
    Binding(Key.CTRL_R, [
        ActionWithArg(
            action_type=ActionWithArgType.CHANGE_PREVIEW_WINDOW,
            argument="right,70%|top,60%",
        ),
        ActionWithArg(
            action_type=ActionWithArgType.EXECUTE,
            argument="notify-send {} -t 3000",
            separator=ActionArgSeparator.PERCENT,
        ),
        ActionSimple.FIRST,
    ])
]

builder: FuzzyFinderBuilder = FuzzyFinderBuilder(
    search=SearchOptions(exact=True, case_sensitive=False),
    results=ResultsOptions(tac=True),
    interface=InterfaceOptions(multi=True, cycle=True, bind=binds),
    layout=LayoutOptions(layout=LayoutType.REVERSE, border=BorderType.SHARP),
    display=DisplayOptions(color=Color(base_scheme=BaseColorScheme.LIGHT_256)),
    history=HistoryOptions(history_size=19),
    preview=PreviewOptions(preview_command="echo {} | tr [:lower:] [:upper:]"),
    scripting=ScriptingOptions(read0=True, print0=True),
)

result = builder.build().run(input_lines="\0".join([
    "aaa a a a aaa a a a a a",
    "bb bw b f b bw b b bf db db  ",
    "cc case_sensitive c c       c c c ccccc",
    "asdasdasdas",
    "johnny",
    "",
    "asdasnkdaks",
]))

print("fzf returned code:", result.exit_status_code)
print("you picked:")
for item in result.output:
    print('\t', item)
```


# `fzf` Version Compatibility

The contents of this package are based on the informations avaliable on my 
system's man pages for fzf. If your version of fzf is older than mine, some of 
the features exposed on this API may not work. Conversely, if it's newer than 
mine, some features you may want to use may be absent here. Regardless, your 
use case is probably supported by this lib. I've included the aformentioned 
manpages in this package's repo, so, if you want to be 100% sure, you can 
download these manpages and run them through 'diff' with your system's manpages 
for fzf. Furthermore I've included a few CLI utilities for you to test said 
compatibility, as described below.

To see if your 'fzf' version is the same as mine, run:

    python -m fzf_but_typed compatibility

To se if, regardless of the version in question, your fzf's CLI is identical to 
mine, `clone` this repository, `cd` into it and run `./diff-man-pages.sh`, like 
this (assuming you're in an unix-like operating system):

    git clone "https://github.com/brunofauth/fzf_but_typed"
    cd fzf_but_typed
    ./diff-man-pages.sh

If any features you want to use are missing and that's sufficiently important 
to you, you can clone this repo, add that functionality and submit a pull 
request. I'll be glad to take in contributions!

