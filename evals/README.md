# Casi di prova

Servono a verificare che una modifica a `core/` o `templates/` non peggiori le
skill. Ci sono due livelli.

## 1. Controllo meccanico

`scripts/verifica_testo.py` controlla le regole misurabili: frase SEO entro
191 caratteri, Threads entro 500, prima riga Instagram entro 125, niente link
nella didascalia Instagram, niente hashtag nel testo, hashtag consigliati senza
accenti, trattino breve nella denominazione, slug valido, numero di emoji,
ordinali sospetti (`9° posizione`, `3° nelle`), costruzioni tipiche dei testi
generati (contrapposizioni a effetto, domande con risposta immediata, "E voi",
frasi fatte: solo avvisi).

```bash
python3 scripts/verifica_testo.py output.md
```

Per un testo copiato al volo: `python3 scripts/verifica_testo.py -`, incolla e
chiudi con Ctrl+D (Ctrl+Z e Invio su Windows). Gli **errori** vanno corretti;
gli **avvisi** vanno valutati (un flash ha legittimamente 3-4 emoji). La CI
esegue lo script sugli esempi in `examples/`.

Lo script non verifica lo stile, l'ordine dei contenuti né il genere degli
atleti: quello resta ai casi del punto 2.

## 2. Casi per skill-creator

`social-progetto-ciclismo/evals.json` ed `editorial-progetto-ciclismo/evals.json`
contengono richieste tipiche e le aspettative da verificare, nel formato della
skill `skill-creator`. Per usarli, chiedi a Claude con skill-creator attiva:
"esegui gli eval di social-progetto-ciclismo" indicando questa cartella, prima
e dopo una modifica, e confronta i risultati.

## Aggiungere un caso

Prendi spunto dai post e dagli articoli pubblicati per la **struttura** (tipo
di input, numero di fronti, categorie, casi difficili), ma **inventa i dati da
zero**: nomi, località minori, piazzamenti. Non copiare né pseudonimizzare
contenuti reali (vedi [docs/privacy.md](../docs/privacy.md)). Usa `example.org`
per i link.

Ogni caso ha:

- `prompt`: la richiesta come la scriverebbe chi gestisce la comunicazione;
- `expected_output`: una descrizione di com'è fatta la risposta giusta;
- `expectations`: affermazioni verificabili una per una.
