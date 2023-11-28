//
//-- ODB/SQL file 'sat_aeolus.sql'
//
//   Last updated:  17-04-2012
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_aeolusl2c AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         azimuth  READONLY,    // r/o
         hlos_ob_err       UPDATED, // possibly updated 
         hlos_fg           UPDATED, // possibly updated
         u_fg              UPDATED, // possibly updated
         u_fg_err          UPDATED, // possibly updated
         v_fg              UPDATED, // possibly updated
         v_fg_err          UPDATED, // possibly updated
         hlos_fg_err       UPDATED, // possibly updated
         hlos_an           UPDATED, // possibly updated
         hlos_an_err       UPDATED, // possibly updated
         u_an              UPDATED, // possibly updated
         v_an              UPDATED, // possibly updated
    FROM timeslot_index, index, hdr, sat, aeolus_hdr, aeolus_l2c
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $lidar
     AND codetype = 187
 ORDERBY seqno
;
