//
//-- ODB/SQL file 'update_hdr_1.sql'
//
//   Last updated:  30-Sep-2003
//

UPDATED;

CREATE VIEW update_hdr_1 AS
  SELECT body READONLY,         // r/o (offset + length)
     update[1:$NMXUPD],     // updated (offset + length)
	 errstat, // updated
    FROM hdr
;
