import asyncio
from datetime import date
from reports.generator import ReportGenerator
from dateutil.relativedelta import relativedelta
import logging

# Configuração básica de logging para ver o que está acontecendo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Esta função força a geração de relatórios para os últimos 3 meses.
    """
    generator = ReportGenerator()
    
    # Pega a data de hoje para calcular os meses anteriores
    # Vamos simular a data de execução para que o gerador olhe para o mês correto
    today = date.today()

    logger.info("--- INICIANDO GERAÇÃO MANUAL DE RELATÓRIOS PARA TESTE ---")

    # Gera para o mês anterior a hoje
    logger.info(f"\nGerando relatório para o mês de referência: {(today - relativedelta(months=1)).strftime('%Y-%m')}")
    generator.generate_monthly_report() 

    # Gera para 2 meses atrás
    logger.info(f"\nGerando relatório para o mês de referência: {(today - relativedelta(months=2)).strftime('%Y-%m')}")
    generator.generate_monthly_report(simulation_date=today - relativedelta(months=1))

    # Gera para 3 meses atrás
    logger.info(f"\nGerando relatório para o mês de referência: {(today - relativedelta(months=3)).strftime('%Y-%m')}")
    generator.generate_monthly_report(simulation_date=today - relativedelta(months=2))


    logger.info("\n--- GERAÇÃO MANUAL CONCLUÍDA ---")
    logger.info("Verifique a pasta /relatorios para os arquivos PDF.")

if __name__ == "__main__":
    main()
