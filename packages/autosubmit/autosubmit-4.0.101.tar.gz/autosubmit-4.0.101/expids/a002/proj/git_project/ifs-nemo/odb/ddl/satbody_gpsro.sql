//
//-- ODB/SQL file 'satbody_gpsro.sql'
//
//   New:  15-Mar-2011
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW satbody_gpsro AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
// For GNSSRO only
     bg_refractivity UPDATED,           // possibly updated
     bg_dndz UPDATED,          // possibly updated
     bg_layerno UPDATED,            // possibly updated
     bg_tvalue UPDATED,            // possibly updated for gnssro (MF) to be cleaned
	 obs_tvalue,                      // r/o for gnssro (MF) to be cleaned
	 obs_zvalue UPDATED,            // r/o for gnssro (MF) to be cleaned
    FROM timeslot_index, index, hdr, sat, gnssro, gnssro_body
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $limb AND codetype = $gpsro
 ORDERBY seqno
;
