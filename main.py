from src.detector import Detector

d = Detector("./resources", language="portuguese")
d.setup_pairs()
results = d.process()
print(results)
