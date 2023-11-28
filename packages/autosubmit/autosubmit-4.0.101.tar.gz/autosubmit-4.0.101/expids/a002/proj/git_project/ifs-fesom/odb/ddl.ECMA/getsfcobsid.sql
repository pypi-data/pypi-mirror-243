//
//-- ODB/SQL file 'getsfcobsid.sql'
//
//   Last updated:  30-Jul-2010
//

READONLY;

CREATE VIEW getsfcobsid AS
      SELECT DISTINCT reportype, statid, stalt, varno, ppcode@conv_body
      FROM timeslot_index, index, hdr, body, conv, conv_body
      WHERE obstype in ($synop,$dribu,$paob) and varno in ($ps,$apdss) and obsvalue@body is not null
;

// Notes:
// 1. if the elements in the SELECT are changed, remember to update varbc_sfcobs.F90
// 2. if the list of varno in the WHERE are changed, remember to update
//        hdepart.F90, hretr.F90, hop.F90, hoptl.F90, and hopad.F90

