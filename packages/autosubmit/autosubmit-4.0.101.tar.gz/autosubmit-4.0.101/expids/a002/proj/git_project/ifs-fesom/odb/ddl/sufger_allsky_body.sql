//
//-- ODB/SQL file 'sufger_allsky_body.sql'
//
//   Last updated:  08-Sep-2013
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_allsky_body AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_tbflag,
  FROM   timeslot_index, index, hdr, body, allsky, allsky_body
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset
;
