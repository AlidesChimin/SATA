# Minimal import tests for SATA/ATAS with current src/ layout.
# These tests only verify that modules can be imported; they do not download heavy models.

def test_import_package():
    import processamento  # src/processamento/__init__.py should exist
    assert hasattr(processamento, "__package__")

def test_import_modules():
    import processamento.filtro_texto
    import processamento.converter_tabela
    import processamento.identificador_sexo
    import processamento.estatisticas_texto
    assert True
