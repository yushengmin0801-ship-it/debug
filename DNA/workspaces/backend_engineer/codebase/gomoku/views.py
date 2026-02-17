from rest_framework.views import APIView
from rest_framework.response import Response
from .engine import GomokuAI
class AIMoveView(APIView):
    def post(self, request):
        board = request.data.get('board')
        move = GomokuAI().get_best_move(board)
        return Response({'row': move[0], 'col': move[1]}) if move else Response({'error': 'no_moves'})
