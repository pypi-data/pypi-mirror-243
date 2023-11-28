//
//-- ODB/SQL file 'robhdr_tc.sql'
//
//   Last updated:  17-May-2001
//

READONLY; // ... view

CREATE VIEW robhdr_tc AS     // Time correlation; ROBHDR-part
  SELECT seqno,              // r/o; Must become first
         body.len,           // r/o
         date, time,         // r/o
         obstype,            // r/o
         codetype,          // r/o
         instrument_type,    // r/o
         retrtype,     // r/o
         areatype,          // r/o
         abnob, mapomm,      // r/o
         lat, lon, statid,   // r/o
    FROM index, hdr
   WHERE obstype = $synop
      OR obstype = $dribu
;
