import gradio as gr
from typing import List
from gradio_client import Client


DESCRIPTION = '''
<div>
<h1 style="text-align: center;">Tic Tac Toe</h1>
<h2>Simple Tic Tac Toe game with a computer opponent.</h2>
'''

LICENSE = """
---
Built with ❤️ by [Gradio](https://gradio.app)
"""

boardTemplate = """
<center>
    <table>
        <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
        </tr>
        <tr>
            <td>{3}</td>
            <td>{4}</td>
            <td>{5}</td>
        </tr>
        <tr>
            <td>{6}</td>
            <td>{7}</td>
            <td>{8}</td>
        </tr>
    </table>
</center>
"""

aiBoardTemplate = """"
       0     1     2
    +-----+-----+-----+
    | {0} | {1} | {2} |
    +-----+-----+-----+
  3 | {3} | {4} | {5} | 5
    +-----+-----+-----+
    | {6} | {7} | {8} |
    +-----+-----+-----+
         6     7     8
"""

css = """
table {
    border-collapse: collapse;
}

td {
    border: 1px solid gray;
    width: 50px;
    height: 50px;
    text-align: center;
}
"""

winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

squares: List[str] = ["   " for i in range(9)]


def aiPlayer(squares: List[str]) -> int:
    print("AI's turn")
    prompt = f""""
    The board is:
    
    {aiBoardTemplate.format(*squares)}
    
    It's your turn. Enter the number of the square you want to place your 'O' in.
    Only enter the number of the square. For example, if you want to place your 'O' in the top right square, enter '2'.
    """

    client = Client("ysharma/Chat_with_Meta_llama3_8b")
    result = client.predict(
        message=prompt,
        request=0.95,
        param_3=512,
        api_name="/chat"
    )
    print(result)

    return 0


def botPlayer(squares: List[str]) -> int:
    print("Bot's turn")
    if squares[4] == "   ":
        return 4
    lockable_moves: List[int] = []

    for condition in winConditions:
        for vacantPosition in range(3):
            if (
                    squares[condition[vacantPosition]] == "   "
                    and squares[condition[(vacantPosition + 1) % 3]] == " X "
                    and squares[condition[(vacantPosition + 2) % 3]] == " X "
            ):
                lockable_moves.append(condition[vacantPosition])
    if not lockable_moves:
        for square in squares:
            if square == "   ":
                return squares.index(square)
    return lockable_moves[0]


def checkWin(current_player: bool, squares: List[str]):
    player_mark: str = " X " if current_player else " O "
    for condition in winConditions:
        if (
                squares[condition[0]] == player_mark
                and squares[condition[1]] == player_mark
                and squares[condition[2]] == player_mark
        ):
            return True
    return False


def is_empty(squares: List[str], index: int) -> bool:
    return squares[index] == "   "


def reset_squares():
    global squares
    squares = ["   " for i in range(9)]


def is_square_empty():
    for square in squares:
        if square == "   ":
            return True
    return False


def on_submit(number):
    if not is_square_empty():
        reset_squares()

    if is_empty(squares, number):
        squares[number] = " X "
        if checkWin(True, squares):
            gr.Info("You win!")
            return "<h3>You win!</h3>"
    else:
        gr.Info("Move already made!")
        return boardTemplate.format(*squares)

    bot_move = botPlayer(squares)
    aiPlayer(squares)
    if is_empty(squares, bot_move):
        squares[bot_move] = " O "
        if checkWin(False, squares):
            gr.Info("You lose!")
            return "<h3>You lose!</h3>"

    if not is_square_empty():
        gr.Info("It's a tie!")
        return "<h3>It's a tie!</h3>"

    return boardTemplate.format(*squares)


with (gr.Blocks(css=css) as demo):
    gr.Markdown(DESCRIPTION)

    with gr.Row():
        with gr.Column():
            board = gr.HTML(
                boardTemplate.format(*squares),
            )

        with gr.Column():
            num = gr.Number(
                0,
                label="Player X move",
                minimum=0,
                maximum=8,
                step=1,
            )
            num.submit(on_submit, inputs=[num], outputs=[board])

    gr.Markdown(LICENSE)

if __name__ == "__main__":
    demo.launch()
