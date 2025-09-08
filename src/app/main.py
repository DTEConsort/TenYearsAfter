Pour ajouter des logs à chaque fonction, vous pouvez utiliser le module `logging` de Python. Voici comment vous pouvez améliorer votre code :

```python
import logging

def run():
    logging.info('Execution de la fonction run')
    print("✅ Base OK : environnement opérationnel.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Début du script')
    run()
    logging.info('Fin du script')
```

Dans ce code, `logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')` configure le niveau de log à INFO, ce qui signifie que tous les messages de niveau INFO et supérieur seront enregistrés. Le format spécifié inclut le temps auquel le log a été enregistré, le niveau de gravité du message et le message lui-même.

`logging.info('Début du script')`, `logging.info('Execution de la fonction run')` et `logging.info('Fin du script')` sont utilisés pour enregistrer des messages de niveau INFO au début du script, lors de l'exécution de la fonction `run` et à la fin du script respectivement.