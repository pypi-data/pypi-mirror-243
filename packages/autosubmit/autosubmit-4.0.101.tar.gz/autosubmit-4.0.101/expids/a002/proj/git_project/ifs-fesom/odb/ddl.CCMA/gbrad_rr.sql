//
//-- ODB/SQL file 'gbrad_rr.sql'
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW gbrad_rr AS
  SELECT seqno,                   // MDBONM (must be the first index; used to build MLNKH2B)
         report_rrflag@gbrad,     // MDB_REPORT_RRFLAG  gbrad

  FROM   timeslot_index, index, hdr, gbrad

  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset 
     AND obstype == 14 AND codetype == 3 
 ORDERBY seqno
;

