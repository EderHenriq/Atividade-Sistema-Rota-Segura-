package rotasegura;

public abstract class Veiculo {
    private final String placa;
    private final String modelo;
    private final int anoFabricacao;
    protected double quilometragemAtual;
    protected double valorVeiculo;
    protected StatusVeiculo status;

    public Veiculo(String placa, String modelo, int anoFabricacao, double valorVeiculo, double quilometragemAtual) {
        this.placa = placa;
        this.modelo = modelo;
        this.anoFabricacao = anoFabricacao;
        this.valorVeiculo = valorVeiculo;
        this.quilometragemAtual = quilometragemAtual;
        this.status = StatusVeiculo.DISPONIVEL;
    }

    public String getPlaca() { return placa; }
    public String getModelo() { return modelo; }
    public int getAnoFabricacao() { return anoFabricacao; }
    public double getQuilometragemAtual() { return quilometragemAtual; }
    public StatusVeiculo getStatus() { return status; }
    public void setStatus(StatusVeiculo status) { this.status = status; }

    public abstract double calcularSeguro();
    public abstract boolean precisaRevisao();

    public void registrarRota(double km, double carga) {
        if (this.status == StatusVeiculo.MANUTENCAO) {
            throw new IllegalStateException("Não é possível registrar rota: veículo em manutenção.");
        }
        
        if (km <= 0) {
            throw new IllegalArgumentException("A quilometragem da rota deve ser positiva.");
        }

        this.quilometragemAtual += km;
        this.status = StatusVeiculo.EM_ROTA;
        
        processarCarga(carga);

        if (precisaRevisao()) {
            this.status = StatusVeiculo.MANUTENCAO;
            System.out.println("Alerta: Veículo " + placa + " atingiu o limite e foi movido para MANUTENCAO.");
        }
    }

    protected void processarCarga(double carga) {
        // Implementação padrão não faz nada com a carga
    }

    public void registrarRota(double km) {
        registrarRota(km, 0);
    }

    public void finalizarRota() {
        if (this.status == StatusVeiculo.EM_ROTA) {
            this.status = StatusVeiculo.DISPONIVEL;
        }
    }
}
