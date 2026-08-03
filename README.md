# Club Communications Toolkit

Prompt strutturati per la comunicazione di una società ciclistica giovanile:
**contenuti social** e **redazione per il sito web**.

Sviluppato per l'**[A.S.D. Progetto Ciclismo - Rodengo Saiano](https://www.asdprogettociclismorodengosaiano.it/)**,
società affiliata FCI attiva nelle categorie Giovanissimi, Esordienti e Allievi.

Il progetto è **agnostico rispetto al modello**: un unico contenuto sorgente
viene assemblato in adapter per Claude Skills, Gemini Gems, OpenAI GPTs e
qualunque API con system prompt.

> **Tutti i contenuti riguardano minori.** Leggi
> [docs/privacy.md](docs/privacy.md) prima di usare questi strumenti con dati
> reali.

## Le due skill

| Skill | Cosa fa |
|---|---|
| **social** | Post pre-gara, risultati, caption per reel e foto, storie Instagram, annunci di canali, saluti di fine stagione |
| **editorial** | Articoli per il sito, resoconti gara, comunicati societari, convocazioni, frasi SEO |

Condividono un modulo di identità comune (denominazione, missione, categorie,
colori, territorio) e le regole di tutela dei minori. Divergono su tono,
formato e lunghezza degli output.

## Input tipici

### Skill social

| Input | Output generato |
|---|---|
| Lista "prossime gare" con località, orari, categorie | Post pre-gara |
| Lista risultati per categoria | Tre versioni: completa, sintetica, story |
| Foto + richiesta di didascalia | Caption 2 frasi + alternativa breve |
| Nomi e motivo di una convocazione | Comunicato breve |
| Elenco atleti in uscita a fine stagione | Post di ringraziamento |

### Skill editorial

| Input | Output generato |
|---|---|
| Dati gara (denominazione, località, distanza, partenza) | Annuncio gara + frase SEO |
| Risultati per categoria | Resoconto con cronaca + frase SEO |
| Verbale o esito di assemblea | Comunicato societario |
| Convocazione FCI | Comunicato breve |

Un esempio completo è in
[examples/sample-input-risultati.md](examples/sample-input-risultati.md), con gli
output corrispondenti per entrambe le skill.

### Se mancano dei dati

Le skill procedono in best-effort e producono comunque il contenuto. Se manca un
dato essenziale (es. il nome dell'atleta da ringraziare), lo segnalano in una
riga e forniscono la versione generica. Non fanno domande su dettagli minori.

## Installazione

### Claude (Skills)

Comprimi `adapters/claude-skill/social-progetto-ciclismo/` in un `.zip`,
rinominalo `.skill` e caricalo dalle impostazioni. Stessa procedura per
`editorial-progetto-ciclismo/`.

### Gemini (Gems)

Crea due Gem distinte e incolla il contenuto di
`adapters/gemini-gem/social-instructions.md` e
`adapters/gemini-gem/editorial-instructions.md`.

### OpenAI (GPT personalizzati)

Come sopra, con i file in `adapters/openai-gpt/`.

### API generica

Usa i file in `adapters/generic/` come system prompt.

## Struttura del repository

```
core/shared/        Identità societaria e regole comuni alle due skill
core/social/        Regole specifiche dei contenuti social
core/editorial/     Regole specifiche della redazione web
templates/          Template di output a struttura fissa
adapters/           Versioni generate per ciascuna piattaforma
examples/           Input e output di esempio (dati fittizi)
docs/               Privacy, linee guida di identità
scripts/            Helper per il build
build.sh            Assembla gli adapter da core/ e templates/
```

**Modifica sempre `core/` e `templates/`, mai gli adapter.** Gli adapter sono
generati:

```
./build.sh
```

Il modulo `core/shared/` finisce in entrambe le skill: una modifica all'identità
societaria o alle regole sui minori si propaga automaticamente a tutti gli
output.

## Privacy

I contenuti riguardano atleti dai 6 ai 16 anni. Non committare mai elenchi
nominativi, risultati reali, foto o liberatorie. Vedi
[docs/privacy.md](docs/privacy.md).

## Contesto e attribuzione

Questo repository nasce dall'attività di comunicazione dell'**A.S.D. Progetto
Ciclismo - Rodengo Saiano** (Brescia), società dedicata al ciclismo giovanile.

Sito ufficiale: https://www.asdprogettociclismorodengosaiano.it/

I template e le regole editoriali sono condivisi pubblicamente perché possano
essere adattati da altre società sportive giovanili. L'identità in
`core/shared/00-identity.md` è il punto da sostituire per riusare il progetto
altrove.

## Licenza

MIT. Vedi [LICENSE](LICENSE).
