//
//-- ODB/SQL file 'nak_resat_averaging_kernel.sql'
//
//   New:  12-Sep-2005
//

SET $tslot = -1;

CREATE VIEW nak_resat_averaging_kernel AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         nak                           // r/o
//    FROM timeslot_index, index, hdr, sat, resat, resat_averaging_kernel
FROM   timeslot_index, index, hdr, sat, resat, resat_averaging_kernel
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
     AND obstype = $satem AND codetype = $resat
;
