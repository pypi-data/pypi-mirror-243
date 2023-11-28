READONLY;

SET $tslot = -1;

CREATE VIEW manda_gene_body AS
SELECT varno, datum_status@body
FROM  index, hdr, body
WHERE timeslot = $tslot
