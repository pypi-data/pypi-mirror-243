//
//-- ODB/SQL file 'suobscor_robhdr.sql'
//
//   Last updated:  27-Mar-2006
//

READONLY;

CREATE VIEW suobscor_robhdr AS
  SELECT seqno  READONLY,              // r/o; MUST COME FIRST
         body.len  READONLY,           // r/o
         date, time,         // r/o
         obstype,            // r/o
         codetype,          // r/o
         instrument_type,    // r/o
         retrtype,     // r/o
         areatype,          // r/o
         sensor,          // r/o
         satellite_identifier@sat,          // r/o
         abnob, mapomm,      // r/o
         lat, lon, statid,   // r/o
         timeslot@timeslot_index,   // r/o
  FROM   index, hdr, sat,  timeslot_index
;
