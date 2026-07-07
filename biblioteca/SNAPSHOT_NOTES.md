# Snapshot Biblioteca

## Modifiche effettuate

- La view `biblioteca_iframe` ora serve un file snapshot locale invece del contenuto remoto.
- Il file snapshot viene letto da `biblioteca/biblioteca_iframe_snapshot.html`.
- Se il file snapshot è presente, viene servito direttamente e viene aggiunta una piccola indicazione discreta in basso a destra con data di creazione.
- Il testo mostra solo "Snapshot locale · data" senza ora.
- Lo snapshot non viene aggiornato automaticamente in futuro; va rigenerato manualmente se necessario.

## File coinvolti

- `biblioteca/views.py`
- `biblioteca/biblioteca_iframe_snapshot.html`
- `biblioteca/management/commands/snapshot_biblioteca_iframe.py`

## Come rigenerare lo snapshot

Eseguire:

```bash
cd /home/azureuser/IlViale
python3 scripts/take_biblioteca_snapshot.py
```
