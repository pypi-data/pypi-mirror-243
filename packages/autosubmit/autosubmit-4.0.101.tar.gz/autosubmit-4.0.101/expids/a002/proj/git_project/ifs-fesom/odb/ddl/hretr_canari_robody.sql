//
//-- ODB/SQL file 'hretr_canari_robody.sql'
//
//   Last updated:  12-Aug-2004
//

READONLY;

SET $kset = 0;

CREATE VIEW hretr_canari_robody AS
  SELECT seqno,
         varno,
         vertco_type@body,
         mf_log_p UPDATED,
         vertco_reference_1 UPDATED,
         pers_error,
         repres_error,
  FROM   index, hdr, body, errstat
  WHERE  kset = $kset
;
