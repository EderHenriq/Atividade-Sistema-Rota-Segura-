import tkinter as tk
from tkinter import scrolledtext, messagebox
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

    def registrar_rota(self, km):
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
        self.root.title("Sistema Rota Segura - Log")
        self.root.geometry("600x500")

        # Mock de dados
        self.veiculo_atual = Caminhao("ABC-1234", "Volvo FH", 500000)

        # Widgets
        self.setup_ui()
        self.log_info(f"Sistema iniciado. Monitorando: {self.veiculo_atual.modelo} ({self.veiculo_atual.placa})")

    def setup_ui(self):
        # Frame de Controles
        frame_ctrl = tk.Frame(self.root, pady=10)
        frame_ctrl.pack()

        tk.Label(frame_ctrl, text="Distância (km):").grid(row=0, column=0)
        self.ent_km = tk.Entry(frame_ctrl, width=10)
        self.ent_km.grid(row=0, column=1, padx=5)

        tk.Label(frame_ctrl, text="Carga (ton):").grid(row=0, column=2)
        self.ent_carga = tk.Entry(frame_ctrl, width=10)
        self.ent_carga.grid(row=0, column=3, padx=5)

        btn_rota = tk.Button(frame_ctrl, text="Registrar Rota", command=self.handle_rota, bg="#e1e1e1")
        btn_rota.grid(row=0, column=4, padx=10)

        btn_maint = tk.Button(frame_ctrl, text="Realizar Manutenção", command=self.handle_maint, bg="#d1ffd1")
        btn_maint.grid(row=1, column=0, columnspan=5, sticky="ew", pady=10)

        # Log de Eventos
        tk.Label(self.root, text="Log de Atividades:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(self.root, height=15, state='disabled')
        self.log_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Tags de cores para o Log
        self.log_area.tag_config("info", foreground="blue")
        self.log_area.tag_config("error", foreground="red")
        self.log_area.tag_config("alert", foreground="orange", font=("TkDefaultFont", 10, "bold"))

    def log(self, tag, message):
        self.log_area.config(state='normal')
        prefix = f"[{tag.upper()}] "
        self.log_area.insert(tk.END, prefix, tag)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)

    def log_info(self, msg): self.log("info", msg)
    def log_error(self, msg): self.log("error", msg)

    def handle_rota(self):
        try:
            km = float(self.ent_km.get())
            carga = float(self.ent_carga.get() or 0)
            
            self.veiculo_atual.registrar_rota(km, carga)
            self.log_info(f"Rota registrada: {km}km | Carga: {carga}t. Total: {self.veiculo_atual.km_atual}km")
            
            if self.veiculo_atual.precisa_revisao():
                self.veiculo_atual.status = Status.MANUTENCAO
                self.log("alert", "ALERTA: Limite atingido! Veículo movido para MANUTENÇÃO.")
            
        except ValueError:
            self.log_error("Valores de KM ou Carga inválidos.")
        except Exception as e:
            self.log_error(str(e))

    def handle_maint(self):
        self.veiculo_atual.status = Status.DISPONIVEL
        self.veiculo_atual.km_ultima_revisao = self.veiculo_atual.km_atual
        if isinstance(self.veiculo_atual, Caminhao):
            self.veiculo_atual.carga_acumulada = 0
        self.log_info("Manutenção realizada com sucesso. Status: DISPONÍVEL.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRotaSegura(root)
    root.mainloop()
