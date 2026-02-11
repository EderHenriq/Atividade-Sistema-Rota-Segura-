package rotasegura;

public class Caminhao extends Veiculo {
    private double capacidadeCarga;
    private int quantidadeEixos;
    private double quilometragemUltimaRevisao;
    private double cargaAcumulada;

    public Caminhao(String placa, String modelo, int anoFabricacao, double valorVeiculo, double quilometragemAtual, double capacidadeCarga, int quantidadeEixos) {
        super(placa, modelo, anoFabricacao, valorVeiculo, quilometragemAtual);
        this.capacidadeCarga = capacidadeCarga;
        this.quantidadeEixos = quantidadeEixos;
        this.quilometragemUltimaRevisao = quilometragemAtual;
        this.cargaAcumulada = 0;
    }

    @Override
    public double calcularSeguro() {
        return (this.valorVeiculo * 0.02) + (this.capacidadeCarga * 50.0);
    }

    @Override
    public boolean precisaRevisao() {
        return (this.quilometragemAtual - this.quilometragemUltimaRevisao) >= 10000 || this.cargaAcumulada >= 500;
    }

    @Override
    protected void processarCarga(double carga) {
        if (carga < 0) {
            throw new IllegalArgumentException("A carga não pode ser negativa.");
        }
        this.cargaAcumulada += carga;
    }

    public void realizarManutencao() {
        this.quilometragemUltimaRevisao = this.quilometragemAtual;
        this.cargaAcumulada = 0;
        this.status = StatusVeiculo.DISPONIVEL;
    }

    public double getCapacidadeCarga() { return capacidadeCarga; }
    public int getQuantidadeEixos() { return quantidadeEixos; }
    public double getCargaAcumulada() { return cargaAcumulada; }
}
