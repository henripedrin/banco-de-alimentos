import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from repository.relatorio_repository import RelatorioRepository
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'relatorios')

class ReportGenerator:
    def __init__(self):
        self.repository = RelatorioRepository()

    def generate_report(self, start_date: date, end_date: date, is_manual: bool = False):
        """
        Função genérica que gera um relatório para um período customizado.
        """
        period_str = f"{start_date.strftime('%Y-%m-%d')}_a_{end_date.strftime('%Y-%m-%d')}"
        reference_month_str = start_date.strftime('%Y-%m') if start_date.day == 1 and (end_date - start_date).days < 32 else period_str

        logger.info(f"Iniciando geração de relatório para o período: {start_date} a {end_date}")

        try:
            data = self.repository.get_data_for_report(start_date, end_date)
            
            prefix = "relatorio_manual" if is_manual else "relatorio_mensal"
            file_name = f"{prefix}_{period_str}.pdf"
            
            # Garante que o diretório de relatórios exista
            os.makedirs(REPORTS_DIR, exist_ok=True)
            file_path = os.path.join(REPORTS_DIR, file_name)

            self._create_pdf(file_path, reference_month_str, data)
            self.repository.save_report_metadata(file_name, reference_month_str, file_path)
            
            logger.info(f"Relatório '{file_name}' gerado com sucesso!")
            return {"file_name": file_name, "file_path": file_path}

        except Exception as e:
            logger.error(f"Falha ao gerar o relatório: {e}", exc_info=True)
            raise

    def generate_monthly_report(self, simulation_date: Optional[date] = None):
        """
        Wrapper para a tarefa agendada. Gera o relatório do mês anterior.
        """
        execution_date = simulation_date if simulation_date else date.today()
        end_date = execution_date.replace(day=1) - relativedelta(days=1)
        start_date = end_date.replace(day=1)
        
        self.generate_report(start_date, end_date, is_manual=False)

    def _create_pdf(self, file_path: str, reference_period: str, data: dict):
        """
        Cria o arquivo PDF com os dados fornecidos.
        """
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(inch, height - inch, "NutriRede - Relatório de Operações")
        
        c.setFont("Helvetica", 12)
        c.drawString(inch, height - inch - 20, f"Período de Referência: {reference_period}")
        c.drawString(inch, height - inch - 40, f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        y_position = height - 2 * inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, y_position, "Resumo Executivo")
        y_position -= 20
        c.line(inch, y_position, width - inch, y_position)
        y_position -= 20

        c.setFont("Helvetica", 11)
        
        doacoes = data.get('doacoes', {})
        cestas = data.get('cestas', {})
        entregas = data.get('entregas', {})
        
        summary_data = [
            f"Total de doações recebidas: {doacoes.get('total', 0) or 0}",
            f"  - Aprovadas: {doacoes.get('aprovadas', 0) or 0}",
            f"  - Rejeitadas: {doacoes.get('rejeitadas', 0) or 0}",
            f"Total de alimentos recebidos (unidades/kg/L): {data.get('alimentos_recebidos', 0) or 0}",
            f"Total de alimentos distribuídos (unidades/kg/L): {data.get('alimentos_distribuidos', 0) or 0}",
            f"Total de cestas montadas: {cestas.get('total_criadas', 0) or 0}",
            f"Total de entregas concluídas: {entregas.get('entregues', 0) or 0}",
        ]

        for line in summary_data:
            c.drawString(inch * 1.2, y_position, line)
            y_position -= 15

        y_position -= 30
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, y_position, "Doações")
        y_position -= 20
        c.line(inch, y_position, width - inch, y_position)
        y_position -= 20

        c.setFont("Helvetica-Bold", 11)
        c.drawString(inch * 1.2, y_position, "Top 5 Doadores do Período:")
        y_position -= 15
        
        c.setFont("Helvetica", 10)
        top_doadores = data.get('top_doadores', [])
        if top_doadores:
            for doador in top_doadores:
                c.drawString(inch * 1.4, y_position, f"- {doador['nome']} ({doador['total_doacoes']} doações)")
                y_position -= 12
        else:
            c.drawString(inch * 1.4, y_position, "Nenhum doador no período.")
            y_position -= 12

        c.save()
