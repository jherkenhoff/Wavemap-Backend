# Controller-Backend


## Datenbank

##### Anforderungen:

- Lokal (Kein Server-Host Datenbanksystem)
- Schneller Lesezugriff (Andernfalls spürbare Verzögerung im Frontend)
- Keine kritischen Anforderungen an Schnelligkeit bei Schreibzugriff
- Austauschformat (Daten können als in sich geschlossene Dateien weitergegeben werden)
- Keine kritischen Anforderungen an Speicherverbrauch

##### Auswahl:

Das Datenbanksystem SQLite3 und das Dateiformat HDF5 erfällen all die genannten Anforderungen.


SQLite:
- Relationale Datenbank - Gute unterstützung für "sparse data" (z.B. Notitzen an einem Messwert)
- SQL ermöglicht vielseitige Queries
- Lineares Speichermodell - Evtl nicht ganz passend für den Anwendungsfall?


HDF5:
- Hierarchisches Datenformat - Gute Strukturierung möglich
- Attribute ermöglichen das abspeichern von Metadaten
- Compound datentypen - Sehr gute Abbildung der anfallenden Daten möglich
- Sehr schnelle Schreib- und Lesezugriffe (siehe benchmark.py)


##### Zusatzinfos:

In der ITU Empfehlung [ITU-R SM.2117-0](https://www.itu.int/dms_pubrec/itu-r/rec/sm/R-REC-SM.2117-0-201809-I!!PDF-E.pdf) (Data format definition for exchanging stored I/Q data for the purpose of spectrum monitoring) wird ein Format zur speicherung in HDF5 Dateien vorgestellt. Hier können sicher einige Ideen übernommen werden, jedoch bezieht sich das vorgestellte Format auf die Speicherung von I/Q Samples an einem fixen Ort.


