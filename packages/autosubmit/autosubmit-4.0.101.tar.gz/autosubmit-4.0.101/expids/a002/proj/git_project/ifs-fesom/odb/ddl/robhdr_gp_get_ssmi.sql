//
//-- ODB/SQL file 'robhdr_gp_get_ssmi.sql'
//

READONLY; // .. except where  UPDATED qualifier was found

SET $tslot = -1;

CREATE VIEW robhdr_gp_get_ssmi AS
  SELECT seqno,                  // MDBONM (must be the first index; used to build MLNKH2B)
         lat,                    // MDBLAT
         lon,                    // MDBLON
         satellite_identifier@sat,                  // MDB_satid_AT_hdr
         scanpos@radiance,       // MDB_SCANPOS_AT_RADIANCE (field-of-view for ssmi)
         sensor@hdr,             // MDBSSIA (sensor ID number)
         zenith,            // MDB_ZENITH_AT_SAT (satellite zenith  angle in degrees)
         azimuth,           // MDB_AZIMUTH_AT_SAT (satellite azimuth angle in degrees)
  FROM   timeslot_index, index, hdr, sat, radiance
  WHERE  timeslot@timeslot_index == $tslot AND obstype == 7 AND codetype == 215 AND (sensor == 6 OR sensor == 10
OR sensor == 9 OR sensor == 17)
;

