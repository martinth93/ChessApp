**Running a single test module:**

To run a single test module, in this case `test_board.py`:

    $ cd ChessKI
    $ python -m unittest tests.test_board

**Running a single test case or test method:**

Also you can run a single `TestCase` or a single test method:

    $ python -m unittest tests.test_board.TestBoardSize
    $ python -m unittest tests.test_antigravity.TestBoardSize.size_odd

**Running all tests:**

You can also use [test discovery][2] which will discover and run all the tests for you, they must be modules or packages named `test*.py` (can be changed with the `-p, --pattern` flag):

    $ cd ChessKI
    $ python -m unittest discover
