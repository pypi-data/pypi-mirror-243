# kontainer

## Why Kontainer?
Most of what `kontainer` wants to do has already been implemented in much better libraries,
[`expression`](https://github.com/dbrattli/Expression),
[`result`](https://github.com/rustedpy/result),
and [`returns`](https://github.com/dry-python/returns).
But each of them had one thing that was missing, and it was hard to ask for a fix.
> 1. `expression`: does not support python 3.8.
> 2. `result`: provides solid but simple functionality.
> 3. `returns`: does not support `pyright`.

In my environment, `expression` was the best fit, 
but dropping support for python 3.8 was the right decision,
so I couldn't ask for it.
(I don't want to use python 3.8 either,
but there are circumstances that make it unavoidable.)

So I created a new library with python 3.8 support,
pulling in some features that seemed to be needed.

## TODO
- [ ] add doc comments
- [ ] add doc pages(like `sphinx`)
- [ ] support apply(fully typed)
- [ ] more robust test codes
- [ ] remove `type: ignore` as much as possible