//
//-- ODB/SQL file 'fcdepar_10.sql'
//
//   Last updated:  06/09/10
//   By          :  Gabor Radnoti 

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW fcdepar_10 AS
  SELECT
    seqno, entryno, 
    an_depar,
    fc_depar UPDATED,
    fc_step UPDATED,
    FROM   timeslot_index, index, hdr, body, fcdiagnostic, fcdiagnostic_body[min(10,$nmxfcdiag)]
    WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset

;

