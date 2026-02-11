# -*- coding: utf-8 -*-
import tkinter as tk 
from tkinter import ttk, scrolledtext, messagebox
from enum import Enum

class Status(Enum):
    DISPONIVEL = "Disponível"
    EM_ROTA = "Em Rota"
    MANUTENCAO = "Manutenção"

class Veiculo:
    def __init__(self, placa, modelo, valor):
        self.placa = placa
        self.modelo = modelo
        self.valor = valor
        self.km_atual = 0
        self.status = Status.DISPONIVEL

    def registrar_rota(self, km, carga=0):
        if self.status == Status.MANUTENCAO:
            raise Exception("Veículo em manutenção!")
        self.km_atual += km
        self.status = Status.EM_ROTA

class Moto(Veiculo):
    def __init__(self, placa, modelo, valor):
        super().__init__(placa, modelo, valor)
        self.km_ultima_revisao = 0

    def precisa_revisao(self):
        return (self.km_atual - self.km_ultima_revisao) >= 3000

class Caminhao(Veiculo):
    def __init__(self, placa, modelo, valor):
        super().__init__(placa, modelo, valor)
        self.km_ultima_revisao = 0
        self.carga_acumulada = 0

    def registrar_rota(self, km, carga):
        super().registrar_rota(km)
        self.carga_acumulada += carga

    def precisa_revisao(self):
        return (self.km_atual - self.km_ultima_revisao) >= 10000 or self.carga_acumulada >= 500

class AppRotaSegura:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Rota Segura - Gestão de Frota")
        self.root.geometry("800x600")

        # Lista de veículos e veículo selecionado
        self.veiculos = []
        self.veiculo_atual = None

        # --- Frame de Cadastro de Veículo ---
        frame_cadastro = tk.LabelFrame(self.root, text="Cadastrar Novo Veículo", padx=10, pady=10)
        frame_cadastro.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_cadastro, text="Tipo:").grid(row=0, column=0, sticky="w")
        self.var_tipo = tk.StringVar(value="Moto")
        tk.Radiobutton(frame_cadastro, text="Moto", variable=self.var_tipo, value="Moto").grid(row=0, column=1)
        tk.Radiobutton(frame_cadastro, text="Caminhão", variable=self.var_tipo, value="Caminhao").grid(row=0, column=2)

        tk.Label(frame_cadastro, text="Placa:").grid(row=1, column=0, sticky="w")
        self.ent_placa = tk.Entry(frame_cadastro)
        self.ent_placa.grid(row=1, column=1, columnspan=2, sticky="ew")

        tk.Label(frame_cadastro, text="Modelo:").grid(row=2, column=0, sticky="w")
        self.ent_modelo = tk.Entry(frame_cadastro)
        self.ent_modelo.grid(row=2, column=1, columnspan=2, sticky="ew")

        tk.Label(frame_cadastro, text="Valor (R$):").grid(row=3, column=0, sticky="w")
        self.ent_valor = tk.Entry(frame_cadastro)
        self.ent_valor.grid(row=3, column=1, columnspan=2, sticky="ew")

        btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar_veiculo, bg="#d1e7dd")
        btn_cadastrar.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        # --- Frame de Seleção de Veículo ---
        frame_selecao = tk.LabelFrame(self.root, text="Operações do Veículo", padx=10, pady=10)
        frame_selecao.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_selecao, text="Selecionar Veículo:").grid(row=0, column=0, sticky="w")
        self.var_veiculo_selecionado = tk.StringVar()
        self.combo_veiculos = ttk.Combobox(frame_selecao, textvariable=self.var_veiculo_selecionado, state="readonly", width=40)
        self.combo_veiculos.grid(row=0, column=1, padx=5, sticky="ew")
        self.combo_veiculos.bind("<<ComboboxSelected>>", self.selecionar_veiculo)

        # --- Frame de Controles (Rota e Manutenção) ---
        frame_ctrl = tk.Frame(frame_selecao, pady=10)
        frame_ctrl.grid(row=1, column=0, columnspan=2, sticky="ew")

        tk.Label(frame_ctrl, text="Distância (km):").grid(row=0, column=0)
        self.ent_km = tk.Entry(frame_ctrl, width=10)
        self.ent_km.grid(row=0, column=1, padx=5)

        tk.Label(frame_ctrl, text="Carga (ton):").grid(row=0, column=2)
        self.ent_carga = tk.Entry(frame_ctrl, width=10)
        self.ent_carga.grid(row=0, column=3, padx=5)

        btn_rota = tk.Button(frame_ctrl, text="Registrar Rota", command=self.handle_rota, bg="#e1e1e1")
        btn_rota.grid(row=0, column=4, padx=10)

        btn_maint = tk.Button(frame_ctrl, text="Realizar Manutenção", command=self.handle_maint, bg="#fff3cd")
        btn_maint.grid(row=1, column=0, columnspan=5, sticky="ew", pady=10)

        # Log de Eventos
        tk.Label(self.root, text="Log de Atividades:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(self.root, height=10, state='disabled')
        self.log_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Tags de cores para o Log
        self.log_area.tag_config("info", foreground="blue")
        self.log_area.tag_config("error", foreground="red")
        self.log_area.tag_config("alert", foreground="orange", font=("TkDefaultFont", 10, "bold"))
        self.log_area.tag_config("success", foreground="green")

        self.log_info("Sistema iniciado. Cadastre ou selecione um veículo.")

    def log(self, tag, message):
        self.log_area.config(state='normal')
        prefix = f"[{tag.upper()}] "
        self.log_area.insert(tk.END, prefix, tag)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)

    def log_info(self, msg): self.log("info", msg)
    def log_error(self, msg): self.log("error", msg)
    def log_success(self, msg): self.log("success", msg)

    def cadastrar_veiculo(self):
        try:
            tipo = self.var_tipo.get()
            placa = self.ent_placa.get().strip()
            modelo = self.ent_modelo.get().strip()
            valor_str = self.ent_valor.get().strip()

            if not placa or not modelo or not valor_str:
                raise ValueError("Preencha todos os campos do cadastro.")

            valor = float(valor_str)

            # Verificar placa duplicada
            for v in self.veiculos:
                if v.placa == placa:
                    raise ValueError(f"Veículo com placa {placa} já existe.")

            novo_veiculo = None
            if tipo == "Moto":
                novo_veiculo = Moto(placa, modelo, valor)
            else:
                novo_veiculo = Caminhao(placa, modelo, valor)

            self.veiculos.append(novo_veiculo)
            self.atualizar_combo_veiculos()
            
            # Limpar campos
            self.ent_placa.delete(0, tk.END)
            self.ent_modelo.delete(0, tk.END)
            self.ent_valor.delete(0, tk.END)
            
            self.log_success(f"Veículo cadastrado: {tipo} {modelo} ({placa})")
            
            # Selecionar automaticamente se for o primeiro
            if len(self.veiculos) == 1:
                self.combo_veiculos.current(0)
                self.selecionar_veiculo(None)

        except ValueError as ve:
            self.log_error(str(ve))
        except Exception as e:
            self.log_error(f"Erro ao cadastrar: {str(e)}")

    def atualizar_combo_veiculos(self):
        lista_formatada = [f"{v.modelo} - {v.placa} ({type(v).__name__})" for v in self.veiculos]
        self.combo_veiculos['values'] = lista_formatada

    def selecionar_veiculo(self, event):
        indice = self.combo_veiculos.current()
        if indice >= 0:
            self.veiculo_atual = self.veiculos[indice]
            self.log_info(f"Veículo selecionado: {self.veiculo_atual.modelo} - {self.veiculo_atual.placa}")

    def handle_rota(self):
        if self.veiculo_atual is None:
            self.log_error("Nenhum veículo selecionado!")
            return

        try:
            km = float(self.ent_km.get())
            carga = float(self.ent_carga.get() or 0)
            
            self.veiculo_atual.registrar_rota(km, carga)
            self.log_info(f"Rota registrada para {self.veiculo_atual.placa}: {km}km. Total: {self.veiculo_atual.km_atual}km")
            
            if self.veiculo_atual.precisa_revisao():
                self.veiculo_atual.status = Status.MANUTENCAO
                self.log("alert", f"ALERTA: {self.veiculo_atual.placa} precisa de MANUTENÇÃO!")
            
        except ValueError:
            self.log_error("Valores de KM ou Carga inválidos.")
        except Exception as e:
            self.log_error(str(e))

    def handle_maint(self):
        if not self.veiculo_atual:
            self.log_error("Nenhum veículo selecionado!")
            return

        self.veiculo_atual.status = Status.DISPONIVEL
        self.veiculo_atual.km_ultima_revisao = self.veiculo_atual.km_atual
        if isinstance(self.veiculo_atual, Caminhao):
            self.veiculo_atual.carga_acumulada = 0
        self.log_success(f"Manutenção realizada para {self.veiculo_atual.placa}. Status: DISPONÍVEL.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRotaSegura(root)
    root.mainloop()
