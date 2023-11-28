//
//-- ODB/SQL file 'caredo_robhdr.sql'
//
//   Last updated:  10-Aug-2009 / 25-Jan-2012
//

READONLY;
SET $obstype = -1;
SET $codetype = -1;

CREATE VIEW caredo_robhdr AS
  SELECT seqno,
         body.len,
         obstype,
         codetype,
         date,
         time,
         statid,
         report_blacklist UPDATED,
         lat,
         lon
  FROM   index, hdr
  WHERE (obstype=$obstype OR $obstype = -1) 
    and (codetype=$codetype OR $codetype = -1)
;
