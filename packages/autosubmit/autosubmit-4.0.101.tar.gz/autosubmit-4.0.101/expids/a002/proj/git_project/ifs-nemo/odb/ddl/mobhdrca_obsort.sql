//
//-- ODB/SQL file 'mobhdrca_obsort.sql'
//
//   Last updated:  17-May-2000 ; 06-Mar-2012
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW mobhdrca_obsort AS
  SELECT seqno,              //  r/o
         obstype , codetype,  sensor, //  r/o
         date, time,         //  r/o
         body.len,           //  r/o
	 numactiveb,         //  r/o
         distribid,          // r/o
         target UPDATED,           //  this is the "dest_proc" and will be updated
  FROM index, hdr
  WHERE ($all >= 1 OR report_status.active = 1)
    AND (timeslot = 4)
    AND ($all = 2 OR $all = -2 OR obstype IN ($synop,$dribu,$temp,$pilot,$paob)) 
;
