"""Dev-only iteration on the rules baseline (never touches test)."""
from prel import evaluate as E

rep, gold, mem, texts = E.load_all()
dev = mem["dev"]
pred = E.run_rules(dev, texts)
print(E.fmt(E.tables(dev, gold, pred)))
