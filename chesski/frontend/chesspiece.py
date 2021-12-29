from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.metrics import dp

class ChessPiece(DragBehavior, Image):

    def __init__(self, board, type, graphics_path, coordinates,
                 match_controller, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        self.size_hint = (.08, .08)
        self.drag_distance = dp(1)
        self.board = board
        self.drag_rectangle = (self.board.x, self.board.y,
                               self.board.width, self.board.height)
        self.source = graphics_path + f'/chessboard_and_pieces/{type}.png'
        self.starting_coordinates = coordinates
        self.last_coordinates = coordinates
        self.match_controller = match_controller

        # workaround for image appearing at 0,0 when first instantiated
        Clock.schedule_once(self.turn_visible, .3)

    def turn_visible(self, dt):
        self.move_to_coordinates(self.starting_coordinates)
        self.opacity=1


    def on_touch_down(self, touch):
        Clock.schedule_interval(self.update, 1/60.0)

        super(ChessPiece, self).on_touch_down(touch)

    def update(self, dt):
        self.stay_on_board()
        # print('update')


    def stay_on_board(self):
        """
        Function adjusting Position of piece if dragged off board.
        """
        if self.x < self.board.x:
            self.x = self.board.x
        elif self.right > self.board.x + self.board.width:
            self.right = self.board.x + self.board.width
        elif self.y < self.board.y:
            self.y = self.board.y
        elif self.top > self.board.y + self.board.height:
            self.top = self.board.y + self.board.height

    def get_nearest_coordinates(self):
        piece_x = self.center_x
        piece_y = self.center_y
        for row in range(8):
            for col in range(8):
                field_left_x = self.board.fields[row][col].x
                field_right_x = self.board.fields[row][col].right
                field_bottom_y = self.board.fields[row][col].y
                field_top_y = self.board.fields[row][col].top
                if (field_left_x < piece_x < field_right_x and
                   field_bottom_y < piece_y < field_top_y):
                   return (row, col)
        return None

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            next_coordinates = self.get_nearest_coordinates()

            if (next_coordinates != None and
            self.match_controller.move_was_possible(self.last_coordinates,
                                                next_coordinates)):
                self.move_to_coordinates(next_coordinates)
                print('move made!')
            else:
                self.move_to_coordinates(self.last_coordinates)

        Clock.unschedule(self.update)

        super(ChessPiece,self).on_touch_up(touch)

    def move_to_coordinates(self, next_coordinates):

        row = next_coordinates[0]
        col = next_coordinates[1]
        self.center_x = self.board.fields[row][col].center_x
        self.center_y = self.board.fields[row][col].center_y
        self.last_coordinates = next_coordinates
        print('moved to coordinates: ', next_coordinates)
