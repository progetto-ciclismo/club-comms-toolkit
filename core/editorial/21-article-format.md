## Tipi di articolo

Il sito pubblica due tipi di articolo, con convenzioni di titolo diverse e non
intercambiabili.

| Tipo | Quando | Convenzione di titolo |
|---|---|---|
| **Anteprima gare** | Prima del weekend o dell'infrasettimanale | Titolo giornalistico a due parti |
| **Risultati** | Dopo la gara | Titolo formulaico rigido |

### Titolo delle anteprime

Struttura a due parti separate dai due punti: **frase evocativa** + **dettaglio
concreto con località e categorie**.

Esempi pubblicati:

- `Inizia agosto: oggi i Giovanissimi a Coccaglio, domenica Esordienti nel Bergamasco e Allievi in Trentino`
- `Caccia al titolo bresciano: Giovanissimi a Roncadelle per il Provinciale, Esordienti e Allievi di scena a Pozzolengo`
- `Sotto le stelle di Soncino: i Giovanissimi protagonisti stasera nel 2° Memorial Linda Scaburri`
- `Il weekend inizia a tutta velocità: oggi il Provinciale Minisprint a Concesio, domenica sfide tra Bergamo e Brescia`
- `Tricolore a Firenze: Lorenzo Delbono convocato per i Campionati Italiani su Pista`

La prima parte crea atmosfera, la seconda dà l'informazione. Un titolo che ha
solo una delle due parti è fuori standard.

### Titolo dei risultati

Formato fisso, senza variazioni creative:

```
Risultati Cat. [Categoria] [specialità, se presente] – [Località] ([PROV])
```

Esempi pubblicati:

- `Risultati Cat. Giovanissimi – Nuvolento (BS)`
- `Risultati Cat. Allievi Pista – Crema (CR)`
- `Risultati Cat. Giovanissimi Minisprint – Soncino (CR)`
- `Risultati Cat. Giovanissimi Campionato Provinciale Minisprint M/F – Concesio (BS)`

Nota il trattino lungo prima della località e la sigla della provincia sempre
tra parentesi.

## Struttura dell'anteprima gare

### 1. Introduzione narrativa

Da 1 a 3 paragrafi. Registro caldo e discorsivo, prima persona plurale
("i nostri Giovanissimi", "la nostra formazione", "il nostro portacolori").

Elementi ricorrenti:

- Apertura che colloca la giornata nel calendario o nella stagione
- Date in grassetto inline: **sabato 1 agosto**, **domenica 2 agosto**
- Località descritte con colore geografico: "le strade bresciane di Coccaglio",
  "varcheranno il confine bergamasco", "trasferta in Trentino"
- Chiusura motivazionale breve

Dai risalto a: gare organizzate dalla società, debutti di categoria, campionati,
convocazioni, trasferte lontane.

### 2. Schede gara

Raggruppate per giorno, poi per categoria. Struttura:

```
##### **SABATO 1 AGOSTO**

##### Giovanissimi

- **Denominazione:** [nome ufficiale con numero di edizione]
- **Località:** [Comune] ([PROV])
- **Distanza:** [valore] Km
- **Partenza:** Ore [HH:MM]
- **Iscritti:** [numero] Atleti
```

Regole:

- Giorno e categoria sono **intestazioni**, non campi della scheda: non ripeterli
  come `Data:` o `Categoria:` nell'elenco.
- Quando Esordienti di primo e secondo anno corrono insieme, l'intestazione è
  `Esordienti 1° e 2° anno`.
- Per i circuiti, la voce Distanza descrive il format:
  "Circuito di 1.000 Km da ripetersi più volte in base alla categoria".
- Il numero di edizione della gara va sempre in forma ordinale: `2° GP Code
  Stampi`, `1° Memorial Bertamini Remo e Vittorio`.

### 3. Paragrafo finale

**Opzionale.** Le anteprime pubblicate si chiudono normalmente con le schede
gara, senza nota di coda.

Inseriscilo solo quando c'è qualcosa di concreto da dire:

- informazioni logistiche, se l'evento è organizzato dalla società (ritrovo,
  verifiche, punto di incontro DS, contatti iscrizioni);
- ringraziamento a staff, volontari e genitori in occasioni particolari.

Non aggiungere ringraziamenti generici di riempimento.

## Struttura dell'articolo risultati

Titolo formulaico, poi i piazzamenti della società raggruppati per
sottocategoria (G1-G6, femminile, primo e secondo anno).

Per i resoconti con cronaca: menziona al massimo i primi 3 per gara o batteria,
più la migliore prestazione femminile, e chiudi con la classifica di società
quando disponibile.

## Lunghezze

| Formato | Lunghezza |
|---|---|
| Anteprima gare | Introduzione 1-3 paragrafi + schede, circa 2 minuti di lettura |
| Articolo con cronaca | Fino a 400-700 parole |
| Comunicato stampa | 200-350 parole, più formale e compatto |
| Versione sintetica | 2-4 frasi |
| Versione "più breve" richiesta | Titolo + 1 paragrafo di introduzione + frase SEO |

## Template

Usa i template in `templates/editorial/`.
