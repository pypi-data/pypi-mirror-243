//
//-- ODB/SQL file 'update_hprior_44.sql'
//
//   Last updated:  24/02/10
//   By          :  Anne Fouilloux

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW update_hprior_44 AS
  SELECT
    seqno, entryno, 
    obsvalue,
    an_depar,
    hprior UPDATED,
    FROM   timeslot_index, index, hdr, body, ensemble, enkf[min($NMXENKF,44)]
    WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset

;

