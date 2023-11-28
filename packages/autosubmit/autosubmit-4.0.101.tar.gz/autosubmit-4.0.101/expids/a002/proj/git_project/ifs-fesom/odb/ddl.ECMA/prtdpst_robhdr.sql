//
//-- ODB/SQL file 'prtdpst_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW prtdpst_robhdr AS
  SELECT seqno, body.len,
	 obstype, 
     codetype,
     instrument_type,
     retrtype,
     areatype,
  FROM   index, hdr
