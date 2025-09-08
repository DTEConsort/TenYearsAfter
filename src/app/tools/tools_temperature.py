# src/app/tools/tools_temperature.py

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convertit une température de Celsius à Fahrenheit"""
    celsius = float(celsius)  # 🔧 conversion explicite
    return (celsius * 9 / 5) + 32