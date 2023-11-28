//
//-- ODB/SQL file 'get_soe_resat.sql'
//
//   Last updated:  11-Oct-2006
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW get_soe_resat AS
  SELECT seqno  READONLY,        // r/o; MUST COME FIRST
         solar_elevation,        // r/o
         methane_correction UPDATED,        // r/o
         surface_height,        // r/o
         retrtype,
         cloud_top_press UPDATED,
  FROM   timeslot_index, index, hdr, sat, resat
  WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND kset = $kset
    AND obstype = $satem AND codetype = $resat
 ORDERBY seqno
;
