//
//-- ODB/SQL file 'update_hdr_3.sql'
//
//   Last updated:  07-Jul-2005
//

UPDATED;

CREATE VIEW update_hdr_3 AS
  SELECT seqno READONLY, // Must become first
	 checksum,
	 stalt READONLY,
	 sensor READONLY,
     window_offset,      // updated to its right value (ECMA only)
    FROM hdr
;
