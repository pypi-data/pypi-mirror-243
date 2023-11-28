//
//-- ODB/SQL file 'update_hprior_31.sql'
//
//   Last updated:  24/02/10
//   By          :  Anne Fouilloux

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW update_hprior_31 AS
  SELECT
    seqno, entryno, 
    obsvalue,
    an_depar,
    hprior UPDATED,
    FROM   timeslot_index, index, hdr, body, ensemble, enkf[min($NMXENKF,31)]
    WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset

;

