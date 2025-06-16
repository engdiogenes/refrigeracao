import streamlit as st
import math

# Função para calcular potência elétrica
def calcular_potencia(tensao, corrente, tipo_sistema, fator_potencia=0.95):
    if tipo_sistema == "Monofásico (220V F+N)":
        potencia = tensao * corrente * fator_potencia
        formula = f"P = V × I × cos(φ) = {tensao} × {corrente} × {fator_potencia} = {potencia:.2f} W"
    elif tipo_sistema == "Trifásico (220V + 220V + 220V)":
        potencia = math.sqrt(3) * tensao * corrente * fator_potencia
        formula = f"P = √3 × V × I × cos(φ) = 1.732 × {tensao} × {corrente} × {fator_potencia} = {potencia:.2f} W"
    else:
        potencia = 0
        formula = "Tipo de sistema não reconhecido."
    return potencia, formula

# Função para estimar COP
def estimar_cop(capacidade_kw, potencia_eletrica):
    if potencia_eletrica == 0:
        return 0, "Potência elétrica é zero, COP indefinido."
    cop = capacidade_kw / (potencia_eletrica / 1000)
    formula = f"COP = Capacidade (kW) / Potência (kW) = {capacidade_kw:.2f} / ({potencia_eletrica:.2f} / 1000) = {cop:.2f}"
    return cop, formula

# Faixa esperada de COP
def faixa_cop(cop):
    if cop < 2.5:
        return "🔴 COP abaixo do ideal (esperado: 2.5 a 4.0)"
    elif 2.5 <= cop <= 4.0:
        return "🟢 COP dentro da faixa ideal (2.5 a 4.0)"
    else:
        return "🟡 COP acima do esperado (pode indicar erro de medição ou sistema superdimensionado)"

# Função para verificar temperatura de descarga
def verificar_temperatura_descarga(temp_descarga):
    if temp_descarga > 110:
        return "⚠️ Temperatura de descarga muito alta! Verifique o sistema."
    elif temp_descarga < 70:
        return "⚠️ Temperatura de descarga muito baixa! Pode indicar subcarga."
    else:
        return "✅ Temperatura de descarga dentro do intervalo esperado."

# Conversão de capacidade para kW
def converter_para_kw(valor, unidade):
    if unidade == "kW":
        return valor, f"{valor} kW (sem conversão)"
    elif unidade == "BTU/h":
        convertido = valor * 0.00029307107
        return convertido, f"{valor} BTU/h × 0.00029307107 = {convertido:.2f} kW"
    elif unidade == "TR (toneladas de refrigeração)":
        convertido = valor * 3.51685
        return convertido, f"{valor} TR × 3.51685 = {convertido:.2f} kW"
    else:
        return 0, "Unidade não reconhecida."

# Interface Streamlit
st.title("Calculadora de Performance de Ar-Condicionado Split")

st.header("Entradas do Sistema")
tipo_sistema = st.selectbox("Tipo de Alimentação Elétrica", ["Monofásico (220V F+N)", "Trifásico (220V + 220V + 220V)"])
tensao = st.number_input("Tensão (V)", min_value=0.0, value=220.0)
corrente = st.number_input("Corrente (A)", min_value=0.0, value=5.0)

unidade_capacidade = st.selectbox("Unidade da Capacidade de Refrigeração", ["kW", "BTU/h", "TR (toneladas de refrigeração)"])
capacidade_valor = st.number_input(f"Capacidade de Refrigeração ({unidade_capacidade})", min_value=0.0, value=12000.0)

temperatura_ambiente = st.number_input("Temperatura Ambiente (°C)", min_value=-10.0, value=25.0)
temperatura_evaporadora = st.number_input("Temperatura da Evaporadora (°C)", min_value=-10.0, value=12.0)
temperatura_descarga = st.number_input("Temperatura de Descarga do Compressor (°C)", min_value=0.0, value=90.0)

if st.button("Calcular Performance"):
    capacidade_kw, formula_capacidade = converter_para_kw(capacidade_valor, unidade_capacidade)
    potencia, formula_potencia = calcular_potencia(tensao, corrente, tipo_sistema)
    cop, formula_cop = estimar_cop(capacidade_kw, potencia)
    alerta_temp = verificar_temperatura_descarga(temperatura_descarga)
    faixa = faixa_cop(cop)

    st.subheader("Resultados")
    st.write(f"🔌 Potência Elétrica Estimada: **{potencia:.2f} W**")
    st.write(f"❄️ Capacidade de Refrigeração: **{capacidade_kw:.2f} kW**")
    st.write(f"📈 Coeficiente de Performance (COP): **{cop:.2f}**")
    st.write(f"{faixa}")
    st.write(f"🌡️ {alerta_temp}")

    st.subheader("🧮 Cálculos Realizados")
    st.markdown(f"- Conversão de Capacidade: `{formula_capacidade}`")
    st.markdown(f"- Cálculo da Potência Elétrica: `{formula_potencia}`")
    st.markdown(f"- Cálculo do COP: `{formula_cop}`")

    st.subheader("📚 Embasamento Teórico")
    st.markdown("""
    - **Potência Elétrica (P)**:
      - Monofásico: `P = V × I × cos(φ)`
      - Trifásico: `P = √3 × V × I × cos(φ)`
      - Onde `cos(φ)` é o fator de potência (assumido como 0.95)

    - **Capacidade de Refrigeração**:
      - 1 TR = 3.51685 kW
      - 1 BTU/h = 0.00029307107 kW

    - **COP (Coeficiente de Performance)**:
      - `COP = Capacidade de Refrigeração (kW) / Potência Elétrica (kW)`
      - Faixa ideal: entre 2.5 e 4.0
      - Indica a eficiência do sistema: quanto maior o COP, mais eficiente é o equipamento.

    - **Temperatura de Descarga**:
      - Faixa ideal: entre 70°C e 110°C
      - Fora dessa faixa pode indicar problemas como subcarga ou superaquecimento.
    """)
    # Diagnóstico inteligente com sugestões
    st.subheader("🧠 Sugestões Inteligentes para Melhorar o COP")

    if cop < 2.5:
        st.markdown("""
        O COP está abaixo da faixa ideal. Aqui estão algumas ações recomendadas para melhorar a eficiência do sistema:

        - 🧼 **Limpeza de filtros e serpentinas**: sujeira acumulada reduz a troca térmica.
        - 🌡️ **Verificação de carga de gás refrigerante**: subcarga ou sobrecarga afetam o desempenho.
        - 🔍 **Inspeção de obstruções no fluxo de ar**: verifique se há bloqueios nas entradas e saídas de ar.
        - 📸 **Termografia no compressor e conexões elétricas**: pode revelar pontos de aquecimento anormal.
        - 🧪 **Análise de óleo e vibração**: útil para detectar desgaste precoce em compressores.
        - 🧰 **Verificação do isolamento térmico das tubulações**: perdas térmicas afetam a eficiência.
        - 🔄 **Avaliação do dimensionamento do equipamento**: sistemas superdimensionados ou subdimensionados operam com baixa eficiência.

        > 💡 **Dica Inteligente**: Se a temperatura de descarga estiver alta e o COP baixo, isso pode indicar **sobrecarga térmica no compressor**. Considere realizar uma inspeção termográfica e verificar o estado do capacitor de partida.
        """)
    else:
        st.markdown("✅ O COP está dentro da faixa ideal. Continue com a manutenção preventiva regular para manter a eficiência do sistema.")

