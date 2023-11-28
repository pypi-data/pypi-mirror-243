//
//-- ODB/SQL file 'ak_resat_averaging_kernel.sql'
//
//   New:  13-Jul-2005
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW ak_resat_averaging_kernel AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         nak,                          // r/o
         obs_ak_error,                 // r/o
         pak[1:$mx_ak],                // r/o
         wak[1:$mx_ak],                // r/o
         apak[1:$mx_ak]                // r/o
    FROM timeslot_index, index, hdr, sat, resat, resat_averaging_kernel, errstat
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $satem AND codetype = $resat
 ORDERBY seqno
;
