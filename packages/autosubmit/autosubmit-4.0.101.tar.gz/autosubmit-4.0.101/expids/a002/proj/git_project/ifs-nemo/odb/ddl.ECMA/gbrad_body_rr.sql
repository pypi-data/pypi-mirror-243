//
//-- ODB/SQL file 'gbrad_body_rr.sql'
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW gbrad_body_rr AS

  SELECT seqno  READONLY,         // MDBONM (used to build MLNKH2B)
         rrvalue@gbrad_body,      // MDB_RRVALUE    gbrad_body
         rrvaluetl@gbrad_body,    // MDB_RRVALUETL  gbrad_body
         rrvaluead@gbrad_body,    // MDB_RRVALUEAD  gbrad_body

  FROM   timeslot_index, index, hdr, gbrad_body

  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
          AND kset = $kset 
          AND obstype == 14 AND codetype == 3
 ORDERBY seqno
;
