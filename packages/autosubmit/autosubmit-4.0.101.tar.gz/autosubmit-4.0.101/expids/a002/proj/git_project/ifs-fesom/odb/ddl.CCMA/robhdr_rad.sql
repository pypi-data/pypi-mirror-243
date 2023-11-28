//
//-- ODB/SQL file 'robhdr_rad.sql'
//
//   Last updated:  30-10-17
//

READONLY; // .. except where  UPDATED qualifier was found

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW robhdr_rad AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         obstype,
         codetype,                     // r/o
	     date, time,                   // r/o
         lat, lon,                     // r/o
         skintemper,
         skintemp[1:($NMXUPD+1)],
         cldne[1:3],
         cldptop[1:3],
         zenith,
         azimuth  READONLY,    // r/o
         solar_zenith  READONLY,       // r/o
         solar_azimuth  READONLY,      // r/o
         scanpos,
         lsm_fov,
  FROM   timeslot_index, index, hdr, sat, radiance
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
          (timeslot@timeslot_index == $tslot))
    AND kset = $kset
    AND obstype = $satem 
    AND codetype = $atovs
;
