package rotasegura;

public class Main {
    public static void main(String[] args) {
        System.out.println("--- Sistema Rota Segura ---\n");

        // Teste Moto
        Moto moto = new Moto("ABC-1234", "Honda CB 500", 2022, 35000, 0, 500);
        System.out.println("Moto: " + moto.getModelo() + " | Placa: " + moto.getPlaca());
        System.out.println("Seguro Moto: R$ " + moto.calcularSeguro());

        try {
            moto.registrarRota(1500);
            System.out.println("Km após rota 1: " + moto.getQuilometragemAtual() + " | Status: " + moto.getStatus());
            moto.finalizarRota();
            
            moto.registrarRota(1600); // Deve atingir 3100km e disparar manutenção
            System.out.println("Km após rota 2: " + moto.getQuilometragemAtual() + " | Status: " + moto.getStatus());
            
            moto.registrarRota(100); // Deve falhar
        } catch (IllegalStateException e) {
            System.err.println("Erro esperado: " + e.getMessage());
        }

        moto.realizarManutencao();
        System.out.println("Status após manutenção: " + moto.getStatus() + "\n");

        // Teste Caminhão
        Caminhao caminhao = new Caminhao("XYZ-9999", "Volvo FH", 2021, 500000, 0, 40, 6);
        System.out.println("Caminhão: " + caminhao.getModelo() + " | Placa: " + caminhao.getPlaca());
        System.out.println("Seguro Caminhão: R$ " + caminhao.calcularSeguro());

        try {
            caminhao.registrarRota(5000, 300);
            System.out.println("Carga acumulada: " + caminhao.getCargaAcumulada() + " | Status: " + caminhao.getStatus());
            caminhao.finalizarRota();
            
            caminhao.registrarRota(1000, 250); // Soma 550 tons, deve disparar manutenção
            System.out.println("Carga acumulada: " + caminhao.getCargaAcumulada() + " | Status: " + caminhao.getStatus());
        } catch (Exception e) {
            System.err.println("Erro: " + e.getMessage());
        }
        
        System.out.println("\n--- Fim dos Testes ---");
    }
}
