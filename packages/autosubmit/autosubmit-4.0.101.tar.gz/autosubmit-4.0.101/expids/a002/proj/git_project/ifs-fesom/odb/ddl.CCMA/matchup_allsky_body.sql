//
//-- ODB/SQL file 'matchup_allsky_body.sql'
//
//   Created:  10-May-2010
//
//

SET $tslot = -1;
SET $pe = 0;
SET $sensor = -1;
SET $hdr_min = 1; // Here: the smallest procid (=global poolno) of the obs.grp. (ECMA)
SET $hdr_max = 0; // Here: the number of pools in (output) ECMA-database

CREATE VIEW matchup_allsky_body AS
  SELECT seqno  READONLY,            // r/o
         entryno  READONLY,          // r/o
         datum_tbflag@allsky_body UPDATED         // mwave (all-sky) observations
    FROM timeslot_index, index, hdr, body, allsky_body
   WHERE target > 0
     AND 1 <= procid - $hdr_min + 1 <= $hdr_max
     AND (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active@hdr
     AND datum_status.active@body
     AND obstype = $allsky
     AND codetype = $ssmi
     AND (($sensor == -1) OR (sensor == $sensor))
     AND paral($pe, procid - $hdr_min + 1)
;

