import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    unit_count = 0
    integration_count = 0
    analyzed = []
    skipped = []
    for test in terminalreporter.stats.get('passed', []):
        markers = {mark.name for mark in getattr(test, 'keywords', {}).values() if hasattr(mark, 'name')}
        if 'unit' in markers:
            unit_count += 1
        elif 'integration' in markers:
            integration_count += 1
        analyzed.append(f"✔ Analizado: {test.nodeid}")
    for test in terminalreporter.stats.get('skipped', []):
        markers = {mark.name for mark in getattr(test, 'keywords', {}).values() if hasattr(mark, 'name')}
        if 'unit' in markers:
            unit_count += 1
        elif 'integration' in markers:
            integration_count += 1
        reason = ""
        condition = ""
        if hasattr(test, 'longrepr') and isinstance(test.longrepr, tuple) and len(test.longrepr) > 2:
            reason = test.longrepr[2]
            condition = reason
        else:
            reason = "Sin motivo especificado"
            condition = "No se especificó condición."
        skipped.append(f"⏭ Saltado: {test.nodeid} - Motivo: {reason}\n    Condición: {condition}\n    ¿Afecta la ejecución?: {'No, es común en proyectos grandes si la condición está justificada.' if reason else 'Revisar el motivo.'}\n    ¿Es común?: Sí, es común saltar tests por condiciones específicas.")

    terminalreporter.write_sep("-", "RESUMEN DE TESTS PERSONALIZADO")
    for line in analyzed:
        terminalreporter.write_line(line)
    for line in skipped:
        terminalreporter.write_line(line)
    terminalreporter.write_sep("-", f"Total tests unitarios ejecutados: {unit_count}")
    terminalreporter.write_sep("-", f"Total tests integrales ejecutados: {integration_count}")
    terminalreporter.write_sep("-", "EXPLICACIÓN DEL INFORME")
    terminalreporter.write_line("✔ Analizado: Test ejecutado correctamente.")
    terminalreporter.write_line("⏭ Saltado: Test omitido por una condición. Se muestra el motivo y la condición exacta si está disponible.")
    terminalreporter.write_line("¿Afecta la ejecución?: Si el motivo del skip es esperado y documentado, no afecta la validez del resto de los tests.")
    terminalreporter.write_line("¿Es común?: Sí, es común saltar tests en proyectos grandes para evitar falsos negativos en entornos donde ciertas pruebas no aplican.")
    terminalreporter.write_line("Para distinguir entre tests unitarios e integrales, usa los marcadores @pytest.mark.unit y @pytest.mark.integration en tus tests.")

# Ejemplo de uso de marcadores en tus tests:
# import pytest
# @pytest.mark.unit
# def test_algo_unitario():
#     ...
# @pytest.mark.integration
# def test_algo_integral():
#     ...
