//
//-- ODB/SQL file 'robhdr_mwave_count_smos.sql'
//

READONLY; // .. except where  UPDATED qualifier was found

SET $hdr_min = 999;   // changed in the call to GETDB
SET $hdr_max = 0;     // changed in the call to GETDB
SET $all = -1;

CREATE VIEW robhdr_mwave_count_smos AS
  SELECT obsvalue,              
  FROM  hdr, body, smos, timeslot_index
  WHERE (timeslot@timeslot_index BETWEEN $hdr_min AND $hdr_max) AND reportype == 18001 AND obstype == 7 AND varno == 190 and polarisation == $all

