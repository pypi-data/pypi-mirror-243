//
//-- ODB/SQL file 'robhdr_gbrad_get_rr.sql'
//

READONLY; // .. except where  UPDATED qualifier was found

SET $hdr_min = 999;
SET $hdr_max = 0;

CREATE VIEW robhdr_gbrad_get_rr AS
  SELECT seqno,                         // MDBONM (must be the first index; used to build MLNKH2B)
         gp_number,                     // MDB_GP_NUMBER hdr
         report_rrflag@gbrad,           // MDB_REPORT_RRFLAG gbrad
         retrtype@hdr,                  // MDB_RETRTYPE_AT_HDR
         source@hdr,                    // MDB_SOURCE_AT_HDR

  FROM   timeslot_index, index, hdr, gbrad

  WHERE  (timeslot@timeslot_index BETWEEN $hdr_min AND $hdr_max) 
     AND codetype == 3 AND obstype == 14
;

