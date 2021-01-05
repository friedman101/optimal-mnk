## optimal-mnk

**optimal-mnk** plays an optimal mnk-game, which is a generalization of tic-tac-toe. To have the computer play itself at tic-tac-toe, run the following to specify you'd like a 3x3 board, with 3 in a row to win:

```
./opt-mnk.py 3 3 3 1
```

The final argument `1` refers to the style of play, with `1` being normal and `-1` being the Misère variant where you win if your opponent gets 3 in a row.

To run the Misère variant of tic-tac-toe, run:

```
./opt-mnk.py 3 3 3 -1
```

To play second move against the computer on a 3x4 board where getting 3 in a row will win, run:

```
./opt-mnk.py 3 4 3 1 --play-second
```

The computer will always be able to win the above game in 4 moves or less.