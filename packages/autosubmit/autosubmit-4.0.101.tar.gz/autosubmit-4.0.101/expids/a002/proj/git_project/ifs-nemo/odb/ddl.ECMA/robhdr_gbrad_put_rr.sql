//
//-- ODB/SQL file 'robhdr_gbrad_put_rr.sql'
//

SET $hdr_min = 999;
SET $hdr_max = 0;

CREATE VIEW robhdr_gbrad_put_rr AS
  SELECT seqno,                       // r/o MUST BE FIRST hdr
         mapomm,                      // r/o MDB_MAPOMM_AT_INDEX index
         gp_number,                   // MDB_GP_NUMBER hdr
         time,                        // MDBETM
         report_status,               // MDBRST hdr
         report_event1,               // MDBREV1 hdr
         report_rrflag@gbrad,         // MDB_REPORT_RRFLAG gbrad
         retrtype@hdr,                // MDB_RETRTYPE_AT_HDR
         source@hdr,                  // MDB_SOURCE_AT_HDR

  FROM   timeslot_index, index, hdr, gbrad
  WHERE  (timeslot@timeslot_index BETWEEN $hdr_min AND $hdr_max) 
    AND codetype == 3 AND obstype == 14
