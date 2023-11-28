//
//-- ODB/SQL file 'matchup_atovs_pred.sql'
//
//   Last updated:  22-Jun-2005
//

SET $tslot = -1;
SET $pe = 0;
SET $sensor = -1;
SET $hdr_min = 1; // Here: the smallest procid (=global poolno) of the obs.grp. (ECMA)
SET $hdr_max = 0; // Here: the number of pools in (output) ECMA-database

CREATE VIEW matchup_atovs_pred AS
  SELECT seqno  READONLY,                         // r/o
         "/skintemp.*@radiance/"          // update all non-MDIs

    FROM timeslot_index, index, hdr, sat, radiance
   WHERE target > 0
     AND 1 <= procid - $hdr_min + 1 <= $hdr_max
     AND (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active
     AND obstype = $satem
     AND codetype = $atovs
     AND (($sensor == -1) OR (sensor == $sensor))
     AND paral($pe, procid - $hdr_min + 1)
;
