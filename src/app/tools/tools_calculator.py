from langchain.tools import tool

@tool
def multiply(a: float, b: float) -> float:
    """
    Multiplie deux nombres.

    Arguments :
    - a : premier nombre
    - b : second nombre

    Retourne :
    - Le produit de a et b
    """
    return a * b
