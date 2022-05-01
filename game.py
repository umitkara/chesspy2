import pygame
from sympy import re
from piece import Piece, PieceColor, PieceType
from board import ChessBoard
from typing import List, Tuple, Optional, Dict


class ChessGame:
    def __init__(self):
        self._board = ChessBoard()
        self._playerColor = PieceColor.WHITE
        self._computerLevel = 1
        self._initWhites()
        self._initBlacks()
        self._selected = None
        self._turn = PieceColor.WHITE
        self._castling = {PieceColor.WHITE: { PieceType.KING: True, PieceType.QUEEN: True }, 
                          PieceColor.BLACK: { PieceType.KING: True, PieceType.QUEEN: True }}
        
    @property
    def board(self) -> ChessBoard:
        """
        Returns the board.
        """
        return self._board
    
    @property
    def selected(self) -> Optional[Piece]:
        """
        Returns the selected piece.
        """
        return self._selected
    
    @selected.setter
    def selected(self, piece: Piece):
        """
        Sets the selected piece.
        """
        self._selected = piece
    
    @property
    def turn(self) -> PieceColor:
        """
        Returns the turn.
        """
        return self._turn

    @property
    def castling(self) -> Dict[str, Dict[str, bool]]:
        """
        Returns the castling status.
        """
        return self._castling
    
    @property
    def playerColor(self) -> PieceColor:
        """
        Returns the player color.
        """
        return self._playerColor
    
    @playerColor.setter
    def playerColor(self, color: PieceColor):
        """
        Sets the player color.
        """
        self._playerColor = color
        self.reset()
    
    @property
    def computerLevel(self) -> int:
        """
        Returns the computer level.
        """
        return self._computerLevel
    
    @computerLevel.setter
    def computerLevel(self, level: int):
        """
        Sets the computer level.
        """
        self._computerLevel = level
    
    def _initWhites(self):
        row = 1 if self._playerColor == PieceColor.WHITE else 8
        pawnRow = 2 if self._playerColor == PieceColor.WHITE else 7
        self.board[("A", 1)] = Piece(PieceType.ROOK, PieceColor.WHITE, ("A", row))
        self.board[("B", 1)] = Piece(PieceType.KNIGHT, PieceColor.WHITE, ("B", row))
        self.board[("C", 1)] = Piece(PieceType.BISHOP, PieceColor.WHITE, ("C", row))
        self.board[("D", 1)] = Piece(PieceType.QUEEN, PieceColor.WHITE, ("D", row))
        self.board[("E", 1)] = Piece(PieceType.KING, PieceColor.WHITE, ("E", row))
        self.board[("F", 1)] = Piece(PieceType.BISHOP, PieceColor.WHITE, ("F", row))
        self.board[("G", 1)] = Piece(PieceType.KNIGHT, PieceColor.WHITE, ("G", row))
        self.board[("H", 1)] = Piece(PieceType.ROOK, PieceColor.WHITE, ("H", row))
        self.board[("A", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("A", pawnRow))
        self.board[("B", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("B", pawnRow))
        self.board[("C", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("C", pawnRow))
        self.board[("D", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("D", pawnRow))
        self.board[("E", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("E", pawnRow))
        self.board[("F", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("F", pawnRow))
        self.board[("G", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("G", pawnRow))
        self.board[("H", 2)] = Piece(PieceType.PAWN, PieceColor.WHITE, ("H", pawnRow))
        
    def _initBlacks(self):
        row = 1 if self._playerColor == PieceColor.BLACK else 8
        pawnRow = 2 if self._playerColor == PieceColor.BLACK else 7
        self.board[("A", 8)] = Piece(PieceType.ROOK, PieceColor.BLACK, ("A", row))
        self.board[("B", 8)] = Piece(PieceType.KNIGHT, PieceColor.BLACK, ("B", row))
        self.board[("C", 8)] = Piece(PieceType.BISHOP, PieceColor.BLACK, ("C", row))
        self.board[("D", 8)] = Piece(PieceType.QUEEN, PieceColor.BLACK, ("D", row))
        self.board[("E", 8)] = Piece(PieceType.KING, PieceColor.BLACK, ("E", row))
        self.board[("F", 8)] = Piece(PieceType.BISHOP, PieceColor.BLACK, ("F", row))
        self.board[("G", 8)] = Piece(PieceType.KNIGHT, PieceColor.BLACK, ("G", row))
        self.board[("H", 8)] = Piece(PieceType.ROOK, PieceColor.BLACK, ("H", row))
        self.board[("A", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("A", pawnRow))
        self.board[("B", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("B", pawnRow))
        self.board[("C", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("C", pawnRow))
        self.board[("D", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("D", pawnRow))
        self.board[("E", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("E", pawnRow))
        self.board[("F", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("F", pawnRow))
        self.board[("G", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("G", pawnRow))
        self.board[("H", 7)] = Piece(PieceType.PAWN, PieceColor.BLACK, ("H", pawnRow))
        
    def posToBoard(self, position: Tuple[int, int]) -> Tuple[str, int]:
        """
        Converts a position to a board position.
        """
        return chr(position[0]//100 + ord('a')).upper(), abs(position[1]//100 - 8)
    
    def draw(self, screen):
        """
        Draws the board to the screen.
        """
        self.board.draw(screen)
        self.drawAwaliableMoves(screen)
        
    def drawAwaliableMoves(self, screen: pygame.Surface) -> None:
        """
        Draws the available moves to the screen.
        """
        if self.selected is not None:
            for move in self.avaliableMoves():
                screenX = (ord(move[0].lower()) - ord('a')) * 100
                screenY = (8 - int(move[1])) * 100
                pygame.draw.circle(screen, (0, 170, 0), (screenX + 50, screenY + 50), 20)
        
    def select(self, position: Tuple[str, int]) -> Optional[Piece]:
        """
        Selects a piece.
        """
        if self._selected is not None:
            self._selected.deselect()
        self._selected = self.board[position]
        if self._selected is not None:
            self._selected.select()
        return self._selected
    
    def deselect(self):
        """
        Deselects a piece.
        """
        if self._selected is not None:
            self._selected.deselect()
        self._selected = None
    
    def move(self, position: Tuple[str, int]) -> None:
        """
        Moves the selected piece to the given position.
        """
        # TODO: Implement Castling
        if self._selected is None:
            return
        oldPos = self._selected.piecePosition
        availableMoves = self.avaliableMoves()
        if oldPos == position:
            return
        if position not in availableMoves:
            return
        if self.board.isOccupied(position):
            self.board.captured[self.selected.pieceColor.name].append(self.board[position])
            self.board[position].isCaptured = True
        self.board[self.selected.piecePosition] = None
        self._selected.move(position)
        self.board[position] = self._selected
        self.board.moves.append((oldPos, position))
    
    def drag(self, screen: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Drags the selected piece to the given position.
        """
        if self._selected is not None:
            self._selected.drag(screen, position)
            
    def reset(self) -> None:
        """
        Resets the board.
        """
        self.board.reset()
        self._initWhites()
        self._initBlacks()
        self._selected = None
        self._castling = {PieceColor.WHITE: { PieceType.KING: True, PieceType.QUEEN: True },
                          PieceColor.BLACK: { PieceType.KING: True, PieceType.QUEEN: True }}
        self._turn = PieceColor.WHITE
        
    def changeTurn(self) -> None:
        """
        Changes the turn.
        """
        if self._turn == PieceColor.WHITE:
            self._turn = PieceColor.BLACK
        else:
            self._turn = PieceColor.WHITE
            
    def avaliableMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected piece.
        """
        if self.selected is None:
            return []
        if self.selected.pieceType == PieceType.PAWN:
            return self._avaliablePawnMoves()
        elif self.selected.pieceType == PieceType.ROOK:
            return self._avaliableRookMoves()
        elif self.selected.pieceType == PieceType.KNIGHT:
            return self._avaliableKnightMoves()
        elif self.selected.pieceType == PieceType.BISHOP:
            return self._avaliableBishopMoves()
        elif self.selected.pieceType == PieceType.QUEEN:
            return self._avaliableQueenMoves()
        elif self.selected.pieceType == PieceType.KING:
            return self._avaliableKingMoves()
        else:
            return []
        
    def _avaliablePawnMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected pawn.
        """
        if self.selected.pieceColor == PieceColor.WHITE:
            return self._avaliablePawnMovesWhite()
        else:
            return self._avaliablePawnMovesBlack()
    
    def _avaliablePawnMovesWhite(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected white pawn.
        """
        moves = []
        if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] + 1)] is None:
            moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] + 1))
            if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] + 2)] is None and self.selected.isMoved == False:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] + 2))
        if (self.selected.piecePosition[0].lower() != "h" 
            and self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1)] is not None 
            and self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1)].pieceColor == PieceColor.BLACK):
            moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1))
        if (self.selected.piecePosition[0].lower() != "a" 
            and self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1)] is not None 
            and self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1)].pieceColor == PieceColor.BLACK):
            moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1))
        return moves
    
    def _avaliablePawnMovesBlack(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected black pawn.
        """
        moves = []
        if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] - 1)] is None:
            moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] - 1))
            if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] - 2)] is None and self.selected.isMoved == False:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] - 2))
        if (self.selected.piecePosition[0].lower() != "h" 
            and self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1)] is not None 
            and self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1)].pieceColor == PieceColor.WHITE):
            moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1))
        if (self.selected.piecePosition[0].lower() != "a" 
            and self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1)] is not None 
            and self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1)].pieceColor == PieceColor.WHITE):
            moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1))
        return moves

    def _avaliableRookMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected rook.
        """
        moves = []
        col = ord(self.selected.piecePosition[0].lower()) - ord("a")
        for i in range(self.selected.piecePosition[1] + 1, 8):
            if self.board[(self.selected.piecePosition[0], i)] is None:
                moves.append((self.selected.piecePosition[0], i))
            else:
                break
        for i in range(self.selected.piecePosition[1] - 1, -1, -1):
            if self.board[(self.selected.piecePosition[0], i)] is None:
                moves.append((self.selected.piecePosition[0], i))
            else:
                break
        for i in range(col + 1, 8):
            if self.board[(chr(i + ord("a")), self.selected.piecePosition[1])] is None:
                moves.append((chr(i + ord("A")), self.selected.piecePosition[1]))
            else:
                break
        for i in range(col - 1, -1, -1):
            if self.board[(chr(i + ord("a")), self.selected.piecePosition[1])] is None:
                moves.append((chr(i + ord("A")), self.selected.piecePosition[1]))
            else:
                break
        return moves
    
    def _avaliableKnightMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected knight.
        """
        col = ord(self.selected.piecePosition[0].lower()) - ord("a")
        row = self.selected.piecePosition[1] - 1
        moves = []
        self._knightForwardMoves(col, row, moves)
        self._knightRightMoves(col, row, moves)
        self._knightBackMoves(col, row, moves)
        self._knightLeftMoves(col, row, moves)
        return moves
    # Knight moves helper functions
    ###
    def _knightForwardMoves(self, col, row, moves):
        if col < 7 and row < 6:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 2)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 2))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 2)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 2))
        if col > 0 and row < 6:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 2)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 2))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 2)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 2))

    def _knightRightMoves(self, col, row, moves):
        if col < 6 and row < 7:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] + 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] + 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] + 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] + 1))
        if col < 6 and row > 0:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] - 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] - 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] - 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 2), self.selected.piecePosition[1] - 1))

    def _knightBackMoves(self, col, row, moves):
        if col < 7 and row > 1:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 2)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 2))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 2)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 2))
        if col > 0 and row > 1:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 2)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 2))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 2)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 2))

    def _knightLeftMoves(self, col, row, moves):
        if col > 1 and row < 7:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] + 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] + 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] + 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] + 1))
        if col > 1 and row > 0:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] - 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] - 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] - 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 2), self.selected.piecePosition[1] - 1))
    ### 
    # End of Knight moves helper functions
    
    def _avaliableBishopMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected bishop.
        """
        col = ord(self.selected.piecePosition[0].lower()) - ord("a")
        row = self.selected.piecePosition[1] - 1
        moves = []
        self._bishopDownRightMoves(col, row, moves)
        self._bishopUpLeftMoves(col, row, moves)
        self._bishopUpRightMoves(col, row, moves)
        self._bishopDownLeftMoves(col, row, moves)
        return moves

    # Bishop moves helper functions
    ###
    def _bishopDownRightMoves(self, col, row, moves):
        for i in range(1, 8):
            if col + i >= 8 or row + i >= 8:
                break
            if self.board[(chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] + i)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] + i))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] + i)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] + i))
                break
            else:
                break

    def _bishopUpLeftMoves(self, col, row, moves):
        for i in range(1, 8):
            if col - i <= -1 or row + i >= 8:
                break
            if self.board[(chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] + i)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] + i))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] + i)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] + i))
                break
            else:
                break

    def _bishopUpRightMoves(self, col, row, moves):
        for i in range(1, 8):
            if col + i >= 8 or row - i <= -1:
                break
            if self.board[(chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] - i)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] - i))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] - i)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + i), self.selected.piecePosition[1] - i))
                break
            else:
                break

    def _bishopDownLeftMoves(self, col, row, moves):
        for i in range(1, 8):
            if col - i <= -1 or row - i <= -1:
                break
            if self.board[(chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] - i)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] - i))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] - i)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - i), self.selected.piecePosition[1] - i))
                break
            else:
                break
    ###
    # End of Bishop moves helper functions
    
    def _avaliableQueenMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected queen.
        """
        return self._avaliableRookMoves() + self._avaliableBishopMoves()
    
    def _avaliableKingMoves(self) -> List[Tuple[str, int]]:
        """
        Returns a list of avaliable moves of the selected king.
        """
        col = ord(self.selected.piecePosition[0].lower()) - ord("a")
        row = self.selected.piecePosition[1] - 1
        moves = []
        self._kingLeftMoves(col, row, moves)
        self._kingBackMoves(row, moves)
        self._kingFrontMoves(row, moves)
        self._kingRightMoves(col, row, moves)
        return self._castlingMoves(moves)

    # King avaliable moves helper functions
    ###
    def _kingLeftMoves(self, col, row, moves) -> None:
        """
        Adds avaliable moves of the selected king to the list.
        """
        if col <= 0:
            return
        if row > 0:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] - 1))
        if self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1])] is None:
            moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1]))
        elif self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1])].pieceColor != self.selected.pieceColor:
            moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1]))
        if row < 7:
            if self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) - 1), self.selected.piecePosition[1] + 1))

    def _kingBackMoves(self, row, moves) -> None:
        """
        Adds avaliable moves of the selected king to the list.
        """
        if row > 0:
            if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] - 1)] is None:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] - 1))
            elif self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] - 1)].pieceColor != self.selected.pieceColor:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] - 1))

    def _kingFrontMoves(self, row, moves) -> None:
        """
        Adds avaliable moves of the selected king to the list.
        """
        if row < 7:
            if self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] + 1)] is None:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] + 1))
            elif self.board[(self.selected.piecePosition[0], self.selected.piecePosition[1] + 1)].pieceColor != self.selected.pieceColor:
                moves.append((self.selected.piecePosition[0], self.selected.piecePosition[1] + 1))

    def _kingRightMoves(self, col, row, moves) -> None:
        """
        Adds avaliable moves of the selected king to the list.
        """
        if col >= 7:
            return
        if row > 0:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] - 1))
        if self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1])] is None:
            moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1]))
        elif self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1])].pieceColor != self.selected.pieceColor:
            moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1]))
        if row < 7:
            if self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1)] is None:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1))
            elif self.board[(chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1)].pieceColor != self.selected.pieceColor:
                moves.append((chr(ord(self.selected.piecePosition[0]) + 1), self.selected.piecePosition[1] + 1))

    def _castlingMoves(self, moves) -> list:
        """
        Returns a list of avaliable moves of the selected king.
        """
        if self.selected.pieceColor == PieceColor.WHITE:
            # King side
            if (self.selected.piecePosition == ("E",1) and self.board["F",1] is None 
                and self.board["G",1] is None 
                and self._castling[PieceColor.WHITE][PieceType.KING]):
                moves.append(("G",1))
            # Queen side
            if (self.selected.piecePosition == ("E",1) and self.board["B",1] is None 
                and self.board["C",1] is None 
                and self.board["D",1] is None 
                and self._castling[PieceColor.WHITE][PieceType.QUEEN]):
                moves.append(("C",1))
        if self.selected.pieceColor == PieceColor.BLACK:
            # King side
            if (self.selected.piecePosition == ("E",8) 
                and self.board["F",8] is None 
                and self.board["G",8] is None
                and self._castling[PieceColor.BLACK][PieceType.KING]):
                moves.append(("G",8))
            # Queen side
            if (self.selected.piecePosition == ("E",8) 
                and self.board["B",8] is None 
                and self.board["C",8] is None 
                and self.board["D",8] is None 
                and self._castling[PieceColor.BLACK][PieceType.QUEEN]):
                moves.append(("C",8))
        return moves
    ###
    # End of king helper functions