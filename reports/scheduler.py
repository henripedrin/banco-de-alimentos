from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .generator import ReportGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")

def schedule_monthly_report():
    """
    Agenda a tarefa de geração de relatório para rodar todo mês.
    """
    logger.info("Agendando a tarefa de geração de relatório mensal.")
    
    # O APScheduler executa funções síncronas em um thread pool por padrão,
    # então podemos chamar a função diretamente sem um wrapper.
    report_generator = ReportGenerator()
    
    scheduler.add_job(
        func=report_generator.generate_monthly_report,
        trigger='cron',
        day=1,
        hour=0,
        minute=0,
        id='monthly_report_job',
        name='Gera o relatório consolidado do mês anterior',
        replace_existing=True
    )

def start_scheduler():
    logger.info("Iniciando o agendador de tarefas...")
    scheduler.start()

def shutdown_scheduler():
    logger.info("Encerrando o agendador de tarefas...")
    scheduler.shutdown()
