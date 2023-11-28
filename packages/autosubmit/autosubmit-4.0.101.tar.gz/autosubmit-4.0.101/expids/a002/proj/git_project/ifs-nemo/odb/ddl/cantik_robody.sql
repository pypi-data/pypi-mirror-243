//
//-- ODB/SQL file 'cantik_robody.sql'
//
//   Last updated:  01-11-2000
//

READONLY;

CREATE VIEW cantik_robody AS
  SELECT seqno,
         varno,
         datum_rdbflag@body,
         datum_anflag@body UPDATED,
         vertco_reference_1
  FROM   index, hdr, body
;
