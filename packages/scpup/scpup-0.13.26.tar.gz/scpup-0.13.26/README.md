# AramEau - pyeau 

## SCPUP Description

Library for Super Crystal Pokebros Ultimate Party game. This library contains the SCPUP ABC and related python classes

This library is not meant to be used in other projects other than AramEau's SCPUP and maybe other games made by AramEau.
So, if for any reason you decide to use this library, it is at your own risk. Sorry but the aim of this library is to
acomplish a personal goal.

## Install

```bash
python -m pip install -U scpup
```

## Usage

Any exported member of any module within this package can be accessed from the root scope, for example:

```python
from scpup import EauSprite
class SomeSprite(EauSprite): ...
# or
import scpup
class SomeSprite(scpup.EauSprite): ...
```
