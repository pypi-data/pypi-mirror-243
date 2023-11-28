# Char

## Description

The Char module is comprised of several submodules that provide functionality for working with (but not limited to) Characters typical to role-playing games, objects that those characters may interact with, take posession of or find and a grid-based game world on which those characters may reside. The submodules are as follows:

* [Char::CharCore](Char/_CharCore/README.md) - The core module is provides windowing and event handling functionality. (As well as a few other things.)
* [Char::entyty](Char/_entyty/README.md) - The entyty module provides a framework for creating and managing entities, which are the foundation of the Charactors created by the CharActor module. Includes the integral `Entity` and `GridEntity` classes.
* [Char::dicepy](Char/_dicepy/README.md) - The dicepy module provides a framework for creating and managing dice, which are a fundamental part of many role-playing games. Includes the integral `Die`, `DiceSet` and `D20` classes.
* [Char::gridengine_framework](Char/_gridengine/README.md) - The gridengine module provides a framework for creating and managing a grid-based game world. Includes the integral `Grid`, `Cell`, `Blueprint`, and `GridObject` classes.
* [Char::CharActor](Char/_CharActor/README.md) - The CharActor module provides a framework for creating and managing characters typical to role-playing games. Includes the integral `Character` class.
* [Char::CharObj](Char/_CharObj/README.md) - The CharObj module provides a framework for creating an endless variety of objects that can be placed on `Grid` objects and obtained/used by `Character` objects. Includes the integral `Armory` and `Goods` objects and the `Item` class.
* [Char::CharTask](Char/_CharTask/README.md) - The CharTask module provides a framework for creating and managing tasks that can be performed by `Character` objects. Includes the integral `Task` class in addition to the `task_list` object.

## Usage

### Importing

Importing `Char` is easy. You can import the entire module, or just the submodules you need. For example:

```python
import Char
```

or

```python
from Char import core, actor, obj, world, task
```

### Creating a Character

Creating a character is easy.

```python
from Char import actor

# Create a new character with random attributes.
actor.create()

# The character can be accessed through the 'character_bank' object.
actor.character_bank.char1
```
You can assign the character a custom identifier by passing a string to the `create()` function.

```python
actor.create('my_char')
actor.character_bank.my_char
```

### Creating a Grid

Creating a grid is easy.

```python
from Char import world

# Create a new grid with default dimensions.

grid = world.grid.Grid()
```

You can specify the dimensions of the grid by passing a tuple to the `Grid()` function.

```python
grid = world.grid.Grid(cell_size=1, dimensions=(1000, 1000))
```

### Creating a GridObject
