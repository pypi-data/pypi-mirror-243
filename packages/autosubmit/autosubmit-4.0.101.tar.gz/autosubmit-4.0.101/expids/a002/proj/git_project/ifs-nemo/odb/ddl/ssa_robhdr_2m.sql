//
//-- ODB/SQL file 'ssa_robhdr_2m.sql'
//
//   Last updated:  17-May-2002
//


READONLY;

CREATE VIEW ssa_robhdr_2m AS // SSA-analysis (2m analyses); ROBHDR-part
  SELECT seqno,              // r/o; Must become first
         body.len,           // r/o
         date, time,         // r/o
         obstype,            // r/o
         codetype,          // r/o
         lat, lon, statid, stalt  // r/o
    FROM hdr
   WHERE ( (reportype >= 16001 AND reportype <= 16004 ) 
            OR reportype == 16022  OR reportype == 16076 )
;
