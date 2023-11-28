//
//-- ODB/SQL file 'ecmwf_matchupsink.sql'
//
//   updated     :  23-Nov-2007
//   Last updated:  22-Apr-2009
//   changed to
//   paral($pe, procid - $hdr_min + 1)
//   and NOT paral($pe, target - $hdr_min + 1)
//

SET $tslot = -1;
SET $pe = 0;
SET $sensor = -1;
SET $hdr_min = 1; // Here: the smallest procid (=global poolno) of the obs.grp. (ECMA)
SET $hdr_max = 0; // Here: the number of pools in (output) ECMA-database

UPDATABLE;
CREATE VIEW ecmwf_matchupsink AS
  SELECT seqno  READONLY,        // r/o
         skintemp[1:($NMXUPD+1)]@radiance,
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
