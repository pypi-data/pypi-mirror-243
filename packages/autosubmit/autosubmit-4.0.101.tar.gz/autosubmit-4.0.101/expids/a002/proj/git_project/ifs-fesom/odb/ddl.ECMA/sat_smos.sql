//
//-- ODB/SQL file 'sat_smos.sql'
//
//   Last updated:  05-May-2010
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_smos AS
  SELECT seqno  READONLY,                // r/o; MUST BECOME FIRST
         distribid  READONLY,            // MDB_distribid_AT_hdr 
         gp_number  READONLY,            // MDB_GP_NUMBER hdr
         gp_dist  READONLY,              // MDB_GP_DIST hdr
         report_tbflag@smos  READONLY,   // MDB_TB_FLAG_SMOS smos
         tbvalue@smos  READONLY          // MDB_TB_SMOS      smos 
  FROM   timeslot_index, index, hdr, smos
  WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND kset = $kset
    AND obstype = $satem AND codetype = 400
 ORDERBY seqno
;
