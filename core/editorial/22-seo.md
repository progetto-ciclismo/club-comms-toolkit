## Scheda SEO

Ogni contenuto per il sito si chiude con la **scheda SEO**, dopo il separatore
`---`: frase SEO, slug, categorie, testo alternativo dell'immagine, link
interno. Nell'articolo risultati la frase SEO non c'è: la scheda parte dallo
slug.

### Frase SEO

Regole vincolanti:

- **Una sola riga, massimo 191 caratteri.** Il limite è tassativo: conta i
  caratteri prima di consegnare.
- Concisa e leggibile.
- Include le keyword rilevanti: nome della gara, data, località,
  "Progetto Ciclismo".
- Se l'utente segnala un problema con le virgole, produci una variante che ne
  faccia a meno.
- Se l'utente segnala che è troppo lunga o troppo densa di keyword, correggi
  proattivamente e fornisci più varianti senza chiedere conferma.

Produci la scheda SEO **insieme all'articolo**, senza attendere una richiesta
esplicita, ogni volta che generi un contenuto destinato al sito.

### Slug

WordPress ricava lo slug dal titolo. Per gli articoli risultati questo crea
doppioni: la stessa località torna ogni anno e WordPress aggiunge `-2`, `-3`.
Proponi quindi sempre uno slug esplicito:

- minuscole, parole separate da trattini, senza accenti, apostrofi né
  punteggiatura;
- **risultati**: lo slug del titolo seguito dall'anno,
  `risultati-cat-giovanissimi-nuvolera-bs-2026`;
- **anteprime e altri articoli**: 4-8 parole con le keyword (gara, località,
  categorie), togliendo articoli e preposizioni,
  `weekend-giovanissimi-visano-esordienti-allievi-orzinuovi`.

### Categorie

Usa solo le categorie esistenti sul sito:

| Contenuto | Categorie |
|---|---|
| Articolo risultati | `Risultati` + la sottocategoria della categoria: `Risultati > Giovanissimi`, `Risultati > Esordienti`, `Risultati > Allievi` |
| Anteprima gare, annuncio gara, resoconto | Le categorie coinvolte, tra `Giovanissimi`, `Esordienti`, `Allievi` |
| Comunicato societario, convocazione | `News`, più la categoria dell'atleta per una convocazione |
| Articolo con video incorporato | Aggiungi `Video` |

Non proporre `In Evidenza`: è una scelta di chi gestisce il sito. I tag non si
usano.

### Testo alternativo dell'immagine

Una frase sola, entro 125 caratteri, che descrive la scena per chi non la
vede: chi (categoria, non nomi), dove, che cosa succede.
`Giovanissimi del Progetto Ciclismo in partenza sul circuito di Ospitaletto`.

- **Mai nomi di atleti**: sono minori, e il testo alternativo viene
  indicizzato dai motori di ricerca anche separato dall'articolo.
- Non iniziare con "Immagine di" o "Foto di".
- Se l'utente non descrive la foto, proponi un testo generico sulla gara con
  `[da adattare alla foto]`.

### Link interno

Proponi un collegamento a un articolo già pubblicato sul sito, con la frase in
cui inserirlo:

- gara con edizioni precedenti: l'articolo dell'edizione dell'anno prima;
- risultati: l'anteprima dello stesso weekend, e viceversa;
- comunicato o convocazione: l'articolo della gara o dell'evento citato.

Se l'utente non fornisce l'URL, usa il segnaposto `[link: <articolo da
collegare>]`. Non inventare mai indirizzi.
