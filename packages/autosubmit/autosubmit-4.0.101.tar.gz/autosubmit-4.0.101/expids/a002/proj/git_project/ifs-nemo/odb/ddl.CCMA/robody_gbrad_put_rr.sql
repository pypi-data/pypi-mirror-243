//
//-- ODB/SQL file 'robody_gbrad_put_rr.sql'
//

SET $hdr_min = 999;
SET $hdr_max = 0;

CREATE VIEW robody_gbrad_put_rr AS

  SELECT seqno,                  // r/o MUST BE FIRST hdr
         entryno,                //     
         varno,                  //     MDBVNM         body
         obsvalue,               //     MDBVAR         body
         rrvalue@gbrad_body,     //     MDB_RRVALUE    gbrad_body
         rrvaluetl@gbrad_body,   //     MDB_RRVALUETL  gbrad_body
         rrvaluead@gbrad_body,   //     MDB_RRVALUEAD  gbrad_body
         datum_status@body,      //     MDBDSTA        body
         biascorr,               //     MDBTORB        body
         obs_error,              //     MDBOER         errstat
         final_obs_error,        //     MDBFOE         errstat
         retrtype@hdr,           //     MDB_RETRTYPE_AT_HDR
         source@hdr,             //     MDB_SOURCE_AT_HDR

  FROM   timeslot_index, index, hdr, body, errstat, gbrad_body

  WHERE  (timeslot@timeslot_index BETWEEN $hdr_min AND $hdr_max) 
    AND codetype == 3 AND obstype == 14 AND varno == 203
;
