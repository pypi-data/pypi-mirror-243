//
//-- ODB/SQL file 'reini_body.sql'
//
//   Last updated:  17-May-2001
//

UPDATED;

CREATE VIEW reini_body AS
  SELECT datum_status@body,                       // updated
	 datum_event1@body,                       // updated
	 datum_blacklist@body,                    // updated
	 datum_anflag@body,                       // updated
  FROM   hdr, body
;
