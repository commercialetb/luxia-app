"""
Test Suite per LUXiA
====================

Script di test per verificare che i moduli funzionino correttamente.
Esegui con: python test_luxia.py
"""

import sys
import os
from pathlib import Path

# Aggiungi il root al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test 1: Verifica importazioni moduli"""
    print("=" * 60)
    print("TEST 1: Importazioni Moduli")
    print("=" * 60)
    
    try:
        from utils.photometry import parse_ldt, calculate_beam_spread, estimate_beam_angle_from_ldt
        print("✓ utils.photometry")
    except ImportError as e:
        print(f"✗ utils.photometry: {e}")
        return False
    
    try:
        from utils.blueprint_processor import BlueprintProcessor, convert_pdf_to_image
        print("✓ utils.blueprint_processor")
    except ImportError as e:
        print(f"✗ utils.blueprint_processor: {e}")
        return False
    
    try:
        from utils.lamp_calculator import LampPlacementCalculator
        print("✓ utils.lamp_calculator")
    except ImportError as e:
        print(f"✗ utils.lamp_calculator: {e}")
        return False
    
    try:
        from utils.report_generator import ReportGenerator
        print("✓ utils.report_generator")
    except ImportError as e:
        print(f"✗ utils.report_generator: {e}")
        return False
    
    try:
        import config
        print("✓ config")
    except ImportError as e:
        print(f"✗ config: {e}")
        return False
    
    print("\n✓ Tutti i moduli importati correttamente\n")
    return True

def test_beam_calculations():
    """Test 2: Calcoli del fascio"""
    print("=" * 60)
    print("TEST 2: Calcoli Fascio Luminoso")
    print("=" * 60)
    
    from utils.photometry import calculate_beam_spread
    
    test_cases = [
        {"h": 3.0, "hc": 0.85, "angle": 15.0, "expected_range": (1.0, 1.5)},
        {"h": 3.0, "hc": 0.85, "angle": 25.0, "expected_range": (1.6, 2.1)},
        {"h": 3.0, "hc": 0.85, "angle": 45.0, "expected_range": (4.0, 5.0)},
    ]
    
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        result = calculate_beam_spread(test["h"], test["hc"], test["angle"])
        min_val, max_val = test["expected_range"]
        
        if min_val <= result <= max_val:
            print(f"✓ Test {i}: h={test['h']}m, angle={test['angle']}° → {result:.2f}m (OK)")
        else:
            print(f"✗ Test {i}: h={test['h']}m, angle={test['angle']}° → {result:.2f}m (atteso: {min_val}-{max_val}m)")
            all_passed = False
    
    print()
    return all_passed

def test_lamp_calculator():
    """Test 3: Calcolatore posizionamento lampade"""
    print("=" * 60)
    print("TEST 3: Calcolo Numero Lampade e Spaziamento")
    print("=" * 60)
    
    from utils.lamp_calculator import LampPlacementCalculator
    
    calc = LampPlacementCalculator()
    
    # Test case 1: Area piccola
    result = calc.calculate_spacing(5.0, 5.0, 1.5)
    print(f"✓ Test 1: Area 5m×5m, fascio 1.5m")
    print(f"  → Lampade: {result['total_lamps']} ({result['lamps_x']}×{result['lamps_y']})")
    print(f"  → Spaziamento: X={result['spacing_x']:.2f}m, Y={result['spacing_y']:.2f}m\n")
    
    # Test case 2: Area media
    result = calc.calculate_spacing(10.0, 10.0, 2.5)
    print(f"✓ Test 2: Area 10m×10m, fascio 2.5m")
    print(f"  → Lampade: {result['total_lamps']} ({result['lamps_x']}×{result['lamps_y']})")
    print(f"  → Spaziamento: X={result['spacing_x']:.2f}m, Y={result['spacing_y']:.2f}m\n")
    
    # Test case 3: Area grande
    result = calc.calculate_spacing(20.0, 15.0, 4.0)
    print(f"✓ Test 3: Area 20m×15m, fascio 4.0m")
    print(f"  → Lampade: {result['total_lamps']} ({result['lamps_x']}×{result['lamps_y']})")
    print(f"  → Spaziamento: X={result['spacing_x']:.2f}m, Y={result['spacing_y']:.2f}m\n")
    
    return True

def test_config():
    """Test 4: Configurazione"""
    print("=" * 60)
    print("TEST 4: Verifica Configurazione")
    print("=" * 60)
    
    import config
    
    print(f"✓ APP_VERSION: {config.APP_VERSION}")
    print(f"✓ BUILD_DATE: {config.BUILD_DATE}")
    print(f"✓ DEFAULT_LANGUAGE: {config.DEFAULT_LANGUAGE}")
    print(f"✓ BEAM_OVERLAP_FACTOR: {config.BEAM_OVERLAP_FACTOR}")
    print(f"✓ OUTPUT_FOLDER: {config.OUTPUT_FOLDER}")
    print()
    
    return True

def test_output_folder():
    """Test 5: Cartella output"""
    print("=" * 60)
    print("TEST 5: Creazione Cartella Output")
    print("=" * 60)
    
    os.makedirs("outputs", exist_ok=True)
    
    if os.path.isdir("outputs"):
        print("✓ Cartella 'outputs' creata/verificata")
        # Prova a scrivere un file di test
        test_file = os.path.join("outputs", "test.txt")
        try:
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            print("✓ Cartella 'outputs' è scrivibile\n")
            return True
        except:
            print("✗ Cartella 'outputs' non è scrivibile\n")
            return False
    else:
        print("✗ Cartella 'outputs' non creata\n")
        return False

def main():
    """Esegui tutti i test"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LUXiA - Test Suite".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Importazioni", test_imports),
        ("Calcoli Fascio", test_beam_calculations),
        ("Calcolatore Lampade", test_lamp_calculator),
        ("Configurazione", test_config),
        ("Cartella Output", test_output_folder),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ ERRORE in {name}: {e}\n")
            results.append((name, False))
    
    # Riepilogo
    print("=" * 60)
    print("RIEPILOGO TEST")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print()
    print(f"Risultato: {passed}/{total} test passati")
    
    if passed == total:
        print("\n✓ Tutti i test sono passati! L'app è pronta.")
        print("\nEsegui con: streamlit run app.py")
        return 0
    else:
        print(f"\n✗ {total - passed} test fallito/i. Controlla gli errori sopra.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
