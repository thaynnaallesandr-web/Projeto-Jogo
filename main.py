import tkinter as tk
from tkinter import messagebox

class JogoXadrezRosa:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess.Pink - Xadrez Rosa 🌸")
        self.root.geometry("680x740")
        self.root.config(bg="#ffe6f2")

        # Paleta de tons de rosa
        self.COR_CLARA = "#fff0f3"       # Rosa bem clarinho
        self.COR_ESCURA = "#ffb3c6"      # Rosa médio suave
        self.COR_SELECAO = "#ff4d6d"     # Rosa choque vibrante (peça selecionada)
        self.COR_MOVIMENTO = "#ff85a1"   # Rosa intermediário (casas válidas)
        self.COR_PAINEL = "#a4133c"      # Rosa escuro / Vinho

        self.turno = "Brancas"  # As "brancas" começam
        self.casa_selecionada = None
        self.movimentos_validos = []
        self.botoes = {}
        self.jogo_encerrado = False

        # Criar cabeçalho
        self.label_turno = tk.Label(
            root, text="Turno das: Brancas 🤍", font=("Arial", 16, "bold"),
            bg="#ffe6f2", fg=self.COR_PAINEL
        )
        self.label_turno.pack(pady=10)

        # Frame do Tabuleiro
        self.frame_tabuleiro = tk.Frame(root, bg=self.COR_PAINEL, bd=5)
        self.frame_tabuleiro.pack()

        self.reiniciar_tabuleiro()
        self.criar_interface()

    def reiniciar_tabuleiro(self):
        self.tabuleiro = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
        ]
        self.jogo_encerrado = False
        self.turno = "Brancas"
        self.casa_selecionada = None
        self.movimentos_validos = []

    def criar_interface(self):
        for r in range(8):
            for c in range(8):
                btn = tk.Button(
                    self.frame_tabuleiro, text=self.tabuleiro[r][c],
                    font=("Arial", 28), width=2, height=1,
                    command=lambda linha=r, coluna=c: self.clicar_casa(linha, coluna)
                )
                btn.grid(row=r, column=c)
                self.botoes[(r, c)] = btn
        self.atualizar_interface()

    def atualizar_interface(self):
        for r in range(8):
            for c in range(8):
                cor_fundo = self.COR_CLARA if (r + c) % 2 == 0 else self.COR_ESCURA
                
                if (r, c) in self.movimentos_validos:
                    cor_fundo = self.COR_MOVIMENTO
                
                if self.casa_selecionada == (r, c):
                    cor_fundo = self.COR_SELECAO

                peca = self.tabuleiro[r][c]
                fg_cor = "#590d22" if peca in ["♙", "♖", "♘", "♗", "♕", "♔"] else "#1f0308"
                
                self.botoes[(r, c)].config(text=peca, bg=cor_fundo, fg=fg_cor)

        if not self.jogo_encerrado:
            texto_turno = "Turno das: Brancas 🤍" if self.turno == "Brancas" else "Turno das: Pretas 🖤"
            self.label_turno.config(text=texto_turno)

    def e_peca_branca(self, peca):
        return peca in ["♙", "♖", "♘", "♗", "♕", "♔"]

    def e_peca_preta(self, peca):
        return peca in ["♟", "♜", "♞", "♝", "♛", "♚"]

    def mesma_equipe(self, p1, p2):
        if p1 == "" or p2 == "":
            return False
        return (self.e_peca_branca(p1) and self.e_peca_branca(p2)) or \
               (self.e_peca_preta(p1) and self.e_peca_preta(p2))

    def calcular_movimentos_validos(self, r, c):
        peca = self.tabuleiro[r][c]
        movs = []
        
        if peca == "":
            return movs

        # Peão Branco
        if peca == "♙":
            if r > 0 and self.tabuleiro[r-1][c] == "":
                movs.append((r-1, c))
                if r == 6 and self.tabuleiro[r-2][c] == "":
                    movs.append((r-2, c))
            for dc in [-1, 1]:
                if 0 <= c + dc < 8 and r > 0:
                    alvo = self.tabuleiro[r-1][c+dc]
                    if alvo != "" and self.e_peca_preta(alvo):
                        movs.append((r-1, c+dc))

        # Peão Preto
        elif peca == "♟":
            if r < 7 and self.tabuleiro[r+1][c] == "":
                movs.append((r+1, c))
                if r == 1 and self.tabuleiro[r+2][c] == "":
                    movs.append((r+2, c))
            for dc in [-1, 1]:
                if 0 <= c + dc < 8 and r < 7:
                    alvo = self.tabuleiro[r+1][c+dc]
                    if alvo != "" and self.e_peca_branca(alvo):
                        movs.append((r+1, c+dc))

        # Cavalo
        elif peca in ["♘", "♞"]:
            saltos = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for dr, dc in saltos:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    alvo = self.tabuleiro[nr][nc]
                    if alvo == "" or not self.mesma_equipe(peca, alvo):
                        movs.append((nr, nc))

        # Rei
        elif peca in ["♔", "♚"]:
            direcoes = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for dr, dc in direcoes:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    alvo = self.tabuleiro[nr][nc]
                    if alvo == "" or not self.mesma_equipe(peca, alvo):
                        movs.append((nr, nc))

        # Torre, Bispo, Dama
        else:
            direcoes = []
            if peca in ["♖", "♜", "♕", "♛"]:
                direcoes.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])
            if peca in ["♗", "♝", "♕", "♛"]:
                direcoes.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

            for dr, dc in direcoes:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    alvo = self.tabuleiro[nr][nc]
                    if alvo == "":
                        movs.append((nr, nc))
                    else:
                        if not self.mesma_equipe(peca, alvo):
                            movs.append((nr, nc))
                        break
                    nr += dr
                    nc += dc

        return movs

    def verificar_fim_de_jogo(self):
        # Procura se o Rei Branco (♔) ou o Rei Preto (♚) ainda existem no tabuleiro
        rei_branco_presente = False
        rei_preto_presente = False

        for r in range(8):
            for c in range(8):
                if self.tabuleiro[r][c] == "♔":
                    rei_branco_presente = True
                elif self.tabuleiro[r][c] == "♚":
                    rei_preto_presente = True

        if not rei_branco_presente:
            self.jogo_encerrado = True
            self.label_turno.config(text="Fim de Jogo! Pretas venceram! 🖤")
            messagebox.showinfo("Fim de Jogo 🌸", "Xeque-Mate! As peças Pretas 🖤 venceram a partida!")
        elif not rei_preto_presente:
            self.jogo_encerrado = True
            self.label_turno.config(text="Fim de Jogo! Brancas venceram! 🤍")
            messagebox.showinfo("Fim de Jogo 🌸", "Xeque-Mate! As peças Brancas 🤍 venceram a partida!")

    def clicar_casa(self, r, c):
        if self.jogo_encerrado:
            return

        peca_clicada = self.tabuleiro[r][c]

        if not self.casa_selecionada:
            if peca_clicada != "":
                if (self.turno == "Brancas" and self.e_peca_branca(peca_clicada)) or \
                   (self.turno == "Pretas" and self.e_peca_preta(peca_clicada)):
                    self.casa_selecionada = (r, c)
                    self.movimentos_validos = self.calcular_movimentos_validos(r, c)
        else:
            origem_r, origem_c = self.casa_selecionada

            if peca_clicada != "" and ((self.e_peca_branca(peca_clicada) and self.turno == "Brancas") or
                                       (self.e_peca_preta(peca_clicada) and self.turno == "Pretas")):
                self.casa_selecionada = (r, c)
                self.movimentos_validos = self.calcular_movimentos_validos(r, c)
            
            elif (r, c) in self.movimentos_validos:
                # Executa o movimento (capturando a peça do destino, se houver)
                self.tabuleiro[r][c] = self.tabuleiro[origem_r][origem_c]
                self.tabuleiro[origem_r][origem_c] = ""
                
                # Verifica se o Rei foi capturado (Xeque-Mate)
                self.verificar_fim_de_jogo()

                if not self.jogo_encerrado:
                    # Alternar turno
                    self.turno = "Pretas" if self.turno == "Brancas" else "Brancas"
                
                self.casa_selecionada = None
                self.movimentos_validos = []
            else:
                self.casa_selecionada = None
                self.movimentos_validos = []

        self.atualizar_interface()

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoXadrezRosa(root)
    root.mainloop()