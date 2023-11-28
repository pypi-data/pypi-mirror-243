//
//-- ODB/SQL file 'reini_hdr.sql'
//
//   Last updated:  17-May-2001
//

CREATE VIEW reini_hdr AS
  SELECT body.len  READONLY,           // r/o
	 report_status,                       // updated
	 report_event1,                       // updated
	 report_blacklist,                    // updated
  FROM   hdr
;
