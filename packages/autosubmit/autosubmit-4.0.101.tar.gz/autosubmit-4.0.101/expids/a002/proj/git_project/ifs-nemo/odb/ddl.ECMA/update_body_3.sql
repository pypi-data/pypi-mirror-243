//
//-- ODB/SQL file 'update_body_3.sql'
//
//   Last updated:  07-Jul-2005
//
//   To be used in concert with 'update_hdr_3.sql'
//

READONLY;

CREATE VIEW update_body_3 AS
  SELECT seqno, // Must become first
	 vertco_reference_1,          
	 obsvalue,
	 varno,
	 obs_error
    FROM hdr, body, errstat
;
