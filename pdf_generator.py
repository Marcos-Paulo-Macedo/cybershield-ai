from typing import List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

from threat_analyzer import DiagnosticoFraude

class GeradorRelatorio:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

    def _configurar_estilos(self):
        self.cor_principal = colors.HexColor("#202122")
        self.cor_cinza = colors.HexColor("#f8f9fa")
        self.cor_borda = colors.HexColor("#a2a9b1")
        self.cor_alerta = colors.HexColor("#b32400")

        self.styles.add(ParagraphStyle(
            'TituloDoc', parent=self.styles['Normal'], fontName='Times-Bold', fontSize=18, leading=22, textColor=self.cor_principal, spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            'SubtituloDoc', parent=self.styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#54595d"), spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            'CabecalhoSecao', parent=self.styles['Normal'], fontName='Times-Bold', fontSize=12, leading=15, textColor=self.cor_principal, spaceBefore=10, spaceAfter=4, keepWithNext=True
        ))
        self.styles.add(ParagraphStyle(
            'TextoPadrao', parent=self.styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=self.cor_principal, spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            'ItemLista', parent=self.styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=self.cor_principal, leftIndent=10, spaceAfter=2
        ))
        self.styles.add(ParagraphStyle(
            'ItemAlerta', parent=self.styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=self.cor_alerta, spaceAfter=2
        ))

    def _cabecalho(self, titulo: str) -> List:
        conteudo = [
            [Paragraph("<b>WIKIFRAUDES</b> &nbsp;|&nbsp; BASE DE CONHECIMENTO", ParagraphStyle('Sub', parent=self.styles['Normal'], fontName='Helvetica-Bold', fontSize=7, textColor=colors.HexColor("#54595d")))],
            [Paragraph(titulo, self.styles['TituloDoc'])],
            [Paragraph("Relatório gerado a partir de consulta de ocorrência", self.styles['SubtituloDoc'])]
        ]
        tabela = Table(conteudo, colWidths=[180*mm])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), self.cor_cinza),
            ('BOX', (0,0), (-1,-1), 0.5, self.cor_borda),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        return [tabela, Spacer(1, 8)]

    def gerar_pdf(self, dados: DiagnosticoFraude, caminho_saida: str) -> str:
        doc = SimpleDocTemplate(caminho_saida, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
        elementos = []

        elementos.extend(self._cabecalho(dados.nome_incidente))

        resumo_data = [[
            Paragraph(f"<b>Descrição:</b><br/>{dados.resumo_tecnico}", self.styles['TextoPadrao']),
            Paragraph(f"<font size=14><b>{dados.nivel_complexidade}/10</b></font><br/><font size=6>COMPLEXIDADE</font>", ParagraphStyle('Score', parent=self.styles['Normal'], fontName='Helvetica-Bold', alignment=1, textColor=self.cor_alerta if dados.nivel_complexidade >= 7 else self.cor_principal))
        ]]
        tabela_resumo = Table(resumo_data, colWidths=[140*mm, 40*mm])
        tabela_resumo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, self.cor_borda),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elementos.append(tabela_resumo)
        elementos.append(Spacer(1, 6))

        elementos.append(Paragraph("1. Ficha Técnica do Evento", self.styles['CabecalhoSecao']))
        detalhes_data = [
            [Paragraph("<b>Vetor Principal:</b>", self.styles['TextoPadrao']), Paragraph(dados.detalhes.vetor, self.styles['TextoPadrao'])],
            [Paragraph("<b>Canal de Origem:</b>", self.styles['TextoPadrao']), Paragraph(dados.detalhes.canal, self.styles['TextoPadrao'])],
            [Paragraph("<b>Gatilho:</b>", self.styles['TextoPadrao']), Paragraph(dados.detalhes.gatilho, self.styles['TextoPadrao'])],
        ]
        tabela_detalhes = Table(detalhes_data, colWidths=[40*mm, 140*mm])
        tabela_detalhes.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, self.cor_borda),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        elementos.append(tabela_detalhes)
        elementos.append(Spacer(1, 6))

        elementos.append(Paragraph("2. Procedimentos Incidentais de Contenção", self.styles['CabecalhoSecao']))
        itens_emergencia = [
            Paragraph("<b>AÇÕES IMEDIATAS:</b>", ParagraphStyle('T', parent=self.styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=self.cor_alerta)),
            Spacer(1, 2)
        ]
        for passo in dados.protocolo_emergencia:
            itens_emergencia.append(Paragraph(f"• {passo}", self.styles['ItemAlerta']))

        caixa_emergencia = Table([[itens_emergencia]], colWidths=[180*mm])
        caixa_emergencia.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff5f5")),
            ('BOX', (0,0), (-1,-1), 0.5, self.cor_alerta),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elementos.append(caixa_emergencia)
        elementos.append(Spacer(1, 6))

        elementos.append(Paragraph("3. Recomendações Preventivas", self.styles['CabecalhoSecao']))
        for item in dados.medidas_preventivas:
            elementos.append(Paragraph(f"• {item}", self.styles['ItemLista']))

        doc.build(elementos)
        return caminho_saida