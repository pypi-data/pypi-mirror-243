//
//-- ODB/SQL file 'mobhdr_obsort.sql'
//
//   Last updated:  11-Mar-2003
//

READONLY;

SET $all = 1;
SET $hdr_min = 0; // here $hdr_min corresponds to distribtype 1 if on the model grid

CREATE VIEW mobhdr_obsort AS
  SELECT seqno,              //  r/o
         obstype , codetype,  sensor, //  r/o
         date, time,         //  r/o
         body.len,           //  r/o
         numactiveb,         //  r/o
         distribid,          // r/o
         target  UPDATED,          //  this is the "dest_proc" and will be updated
         gp_number,
    FROM index, hdr
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1)
	  OR ($all = 2 ) )
      AND distribtype = $hdr_min
   ORDERBY sensor, distribid, gp_number
;
