package rotasegura;

public class Moto extends Veiculo {
    private int cilindrada;
    private double quilometragemUltimaRevisao;

    public Moto(String placa, String modelo, int anoFabricacao, double valorVeiculo, double quilometragemAtual, int cilindrada) {
        super(placa, modelo, anoFabricacao, valorVeiculo, quilometragemAtual);
        this.cilindrada = cilindrada;
        this.quilometragemUltimaRevisao = quilometragemAtual;
    }

    @Override
    public double calcularSeguro() {
        return this.valorVeiculo * 0.05;
    }

    @Override
    public boolean precisaRevisao() {
        return (this.quilometragemAtual - this.quilometragemUltimaRevisao) >= 3000;
    }

    public void realizarManutencao() {
        this.quilometragemUltimaRevisao = this.quilometragemAtual;
        this.status = StatusVeiculo.DISPONIVEL;
    }

    public int getCilindrada() { return cilindrada; }
}
