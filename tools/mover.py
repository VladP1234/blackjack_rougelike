class Mover():
    def __init__(self) -> None:
        self.objects_to_move = {}
    def add_object(self, object, final_pos, time_to_move):
        self.objects_to_move[object] = (final_pos, time_to_move)
    def update(self, elapsed_time):
        for object, (final_pos, time_to_move) in self.objects_to_move.items():
            object.x += (final_pos.x - object.x) * (time_to_move - elapsed_time)
            object.y += (final_pos.y - object.y) * (time_to_move - elapsed_time)
            self.objects_to_move[object] = (final_pos, time_to_move-elapsed_time)